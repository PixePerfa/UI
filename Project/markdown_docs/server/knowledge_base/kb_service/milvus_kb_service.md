## ClassDef MilvusKBService
**MilvusKBService**: The MilvusKBService class is a service for managing and manipulating a knowledge base in a Milvus vector database. 

**Properties**:
- `milvus`: A Milvus instance that performs operations related to the Milvus database.

**Code Description**:
The MilvusKBService class inherits from the KBService class and provides a set of methods for managing and manipulating the knowledge base in the Milvus vector database. This includes adding, deleting, searching, and creating, initializing, and deleting knowledge bases. 

- `get_collection` The static method is used to get a Collection in Milvus.
- `get_doc_by_ids` The method retrieves a document based on a list of document IDs and returns a list of Document objects that contain the document's content and metadata.
- `del_doc_by_ids` Method: Delete a document from the knowledge base based on the list of document IDs.
- `search` The static method implements content-based search functionality, returning a list of documents that are most relevant to the searched content.
- `do_create_kb` The method used to create a knowledge base is an empty implementation in the MilvusKBService class, and the specific logic needs to be defined in the subclass.
- `vs_type` The method returns the type of vector store used by the knowledge base, and in the case of the MilvusKBService class, it always returns `SupportedVSType.MILVUS`. 
- `_load_milvus` Methods are responsible for loading Milvus instances, including setting embedding functions, collection names, connection parameters, and so on.
- `do_init` method to initialize the Milvus instance.
- `do_drop_kb` Methods to delete a knowledge base, including releasing and deleting collections.
- `do_search` method implements query-based search that returns a list of documents that are most relevant to the query.
- `do_add_doc` Methods add documentation to the knowledge base.
- `do_delete_doc` The method deletes a document from the knowledge base based on the KnowledgeFile object.
- `do_clear_vs` The method clears all documents in the knowledge base.

**Note**:
- Before using the MilvusKBService class, you need to make sure that the Milvus service is up and ready to connect.
- When calling `do_add_doc`  and `do_delete_doc` method, you need to pass in a document format that meets Milvus's requirements. 
- `get_collection` The method needs to ensure that the collection name passed in already exists in Milvus.

**Example output**:
```python
# 假设执行搜索操作后的返回示例
[
    {"id": "123", "content": "文档内容示例", "score": 0.95},
    {"id": "456", "content": "另一个文档内容示例", "score": 0.90}
]
```
This means that when the search operation is performed, two documents and their relevance scores are returned.
### FunctionDef get_collection(milvus_name)
**get_collection**: The function of this function is to get the Milvus collection with the specified name. 

**Parameters**:
- **milvus_name**: The name of the Milvus collection that needs to be fetched. 

**Code Description**:
`get_collection`A function is a `MilvusKBService`method in a class that is used to get a collection of specific names in the Milvus database. It`milvus_name` takes the name of the collection by the argument and uses`pymilvus` the class in the library `Collection`to get and return an instance of the collection. The main role of this function in the project is to provide collection instances for other methods that need to manipulate Milvus collections, for example,`search` in a method, it `get_collection`calls to get a collection instance and then performs a search operation on that collection. 

In a `search`method, `get_collection`it is used to get an instance of a collection and then use that instance to perform a search operation, which includes specifying search parameters and return fields. This shows the`get_collection` importance of being a basic feature in the project as a basis for getting an instance of a Milvus collection. 

**Note**:
- Make sure that the parameters passed in `milvus_name`are correct and that the corresponding Milvus collection already exists, otherwise`Collection` the class may throw an exception. 
- Using `get_collection`functions requires the library to be installed and properly configured`pymilvus`. 

**Example output**:
The call `get_collection("example_collection")`may return an `Collection`instance of a class that represents `example_collection`a collection called Milvus. The specific return value depends on the state and content of the collection in the Milvus database. 
***
### FunctionDef get_doc_by_ids(self, ids)
**get_doc_by_ids**: The function of this function is to retrieve documents from the Milvus database based on the list of IDs provided. 

