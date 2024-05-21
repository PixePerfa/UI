from langchain.utilities.bing_search import BingSearchAPIWrapper
from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from configs import (BING_SEARCH_URL, BING_SUBSCRIPTION_KEY, METAPHOR_API_KEY,
                     LLM_MODELS, SEARCH_ENGINE_TOP_K, TEMPERATURE, OVERLAP_SIZE)
from langchain.chains import LLMChain
from langchain.callbacks import AsyncIteratorCallbackHandler

from langchain.prompts.chat import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from fastapi import Body
from fastapi.concurrency import run_in_threadpool
from sse_starlette import EventSourceResponse
from server.utils import wrap_done, get_ChatOpenAI
from server.utils import BaseResponse, get_prompt_template
from server.chat.utils import History
from typing import AsyncIterable
import asyncio
import json
from typing import List, Optional, Dict
from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from markdownify import markdownify


def bing_search(text, result_len=SEARCH_ENGINE_TOP_K, **kwargs):
    if not (BING_SEARCH_URL and BING_SUBSCRIPTION_KEY):
        return [{"snippet": "please set BING_SUBSCRIPTION_KEY and BING_SEARCH_URL in os ENV",
                 "title": "env info is not found",
                 "link": "https://python.langchain.com/en/latest/modules/agents/tools/examples/bing_search.html"}]
    search = BingSearchAPIWrapper(bing_subscription_key=BING_SUBSCRIPTION_KEY,
                                  bing_search_url=BING_SEARCH_URL)
    return search.results(text, result_len)


def duckduckgo_search(text, result_len=SEARCH_ENGINE_TOP_K, **kwargs):
    search = DuckDuckGoSearchAPIWrapper()
    return search.results(text, result_len)


def metaphor_search(
        text: str,
        result_len: int = SEARCH_ENGINE_TOP_K,
        split_result: bool = False,
        chunk_size: int = 500,
        chunk_overlap: int = OVERLAP_SIZE,
) -> List[Dict]:
    from metaphor_python import Metaphor

    if not METAPHOR_API_KEY:
        return []

    client = Metaphor(METAPHOR_API_KEY)
    search = client.search(text, num_results=result_len, use_autoprompt=True)
    contents = search.get_contents().contents
    for x in contents:
        x.extract = markdownify(x.extract)

    # The content returned by metaphor is all long text, which needs to be retrieved by word segmentation
    if split_result:
        docs = [Document(page_content=x.extract,
                         metadata={"link": x.url, "title": x.title})
                for x in contents]
        text_splitter = RecursiveCharacterTextSplitter(["\n\n", "\n", ".", " "],
                                                       chunk_size=chunk_size,
                                                       chunk_overlap=chunk_overlap)
        splitted_docs = text_splitter.split_documents(docs)

        # Put the sharded documents into the temporary vector library and re-filter out TOP_K documents
        if len(splitted_docs) > result_len:
            normal = NormalizedLevenshtein()
            for x in splitted_docs:
                x.metadata["score"] = normal.similarity(text, x.page_content)
            splitted_docs.sort(key=lambda x: x.metadata["score"], reverse=True)
            splitted_docs = splitted_docs[:result_len]

        docs = [{"snippet": x.page_content,
                 "link": x.metadata["link"],
                 "title": x.metadata["title"]}
                for x in splitted_docs]
    else:
        docs = [{"snippet": x.extract,
                 "link": x.url,
                 "title": x.title}
                for x in contents]

    return docs


SEARCH_ENGINES = {"bing": bing_search,
                  "duckduckgo": duckduckgo_search,
                  "metaphor": metaphor_search,
                  }


def search_result2docs(search_results):
    docs = []
    for result in search_results:
        doc = Document(page_content=result["snippet"] if "snippet" in result.keys() else "",
                       metadata={"source": result["link"] if "link" in result.keys() else "",
                                 "filename": result["title"] if "title" in result.keys() else ""})
        docs.append(doc)
    return docs


async def lookup_search_engine(
        query: str,
        search_engine_name: str,
        top_k: int = SEARCH_ENGINE_TOP_K,
        split_result: bool = False,
):
    search_engine = SEARCH_ENGINES[search_engine_name]
    results = await run_in_threadpool(search_engine, query, result_len=top_k, split_result=split_result)
    docs = search_result2docs(results)
    return docs

async def search_engine_chat(query: str = Body(..., description="User Input", examples=["Hello"]),
                             search_engine_name: str = Body(..., description="Search engine name", examples=["duckduckgo"]),
                             top_k: int = Body(SEARCH_ENGINE_TOP_K, description="Number of search results"),
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
                             max_tokens: Optional[int] = Body(None,
                                                              description="Limit the number of tokens generated by LLM, default None represents the maximum value of the model"),
                             prompt_name: str = Body("default",
                                                     description="Name of the prompt template used (configured in configs/prompt_config.py)"),
                             split_result: bool = Body(False,
                                                       description="Whether to split the search results (mainly used in the metaphor search engine)")
                             ):
    if search_engine_name not in SEARCH_ENGINES.keys():
        return BaseResponse(code=404, msg=f"Search engine not supported {search_engine_name}")

    if search_engine_name == "bing" and not BING_SUBSCRIPTION_KEY:
        return BaseResponse(code=404, msg=f"To use the Bing search engine, you need to set 'BING_SUBSCRIPTION_KEY'")

    history = [History.from_data(h) for h in history]

    async def search_engine_chat_iterator(query: str,
                                          search_engine_name: str,
                                          top_k: int,
                                          history: Optional[List[History]],
                                          model_name: str = LLM_MODELS[0],
                                          prompt_name: str = prompt_name,
                                          ) -> AsyncIterable[str]:
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

        docs = await lookup_search_engine(query, search_engine_name, top_k, split_result=split_result)
        context = "\n".join([doc.page_content for doc in docs])

        prompt_template = get_prompt_template("search_engine_chat", prompt_name)
        input_msg = History(role="user", content=prompt_template).to_msg_template(False)
        chat_prompt = ChatPromptTemplate.from_messages(
            [i.to_msg_template() for i in history] + [input_msg])

        chain = LLMChain(prompt=chat_prompt, llm=model)

        # Begin a task that runs in the background.
        task = asyncio.create_task(wrap_done(
            chain.acall({"context": context, "question": query}),
            callback.done),
        )

        source_documents = [
            f"""Source: [{inum + 1}] [{doc.metadata["source"]}]({doc.metadata["source"]}) \n\n{doc.page_content}\n\n"""
            for inum, doc in enumerate(docs)
        ]

        if len(source_documents) == 0: # No information found (unlikely)
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

    return EventSourceResponse(search_engine_chat_iterator(query=query,
                                                           search_engine_name=search_engine_name,
                                                           top_k=top_k,
                                                           history=history,
                                                           model_name=model_name,
                                                           prompt_name=prompt_name),
                               )
