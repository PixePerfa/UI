## FunctionDef _get_result_to_documents(get_result)
**_get_result_to_documents**: The function of this function is to convert the`GetResult` query results of a type into`Document` a list of objects. 

**Parameters**:
- `get_result`: `GetResult`Type, which indicates the result obtained from the database query. 

**Code Description**:
`_get_result_to_documents`Functions are primarily used to process the results of a database query and convert those results into`Document` a list of objects. First of all, the function checks`get_result` whether the field in it `documents`is empty, and if it is, it directly returns an empty list. If it is not empty, the processing continues. 

Next, the function checks`get_result` the fields in it`metadatas`. If the `metadatas`field exists and is not empty, the value of the field is used; If it doesn't exist or is empty, an empty dictionary list is created that is `documents`the same length as the field. This step ensures that each document has a corresponding metadata, and that an empty dictionary is assigned even if some documents do not have metadata. 

The function then traverses`documents` and `metadatas`lists, packages their elements into `Document`objects, and adds them to a new list`document_list`. Here, `Document`the objects are constructed by keyword arguments`page_content` and corresponding `metadata`to the content and metadata of each document, respectively. 

Finally, the function returns a `Document`list of constructed objects. 

In a project, `_get_result_to_documents`a function is called by`ChromaKBService` a class's`get_doc_by_ids` methods. `get_doc_by_ids`The method is responsible for querying the document from the database based on a given list of IDs and uses`_get_result_to_documents` a function to convert the query result into `Document`a list of objects for further processing or in response to client requests. 

**Note**:
- Make sure that the incoming `get_result`parameters are formatted correctly, especially`documents` the and `metadatas`fields, to avoid runtime errors. 
- This function does not interact directly with the database, but processes the results that have already been queried.

**Example output**:
```python
[
    Document(page_content="文档内容1", metadata={"作者": "张三"}),
    Document(page_content="文档内容2", metadata={"作者": "李四"})
]
```
This example shows what a `_get_result_to_documents`list of objects can look like when a function processes the results of a query that contains the contents of two documents and the corresponding metadata`Document`. 
## FunctionDef _results_to_docs_and_scores(results)
**_results_to_docs_and_scores**: The function of this function is to convert the search results into a list of documents and scores. 

**Parameters**:
- `results`: Search results of any type that are expected to include document content, metadata, and distance.

**Code Description**:
`_results_to_docs_and_scores` The function receives a parameter containing the search results`results`, which is expected to be a dictionary with three keys:`"documents"` ,`"metadatas"` , and `"distances"`. The value of each key is a list, and each element in the list represents the content of the searched document, the metadata of the document, and the distance between the document and the query (often used to represent a score of similarity or relevance). 

The function iterates over the three lists in parallel (using `zip` a function) to create a tuple for each search result that contains an `Document` object and a floating-point number. `Document` An object is made up of document content and metadata, and a floating-point number is the distance between the document and the query. This process generates a list of tuples, each representing a search result and its relevance score. 

In a project,`_results_to_docs_and_scores` a function is called by `ChromaKBService` a method of the class `do_search` . `do_search` The method is responsible for executing the search query and using  the function `_results_to_docs_and_scores` to process the query results, converting them into a format that is easier to process and present. This design pattern allows for the separation of the search logic from the result processing logic, improving the readability and maintainability of the code. 

**Note**:
- Make sure that the input `results` parameter is formatted correctly, that is, it contains `"documents"` three keys,`"metadatas"` , and  that `"distances"` the value corresponding to each key is in list format. 
- The function relies on `Document` the correct implementation of the class. `Document` The class needs to be able to accept page content and metadata as parameters and encapsulate them as an object. 

**Example output**:
```python
[
    (Document(page_content="文档内容1", metadata={"作者": "张三"}), 0.95),
    (Document(page_content="文档内容2", metadata={"作者": "李四"}), 0.89)
]
```
This output example shows the possible form of a function return value, with two tuples, each containing an `Document` object and a score representing the similarity to the query. 
## ClassDef ChromaKBService
**ChromaKBService**: The ChromaKBService class is a ChromaDB-based knowledge base service for operating and managing ChromaDB. 

**Properties**:
- `vs_path`: Vector storage path.
- `kb_path`: Knowledge base path.
- `client`: ChromaDB client instance.
- `collection`: A collection of the current knowledge base.

