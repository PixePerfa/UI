## FunctionDef _parse_files_in_thread(files, dir, zh_title_enhance, chunk_size, chunk_overlap)
**_parse_files_in_thread**: This function saves the uploaded file to a specified directory through multi-threading and processes the file content. 

**Parameters**:
- `files`: A `UploadFile`list of objects that represent the uploaded files that need to be processed. 
- `dir`: A string that represents the directory to which the file is saved.
- `zh_title_enhance`: Boolean value, indicating whether to enable the Chinese title enhancement function.
- `chunk_size`: An integer that specifies the size of a single block when text is processed.
- `chunk_overlap`: An integer that specifies the length of the overlap between adjacent blocks when text is processed.

**Code Description**:
This function first defines an internal function`parse_file` that works with a single file. `parse_file`Try to read the contents of the uploaded file and save it to the specified directory. If the directory does not exist, it is created. After that, `KnowledgeFile`the file content is processed using objects, including text extraction and possibly Chinese title enhancement, chunking the text according to`chunk_size` and `chunk_overlap`parameters. After successful processing, a tuple containing a success flag, file name, success message, and a list of document objects is returned; When processing a failure, a tuple containing the failure flag, file name, error message, and empty list is returned. 

Next, the function uses `run_in_thread_pool`the function to execute the function concurrently on`files` each file in the list`parse_file`. `run_in_thread_pool`Accept a function and a list of parameters, create a thread pool and execute the function concurrently in it, and finally return the result of each task in the form of a generator. `_parse_files_in_thread`The function iterates through these results and returns them one by one. 

**Note**:
- Make sure that the incoming `dir`path exists or that the function has permission to create a directory. 
- Due to the use of multithreading, it is ensured that all operations, especially file writing and text processing, are thread-safe.
- When this function is called, the returned generator should be processed iteratively to get the results of processing for all files.

**Example output**:
```python
[
    (True, "example.txt", "成功上传文件 example.txt", [<文档对象>]),
    (False, "error.txt", "error.txt 文件上传失败，报错信息为: 文件无法读取", [])
]
```
This output example shows the possible results of a function processing two files: the first file is successfully processed, returning a success flag, a file name, a success message, and a list of document objects; The second file fails to process, returning a failure flag, a file name, an error message, and an empty list.
### FunctionDef parse_file(file)
**parse_file**: The function of this function is to save a single file and convert its contents into a text list. 

**Parameters**:
- `file`: Type `UploadFile`, which indicates the uploaded file to be parsed and saved. 

**Code Description**:
`parse_file`The function first extracts the file name from the uploaded file and constructs the path to which the file should be saved. It then checks to see if the directory where this path is located exists, and if it doesn't, creates it. Next, the function opens the file in binary write mode to the destination path and writes the contents of the uploaded file into it. 

After the file is successfully saved, the function creates an `KnowledgeFile`instance that processes and transforms the contents of the file. By calling`KnowledgeFile` the class's `file2text`methods, the file content is converted into a list of text. This process supports Chinese title enhancement, chunking processing, and custom text splitters for subsequent text analysis or processing tasks. 

If there are any exceptions during file processing and conversion, the function catches those exceptions and returns a response with an error message indicating that the file upload failed.

**Note**:
- Make sure that the uploaded file path is valid and that the server has sufficient permissions to create files and directories in the specified location.
- `KnowledgeFile`The use of classes requires that the file format is supported and that the relevant processing parameters (such as Chinese title enhancement, tile size, etc.) are set correctly.
- The exception handling section is important to identify and debug issues that may arise during file upload or processing.

**Example output**:
Calling `parse_file`a function might return a tuple in the form of:
```python
(True, "example.txt", "成功上传文件 example.txt", ["文档内容示例"])
```
If you encounter an error, the tuple returned might look like this:
```python
(False, "example.txt", "example.txt 文件上传失败，报错信息为: 文件格式不支持", [])
```
This return value indicates the success of the processing, the file name, the related message, and the processed text list (or an empty list in case of failure).
***
## FunctionDef upload_temp_docs(files, prev_id, chunk_size, chunk_overlap, zh_title_enhance)
**upload_temp_docs**: The function of this function is to save the file to a temporary directory and vectorize it. 