**Parameters**:
- `ids`: A list of strings containing the ID of the document to be retrieved.

**Code Description**:
`get_doc_by_ids` The function takes a list of IDs as a parameter and returns a list of documents containing the corresponding IDs. First, the function checks for the existence of a collection of Milvus databases. If the collection exists, the function proceeds with the following steps:

1. Convert each ID in the entered ID list to an integer, as these IDs may be stored as integers in the Milvus database.
2. Using the transformed list of IDs, a query expression is constructed for retrieving documents with these IDs from collections in the Milvus database.
3. Execute a query to retrieve a list of documents that contain all the specified fields. This`output_fields=["*"]` represents all the fields in which the document is retrieved. 
4. Traverse the query results, extract the text content from each result, and store the rest as metadata. Each document is encapsulated as an`Document` object that contains the page content (`page_content`) and metadata (`metadata`). 
5. Collect all `Document`objects into a list and return to that list. 

**Note**:
- Make sure that the IDs in the incoming ID list match the ID type stored in the Milvus database. If the ID in the database is of integer type, make sure to convert the ID type.
- This function depends on the connection instance () of the Milvus database`self.milvus` and its collection (`self.milvus.col`). Make sure that these connections are properly configured before calling this function. 

**Example output**:
Suppose there are two documents with IDs of "1" and "2", and the call`get_doc_by_ids(["1", "2"])` may return the following list:

```python
[
    Document(page_content="文档1的内容", metadata={"id": 1, "title": "文档1标题", ...}),
    Document(page_content="文档2的内容", metadata={"id": 2, "title": "文档2标题", ...})
]
```

This example shows a list of objects returned by the function`Document`, each containing the page content and metadata of the corresponding document. 
***
### FunctionDef del_doc_by_ids(self, ids)
**del_doc_by_ids**: The function of this function is to delete documents in the Milvus database based on the list of IDs provided. 

**Parameters**:
- `ids`: A list of IDs of the documents to be deleted, of type`List[str]`. 

**Code Description**:
`del_doc_by_ids`The function takes as an argument a list of `ids`strings containing the IDs of the documents that need to be deleted from the Milvus database. function, by calling`self.milvus.col.delete` a method to perform a delete operation. This method uses an expression`expr=f'pk in {ids}'` that `pk`represents the primary key field in the Milvus database, which means that all documents with primary keys in the`ids` list are selected for deletion. 

**Note**:
- Make sure that `ids`the IDs in the incoming list are present in the Milvus database, otherwise the deletion will not affect any documents. 
- Deletion is irreversible, and once executed, the corresponding document will be permanently removed from the database, so use this feature with caution.
- Before deleting data, we recommend that you back up your data to prevent accidental deletion of important data.
- This function returns a Boolean value indicating whether the deletion operation was successfully executed, but it is important to note that even if the deletion operation is successful, it does not mean that all the specified IDs have been successfully deleted, as some IDs may not exist in the database in the first place.
***
### FunctionDef search(milvus_name, content, limit)
**search**: The function of this function is to perform a vector search operation in the Milvus collection. 

**Parameters**:
- **milvus_name**: String type, specifying the name of the Milvus collection to be searched. 
- **content**: Search for content, usually a vector or array of vectors. 
- **limit**: Integer, specifies the maximum number of results to be returned, defaults to 3. 

**Code Description**:
`search`A function is a `MilvusKBService`method in a class that is used to perform a vector search operation in a specified collection of Milvus. It first defines a search parameter `search_params`that includes the metric type ("L2") and other search-related parameters (e.g., "nprobe": 10). These parameters are used to control behavior during the search process, for example, "L2" specifies the use of L2 distance (Euclidean distance) as a measure of similarity. 