**Code Description**:
The ChromaKBService class inherits from the KBService class and is specifically designed to handle ChromaDB-based knowledge base operations. It provides a range of methods to initialize services, create knowledge bases, delete knowledge bases, add documents, delete documents, empty vector storage, and perform document searches. 

- `vs_type` The method returns the vector storage type used by the current knowledge base service, i.e., ChromaDB.
- `get_vs_path` The and `get_kb_path` methods are used to get the path to the vector store and the knowledge base, respectively. 
- `do_init` method to initialize the ChromaDB client and collection.
- `do_create_kb` method to create a new knowledge base, in effect creating a new collection in ChromaDB.
- `do_drop_kb` method to delete the knowledge base, that is, to delete the collection in ChromaDB.
- `do_search` The method performs a document search, returning a list of documents that are most relevant to the query and their scores.
- `do_add_doc` Methods add documents to the knowledge base, including the document's text, embedding vectors, and metadata.
- `get_doc_by_ids` The and `del_doc_by_ids` methods get and delete documents based on their IDs, respectively. 
- `do_clear_vs` method to empty the vector store, which is achieved by deleting and recreating the collection.
- `do_delete_doc` Method: Deletes the document based on the knowledge file provided.

**Note**:
- Before using ChromaKBService, you need to make sure that your ChromaDB environment is properly set up and available.
- When you call  the method `do_add_doc` to add a document, you need to make sure that the document data contains valid text, embedding vectors, and metadata. 
- Deletion operations (`do_drop_kb`, `del_doc_by_ids`, `do_delete_doc`) should be used with caution to avoid accidental data loss. 

**Example output**:
```python
# 搜索文档的示例输出
[
    (Document(text="文档内容示例", metadata={"author": "作者示例"}), 0.95),
    (Document(text="另一个文档内容示例", metadata={"author": "另一个作者示例"}), 0.90)
]
```
This example shows the list of documents that might be returned after performing a document search operation and their relevance scores. Each tuple contains an instance of Document, which contains the text and metadata of the document, and a score.
### FunctionDef vs_type(self)
**vs_type**: The function of the vs_type function is to return the vector storage type that is currently supported by the knowledge base service. 

****Arguments: This function has no arguments. 

**Code Description**: The vs_type function is a method of the ChromaKBService class that specifies the type of vector storage supported by the knowledge base service instance. In this concrete implementation, the vs_type method explicitly indicates that ChromaKBService supports ChromaDB as its vector storage service by returning the CHROMADB value in the SupportedVSType enumeration class. The SupportedVSType enumeration class defines a series of vector storage types that are supported in a series of projects, including but not limited to FAISS, MILVUS, ZILLIZ, PostgreSQL, Elasticsearch, etc., where CHROMADB stands for using ChromaDB as a vector storage service. This design allows the repository service to specify and use different vector storage solutions in a flexible way in the project, while also facilitating the dynamic selection and instantiation of the corresponding repository service implementation as needed in KBServiceFactory. 

**Note**:
- When using the vs_type method, the developer does not need to pass any parameters, and the method will automatically return the vector storage type supported by ChromaKBService.
- The returned vector store type should be consistent with the type defined in the SupportedVSType enumeration class to ensure proper instantiation and use of the knowledge base service.
- When extending your project to support a new vector store service, you should add new types to the SupportedVSType enumeration class and ensure that the knowledge base service class correctly implements vs_type methods to reflect this change.

**Example output**: 
```python
'chromadb'
```
In this example, the vs_type method will return a string 'chromadb', indicating that the ChromaKBService class supports the use of ChromaDB as its vector storage service.
***
### FunctionDef get_vs_path(self)
**get_vs_path**: The function of this function is to get the path of the vector space. 

**Parameters**: This function has no explicit arguments, but depends on the sum properties of the object`kb_name``embed_model`. 

**Code Description**: `get_vs_path`A function is `ChromaKBService`a method of a class that returns a vector space path to a knowledge base. It is implemented by calling a global function`get_vs_path` that takes two parameters: the knowledge base name (`kb_name`) and the embedding model (`embed_model`). These two parameters are `ChromaKBService`properties of the object, representing the name of the current knowledge base and the embedding model used, respectively. The return value for this method is a string that represents the file path in the vector space. 

