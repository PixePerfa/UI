## FunctionDef search_docs(query, knowledge_base_name, top_k, score_threshold, file_name, metadata)
**search_docs**: The function of this function is to search for related documents in a specified knowledge base based on the query criteria entered by the user. 

**Parameters**:
- `query`: String type, which defaults to an empty string and represents the user's query input.
- `knowledge_base_name`: String type, required, indicates the name of the knowledge base to be searched.
- `top_k`: Integer, which indicates the number of matching vectors returned.
- `score_threshold`: Floating-point type, with a value range of 0 to 1, indicates the relevance threshold of the knowledge base. The lower the SCORE, the higher the correlation, and a score of 1 is equivalent to no screening.
- `file_name`: String type, which is an empty string by default, indicates the file name, and supports SQL wildcards.
- `metadata`: The dictionary type, which is an empty dictionary by default, indicates that the filter is based on metadata, and only the first-level key is supported.

**Code Description**:
The function first `KBServiceFactory.get_service_by_name`obtains the service instance of the specified knowledge base through a method. If a knowledge base service instance exists, the function will`query` determine the search logic based on whether or not parameters are provided. If a parameter is provided`query`, the function will call the method of the knowledge base service instance`search_docs` to search and convert the search results into`DocumentWithVSId` a list of objects returned. If no `query`arguments are provided but are provided`file_name``metadata`, the function will call the knowledge base service instance of the`list_docs` method listed document. Eventually, the function returns a`DocumentWithVSId` list of objects. 

**Note**:
- When using this function, make sure that the incoming knowledge base name already exists in the system, otherwise you will not be able to get the knowledge base service instance, causing the search to fail.
- `score_threshold`Parameters are used to filter search results, and lower values mean higher relevance requirements that can be adjusted to meet actual needs.
- When the `query`parameter is empty, you can`file_name` `metadata`list the documents in the knowledge base by or parameters, which is useful when you need to get a list of documents based on specific criteria. 

**Example output**:
Suppose you search for "technical documentation" in the knowledge base, and you set`top_k=2` it, `score_threshold=0.5`you might get something like this:
```python
[
    DocumentWithVSId(id="doc1", score=0.45, metadata={"title": "Technical Document Introduction", "author": "Zhang San"}),
    DocumentWithVSId(id="doc2", score=0.48, metadata={"title": "Technical Document User Manual", "author": "Li Si"})
]
```
This output example shows a list of the top two most relevant document objects returned based on query criteria, each containing a unique identifier for the document, a match score, and metadata information.
## FunctionDef update_docs_by_id(knowledge_base_name, docs)
**update_docs_by_id**: Update the document content by the document ID. 

**Parameters**:
- `knowledge_base_name`: The name of the knowledge base, of type String. This parameter is used to specify the knowledge base for which the document is to be updated.
- `docs`: The content of the document to be updated, of type dictionary, like  .`{id: Document, ...}` The key of the dictionary is the ID of the document and the value is `Document` Object. 

**Code Description**:
`update_docs_by_id` The function first obtains  the corresponding knowledge base service instance `KBServiceFactory.get_service_by_name` based on the incoming knowledge base name through the  method `knowledge_base_name` . If the specified knowledge base does not exist, the function will return an `BaseResponse` object with  a Property `code` set to 500, which`msg` represents an error message that the specified knowledge base does not exist. If the knowledge repository is there, the function will call the methods of the knowledge base service instance `update_doc_by_ids` to attempt to update the incoming document. If the update is successful, the function returns an `BaseResponse` object whose `msg` property represents the information that the document was successfully updated; If the update fails, the returned `BaseResponse` object's `msg` property will represent information that the document update failed. 

**Note**:
- Before calling this function, make sure that the incoming  is `knowledge_base_name` present in the system, otherwise you will not be able to find the corresponding knowledge base to operate. 
- `docs` The object in the parameter `Document` should contain the content of the document to be updated. Ensure that the document ID matches the ID of an existing document in the knowledge base so that it is updated correctly. 
- The result of the execution of this function (success or failure) is fed back by `BaseResponse` the returned object's `msg` properties. Therefore, you should check the return value after calling this function to confirm the result of the operation. 

