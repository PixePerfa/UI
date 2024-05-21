## FunctionDef embed_texts(texts, embed_model, to_query)
**embed_texts**: The function of this function is to vectorize the text and return the vectorization result. 

**Parameters**:
- `texts`: A list of text that needs to be vectorized.
- `embed_model`: The name of the embedding model used, which defaults to the embedding model specified in the configuration.
- `to_query`: Boolean, which indicates whether the vectorized text is used in the query, defaults to False.

**Code Description**:
`embed_texts`The function first checks whether the specified embedding model is in the list of local embedding models. If so, it `load_local_embeddings`will use a function to load the local embedding model, vectorize the text, and then return an object containing the vectorized result`BaseResponse`. If the specified embedding model is not in the list of local models, the function checks whether the model is in the list of online models that support embedding functionality. For online models, the function will create the corresponding working class instance according to the model configuration, and call its embedding method for text vectorization, which also returns`BaseResponse` the object. If the specified embedding model is neither in the local model list nor in the online model list, the function will return an error message stating that the specified model does not support the embedding feature. Throughout the process, if any exceptions are encountered, the function will catch the exceptions and return an object with the error message`BaseResponse`. 

**Note**:
- When using `embed_texts`functions, you need to make sure that the arguments you pass in`texts` are valid text lists. 
- `embed_model`The parameters should be specified correctly so that the function can find and use the correct embedding model for text vectorization.
- `to_query`Parameters should be set according to actual needs to optimize the use scenarios of vectorization results.
- The execution result of a function depends on the validity and availability of the specified embedded model, so you should confirm that the model is configured correctly and that the model is available before using it.

**Example output**:
The call `embed_texts(texts=["Hello", "World"], embed_model="example_model", to_query=False)`might return something like this`BaseResponse`:
```python
BaseResponse(code=200, msg="success", data=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
```
This means that the two texts "Hello" and "World" are successfully vectorized, and the vectorization results are`[0.1, 0.2, 0.3]` and `[0.4, 0.5, 0.6]`respectively. 
## FunctionDef aembed_texts(texts, embed_model, to_query)
**aembed_texts**: The function of this function is to perform asynchronous vectorization of a list of text and return a BaseResponse object containing the vectorization result. 

**Parameters**:
- `texts`: A list of text that needs to be vectorized, of type List[str]. 
- `embed_model`: The name of the embedding model used, the default value is the embedding model specified in the configuration, and the type is str.
- `to_query`: Boolean, which indicates whether the vectorized text is used in the query, defaults to False.

**Code Description**:
`aembed_texts`The function first checks `embed_model`to see if it is in the list of locally embedded models. If so, a `load_local_embeddings`function is used to load the local embedding model, and the method is called asynchronously`aembed_documents` for text vectorization, and finally an object containing the vectorization result is returned`BaseResponse`. If `embed_model`you are in the list of online models that support embedding, the function is`run_in_threadpool` called asynchronously to `embed_texts`perform text vectorization and return the corresponding `BaseResponse`object. If an exception occurs during vectorization, the function will catch the exception and return an object with an error message`BaseResponse` set to 500. 

**Note**:
- When you call this function, you need to make sure that the arguments you pass in`texts` are valid text lists. 
- `embed_model`The parameters should be specified correctly so that the function can find and use the correct embedding model for text vectorization. If not specified, the embedding model with the default configuration will be used.
- `to_query`The parameters should be set according to the actual requirements. If the vectorized text is used for queries, this parameter should be set to True to optimize the use case of the vectorized results.
- The execution result of a function depends on the validity and availability of the specified embedded model, so you should confirm that the model is configured correctly and that the model is available before using it.

**Example output**:
The call `await aembed_texts(texts=["你好", "世界"], embed_model="example_model", to_query=False)`might return something like this`BaseResponse`:
```python
BaseResponse(code=200, msg="success", data=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
```
This means that the two texts "Hello" and "World" are successfully vectorized, and the vectorization results are`[0.1, 0.2, 0.3]` and `[0.4, 0.5, 0.6]`respectively. 

