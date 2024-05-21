## ClassDef ZillizKBService
**ZillizKBService**: The ZillizKBService class is a service for managing and manipulating a knowledge base in a Zilliz vector database. 

**Properties**:
- `zilliz`: A Zilliz instance that interacts with the Zilliz vector database.

**Code Description**:
The ZillizKBService class inherits from the KBService class and provides a set of methods specifically for managing and manipulating the knowledge base in the Zilliz vector database. These methods include getting collections, getting documents by ID, deleting documents by ID, searching, creating a knowledge base, initializing, deleting a knowledge base, adding documents, deleting documents, and clearing vector spaces. 

- `get_collection` A static method is used to get a collection of specified names.
- `get_doc_by_ids` The method queries and returns a list of documents based on the list of IDs provided.
- `del_doc_by_ids` The method deletes the document based on the list of IDs provided.
- `search` Static methods are used to search for documents that are similar to a given content in a specified collection.
- `do_create_kb` The method is used to create a knowledge base and is currently an empty implementation.
- `vs_type` The method returns a supported vector storage type, i.e., Zilliz.
- `_load_zilliz` method is used to load a Zilliz instance.
- `do_init` Methods are used to initialize the service, including loading a Zilliz instance.
- `do_drop_kb` Methods are used to delete the knowledge base.
- `do_search` Methods are used to search the knowledge base.
- `do_add_doc` Methods are used to add documents to the knowledge base.
- `do_delete_doc` Methods are used to delete the specified document from the knowledge base.
- `do_clear_vs` method is used to clear the vector space.

**Note**:
- Before using ZillizKBService, you need to make sure that the Zilliz vector database is properly configured and available.
- Since ZillizKBService inherits from KBService, the implementation of some methods may depend on the abstract methods defined in the KBService class.
- When calling `do_add_doc` `do_delete_doc` methods such as and , you need to pay attention to the format and type of arguments you pass in. 

**Example output**:
```python
# 假设已经有一个 ZillizKBService 实例，名为 zilliz_service
# 搜索内容为 "example content" 的文档，限制返回结果为前3个
search_results = zilliz_service.search("example_collection", "example content", limit=3)
# 输出可能为：
[
    {"content": "文档1内容", "score": 0.95},
    {"content": "文档2内容", "score": 0.90},
    {"content": "文档3内容", "score": 0.85}
]
```
This output example shows the `search` possible outcomes of a content search using the method, including the content and similarity score for each matching document. 
### FunctionDef get_collection(zilliz_name)
**get_collection**: The function of this function is to get a collection of specified names. 

**Parameters**:
- **zilliz_name**: The name of the collection. 

**Code Description**:
`get_collection` A function is `ZillizKBService`a method in a class, and its main function is to`zilliz_name` use the class `pymilvus`in the library `Collection`to get the corresponding collection object by passing in the collection name. This method is straightforward and involves only importing`pymilvus` `Collection`a class and returning a collection object. 

In a project, `get_collection`methods are called by`search` methods. In the`search` method, you first `get_collection`get a collection object with a specified name, and then use this collection object to perform a search operation. This indicates that `get_collection`the method is fundamental to the implementation of the search function, which ensures that the search operation can be performed on the correct collection. 

**Note**:
- Make sure that the specified collection name `zilliz_name`already exists in the Milvus database before calling this function, otherwise it will cause the collection to fail. 
- Using this function requires the library to be installed and properly configured`pymilvus`. 

**Example output**:
The call `get_collection("example_collection")`may return an `pymilvus`object from a library `Collection`that represents a collection called a "example_collection". 
***
### FunctionDef get_doc_by_ids(self, ids)
**get_doc_by_ids**: The function of this function is to retrieve documents from Zilliz's collection based on the list of IDs provided. 

**Parameters**:
- `ids`: A list of strings containing the ID of the document to be retrieved.