**Example output**:
If the specified knowledge base name does not exist, the function may return an object like this `BaseResponse` :
```python
BaseResponse(code=500, msg="The specified knowledge base does not exist")
```
If the document update is successful, the function will return:
```python
BaseResponse(msg="Document updated successfully")
```
If the document update fails, the function returns:
```python
BaseResponse(msg="Document update failed")
```

This function is part of the knowledge base management feature in the project and allows you to update the content of a document in the knowledge base directly based on the document ID through the API. It `server/api.py` `mount_knowledge_routes` is registered as an API route in the file via a function, which allows the frontend or other service to invoke this function by sending an HTTP request to update the knowledge base document. 
## FunctionDef list_files(knowledge_base_name)
**list_files**: This function is used to list all file names in the specified knowledge base. 

**Parameters**:
- `knowledge_base_name`: String type, which indicates the name of the knowledge base for which you want to query the list of files.

**Code Description**: `list_files` The function first verifies the validity of the incoming knowledge base name, and returns a 403 status code and error message if the name is invalid (for example, it contains potentially security risk characters). After that, the function decodes the knowledge base name to ensure that the URL-encoded knowledge base name is handled correctly. Then, the `KBServiceFactory.get_service_by_name` service instance of the corresponding knowledge base is obtained through the method. If the knowledge base does not exist, a 404 status code and error message are returned. If the knowledge repository is there, the function will call the knowledge base service instance's `list_files` method to get all the file names and return those file names to the client as data. 

**Note**:
- Before calling this function, you need to make sure that the incoming knowledge base name is URL-encoded to avoid potential URL parsing errors.
- This function relies on `KBServiceFactory.get_service_by_name` the method to get the knowledge base service instance, so you need to make sure that the knowledge base name is present in the system. 
- The returned list of file names is `ListResponse` encapsulated by the class, which means that in addition to the file name list data, it also contains the status code and status message of the response. 

**Example output**:
Suppose there is a knowledge base called Technical Documentation Library with three files "doc1.docx", "doc2.pdf", "doc3.txt", and calling `list_files("Technical Documentation Library")` will  return a response body like this:
```
{
    "code": 200,
    "msg": "success",
    "data": ["doc1.docx", "doc2.pdf", "doc3.txt"]
}
```
If the incoming knowledge base name is invalid or the knowledge base does not exist, the corresponding error status code and message will be returned, such as:
```
{
    "code": 403,
    "msg": "Don't attack me",
    "data": []
}
```
or
```
{
    "code": 404,
    "msg": "未找到知识库 技术文档库",
    "data": []
}
```
## FunctionDef _save_files_in_thread(files, knowledge_base_name, override)
**_save_files_in_thread**: This function saves the uploaded file to the corresponding knowledge base directory through multithreading. 

**Parameters**:
- `files`: A `UploadFile`list of objects that represent the files that need to be saved. 
- `knowledge_base_name`: String, specifying the name of the knowledge base where you want to save the file.
- `override`: A boolean value that indicates whether the original file was overwritten if the file already exists.

**Code Description**:
`_save_files_in_thread`Functions primarily handle the `save_file`saving logic of individual files through internally defined functions. For each uploaded file, it first checks for the presence of a file with the same name in the destination path, and if it exists and does not allow overwriting, or if the file size is the same, it logs a warning log and returns a dictionary with error code 404. If the file does not exist or is allowed to be overwritten, the function creates the necessary directory structure and writes the contents of the file to the destination path. During the writing process to a file, if an exception is encountered, an error log is logged and a dictionary containing the error code 500 is returned. 