In a project, `get_vs_path`methods are called by`do_init` methods. In the`do_init` method, you first `get_kb_path`get the path to the knowledge base by calling it, then call `get_vs_path`the path to get the vector space, and use this path to initialize`PersistentClient` the object. This shows that `get_vs_path`the method plays a key role in the knowledge base initialization process, ensuring that the path of the vector space can be correctly retrieved and used for subsequent database clients and collection creation. 

**Note**: When using `get_vs_path`the method, you need to make sure that`ChromaKBService` the sum properties of the object`kb_name` `embed_model`are set correctly, as these two properties directly affect the generation of vector space paths. 

**Example output**: Assuming the knowledge base name is and`example_kb` the embedding model is`model_v1`, an `get_vs_path`example of the path that might be returned is`/path/to/vector_space/example_kb_model_v1.vs`. 
***
### FunctionDef get_kb_path(self)
**get_kb_path**: The function of this function is to get the path to the knowledge base. 

****Arguments: This function has no arguments. 

**Code Description**:  A `get_kb_path` function is `ChromaKBService` a method of a class, and its main function is to return the path to the knowledge base. This method does this by calling `get_kb_path` a function and passing `self.kb_name` it  as an argument. Here,`self.kb_name` is `ChromaKBService` a property of the class, which stores the name of the current knowledge base. In this way, the`get_kb_path` method is able to dynamically get the path of the knowledge base based on its name. 

In a project,`get_kb_path` a method is called by `do_init` a  method. In a `do_init` method, you first `get_kb_path` get the knowledge base path by calling the method and store it in a `self.kb_path` property. This step is part of the initialization process and ensures that subsequent operations are based on the correct knowledge base path. In addition,`do_init` the method involves operations such as getting the view store path and initializing the persistence client, which are all steps that are necessary for the proper functioning of the knowledge-based service. 

**Note**: When using `get_kb_path` the method, you need to make sure that  has `self.kb_name` been assigned correctly, as this will directly affect the result of getting the path. 

**Example output**: Assuming the name of the current knowledge base is "example_kb", the `get_kb_path` return value of the method might look something like this:
```
"/path/to/knowledge_bases/example_kb"
```
***
### FunctionDef do_init(self)
**do_init**: The function of this function is to initialize the ChromaKBService object. 

****Arguments: This function has no arguments. 

**Code Description**: `do_init`Methods `ChromaKBService`are a key method of the class that is responsible for initializing the core components of the knowledge base service. This method first calls`get_kb_path` the method to get the path to the knowledge base and stores this path in the`self.kb_path` properties. Next, it calls `get_vs_path`a method to get the path to the vector space and uses that path to initialize`PersistentClient` the object, which is stored in properties`self.client`. Finally, the `self.client`method uses a `get_or_create_collection`property (i.e., the name of the knowledge base) to get or create a collection, and this collection object is stored`self.kb_name` `self.collection`in the property. 

From a functional point of view,`do_init` methods ensure that the knowledge base service can correctly access the knowledge base path and vector space path through the combination`get_kb_path` and `get_vs_path`function of the method. These two paths are critical for subsequent knowledge base operations because they determine where the knowledge base data is stored and where the vector space data is stored, respectively. Through`PersistentClient` objects, `do_init`methods further ensure that the knowledge base service is capable of persistent operations, such as data storage and retrieval. In addition, the `self.collection`initialization provides a basis for the management of data in the knowledge base, so that the addition, deletion, query and modification of data can be carried out on this basis. 

**Note**: Before calling `do_init`a method, you need to make sure that `ChromaKBService`the sum properties of the object`kb_name` `embed_model`are set correctly, as these properties will affect `get_vs_path`the execution result of the method, which in turn will affect the initialization process of the entire knowledge base service. In addition, the `do_init`successful execution of the method is a prerequisite for all subsequent knowledge base operations to be carried out normally, so the invocation of this method is an indispensable step in the startup process of the knowledge base service. 
***
### FunctionDef do_create_kb(self)
**do_create_kb**: The function of this function is to create a knowledge base (KB) in ChromaDB. 

**Parameters**: This function does not accept any external parameters. 