**Code Description**:
`get_doc_by_ids`The function takes a list of IDs as a parameter and returns a list of documents. This function first checks `self.zilliz.col`for the existence of a reference to the Zilliz collection. If this collection exists, the function will continue to execute the query. 

The query is implemented by calling`self.zilliz.col.query` a method whose `expr`parameters are set to`'pk in {ids}'`, where `{ids}`is the list of IDs passed in. This means that the function will query all the records of the primary key (pk) in the given ID list. `output_fields=["*"]`The parameter instructs the query to return data for all fields. 

For each piece of data in the query results, the function extracts fields from the data`text` and uses the remaining fields as metadata. It then uses this information to create an`Document` object that `page_content`is set to the extracted text and `metadata`set to the remaining data field. These `Document`objects are collected into a list and finally returned to this list. 

**Note**:
- Make sure that the IDs in the incoming ID list are valid IDs that exist in the Zilliz collection, otherwise the query will return no results.
- This function depends on `self.zilliz.col`the existence of the function, which means that the corresponding Zilliz collection reference must be properly initialized and set before this function can be called. 

**Example output**:
Let's say there are two documents with IDs "123" and "456", and these documents exist in the Zilliz collection. The call`get_doc_by_ids(['123', '456'])` might return a list like this:

```python
[
    Document(page_content="这是文档123的内容", metadata={'id': '123', 'title': '文档123标题', 'date': '2023-01-01'}),
    Document(page_content="这是文档456的内容", metadata={'id': '456', 'title': '文档456标题', 'date': '2023-01-02'})
]
```

This list contains two `Document`objects, each containing the content and metadata of the document retrieved from the Zilliz collection. 
***
### FunctionDef del_doc_by_ids(self, ids)
**del_doc_by_ids**: The function of this function is to delete the corresponding document based on the list of IDs provided. 

**Parameters**:
- ids: A list of strings containing the IDs of the documents that need to be deleted.

**Code Description**:
`del_doc_by_ids`A function is `ZillizKBService`a method of the class that is used to delete a document with a specified ID from Zilliz's knowledge base service. This function accepts a parameter`ids`, which is a list of strings, each representing the ID of a document that needs to be deleted. Inside the function, the delete operation is performed by calling`self.zilliz.col.delete` a method, where `expr=f'pk in {ids}'`is an expression that specifies the ID condition of the document to be deleted. Here`pk` represents the primary key of the document, which `in {ids}`means that the primary key in the provided ID list of the document will be deleted. 

**Note**:
- Ensure that each ID in the incoming ID list is valid and corresponds to the document that actually exists in the knowledge base. If the list contains invalid or non-existent IDs, they will be ignored and will not affect the deletion of other valid IDs.
- Once the deletion operation is performed, the deleted document cannot be restored, so please check carefully before performing the deletion operation.
- This function returns a Boolean value that indicates whether the delete operation was successfully executed. However, there is no explicit return value in the specific code implementation, which may need to be adjusted or supplemented accordingly based on the actual business logic.
***
### FunctionDef search(zilliz_name, content, limit)
**search**: The function of this function is to perform a content-based search operation in a specified collection. 

**Parameters**:
- **zilliz_name**: The name of the specified collection. 
- **content**: The content of the search. 
- **limit**: The maximum number of results returned, the default value is 3. 

**Code Description**:
`search` A function is `ZillizKBService`a method in a class that is used to perform a content-based search operation in a specified collection. First, the function defines the search parameters`search_params`, which include the type of measure ("IP") and other search-related parameters. Next, the `get_collection`collection object with the specified name is obtained by calling the method. Finally, the search operation is performed using the method of the collection object`search`, which is based on `content`the parameters, and the search scope is limited to the "embeddings" field, and the search parameters`search_params` and the upper limit of the number of results`limit` are specified. In addition, `output_fields`you specify the fields that need to be included in the search results by parameters, in this case["content"]. 