This function is used `run_in_thread_pool`to execute functions concurrently `save_file`to improve the efficiency of file saving. `run_in_thread_pool`Accept a function and a list of arguments, where each argument is a dictionary containing the`save_file` required parameters. In this way, `_save_files_in_thread`multiple file save operations can be processed at the same time, and each file save operation is performed in a separate thread. 

**Note**:
- When using this function, you need to make sure that `knowledge_base_name`it is valid and that the corresponding knowledge base directory has write permissions. 
- Due to the use of multithreading, you need to be aware of thread safety issues, especially when writing files and creating directories.
- The function returns a generator that returns the saved results of one file per iteration, so these results need to be handled appropriately when this function is called.

**Example output**:
```python
{
    "code": 200,
    "msg": "Successfully uploaded the file example.txt",
    "data": {
        "knowledge_base_name": "sample_kb",
        "file_name": "example.txt"
    }
}
```
This example shows the return value of a successfully saved file, which contains the status code, message, and information about the file.
### FunctionDef save_file(file, knowledge_base_name, override)
**save_file**: The function of this function is to save the uploaded individual file to the specified knowledge base. 

**Parameters**:
- file: UploadFile type, which indicates the file to be uploaded.
- knowledge_base_name: String type, which indicates the name of the target knowledge base.
- override: A boolean type that indicates whether the original file is overwritten if the file already exists.

**Code Description**:
`save_file` The function first extracts the file name from the uploaded file and uses  the function to `get_file_path` construct the storage path of the object file. This path is dynamically generated based on the knowledge base name and file name to ensure that the file can be stored correctly in the corresponding knowledge base directory. 

The function then reads the contents of the uploaded file. Before attempting to save a file, it is checked to see if the file already exists on the destination path and if the option ( parameter is set not to overwrite the existing file`override` ). If the file already exists and is not allowed to be overwritten, the function logs a warning log and returns a dictionary with error codes and messages. 

If the destination folder does not exist, the function creates the necessary directory structure. Then, open the target file path in binary write mode and write the uploaded file content into it.

After the file is successfully saved, the function returns a dictionary containing the success code and message. If an exception occurs during file saving, the function catches the exception, logs an error log, and returns a dictionary with the error code and message.

**Note**:
- Before using this function, make sure that the argument passed in `file` is a valid `UploadFile` object and  that the `knowledge_base_name` argument correctly points to an existing knowledge base. 
- If  the parameter `override` is set to  , `False`and the target file already exists and the file size is the same as the uploaded file, the file will not be overwritten, but a message that the file already exists will be returned. 
- Exception handling is an important part of this function, ensuring stability and reliability during file operations.

**Example output**:
When a file is successfully uploaded, the possible return value is:
```
{
    "code": 200,
    "msg": "成功上传文件 example.docx",
    "data": {
        "knowledge_base_name": "my_knowledge_base",
        "file_name": "example.docx"
    }
}
```
If the file already exists and is not overwritten, the return value might be:
```
{
    "code": 404,
    "msg": "The file example.docx already exists.",
    "data": {
        "knowledge_base_name": "my_knowledge_base",
        "file_name": "example.docx"
    }
}
```
When a file upload fails, the return value may be:
```
{
    "code": 500,
    "msg": "example.docx File upload failed，The error message is: [specific error message]",
    "data": {
        "knowledge_base_name": "my_knowledge_base",
        "file_name": "example.docx"
    }
}
```
***
## FunctionDef upload_docs(files, knowledge_base_name, override, to_vector_store, chunk_size, chunk_overlap, zh_title_enhance, docs, not_refresh_vs_cache)
**upload_docs**: This function is used to upload files to the knowledge base, with the option to vectorize the files. 