Next, the function`get_collection` gets `milvus_name`an instance of the Milvus collection with the specified name () by calling the method. `get_collection`Methods `MilvusKBService`are an important method in the class that is responsible for connecting to the Milvus database and getting an instance of the collection for subsequent operations, such as the search operation in this function. 

Once a collection instance is obtained, the function performs a search operation using the method of that instance`search`. The parameters of a search operation include the search content (`content`), the search field ("embeddings"), the search parameter (),`search_params` the limit on the number of results (`limit`), and the output field (["content"]). This allows the function to search based on a given vector content in a specified set and return a few results that are most similar to the searched content. 

**Note**:
- Make sure that the `milvus_name`parameters are correct and that the corresponding Milvus collection already exists, otherwise the collection instance may not be obtained, resulting in a failed search. 
- `search_params`The "metric_type" and "params" in the search parameters should be adjusted according to the actual search needs. 
- `limit`The parameter controls the number of results returned, adjusting this value according to actual needs.

**Example output**:
The call `search("example_collection", some_vector, limit=2)`may return a result in the following format:
```python
[
    {"content": "文档1的内容", "distance": 0.1},
    {"content": "文档2的内容", "distance": 0.2}
]
```
This example shows the two most similar results returned by a search operation, each of which includes a match and distance from the searched content (a measure of similarity).
***
### FunctionDef do_create_kb(self)
**do_create_kb function function**: This function is used to create a knowledge base. 

****Arguments: This function has no arguments. 

**Code Description**: `do_create_kb`A function is `MilvusKBService`a method in a class that currently has an empty internal implementation (using `pass`a statement). This means that nothing is done when the function is called. In practice, this function may be designed to be responsible for creating a new knowledge base in the Milvus vector database, including but not limited to initializing the structure of the knowledge base, configuring the storage parameters of the knowledge base, etc. Since the implementation of this function in the current code is empty, developers need to complete the corresponding function implementation according to actual requirements. 

**Note**: 
- Since `do_create_kb`the function doesn't currently implement any functionality, calling it directly won't have any impact on the system. Developers need to add specific implementation logic when using it. 
- When `do_create_kb`adding implementation logic to your functions, you should make sure to understand the relevant API and knowledge base requirements of the Milvus vector database to ensure that the knowledge base is created correctly and efficiently. 
- Considering possible future changes in requirements and feature extensions, it is advisable to write clear, maintainable code and adequately test specific logic implementations.
***
### FunctionDef vs_type(self)
**vs_type**: The function of the vs_type function is to return the vector storage type that is currently supported by the knowledge base service. 

**Parameters**: This function does not accept any parameters. 

**Code Description**: The vs_type function is a method of the MilvusKBService class that identifies the types of vector stores supported by the service instance. In this concrete implementation, the vs_type method makes it clear by returning SupportedVSType.MILVUS that the current knowledge base service uses MILVUS as its vector storage solution. SupportedVSType is an enumeration class that defines a set of supported vector storage types, including but not limited to FAISS, MILVUS, ZILLIZ, etc. By returning SupportedVSType.MILVUS, the vs_type method provides the knowledge base service factory (KBServiceFactory) with the necessary information to be able to properly instantiate and manage MilvusKBService objects when needed. This design allows the system to flexibly support multiple vector storage services while maintaining the modularity and extensibility of the code. 

**Note**:
- When using the vs_type method, you don't need to pass any arguments, it will return a string representing the supported vector storage type.
- The returned vector store type should be consistent with the type defined in the SupportedVSType enumeration class to ensure system consistency and reliability.
- When you need to extend your knowledge base service to support more vector store types, you should first add a new type in the SupportedVSType enumeration class, and then implement a vs_type method in the corresponding knowledge base service class to return the new type.

**Example output**: 
```python
'milvus'
```
In this example, the vs_type method returns a string 'milvus', indicating that the current knowledge base service instance uses MILVUS as its vector storage solution.
***
### FunctionDef _load_milvus(self)
**_load_milvus**: The function of this function is to initialize the connection to the Milvus service and configure the relevant parameters. 