From a functional point of view, methods`get_collection` provide the `search`collection objects that methods need to perform the search, ensuring that the search operation can take place on the correct collection. This design embodies the principle of modularity and functional separation, which facilitates the maintenance and expansion of the code. 

**Note**:
- Before using the `search`function, make sure that the `zilliz_name`specified collection already exists and that the data in the collection has been indexed as needed. 
- `limit`Parameters should be adjusted to meet your needs to balance the comprehensiveness of your search results with the performance overhead.
- Make sure that the `pymilvus`library is properly installed and configured, as `search`the implementation of the function depends on this library. 

**Example output**:
The call `search("example_collection", "some search content")`might return search results in the following format:
```python
[
    {"content": "匹配的内容1"},
    {"content": "匹配的内容2"},
    {"content": "匹配的内容3"}
]
```
This example shows what it would be like to get a search result when the search is limited to a maximum of 3 results. Each result contains the specified output field, "content", which contains data from the collection that matches the search.
***
### FunctionDef do_create_kb(self)
**do_create_kb**: The function of this function is to create a knowledge base. 

****Arguments: This function has no arguments. 

**Code Description**: `do_create_kb` A function is `ZillizKBService` a method of the class that is used to create a knowledge base. In the current code implementation, there is no concrete execution code in the body of this function, and it contains only a  statement `pass` . This means that the function exists as a framework or placeholder, waiting for subsequent implementations. In practice, developers need to populate this function to implement the logic of creating a knowledge base according to specific requirements, such as initializing the database connection, setting the structure of the knowledge base, and importing data. 

**Note**: While the current `do_create_kb` function does not implement a specific function, developers may add specific implementation code in a future release. Therefore, when using this function, you need to pay attention to its latest implementation status and documentation to ensure proper use. At the same time, considering that the purpose of this function is to create a knowledge base, developers should ensure that they have sufficient permissions and correct configuration information when implementing it to avoid potential permission issues or misconfigurations. 
***
### FunctionDef vs_type(self)
**vs_type**: The function of the vs_type function is to return the vector storage type that is currently supported by the knowledge base service. 

****Arguments: This function has no arguments. 

**Code Description**: The vs_type function is a method of the ZillizKBService class that identifies the types of vector stores supported by the knowledge base service instance. In this concrete implementation, the vs_type method makes it clear by returning SupportedVSType.ZILLIZ that the current knowledge base service uses ZILLIZ as its vector storage solution. SupportedVSType is an enumeration class that defines all vector storage types supported by the project, including but not limited to FAISS, MILVUS, ZILLIZ, etc. ZILLIZ was chosen here, meaning that ZillizKBService is specifically designed to interact with the ZILLIZ vector storage service. This design makes it easy to dynamically select and instantiate specific knowledge base service implementations as needed in the KBServiceFactory, increasing the flexibility and scalability of the project. 

**Note**: 
- When using the ZillizKBService class, developers should understand that the vector storage type behind it is ZILLIZ, which is critical to understanding how to configure and use the service.
- If your project needs to support other types of vector storage services, you should add the appropriate types to the SupportedVSType enumeration class and implement the corresponding logic in the knowledge base service factory to support the new service types.

**Example output**: The function call will return a string value: "zilliz". 
***
### FunctionDef _load_zilliz(self)
**_load_zilliz**: The function of this function is to load the Zilliz service. 

**Parameters**: This function has no explicit arguments, it accesses member variables through a class instance. 

**Code Description**:  The `_load_zilliz`function first obtains the parameters named from the configuration`zilliz`, which are used to configure the connection to the Zilliz service. It then creates an `Zilliz`instance that handles the storage and search of the embedding vectors. When creating an`Zilliz` instance, it uses a class to pass `EmbeddingsFunAdapter`the properties of the current object`embed_model` as an embedding function`Zilliz`. `EmbeddingsFunAdapter`is an adapter class that converts text to embedding vectors, supporting both synchronous and asynchronous methods. In addition, the`Zilliz` instance receives the name of the knowledge base (`kb_name`) and the connection parameter ().`zilliz_args` This means that whenever a search operation needs to be initialized or performed, the `Zilliz`Zilliz service is interacted with through an instance in order to handle the storage of embedding vectors and similarity searches. 