**Parameters**:
- `files`: A list of uploaded files, which supports multi-file uploading.
- `knowledge_base_name`: Knowledge base name, specifies the target knowledge base to which you want to upload files.
- `override`: Boolean value, indicating whether to overwrite an existing file.
- `to_vector_store`: Boolean value, which indicates whether the file is vectorized after it is uploaded.
- `chunk_size`: The maximum length of a single piece of text in the knowledge base.
- `chunk_overlap`: The coincident length of adjacent text in the knowledge base.
- `zh_title_enhance`: Boolean value, indicating whether to enable the Chinese title enhancement function.
- `docs`: Custom docs, which needs to be converted to JSON string format.
- `not_refresh_vs_cache`: Boolean value to indicate whether to temporarily save the vector library (for FAISS).

**Code Description**:
The function first verifies the validity of the knowledge base name, and if it is not valid, it returns a 403 status code and displays an error message. Then, obtain the corresponding knowledge base service instance based on the knowledge base name. If the instance fails to be obtained, a 404 status code is returned and a message indicating that the knowledge base was not found. 

The function continues to execute, saving the uploaded file to disk and recording the file that failed to be saved. For files that need to be vectorized, the function will call`update_docs` the function to process them and update the list of failed files. If it`not_refresh_vs_cache` is`False`, the vector library is saved. 

Finally, the function returns a response with the result of the operation, which includes a list of failed files.

**Note**:
- Make sure that the incoming knowledge base name already exists in the system.
- The uploaded file will be saved to the specified knowledge base directory, and if`override` the parameter is Yes`False`, the existing file with the same name will not be overwritten. 
- If you choose to do vectorization, you need to consider the performance and resource constraints of the server.
- Custom docs need to be properly formatted as JSON strings to ensure they can be parsed and processed correctly.

**Example output**:
```json
{
  "code": 200,
  "msg": "File upload and vectorization completed",
  "data": {
    "failed_files": {
      "error_file.txt": "Error message of file saving failure"
    }
  }
}
```
This example shows the success of a function execution, with `failed_files`a field listing the files that failed to be processed and their error messages. 
## FunctionDef delete_docs(knowledge_base_name, file_names, delete_content, not_refresh_vs_cache)
**delete_docs**: This function is used to delete the specified file from the knowledge base. 

**Parameters**:
- `knowledge_base_name`: The name of the knowledge base, the type is a string, and the example value is["samples"]. 
- `file_names`: A list of file names to be deleted, of type as a string list, and an example value of [["file_name.md", "test.txt"]]. 
- `delete_content`: Boolean value, specifies whether to delete the file contents from disk, defaults`False`. 
- `not_refresh_vs_cache`: Boolean, specifies whether to temporarily save the vector library (for FAISS), defaults`False`, and describes it as "temporarily do not save vector library (for FAISS)". 

**Code Description**:
The function first verifies the validity of the knowledge base name, and if it is not, it returns a 403 status code and the error message "Don't attack me". After that, the URL of the knowledge base name is decoded and the corresponding knowledge base service instance is obtained. If the knowledge base service instance does not exist, a 404 status code and an error message are returned, indicating that the knowledge base was not found. 

For each specified file name, the function checks whether the file exists in the knowledge base. If the file doesn't exist, add it to the list of failed files. For files that exist, try to delete the files, including deleting the records from the knowledge base and optionally deleting the file contents from disk. If an exception occurs during the deletion process, the exception information is recorded in the list of failed files, and an error log is recorded.

If so`not_refresh_vs_cache``False`, then the `save_vector_store`method is called to save the vector library. Finally, the function returns a 200 status code and a response with a list of failed files. 

**Note**:
- Before calling this function, make sure that the incoming list of knowledge base names and file names is correct, and that the knowledge inventory is there.
- `delete_content`Parameters should be used sparingly, as the operation is irreversible once the file contents are deleted from the disk.
- `not_refresh_vs_cache`The parameter is used to control whether the state of the vector library is saved immediately, which can be used to optimize performance when deleting files in bulk.

**Example output**:
If all the specified files are successfully deleted and there is no vector library to refresh, the function may return a response like this:
```json
{
  "code": 200,
  "msg": "File deletion complete",
  "data": {
    "failed_files": {}
  }
}
```
If there are files that were not found or failed to be deleted, the response `failed_files`will include the names of those files and the associated error information. 
## FunctionDef update_info(knowledge_base_name, kb_info)
**update_info**: This function is used to update the introductory information of the knowledge base. 