**Arguments**: This function doesn't have explicit arguments, but it relies on class properties to operate. 

**Code Description**: `_load_milvus`The function is responsible for creating a Milvus instance and connecting to the Milvus service through that instance. It uses `EmbeddingsFunAdapter`classes to fit the embedding model, which will be used for embedding representation transformations of text. In addition, it configures the name, connection parameters, index parameters, and search parameters of the Milvus collection. These parameters are taken from`kbs_config` the configuration object, which includes:
- `embedding_function`: Uses `EmbeddingsFunAdapter`a class that generates an embedding representation of the text based on the embedding model (`embed_model`) provided. 
- `collection_name`: Specifies the name of the collection in Milvus, which is used here`self.kb_name` as the collection name. 
- `connection_args`: Contains the parameters required to connect to the Milvus service, which are obtained from it`kbs_config.get("milvus")`. 
- `index_params`And`search_params`: Used to configure the creation and search parameters of the Milvus index, respectively, which are obtained by`kbs_config.get("milvus_kwargs")` fetching. 

This function is a `MilvusKBService`private method of the class, and is called mainly before the class's initialization process (`do_init`) and the search operation () is performed `do_search`to ensure that the connection to the Milvus service has been established and the corresponding parameters are configured. 

**Note**:
- `_load_milvus`Before calling, make sure that `kbs_config`the configuration object contains the correct Milvus connection parameters, index parameters, and search parameters. 
- `EmbeddingsFunAdapter`The class is a key component that is responsible for converting the text into embedding vectors that will then be used for similarity search in Milvus. Therefore, make sure that`embed_model` the properties are set correctly and that the embedding model you are referencing is valid. 
- `_load_milvus`Functions should not be called directly from outside the class, but indirectly through the class's public methods such as`do_init` and`do_search`. 
***
### FunctionDef do_init(self)
**do_init**: The function of this function is to initialize the Milvus knowledge base service. 

****Arguments: This function has no arguments. 

**Code Description**: `do_init`A function is a `MilvusKBService`public method of a class, and its primary responsibility is to call `_load_milvus`a private method to complete the initialization of the Milvus service. In the `_load_milvus`method, a Milvus instance is created and connected to the Milvus service through that instance, and the relevant parameters are configured, such as the embedding model, collection name, connection parameters, index parameters, and search parameters. The configuration of these parameters is based on the`kbs_config` configuration object. Therefore, the`do_init` method indirectly `_load_milvus`completes the connection and parameter configuration of the Milvus service through the call, and prepares it for subsequent knowledge base operations (such as search). 

**Note**:
- `do_init`Methods are usually `MilvusKBService`called as soon as the class is instantiated to ensure that the connection and configuration of the Milvus service completes correctly. 
- Before calling `do_init`a method, you should make sure that `kbs_config`the configuration object is set up correctly, including the connection information and operation parameters of the Milvus service. 
- In addition to being called at class initialization, `do_init`methods can also be called when a Milvus service connection needs to be reinitialized, e.g`do_clear_vs`. in a method that will be called to reinitialize a service if an existing Milvus collection is`do_init` cleared. 
- Because `do_init`methods depend on `_load_milvus`private methods, you should be aware of the relationships and dependencies between the two methods when modifying or maintaining code. 
***
### FunctionDef do_drop_kb(self)
**do_drop_kb**: The function of this function is to release and delete the collection in the current Milvus database. 

****Arguments: This function has no arguments. 

**Code Description**: `do_drop_kb`A function is `MilvusKBService`a method of a class that handles deletion operations related to collections in the Milvus database. When this function is called, it is first checked to see`self.milvus.col` if there is a collection of Milvus for the current operation. If present, the method performs two steps: first, the collection is released using`release()` the method, which is to ensure that all resources are properly freed before the collection is deleted; Subsequently, the method is called`drop()` to delete the collection. This process ensures that collections are safely and completely removed from the Milvus database. 