**Note**: 
- Before calling `_load_zilliz`a function, you need to make sure that `kbs_config`the parameters are configured correctly`zilliz`, including the connection information of the Zilliz service. 
- `EmbeddingsFunAdapter`The use of the class relies on a valid embedding model name(`embed_model`) that points to a pre-trained model for text embedding transformations. 
- `_load_zilliz`Functions are typically called during the initialization(`do_init`) and search() processes of the knowledge base service `do_search`to ensure that the connection and configuration of the Zilliz service are ready before proceeding. 

In this way, functions `_load_zilliz`provide a core function for the knowledge base service, i.e., configure and initialize the connection to the Zilliz service, which is essential for subsequent text embedding storage and similarity search operations. 
***
### FunctionDef do_init(self)
**do_init**: The function of this function is to initialize the Zilliz knowledge base service. 

****Arguments: This function has no explicit arguments. 

**Code Description**: `do_init`A function is `ZillizKBService`a method of a class that is used to initialize the Zilliz knowledge base service. It`_load_zilliz` loads and configures the Zilliz service by calling methods. `_load_zilliz`The method is responsible for creating a Zilliz instance that handles the storage and search of embedding vectors. This process involves getting the connection parameters of the Zilliz service from the configuration and`EmbeddingsFunAdapter` using the class to pass the properties of the current object `embed_model`as an embedding function to the Zilliz instance. This ensures that the Zeroliz service is able to convert text into embedding vectors based on pre-trained models, and perform storage and similarity search operations. 

**Note**:
- Before calling `do_init`a method, you should make sure that the `kbs_config`connection information for the Zilliz service has been configured correctly in . 
- `do_init`Methods are usually called when a knowledge base service needs to be reinitialized, for example, `do_clear_vs`in a method, if a knowledge base collection is detected to exist, the existing collection is deleted first, and then the Zilliz service is reinitialized by`do_init` calling. 
- The successful execution of this method is necessary for subsequent knowledge base operations such as text embedding storage and similarity search, as it ensures that the connection and configuration of the Zilliz service are ready.

Methods`do_init` `ZillizKBService`enable classes to ensure that the Zilliz Knowledge Base service is properly initialized and configured, providing the basis for subsequent operations. 
***
### FunctionDef do_drop_kb(self)
**do_drop_kb**: The function of this function is to release and delete the current collection of knowledge bases. 

****Arguments: This function does not accept any arguments. 

**Code Description**: `do_drop_kb` A function is `ZillizKBService`a method of a class that handles the release and deletion of a collection of knowledge bases. When`ZillizKBService` a property in the instance`zilliz.col` exists, this method first calls `release`the method to release the collection, and then calls `drop`the method to delete the collection. This process ensures that the collection of knowledge bases is cleaned up correctly and that resources are leaked or unnecessarily stored. 

In a project, `do_drop_kb`methods are called by`do_clear_vs` methods. `do_clear_vs`The purpose of a method is to clean up the view state, and during the cleanup process, it is first called`do_drop_kb` to release and delete the knowledge base collection, and then `do_init`the state is reinitialized by calling the method. This shows that `do_drop_kb`it plays an important role in the knowledge base management process, ensuring that collections of knowledge bases are properly processed when they are no longer needed. 

**Note**: When using `do_drop_kb`a method, you need to ensure that the `zilliz.col`property is initialized correctly, and that the associated collection resources are freed and deleted after this method is called. Therefore, you should make sure that you no longer need to do anything with the collection before you call this method. 
***
### FunctionDef do_search(self, query, top_k, score_threshold)
**do_search**: The function of this function is to perform a search operation for a text query and return a list of documents that meet the criteria. 