**Parameters**:
- `knowledge_base_name`: The name of the knowledge base, of type String. This parameter is required to specify the knowledge base to update the introductory information.
- `kb_info`: Introduction to the knowledge base, type of string. This parameter is required to provide a new knowledge base introduction.

**Code Description**:
First, the`update_info` function `validate_kb_name` verifies that the incoming knowledge base name is valid by calling the function. If the knowledge base name is invalid (for example, it contains potentially security risk characters), the function will return an object with status code 403 `BaseResponse` and the message "Don't attack me", indicating that the request was denied. 

If the knowledge base name is validated, the function then tries to `KBServiceFactory.get_service_by_name` get the service instance of the corresponding knowledge base through the method. If the specified knowledge base does not exist (i.e., the service instance is None), the function will return an object with status code 404 with the `BaseResponse` message "Knowledge base not found {knowledge_base_name}", indicating that the specified knowledge base was not found. 

When the knowledge base service instance is successfully obtained, the function calls the method of the instance `update_info` and passes in the new knowledge base introduction information `kb_info` to update it. 

Finally, the function returns an object with status code 200 `BaseResponse` with the message "Knowledge Base Introduction Modified Completed" and returns the updated knowledge base introduction information in the data field, indicating that the knowledge base introduction information has been updated successfully. 

**Note**:
- Before calling this function, make sure that the incoming knowledge base name already exists and is valid in the system, otherwise it may cause the update to fail.
- The operation of updating the information about the knowledge base may be limited by the instance type of the knowledge base service, ensuring that the knowledge base service supports the information update operation.

**Example output**:
If the update operation succeeds, the function might return an example object like this `BaseResponse` :
```
{
    "code": 200,
    "msg": "The knowledge base introduction has been modified.",
    "data": {
        "kb_info": "This is an updated knowledge base introduction"
    }
}
```
If the knowledge base name is invalid, an example of an object returned `BaseResponse` might be as follows:
```
{
    "code": 403,
    "msg": "Don't attack me",
    "data": null
}
```
If the specified knowledge base is not found, an example of the returned `BaseResponse` object might be as follows:
```
{
    "code": 404,
    "msg": "Knowledge Base Not Found {knowledge_base_name}",
    "data": null
}
```
## FunctionDef update_docs(knowledge_base_name, file_names, chunk_size, chunk_overlap, zh_title_enhance, override_custom_docs, docs, not_refresh_vs_cache)
**update_docs**: This function is used to update documents in the knowledge base. 

**Parameters**:
- `knowledge_base_name`: Knowledge base name, string type, required parameters.
- `file_names`: A list of file names, which supports multiple files, and each element in the list is of string type.
- `chunk_size`: The maximum length of a single paragraph of text in the knowledge base, integer type.
- `chunk_overlap`: The coincident length of adjacent text in the knowledge base, integer type.
- `zh_title_enhance`: Whether to enable Chinese title enhancement, Boolean type.
- `override_custom_docs`: Whether to override the previously customized docs, Boolean type, default is False.
- `docs`: Custom docs, need to be converted to json string, dictionary type.
- `not_refresh_vs_cache`: Do not save vector library (for FAISS), Boolean type, default is False.

**Code Description**:
This function first verifies whether the incoming knowledge base name is valid, and if not, returns a 403 status code and an error message. Then, obtain the corresponding knowledge base service instance by the knowledge base name. If the instance fails to be obtained, a 404 status code and error message are returned. 

The function continues to run and generates a list of files that need to be loaded with docs. For each file, first check if the file uses custom docs, if it is and does not override the custom docs, then skip the file. Otherwise, try adding the file to the pending list. If an exception occurs during this process, an error message is logged.