In a project, `do_drop_kb`a function is `do_clear_vs`called by a method. `do_clear_vs`The purpose of the method is to clean up the view state, which is called to`do_drop_kb` remove the relevant Milvus collection, and then `do_init`to reinitialize the state by calling. This shows that `do_drop_kb`it plays an important role in the project, and it is an integral part of the process of handling data cleansing and state reset. 

**Note**: When using `do_drop_kb`the function, you need to make sure that the connection to the Milvus database is normal, and calling this function will permanently delete the collection and all its data, which is an irreversible operation. Therefore, before calling this function, you should carefully consider whether you really need to delete the collection to avoid accidental loss of important data. 
***
### FunctionDef do_search(self, query, top_k, score_threshold)
**do_search**: The function of this function is to execute a text query and return the top k documents that are most similar to the query and their similarity scores. 

**Parameters**:
- `query`: The text to be queried, and the data type is a string.
- `top_k`: The maximum number of documents to be returned, with data type as an integer.
- `score_threshold`: Score threshold, which is used to filter documents with similarity above this threshold, and the data type is floating-point.

**Code Description**:
`do_search`The function first calls `_load_milvus`a method to initialize the connection to the Milvus service and configure the relevant parameters to ensure that the Milvus service can be accessed correctly. Next,`EmbeddingsFunAdapter` an instance of the class is `embed_func`used to process the input query text `query`and convert it into an embedding vector. This step is achieved by calling`embed_func.embed_query(query)` a method that returns an embedding vector of the query text. 

Subsequently, the function uses `self.milvus.similarity_search_with_score_by_vector`the method to pass in the embedding vectors and parameters of the query text `top_k`to perform a similarity search. This method returns the previous document that most closely resembles the query`top_k` and its similarity score. 

Finally, the function is called`score_threshold_process`, passing in`score_threshold` and `top_k`the search results `docs`as parameters, filtering out the documents that meet the criteria according to the score threshold, and returning the previous `top_k`document and its similarity score. This step ensures that the final returned document not only has a high similarity to the query text, but also that its similarity score exceeds the specified threshold. 

**Note**:
- Before calling `do_search`a function, make sure that the Milvus service is properly configured and accessible. 
- `top_k`Parameters should be set reasonably according to actual needs to avoid returning too many irrelevant results.
- `score_threshold`The parameter is used to further filter documents with a high degree of similarity, and its value should be adjusted according to the actual situation.

**Example output**:
Let's say the input query is "Recent Tech News",`top_k` which is 3, which `score_threshold`is 0.5, and the possible return value is:
```
[
    ("doc1", 0.8),
    ("doc2", 0.75),
    ("doc3", 0.65)
]
```
This means that out of all documents, there are three documents that have a similarity score of 0.5 or greater and are the top 3 documents that are most similar to the query "Recent Tech News".
***
### FunctionDef do_add_doc(self, docs)
**do_add_doc**: The function of this function is to add documents to the Milvus database and return the added document information. 

**Parameters**:
- `docs`: A list of documents that need to be added to the Milvus database, each document is a Document object.
- `**kwargs`: Accepts a variable number of keyword parameters that can be used to extend or customize functionality.

**Code Description**:
This function first iterates through the list of documents entered`docs`. For each document, it traverses the document's metadata`metadata`, converting the values of all metadata to a string type. It then checks the fields in the Milvus database to make sure they are included in the metadata for each document, and if they are missing, it adds an empty string as the default. In addition, it removes specific fields from the metadata, which are typically those used for text and vector data, as they may not be suitable for direct storage as metadata. 

After processing all the document's metadata, the function calls `self.milvus.add_documents(docs)`the method to add the document to the Milvus database. This method returns a list of IDs for the added documents. 

Finally, the function constructs a dictionary list containing the document ID and updated metadata, and returns this list as a result.