**Parameters**:
- `query`: The query text that needs to be searched, and the data type is a string.
- `top_k`: The maximum number of documents to be returned, with data type as an integer.
- `score_threshold`: Score threshold, which is used to filter documents with similarity above this threshold, and the data type is floating-point.

**Code Description**:
`do_search`The function first calls `_load_zilliz`the method to load the Zilliz service, which ensures that the connection to the Zilliz service has been established and that the relevant configuration is in place. Next, the function creates an`EmbeddingsFunAdapter` instance that uses the properties in the class`embed_model` as the embedding model. The `EmbeddingsFunAdapter`method converts the entered query text`embed_query` `query`into an embedding vector. 

After the embedding vector is obtained, the function calls`zilliz` the method of the instance `similarity_search_with_score_by_vector`to perform a similarity search operation. This method receives embedding vectors,`top_k` parameters, and returns a list of documents and their similarity scores. 

Finally, the function calls`score_threshold_process` the method to `score_threshold`filter out the documents with similarity scores higher than the threshold according to the parameters, and limits the number of documents returned to not exceed the threshold`top_k`. This step ensures that the list of documents returned meets both the similarity and the maximum number of documents. 

**Note**:
- Before you call `do_search`a function, you need to make sure that `embed_model`it is properly configured and points to a valid pre-trained embedding model. 
- `score_threshold`Parameters allow the caller to filter documents with a higher degree of similarity as needed, and if set to a lower value, more documents may be returned; If you set it to a higher value, fewer documents may be returned.
- `top_k`The upper limit of the number of documents returned by the parameter control should be reasonably set according to actual needs.

**Example output**:
Suppose the input query text is "Artificial Intelligence",`top_k` which is 3, `score_threshold`which is 0.5, and the similarity search returns a list of documents and their similarity[("doc1", 0.6), ("doc2", 0.4), ("doc3", 0.7), ("doc4", 0.5)] scores. `score_threshold_process`After processing, the final list of documents returned may be [("doc1", 0.6), ("doc3", 0.7), ("doc4", 0.5)]0.5 or greater, indicating that the similarity score of the three documents is greater than or equal to 0.5, and the number does not exceed 3. 
***
### FunctionDef do_add_doc(self, docs)
**do_add_doc**: The function of this function is to add documents to the knowledge base and return a list with document IDs and metadata. 

**Parameters**:
- `docs`: A list of documents that need to be added to the knowledge base, each document is a Document object.
- `**kwargs`: Receive additional keyword parameters for extended or custom functionality.

**Code Description**:
This function first iterates through the incoming list of documents`docs`. For each document, it traverses the document's metadata`metadata`, converting the values of all metadata into a string format. It then checks for missing fields and, if so, sets default empty string values for those fields. In addition, the function removes specific fields from the metadata, which are typically fields used for text and vector representations, specified by`self.zilliz._text_field` and`self.zilliz._vector_field` . 

After processing all the document's metadata, the function calls `self.zilliz.add_documents(docs)`the method to add the document to the knowledge base and receives a list of document IDs returned. Finally, the function constructs a list of document IDs and updated metadata and returns it. 

**Note**:
- Make sure that each document in the incoming document list has a`metadata` property and that its value is of dictionary type. 
- This function does not handle the addition of text and vector fields, ensuring that they are set correctly before calling this function.
- The incoming document object should be ready to be added to the knowledge base, including all necessary metadata and content.

**Example output**:
```python
[
    {"id": "123", "metadata": {"title": "文档标题1", "author": "作者1"}},
    {"id": "456", "metadata": {"title": "文档标题2", "author": "作者2"}}
]
```
This example shows what the function can return a value for, including the ID of each document and updated metadata.
***
### FunctionDef do_delete_doc(self, kb_file)
**do_delete_doc**: This function is used to delete documents for the specified file from the knowledge base. 