**Code Description**: `do_create_kb`A function is `ChromaKBService`a method of a class that is used to create a new knowledge base in ChromaDB. In ChromaDB, the concept of a knowledge base corresponds to a collection. Therefore, the main task of this function is to create or get a collection that corresponds to the name of the knowledge base (`self.kb_name`). This is done by calling`self.client.get_or_create_collection(self.kb_name)` a `self.client`reference to the ChromaDB client and the `self.kb_name`name of the collection that needs to be created or obtained. If a collection with the specified name already exists, this operation will return a reference to the existing collection; If it doesn't exist, a new collection is created and its reference is returned. After the operation is complete, the reference to the collection is stored`self.collection` in a property so that it can be used by subsequent operations. 

**Note**: When using `do_create_kb`the method, you need to make sure that it `self.client`has been initialized correctly and that you can connect to the ChromaDB server. In addition, `self.kb_name`it should be a valid collection name, following any restrictions or rules that ChromaDB has on collection names. Before calling this method, it's a good idea to confirm that these conditions have been met to avoid runtime errors. 
***
### FunctionDef do_drop_kb(self)
**do_drop_kb**: The function of this function is to delete a collection in ChromaDB. 

****Arguments: This function has no arguments. 

**Code Description**: `do_drop_kb`The function is responsible for deleting a collection named in the ChromaDB database`kb_name`. This process first tries to do this by calling`self.client.delete_collection` a method, which `self.kb_name`is passed as an argument, specifying the name of the collection to be deleted. If an exception is encountered during the deletion process `ValueError`and the exception message is not because the collection does not exist (i.e. the error message is not "Collection {self.kb_name} does not exist." ), the exception will be re-thrown so that the caller can handle the exception. This design ensures that the execution of the program is interrupted only when an unexpected error is encountered, and that the continuation of the program is not affected if there is no such possible expectation for the collection. 

In a project, `do_drop_kb`a function is `do_clear_vs`called by a function as part of the operation to empty the vector store. In a`do_clear_vs` function, a call `do_drop_kb`can be understood as deleting the corresponding collection before emptying the vector store, probably because in some cases it is more efficient or business logic to delete the collection directly than to attempt to empty its contents. 

**Note**: When using `do_drop_kb`functions, you need to make sure that the name of the `self.kb_name`target collection has been set correctly, and that the caller should be prepared to handle exceptions that may be thrown`ValueError`, especially if the collection may not exist. In addition, considering that deleting a collection is an irreversible operation, this function should be used with caution to ensure that its invocation is in the appropriate context and in accordance with the needs of the business logic. 
***
### FunctionDef do_search(self, query, top_k, score_threshold)
**do_search**: The function of this function executes a text query and returns the documents that are most relevant to the query and their relevance scores. 

**Parameters**:
- `query`: The query text that needs to be searched, and the data type is a string.
- `top_k`: The number of the most relevant documents returned, with data type as an integer.
- `score_threshold`: The threshold for the relevance score, which defaults to SCORE_THRESHOLD, and only documents with scores above this threshold will be returned, with the data type floating-point number.

**Code Description**:
`do_search`Functions are first used `EmbeddingsFunAdapter`as an embedding model to create an embedding function`self.embed_model` through the instantiation of a class`embed_func`. Then, use `embed_func.embed_query(query)`the method to convert the query text`query` into an embedding vector`embeddings`. This step is done by converting the text into a vectorized representation so that the similarity calculation can be carried out subsequently. 

Next, the function calls `self.collection.query`the method, passing in the query embedding vector`embeddings` and the number of results`n_results` equal `top_k`to the number of results, to perform the query operation. This method returns an`QueryResult` object that contains the results of the query. 

Finally, the function is called`_results_to_docs_and_scores(query_result)`, which converts the query results into a list of documents and scores. This step parses `QueryResult`the object, extracts each document and its similarity score to the query text, and then encapsulates the information into a tuple list. 

Throughout the process,`do_search` the function`EmbeddingsFunAdapter` `_results_to_docs_and_scores`implements the complete process from text query to obtaining the relevant document and its score by interacting with the sum function. 

**Note**:
- Make sure that `query`the parameter is a valid utterance and that the parameter is`top_k` set correctly to return the desired number of results. 
- The performance and accuracy of functions depend on the quality of the embedding model and the query processing mechanism, so choosing the appropriate embedding model and adjusting the query parameters are critical to obtaining useful search results.
- The default `score_threshold`is SCORE_THRESHOLD, which can be adjusted as needed to filter out low-relevance results. 