**Note**:
- Ensure that each document in the incoming document list`docs` is a valid Document object and that the necessary metadata has been set correctly. 
- This function does not handle the storage of text and vector fields, so make sure that the data has been processed appropriately before calling this function.

**Example output**:
```python
[
    {"id": "123456789", "metadata": {"title": "文档标题1", "author": "作者1"}},
    {"id": "987654321", "metadata": {"title": "文档标题2", "author": "作者2"}}
]
```
This example shows what the function can look like, including the ID and updated metadata of each document added to the Milvus database.
***
### FunctionDef do_delete_doc(self, kb_file)
**do_delete_doc**: The function of this function is to delete the document record in the specified knowledge base file. 

**Parameters**:
- `kb_file`: KnowledgeFile type, which indicates the knowledge base file of the document to be deleted.
- `**kwargs`: Receive a variable number of keyword parameters for extending or customizing functionality.

**Code Description**:
`do_delete_doc`The function is mainly used to delete the document records associated with a specified knowledge base file in the Milvus vector database. First, by calling`list_file_num_docs_id_by_kb_name_and_file_name` the function, the list of`kb_file` all document IDs corresponding to the file is obtained according to the knowledge base name (`kb_name`) and file name ()`filename` provided by the object. Then, if Milvus's collection(`col`) exists, use Milvus's `delete`method to construct a delete expression `expr=f'pk in {id_list}'`and perform the delete operation conditional on this expression. The`pk` primary key, which is the unique identifier of the document,`id_list` is the list of document IDs that need to be deleted. 

This function is `list_file_num_docs_id_by_kb_name_and_file_name`closely related to the function, which is responsible for querying and returning the IDs of all documents in the specified file, and `do_delete_doc`uses these IDs to locate and delete the corresponding document records in the Milvus database. This design makes the deletion of documents accurate and efficient, ensuring the consistency and accuracy of the knowledge base. 

**Note**:
- Before calling this function, make sure that `kb_file`the object is initialized correctly and that its properties`kb_name` and `filename`values are correct to match the records in the database. 
- This function relies on the connection to the Milvus database and is configured correctly to ensure that it`self.milvus.col` points to a valid Milvus collection. 
- Once the deletion operation is performed, the deleted document records cannot be recovered, so please use this function with caution to avoid data loss.
***
### FunctionDef do_clear_vs(self)
**do_clear_vs**: The function of this function is to clean up the view state of the Milvus Knowledge Base service. 

****Arguments: This function has no arguments. 

**Code Description**: `do_clear_vs`A function is `MilvusKBService`a method of the class that cleans up the view state of the Milvus Knowledge Base service. The method first `self.milvus.col`checks, i.e., the Milvus collection of the current operation, exists. If it exists, two actions are performed: first the`do_drop_kb` method is called to release and delete the collection in the current Milvus database, and then`do_init` the method is called to reinitialize the Milvus knowledge base service. 

Specifically, the `do_drop_kb`method is responsible for releasing and deleting collections from the Milvus database, ensuring that the collections are safely and completely removed from the database. Subsequently,`do_init` the method is called to reinitialize the connection and configuration of the Milvus service, in preparation for subsequent knowledge base operations such as search. This process shows that`do_clear_vs` the method plays an important role in handling the data cleansing and state reset process,`do_drop_kb` and it `do_init`enables a complete cleanup and reset of the state of the Milvus Knowledge Base service view through a combination and the functionality of both methods. 

**Note**:
- Before calling `do_clear_vs`a method, you should make sure that the connection to the Milvus service is healthy. 
- Since `do_clear_vs`the method causes the collection in the current Milvus database to be deleted, this is an irreversible operation. Therefore, before doing this method, you should carefully consider whether you really need to clean up the view state to avoid accidental loss of important data. 
- `do_clear_vs`The execution of a method depends on`do_drop_kb` and `do_init`two methods, so when modifying or maintaining these methods, you should pay attention to the relationships and dependencies between them to ensure the correct execution of the entire process. 
***