Next, the function converts the files in the file list into docs and vectorizes them. This step is performed in the background using multiple threads to improve processing efficiency. After processing is complete, if you specify not to flush the vector library cache, the vector library is not saved immediately; Otherwise, the method of the knowledge base service is called`save_vector_store` to save the vector library. 

Finally, the function returns 200 status codes and processing results, including a list of files that failed to be processed.

**Note**:
- When using this function, make sure that the incoming knowledge base name already exists in the system.
- If you need to perform custom docs processing on the file, make sure that the`docs` parameters are formatted correctly and that the file name`file_names` matches the file name in . 
- This function supports batch processing of files, but you need to be aware of server resource and performance limitations.

**Example output**:
```json
{
  "code": 200,
  "msg": "Update document completed",
  "data": {
    "failed_files": {
      "error_file.txt": "Error loading document"
    }
  }
}
```
This example shows the success of a function execution, with `failed_files`a field listing the files that failed to be processed and their error messages. 
## FunctionDef download_doc(knowledge_base_name, file_name, preview)
**download_doc**: This function is used to download documents from the knowledge base. 

**Parameters**:
- `knowledge_base_name`: The name of the knowledge base, which specifies the knowledge base from which the document is downloaded.
- `file_name`: File name, specifying the name of the file to be downloaded.
- `preview`: Preview, a boolean value that indicates whether the user wants to preview the file in the browser or download the file directly.

**Code Description**:
`download_doc` The function first `validate_kb_name` verifies that the incoming knowledge base name is valid by calling the function. If the knowledge base name is invalid, the function will return an object with a 403 status code `BaseResponse` , prompting the user not to attack. Next, the function tries to `KBServiceFactory.get_service_by_name` get the service instance of the corresponding knowledge base through the method. If the corresponding KB instance cannot be found, an object with a 404 status code will be returned `BaseResponse` , indicating that the specified KB cannot be found. 

Depending on `preview` the value of the parameter, the function is set . `content_disposition_type` If `preview`  is , `True`it is set to  allow the `"inline"`file to be previewed in the browser; Otherwise,`content_disposition_type` for  , `None`the file will be downloaded. 

The function then creates an `KnowledgeFile` instance that represents and processes the files in the knowledge base. If the file exists on disk, the function returns an `FileResponse` object that allows the user to download or preview the file. If an exception occurs when trying to read a file, the function will log an error message and return an object with a 500 status code `BaseResponse` indicating that the file failed to be read. 

**Note**:
- Before calling this function, make sure that the incoming knowledge base name and file name are correct.
- If the knowledge base name is invalid or the file does not exist, the function will return an error response.
- This function supports file preview and download functions, which are controlled by `preview` parameters. 

**Example output**:
Suppose there is a knowledge base called "samples" that contains a file named "test.txt". If called `download_doc(knowledge_base_name="samples", file_name="test.txt", preview=False)`, the function will return an `FileResponse` object that allows the user to download a "test.txt" file. If the specified file does not exist, an object with a 404 status code will be returned `BaseResponse` indicating that the file was not found. 
## FunctionDef recreate_vector_store(knowledge_base_name, allow_empty_kb, vs_type, embed_model, chunk_size, chunk_overlap, zh_title_enhance, not_refresh_vs_cache)
**recreate_vector_store**: This function is used to rebuild a vector library from a document in the content folder. 

**Parameters**:
- `knowledge_base_name`: The name of the knowledge base, the type is string, and the default example is samples.
- `allow_empty_kb`: Whether to allow empty knowledge base, Boolean type, default is True.
- `vs_type`: Vector library type, string type, default value`DEFAULT_VS_TYPE`. 
- `embed_model`: Embedding model name, string type, default value`EMBEDDING_MODEL`. 
- `chunk_size`: The maximum length of a single paragraph of text in the knowledge base, integer type, default value`CHUNK_SIZE`. 
- `chunk_overlap`: The coincident length of adjacent text in the knowledge base, integer type, default value`OVERLAP_SIZE`. 
- `zh_title_enhance`: Whether to enable the Chinese title enhancement function, Boolean type, the default value is`ZH_TITLE_ENHANCE`. 
- `not_refresh_vs_cache`: Whether to temporarily save the vector library (for FAISS), Boolean type, default is False.