**Example output**:
```python
[
    (Document(page_content="文档内容1", metadata={"作者": "张三"}), 0.95),
    (Document(page_content="文档内容2", metadata={"作者": "李四"}), 0.89)
]
```
This output example shows what a function can return a value in a possible way, with two tuples, each containing an `Document`object and a score representing the similarity to the query. This output format facilitates the subsequent processing and presentation of search results. 
***
### FunctionDef do_add_doc(self, docs)
**do_add_doc**: The function of this function is to add a list of documents to the database and return a list of information containing document IDs and metadata. 

**Parameters**:
- `docs`: A list of document objects of type that need to be added to the database`List[Document]`. 
- `**kwargs`: Accepts a variable number of keyword arguments for extended or custom functionality.

**Code Description**:
`do_add_doc`The function first calls `_docs_to_embeddings`a private method to convert the list of document objects into vectorized data, including text content, vectorized results, and metadata. This step is to prepare the document for storage in a vector database for subsequent retrieval and analysis operations. 

Next, the function generates a unique ID for each document (using the`uuid.uuid1()` method) and invokes the method to add the document's ID, vectorization result, metadata, and textual content to the database's collection by iterating through the vectorized data for each document`collection.add`. After each add operation, the function collects the document's ID and metadata into a`doc_infos` list. 

Finally, the function returns `doc_infos`a list containing the ID and metadata information of each document added to the database, which provides convenience for subsequent document management and retrieval. 

**Note**:
- Make sure that the parameters you pass `docs`in are a valid list of document objects, and that each document object should contain the necessary content and metadata. 
- `_docs_to_embeddings`Methods rely on specific document vectorization models, so you `do_add_doc`should make sure that the relevant vectorization model has been set up and initialized correctly before using functions. 
- The generated document ID is a timestamp-based UUID that guarantees the uniqueness of each document.

**Example output**:
The call `do_add_doc(docs=[Document1, Document2])`might return a list like this:
```python
[
    {"id": "文档1的UUID", "metadata": {"title": "文档1标题"}},
    {"id": "文档2的UUID", "metadata": {"title": "文档2标题"}}
]
```
This list contains the unique ID and metadata information of each document added to the database, which is convenient for subsequent document management and retrieval operations.
***
### FunctionDef get_doc_by_ids(self, ids)
**get_doc_by_ids**: The function of this function is to query and return the corresponding list of document objects from the database based on a set of IDs. 

**Parameters**:
- `ids`: `List[str]`Type: indicates the list of document IDs to be queried. 

**Code Description**:
`get_doc_by_ids`A method `ChromaKBService`is a part of the class that is responsible for retrieving documents from a database based on a given list of IDs. This method first calls the method of the collection`get`, passing in the ID list as a parameter to obtain the corresponding document data from the database. The result is a`GetResult` type, and then the method calls a`_get_result_to_documents` function to convert the`GetResult` query result of the type into`Document` a list of objects. 

`_get_result_to_documents`Functions deal in detail with how to `GetResult`extract document content and metadata from the query results of a type and encapsulate them into`Document` objects. This process involves checking the sum fields in the query results`documents` to `metadatas`ensure that each document correctly corresponds to its metadata, and ultimately generating an object list containing all queried documents`Document`. 

In this way, the `get_doc_by_ids`method can provide an efficient and convenient interface for querying and obtaining the document content and its metadata based on the document ID, which in turn supports subsequent document processing or responds to client requests. 

**Note**:
- The incoming list of IDs should be valid to avoid missing the document or generating exceptions.
- This method relies on `_get_result_to_documents`the function to process the query results correctly, so you need to ensure that the`GetResult` data structure of the type matches as expected. 

**Example output**:
```python
[
    Document(page_content="文档内容1", metadata={"作者": "张三"}),
    Document(page_content="文档内容2", metadata={"作者": "李四"})
]
```
This example shows the morphology of the list of objects that a method might return`get_doc_by_ids` when querying a database against a given list of IDs and processing the results`Document`. Each `Document`object contains the contents of the document (`page_content`) and metadata (`metadata`). 
***
### FunctionDef del_doc_by_ids(self, ids)
**del_doc_by_ids**: The function of this function is to delete documents in the database based on the list of IDs provided. 

**Parameters**:
- ids: A list of strings containing the IDs of the documents to be deleted.

