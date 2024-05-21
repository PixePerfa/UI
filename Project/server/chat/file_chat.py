from fastapi import Body, File, Form, UploadFile
from sse_starlette.sse import EventSourceResponse
from configs import (LLM_MODELS, VECTOR_SEARCH_TOP_K, SCORE_THRESHOLD, TEMPERATURE,
                     CHUNK_SIZE, OVERLAP_SIZE, ZH_TITLE_ENHANCE)
from server.utils import (wrap_done, get_ChatOpenAI,
                        BaseResponse, get_prompt_template, get_temp_dir, run_in_thread_pool)
from server.knowledge_base.kb_cache.faiss_cache import memo_faiss_pool
from langchain.chains import LLMChain
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import AsyncIterable, List, Optional
import asyncio
from langchain.prompts.chat import ChatPromptTemplate
from server.chat.utils import History
from server.knowledge_base.kb_service.base import EmbeddingsFunAdapter
from server.knowledge_base.utils import KnowledgeFile
import json
import os
from pathlib import Path


def _parse_files_in_thread(
    files: List[UploadFile],
    dir: str,
    zh_title_enhance: bool,
    chunk_size: int,
    chunk_overlap: int,
):
    """
    Save the uploaded file to the corresponding directory through multithreading.
    The generator returns the saved result: [success or error, filename, msg, docs]
    """
    def parse_file(file: UploadFile) -> dict:
        '''
        Save a single file.
        '''
        try:
            filename = file.filename
            file_path = os.path.join(dir, filename)
            file_content = file.file.read() # Read the contents of the uploaded file

            if not os.path.isdir(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            with open(file_path, "wb") as f:
                f.write(file_content)
            kb_file = KnowledgeFile(filename=filename, knowledge_base_name="temp")
            kb_file.filepath = file_path
            docs = kb_file.file2text(zh_title_enhance=zh_title_enhance,
                                     chunk_size=chunk_size,
                                     chunk_overlap=chunk_overlap)
            return True, filename, f"Successfully uploaded file {filename}", docs
        except Exception as e:
            msg = f"{filename} file upload failed with the following error message: {e}"
            return False, filename, msg, []

    params = [{"file": file} for file in files]
    for result in run_in_thread_pool(parse_file, params=params):
        yield result


def upload_temp_docs(
    files: List[UploadFile] = File(..., description="Upload file, multi-file supported"),
    prev_id: str = Form(None, description="Pre-KB ID"),
    chunk_size: int = Form(CHUNK_SIZE, description="Maximum length of a single paragraph of text in the knowledge base"),
    chunk_overlap: int = Form(OVERLAP_SIZE, description="Coincident length of adjacent text in the knowledge base"),
    zh_title_enhance: bool = Form(ZH_TITLE_ENHANCE, description="Whether to turn on Chinese Title Enhancement"),
) -> BaseResponse:
    '''
    Save the file to a temporary directory and vectorize it.
    Returns the name of the temporary directory as the ID, which is also the ID of the temporary vector library.
    '''
    if prev_id is not None:
        memo_faiss_pool.pop(prev_id)

    failed_files = []
    documents = []
    path, id = get_temp_dir(prev_id)
    for success, file, msg, docs in _parse_files_in_thread(files=files,
                                                        dir=path,
                                                        zh_title_enhance=zh_title_enhance,
                                                        chunk_size=chunk_size,
                                                        chunk_overlap=chunk_overlap):
        if success:
            documents += docs
        else:
            failed_files.append({file: msg})

    with memo_faiss_pool.load_vector_store(id).acquire() as vs:
        vs.add_documents(documents)
    return BaseResponse(data={"id": id, "failed_files": failed_files})


async def file_chat(query: str = Body(..., description="User Input", examples=["Hello"]),
                    knowledge_id: str = Body(..., description="Temporary KB ID"),
                    top_k: int = Body(VECTOR_SEARCH_TOP_K, description="Number of matching vectors"),
                    score_threshold: float = Body(SCORE_THRESHOLD, description="The relevance threshold of the knowledge base is matched, the value range is between 0 and 1, the smaller the SCORE, the higher the relevance, and the score is not filtered, it is recommended to set it to about 0.5", ge=0, le=2),
                    history: List[History] = Body([],
                                                description="Historical Conversations",
                                                examples=[[
                                                    {"role": "user",
                                                    "content": "Let's play idiom solitaire, I'll come first, live the dragon and the tiger"},
                                                    {"role": "assistant",
                                                    "content": "Tiger Brain"}]]
                                                ),
                    stream: bool = Body(False, description="Streaming output"),
                    model_name: str = Body(LLM_MODELS[0], description="LLM model name. "),
                    temperature: float = Body(TEMPERATURE, description="LLM sample temperature", ge=0.0, le=1.0),
                    max_tokens: Optional[int] = Body(None, description="Limit the number of tokens generated by LLM, default Never represents the maximum value of the model"),
                    prompt_name: str = Body("default", description="Name of prompt template used (configured in configs/prompt_config.py)"),
                ):
    if knowledge_id not in memo_faiss_pool.keys():
        return BaseResponse(code=404, msg=f"Temporary knowledge base {knowledge_id} not found, please upload file first")

    history = [History.from_data(h) for h in history]

    async def knowledge_base_chat_iterator() -> AsyncIterable[str]:
        nonlocal max_tokens
        callback = AsyncIteratorCallbackHandler()
        if isinstance(max_tokens, int) and max_tokens <= 0:
            max_tokens = None

        model = get_ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            callbacks=[callback],
        )
        embed_func = EmbeddingsFunAdapter()
        embeddings = await embed_func.aembed_query(query)
        with memo_faiss_pool.acquire(knowledge_id) as vs:
            docs = vs.similarity_search_with_score_by_vector(embeddings, k=top_k, score_threshold=score_threshold)
            docs = [x[0] for x in docs]

        context = "\n".join([doc.page_content for doc in docs])
        if len(docs) == 0: ## If no relevant document is found, use the Empty template
            prompt_template = get_prompt_template("knowledge_base_chat", "empty")
        else:
            prompt_template = get_prompt_template("knowledge_base_chat", prompt_name)
        input_msg = History(role="user", content=prompt_template).to_msg_template(False)
        chat_prompt = ChatPromptTemplate.from_messages(
            [i.to_msg_template() for i in history] + [input_msg])

        chain = LLMChain(prompt=chat_prompt, llm=model)

        # Begin a task that runs in the background.
        task = asyncio.create_task(wrap_done(
            chain.acall({"context": context, "question": query}),
            callback.done),
        )

        source_documents = []
        for inum, doc in enumerate(docs):
            filename = doc.metadata.get("source")
            text = f"""Source [{inum + 1}] [{filename}] \n\n{doc.page_content}\n\n"""
            source_documents.append(text)

        if len(source_documents) == 0: # No documentation found
            source_documents.append(f"""<span style='color:red'> no relevant documents found, this answer is the answer of the large model's own capabilities! </span>""")

        if stream:
            async for token in callback.aiter():
                # Use server-sent-events to stream the response
                yield json.dumps({"answer": token}, ensure_ascii=False)
            yield json.dumps({"docs": source_documents}, ensure_ascii=False)
        else:
            answer = ""
            async for token in callback.aiter():
                answer += token
            yield json.dumps({"answer": answer,
                              "docs": source_documents},
                             ensure_ascii=False)
        await task

    return EventSourceResponse(knowledge_base_chat_iterator())