**Parameters**:
- `kb_file`: KnowledgeFile object, which represents the knowledge base file that needs to be deleted.
- `**kwargs`: Receive a variable number of keyword parameters for extending or customizing functionality.

**Code Description**:
`do_delete_doc`A function is `ZillizKBService`a method of a class that is responsible for deleting documents in the knowledge base that are related to a specified file. First, the function checks for`zilliz` the existence of the object's`col` properties, which `col`represent the database collection for the current operation. If the collection exists, proceed with the deletion operation. 

The function `kb_file`receives an object with parameters `KnowledgeFile`that contains the details of the knowledge base file, such as the file path, and so on. To ensure that the file path is used correctly in the database query, the function first replaces the backslash() in the file path`\` with a double backslash(`\\`) to accommodate the database query syntax. 

Next, the function uses `self.zilliz.col.query`the method to query all documents that match the specified file path, and extracts the list of primary keys () of the documents from the query results`pk`. This step is to find out the unique identifier of the document that needs to be deleted. 

Finally, the function `self.zilliz.col.delete`uses a method to construct a delete expression using the extracted list of primary keys to remove these documents from the database collection. The expression for the delete operation is in the form`'pk in {delete_list}'` of a `{delete_list}`list of primary keys for the document to be deleted. 

**Note**:
- When using `do_delete_doc`functions, you need to make sure that the object you pass in`kb_file` is valid and that the file is registered with the knowledge base. 
- The delete operation relies on`zilliz` the object's `col`properties, which must point to a valid collection of databases. 
- The file path is handled to accommodate the database query syntax, ensuring that query and delete operations are executed correctly.
- The deletion operation is performed based on the primary key (`pk`) of the document, so you need to ensure that the document in the database has a unique primary key identifier. 

This function is `KnowledgeFile`closely related to an object because it uses the `KnowledgeFile`file path information provided by the object to locate and delete documents in the knowledge base. In this way, `do_delete_doc`functions support efficient management of knowledge base content, allowing users to quickly delete related documents based on file information, thereby maintaining the accuracy and cleanliness of the knowledge base. 
***
### FunctionDef do_clear_vs(self)
**do_clear_vs**: The function of this function is to clean up the view state of the Zilliz knowledge base service. 

****Arguments: This function does not accept any arguments. 

**Code Description**: `do_clear_vs`A function is `ZillizKBService`a method in a class that cleans up the view state of the Zilliz Knowledge Base service in a specific situation. The method first checks for`ZillizKBService` the existence of an `zilliz.col`instance property, which represents the current set of knowledge bases. If this property exists, it means that there is currently an active knowledge base collection, and the`do_clear_vs` method performs two steps: first, call `do_drop_kb`the method to release and delete the current knowledge base collection; Second, call`do_init` the method to reinitialize the Zilliz knowledge base service. 

`do_drop_kb`The method is responsible for releasing and deleting the knowledge base collection, ensuring that the current collection resources are properly cleaned up before reinitialization. `do_init`Methods are used to reload and configure the Zilliz service, including creating a new knowledge base collection and configuring the processing of embedding vectors. This sequence of actions ensures that the Zilliz knowledge base service can be cleaned up and restarted with the correct configuration. 

**Note**:
- Before calling `do_clear_vs`a method, you should make sure that the `ZillizKBService`instance has been initialized correctly, especially the `zilliz.col`property, which represents the current collection of knowledge bases. 
- `do_clear_vs`Methods are typically invoked when the knowledge base service state needs to be reset, such as during testing or when the knowledge base data structure needs to be updated.
- Because this method deletes the current knowledge base collection, you should make sure that you no longer need the data in the collection, or that you have made a backup of the data before calling it.
- The execution of this method will affect the state of the Zilliz knowledge base service, so it is recommended to do it during off-peak hours to avoid affecting the normal service.
***