**Code Description**:
`del_doc_by_ids`The function accepts a parameter`ids`, which is a list of strings, each representing the ID of a document that needs to be removed from the database. A function calls`self.collection.delete` a method internally, passing `ids`it as an argument to the method in order to delete the corresponding document. After the deletion operation is complete, the function returns`True`, indicating that the document has been successfully deleted. 

**Note**:
- Ensure that each ID in `del_doc_by_ids`the list passed to the function `ids`is valid and exists in the database, otherwise the deletion operation may fail or be incomplete. 
- This function always returns`True`, even though some IDs may not have been actually deleted because they don't exist. As a result, the caller may need additional logic to verify the actual effect of the delete operation. 

**Example output**:
Since this function returns a Boolean value, `del_doc_by_ids(['123', '456'])`the expected return value when called is:
```
True
```
This indicates that the specified document has been successfully deleted.
***
### FunctionDef do_clear_vs(self)
**do_clear_vs**: The function of this function is to empty the vector store. 

****Arguments: This function has no arguments. 

**Code Description**: `do_clear_vs`A function is a method in the ChromaKBService class that empties the vector store. In terms of implementation, it`do_drop_kb` uses methods to empty the vector store. According to`do_drop_kb` the method's documentation, we know that `do_drop_kb`the feature is to delete a collection in ChromaDB. Therefore, emptying `do_clear_vs`a vector store by deleting a collection may be because it is more efficient or business logic to delete a collection directly than to attempt to empty its contents. When called`do_drop_kb`, an attempt is made to delete a collection named it`kb_name`, and if an exception is encountered during the deletion process`ValueError`, and the exception information is not because the collection does not exist, the exception will be re-thrown. This design ensures that the execution of the program is interrupted only if an unexpected error is encountered. 

**Note**: When using `do_clear_vs`functions, you need to make sure that the name of the `self.kb_name`target collection is correctly set. In addition, considering that deleting a collection is an irreversible operation, this function should be used with caution to ensure that its invocation is in the appropriate context and in accordance with the needs of the business logic. Since`do_clear_vs` the implementation of the function depends`do_drop_kb`, you `do_clear_vs`should also be prepared to handle`do_drop_kb` exceptions that may be thrown when using `ValueError`it, especially if the collection may not exist. 
***
### FunctionDef do_delete_doc(self, kb_file)
**do_delete_doc**: This function is used to delete the specified file in the knowledge base. 

**Parameters**:
- `kb_file`: KnowledgeFile object, which represents the knowledge base file to be deleted.
- `**kwargs`: Receive additional keyword parameters that can be used to extend functionality or pass additional information.

**Code Description**:
`do_delete_doc`A function is `ChromaKBService`a method of a class that is responsible for deleting a specified file from the knowledge base. The method takes as a parameter an`KnowledgeFile` object that contains the details of the file to be deleted, including the path to the file, etc. The function performs`self.collection.delete` the deletion operation by calling a method, where the `where`parameter is used to specify the deletion condition, and in this case, the path () of the file is`kb_file.filepath` used as the basis for deletion. 

In the hierarchy of a project,`KnowledgeFile` an object `server/knowledge_base/utils.py`is defined by , which encapsulates the information and actions related to the knowledge base file. `do_delete_doc`By using this object, you can accurately locate and manipulate a specific file in the knowledge base, and realize the file deletion function. 

The implementation of this method relies on`collection` the object's `delete`method, which is an abstraction of database operations that allows records to be deleted by specifying conditions. In this project, `collection`it is likely that you represent an instance of a class that encapsulates database operations to manage data records in the knowledge base. 

**Note**:
- When you call `do_delete_doc`a method, you need to make sure that the object passed in`kb_file` is valid and that its `filepath`properties correctly point to the path of the file you want to delete. 
- The execution of this method depends on `collection.delete`the implementation of the method, so its specific behavior may vary in different database or data storage scenarios. 
- The deletion operation is irreversible, so you should make sure that the files are indeed no longer needed before performing it to avoid data loss.

**Example output**:
Since `do_delete_doc`the primary function of a method is to remove records from the database, its return value depends on `collection.delete`the implementation of the method. Typically, the method might return an object or Boolean value that represents the result of the delete operation. For example, if the deletion is successful,`True` an object containing the deletion success message may be returned; If the deletion fails,`False` an object may be returned that contains an error message. 
***