In the project, `aembed_texts`functions are used to handle scenarios that require asynchronous text vectorization, such as asynchronous vectorization of text in the knowledge base service to support fast text queries and similarity calculations. In addition, it also supports text vectorization through an online API, providing a flexible vectorization solution for projects. 
## FunctionDef embed_texts_endpoint(texts, embed_model, to_query)
**embed_texts_endpoint**: The function of this function is to vectorize the text list and return the processing result. 

**Parameters**:
- `texts`: The list of text to be embedded is a list of strings. This parameter is mandatory.
- `embed_model`: Embedding model used. This can be an on-premise Embedding model or an embedding service provided by an online API. The default value is the embedding model specified in the configuration.
- `to_query`: A boolean value that indicates whether the vector is used for the query. Some models, such as Minimax, are optimized for storage/query vectors. The default value is False.

**Code Description**:
`embed_texts_endpoint`The function first receives a list of texts, an embedding model name, and a Boolean parameter. It calls`embed_texts` a function and passes those parameters to the function for processing. `embed_texts`The function vectorizes the text according to the specified embedding model and returns an `BaseResponse`object containing the results of the vectorization. If any exceptions are encountered during the vectorization process, the`embed_texts` function catches those exceptions and returns an object with error information`BaseResponse`. `embed_texts_endpoint`The function ultimately returns `embed_texts`the output of the function, which is the result of the vectorization process. 

**Note**:
- When calling a `embed_texts_endpoint`function, you must provide a valid list of texts. 
- `embed_model`Parameters should be specified accurately to ensure that the function can find and process with the correct embedding model.
- Set parameters based on actual requirements `to_query`to optimize the use scenarios of vectorization results. 
- The execution result of a function depends on the validity and availability of the specified embedded model, so you should confirm that the model is configured correctly and that the model is available before using it.

**Example output**:
The call `embed_texts_endpoint(texts=["hello", "world"], embed_model="example_model", to_query=False)`might return something like this`BaseResponse`:
```python
BaseResponse(code=200, msg="success", data=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
```
This means that the two texts "hello" and "world" were successfully vectorized, and the vectorization results were`[0.1, 0.2, 0.3]` and `[0.4, 0.5, 0.6]`respectively. 
## FunctionDef embed_documents(docs, embed_model, to_query)
**embed_documents**: The function of this function is to vectorize the list of documents into a parameter format that can be accepted by the vector storage system. 

**Parameters**:
- `docs`: A list of document objects, each containing page content and metadata.
- `embed_model`: String type, specifies the embedding model used for document vectorization, and uses the preset embedding model by default.
- `to_query`: Boolean type, which indicates whether the result of the vectorization is used in the query, defaults to False.

**Code Description**:
`embed_documents`The function first extracts the page content and metadata from the list of documents, which are stored in and`texts` `metadatas`list, respectively. Next,`embed_texts` the function is called to `texts`vectorize the text in the list, where the `embed_model`argument specifies the embedding model to be used, and the`to_query` argument indicates the purpose of the vectorization. `embed_texts`The function returns a data structure that contains the results of the vectorization. If the vectorization is successful, the`embed_documents` function returns a dictionary containing a list of raw text`texts`, the vectorization results,`embeddings` and a list of metadata`metadatas`. 

**Note**:
- When calling a `embed_documents`function, make sure that the arguments passed in`docs` are a valid list of document objects. 
- `embed_model`Parameters should point to a valid embedding model to ensure that the text is properly vectorized.
- Select `to_query`the values of the parameters based on the usage scenario to optimize the application of the vectorization results. 

**Example output**:
Suppose you call`embed_documents(docs=[Document1, Document2], embed_model="example_model", to_query=False)`, you might return a dictionary like this:
```python
{
    "texts": ["Contents of document 1", "Contents of document 2"],
    "embeddings": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
    "metadatas": [{"title": "Document 1 title"}, {"title": "Document 2 title"}]
}
```
This means that the two documents have been successfully vectorized, containing`texts` the original content of the document, `embeddings`the corresponding vectorization results, and`metadatas` the metadata information of the document. 