**Parameters**:
- `files`: A list of uploaded files, of type`List[UploadFile]`. Multi-file upload is supported. 
- `prev_id`: The ID of the former knowledge base, of type`str`. Lets you specify the previous temporary directory ID, and if provided, try to reuse the directory. 
- `chunk_size`: The maximum length of a single piece of text in the knowledge base, of type`int`. Used to specify the size of a single block when text is being processed. 
- `chunk_overlap`: The coincident length of adjacent text in the knowledge base, of type`int`. Lets you specify the length of overlap between adjacent blocks during text processing. 
- `zh_title_enhance`: Whether to enable Chinese title enhancement, the type is`bool`. Used to indicate whether to strengthen Chinese titles. 

**Code Description**:
The function first checks for`prev_id` its existence and, if it does, `memo_faiss_pool`removes the corresponding temporary vector library from it. Next, initialize the list of failed files`failed_files` and documents`documents`. By calling `get_temp_dir`the function, the `prev_id`path and ID of the temporary directory are obtained or created. The `_parse_files_in_thread`uploaded file is then processed concurrently using a function that saves the file to a specified temporary directory with the necessary text processing and vectorization. The results include success flags, file objects, messages, and a list of documents. For files that have been successfully processed, their document list will be added to`documents` the file; For files that fail to process, their file names and error messages are added to the`failed_files` list. After that, the `load_vector_store`ephemeral vector library is loaded or initialized via a function, and `acquire`thread-safe is ensured using the context manager. Finally, add a list of documents to the vector library and return an object containing the temporary directory ID and the list of failed files`BaseResponse`. 

**Note**:
- When uploading a file, you should ensure that the file type and size meet the requirements to avoid upload failures.
- If specified`prev_id`, the function will attempt to reuse the previous temporary directory, which can reduce unnecessary directory creation. 
- When dealing with a large number of files or large files, you should be aware of the execution time of the function, which may require a long processing time.
- Use `zh_title_enhance`parameters to enhance the processing of Chinese titles and improve the quality of text processing. 