**Code Description**:
`recreate_vector_store`Functions are primarily used to rebuild vector libraries from content files in cases where the user copies the files directly to the content folder rather than transferring them over the network. By default, only`info.db` knowledge bases that exist in and contain document files are returned. By setting`allow_empty_kb` it to True, you can make the function also work for `info.db`empty knowledge bases that don't exist in or have no documentation in them. The function internally first tries to get the specified knowledge base service, and if the knowledge base does not exist and an empty knowledge base is not allowed, a 404 error is returned. If the knowledge stock is there, clear the existing vector library and recreate it. The function then iterates through all the files in the content folder and converts them to documents, taking into account the chunk size of the text, the coincident length, and whether Chinese title enhancement is turned on. Each time a file is processed, a JSON object containing the processing status is generated and returned by the generator. If an error occurs while adding a file to the knowledge base, the error is logged and the file is skipped. Finally, if it's not set to not flush the vector library cache, save the vector library. 

In the project, `recreate_vector_store`the function is `server/api.py/mount_knowledge_routes`routed through a POST that is registered as FastAPI. This means that the function can be called via an HTTP POST request to rebuild the knowledge base's vector library after the user has otherwise dropped the file directly into the content folder. This is especially useful when managing a knowledge base, especially if you need to bulk update document content without wanting to upload them one by one. 

**Note**:
- Make sure that the file format and content in the content folder meet the requirements of the knowledge base before calling this function.
- The execution time of a function can vary greatly depending on the number and size of files in the content folder.

**Example output**:
```json
{
    "code": 200,
    "msg": "(1 / 10): example.docx",
    "total": 10,
    "finished": 1,
    "doc": "example.docx"
}
```
This JSON object indicates that the first file has been processed successfully, and there are a total of 10 files to be processed, and 1 has been completed.
### FunctionDef output
**output**: The function of this function is to reconstruct the vector storage of the knowledge base and output the state information during processing. 

**Parameters**: This function does not accept any external parameters. 

**Code Description**: 
`output` The function first `KBServiceFactory.get_service` obtains the service instance of the corresponding knowledge base through the method, which is determined according to the knowledge base name, vector storage type, and embedding model. If the specified knowledge base does not exist and does not allow the creation of an empty knowledge base, the function generates and returns a JSON object containing the error code 404 and the corresponding error message. If the knowledge stock is there, the function clears the vector store in the knowledge base and then recreates the knowledge base. 

Next, the function `list_files_from_folder` lists all the files in the knowledge base folder via the method and creates an instance for each file `KnowledgeFile` . These file instances are then batched to `files2docs_in_thread` convert the file content into documents and add to the knowledge base via the method. During the file conversion process, the function generates and returns JSON objects containing the processing status one by one, including information such as processing progress and file names. 

If an error is encountered during the file conversion process, the function logs the error message and generates a JSON object containing the error code 500 and the corresponding error message. Once all file processing is complete, if you don't need to flush the vector storage cache, `save_vector_store` the Save  Vector library method is called. 

**Note**:
- Before you can call this function, you need to ensure that  the `KBServiceFactory.get_service` knowledge base service instance is returned correctly based on the parameters provided. 
- `list_files_from_folder` The method is used to list all the files in the knowledge base folder to ensure that the knowledge base folder path is correct.
- `files2docs_in_thread` The method is responsible for converting the file content into a document and adding it to the knowledge base, the process is multi-threaded, and thread safety issues need to be noted.
- `save_vector_store` Methods are used to hold vector libraries, ensuring that all the data that needs to be saved has been processed correctly before calling this method.
- This function returns processing state information through the generator, and the caller needs to handle these generated JSON objects appropriately for state monitoring or error handling.
***