**Example output**:
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "id": "临时目录ID",
    "failed_files": [
      {"file1": "错误消息1"},
      {"file2": "错误消息2"}
    ]
  }
}
```
This example of the output shows the return value of the function after it is successfully executed, including the ID of the temporary directory and the list of failed files. If all files are processed successfully, the`failed_files` list will be empty. 
## FunctionDef file_chat(query, knowledge_id, top_k, score_threshold, history, stream, model_name, temperature, max_tokens, prompt_name)
**file_chat**: This function is used to process queries sent by users through the File Chat interface and return the relevant knowledge base document content and the conversation replies based on those contents. 

**Parameters**:
- `query`: The query entered by the user, which is of string type and is required.
- `knowledge_id`: Temporary knowledge base ID, which is used to specify the knowledge base of the query, is a string type, and is required.
- `top_k`: Number of matching vectors, specifies the number of related documents returned, which is of integer type.
- `score_threshold`: The knowledge base matches the relevance threshold, with a value range of 0 to 1, which is used to filter documents with high relevance and is of the floating-point type.
- `history`: A list of historical conversations, which contains the conversation history of users and assistants.
- `stream`: Whether to stream the output, which is a boolean type, specifies whether to return data in the form of a stream.
- `model_name`: The LLM model name, which specifies the language model to use when generating responses, and is of the string type.
- `temperature`: LLM sampling temperature, which is used to adjust the diversity of the generated text, which is of floating-point type.
- `max_tokens`: Limit the number of tokens generated by LLMs, which is an integer type, optional.
- `prompt_name`: The name of the prompt template used, which specifies the template to be used when generating the reply, which is a string type.

**Code Description**:
The function first checks if the incoming`knowledge_id` Yu exists`memo_faiss_pool`, and if it doesn't, returns a 404 error. Next, convert the incoming list of historical conversations to`History` a list of objects. The function defines an asynchronous generator `knowledge_base_chat_iterator`that generates conversation replies and related document content. In this generator, the `max_tokens`limit on the number of tokens is first adjusted based on the value, and then a chat model is created with the specified LLM model and temperature parameters. Find`embed_func` the most relevant documents by embedding user queries as vectors and using `memo_faiss_pool`the vector search feature. Build chat prompts based on found documents and historical conversations, then generate responses using the LLM model. Finally, depending on`stream` the value of the parameter, decide whether to stream the output or return all the data at once. 

**Note**:
- Before you can use this function, you need to make sure that `memo_faiss_pool`it has been initialized and that it contains at least one knowledge base. 
- `history`The historical conversation records in the parameters should be arranged in chronological order so that the conversation context is properly constructed.
- Settings `score_threshold`can help filter out less relevant documents and improve the accuracy of your responses. 
- If `stream`the parameter is set to True, data will be returned in the form of server-sent events (SSE), which is suitable for scenarios that need to be updated in real time. 

**Example output**:
```json
{
  "answer": "这是基于您的查询和相关文档生成的回复。",
  "docs": [
    "出处 [1] [source_document.pdf] \n\n这是相关文档的内容。\n\n"
  ]
}
```
If `stream`the parameter is True, the data will be returned in batches, one JSON object containing the reply fragment at a time, and finally a JSON object containing the content of the relevant document. 
### FunctionDef knowledge_base_chat_iterator
**knowledge_base_chat_iterator**: The function of this function is to iteratively generate knowledgebase-based chat answers asynchronously. 

**Parameters**:
- No arguments are passed directly into this function, but the function internally uses methods for multiple global variables and other objects.

**Code Description**:
`knowledge_base_chat_iterator`A function is an asynchronous generator that processes knowledgebase-based chat answers. First, it checks`max_tokens` if it is an integer and less than or equal to 0, and if it is, it will be`max_tokens` set to None. Next, `get_ChatOpenAI`use the function to initialize a ChatOpenAI instance, which is used to generate chat answers. In this process,`model_name` parameters such as ,`temperature` , , and `max_tokens`so on are used to configure the model, and`callbacks` the parameters contain an `AsyncIteratorCallbackHandler`instance to handle asynchronous callbacks. 

The function continues to`EmbeddingsFunAdapter` `aembed_query`asynchronously get the embedding vector of the query text through the class's methods. Then, use `memo_faiss_pool.acquire`the method to securely fetch the knowledge base vector storage object from the cache pool and perform a similarity search, with the search results stored`docs` in variables. 

Based on the searched documents, the function builds the context of the conversation`context`. If no relevant documentation is found, the function will`get_prompt_template` be used to get an empty template; Otherwise, get `prompt_name`the appropriate template according to the acquisition. Next, use`History` classes and `ChatPromptTemplate`build chat prompts. 

Through `LLMChain`classes, the function passes the chat prompt and context to the ChatOpenAI model for processing, and the generated answers are managed through`wrap_done` asynchronous tasks wrapped by the function. 

Finally, the function generates the answer differently depending on whether streaming (`stream`variable) is enabled or not. If streaming is enabled, the answer will be `callback.aiter()`iteratively answered and sent one by one in the form of server-sent-events; If streaming isn't enabled, complete responses will be collected and returned in one go. 

**Note**:
- The function is asynchronous and needs to be run in an asynchronous environment.
- When using `knowledge_base_chat_iterator`functions, you need to make sure that the relevant global variables (e.g`model_name`., , `temperature`etc.) are set correctly. 
- Internally, there are several externally defined objects and methods (e.g`get_ChatOpenAI`., , etc.) that are used inside `EmbeddingsFunAdapter`the function to ensure that these dependencies are properly initialized and configured before the function is called. 
- Functions can take longer to execute when processing a large number of or complex queries, so the user interface and interaction flow should be designed with potential latency in mind.
***
