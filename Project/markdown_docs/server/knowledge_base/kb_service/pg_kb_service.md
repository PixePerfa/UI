## ClassDef PGKBService
**PGKBService**: The PGKBService class is a concrete class used to implement knowledge base services with PostgreSQL. 

**Properties**:
- `engine`: A connection engine created through SQLAlchemy to interact with the PostgreSQL database.
- `pg_vector`: A PGVector instance used to store and retrieve embedding vectors.

**Code Description**:
The PGKBService class inherits from the KBService class and provides a concrete implementation of interacting with a PostgreSQL database. It uses SQLAlchemy as an ORM tool to `engine` establish a connection to the database via attributes. This class is mainly responsible for initializing vector storage, adding, deleting, checking and modifying documents, and creating and deleting knowledge bases. 

- `_load_pg_vector` The method is used to load a PGVector instance, which is responsible for the storage and retrieval of embedding vectors.
- `get_doc_by_ids` The method obtains the document content and metadata by the document ID.
- `del_doc_by_ids` The method deletes the document with the specified ID and actually calls the method of the same name of the base class.
- `do_init` The method is called at class initialization and is used to load the PGVector instance.
- `do_create_kb` The method is to create a concrete implementation of the knowledge base, which is currently empty.
- `vs_type` The method returns a supported vector storage type, i.e., PostgreSQL.
- `do_drop_kb` The method deletes the knowledge base, including the related records in the database and the path to the knowledge base on the file system.
- `do_search` The method implements a query-based document search function, which returns a list of documents that are most relevant to the query.
- `do_add_doc` The method adds a document to the knowledge base and returns the added document information.
- `do_delete_doc` Method deletes the specified document from the knowledge base.
- `do_clear_vs` method to empty all the contents of the vector store and recreate the collection.

**Note**:
- Before you use the PGKBService class, you need to make sure that the PostgreSQL database is properly configured and `kbs_config` that the configuration item  in contains `pg` the correct database connection URI. 
- When you call `do_add_doc` `do_delete_doc` methods such as and to modify the contents of the database, you need to ensure that the parameters passed in are in the expected format to avoid execution errors or data corruption. 
- `do_drop_kb` When deleting a knowledge base, the records in the database and the path of the knowledge base on the file system are deleted at the same time.

**Example output**:
```python
# 假设调用 get_doc_by_ids 方法查询 ID 为 ['doc1', 'doc2'] 的文档
docs = pgkb_service.get_doc_by_ids(['doc1', 'doc2'])
# 可能的返回值为
[
    Document(page_content="文档1的内容", metadata={"author": "作者1"}),
    Document(page_content="文档2的内容", metadata={"author": "作者2"})
]
```
This example shows the process of obtaining document content and metadata by document ID and its possible return value.
### FunctionDef _load_pg_vector(self)
**_load_pg_vector**: The function of this function is to load the PostgreSQL vector space search engine. 

**Parameters**: This function has no explicit arguments, but it relies on several properties of the class instance. 

**Code Description**: `_load_pg_vector`The function is responsible for initializing a PGVector instance that is used for vector space search in the PostgreSQL database. This process includes the following key steps:

1. Use `EmbeddingsFunAdapter`the class to create an embedding function adapter. This adapter is based on the properties of the class instance`embed_model` and is used to convert the text into a vector representation. `EmbeddingsFunAdapter`Synchronous and asynchronous text embedding methods are supported, which are suitable for different application scenarios. 

2. Specifies the collection name for the vector space search, here using the properties of the class instance`kb_name` as the collection name. 

3. Set the distance strategy to Euclidean distance (), `DistanceStrategy.EUCLIDEAN`which is used to calculate the distance between vectors. 

4. Use `PGKBService.engine`as a database connection. This is a class property that represents the connection engine to the PostgreSQL database. 

5. Obtain `kbs_config.get("pg").get("connection_uri")`the database connection string, which contains the database address, port, user name, password, and other information, and is used to establish a database connection. 

With these steps, `_load_pg_vector`the function configures a PGVector instance for vector space search and saves it in the properties of the class instance`pg_vector`. This allows other methods of the class to take advantage of this PGVector instance to perform vector space search operations, such as finding documents that most closely resemble a given text vector. 

**Note**:
- Before calling `_load_pg_vector`a function, you need to make sure that the sum properties of the class instance`embed_model` `kb_name`are set correctly. These attributes are essential for initializing a PGVector instance. 
- `PGKBService.engine`It needs to be pre-configured to ensure a successful connection to the PostgreSQL database.
- Database connection strings should be kept private to avoid revealing sensitive information about the database.

This function `do_init`is called in a method that `do_init`is responsible for performing the initialization of the class, including loading the PostgreSQL vector space search engine. This suggests that`_load_pg_vector` functions are an important part of the class initialization process, ensuring the usability of vector space search capabilities. 
***
### FunctionDef get_doc_by_ids(self, ids)
**get_doc_by_ids**: The function of this function is to query and return the corresponding list of documents based on the provided list of IDs. 

**Parameters**:
- ids: A list of strings containing the IDs of the documents that need to be queried.

**Code Description**:
`get_doc_by_ids` The function takes as a parameter a list of strings `ids` containing the IDs of the documents to be queried. Internally, the function first creates `Session` a session using the context manager, through which it interacts with the database. Next, define an SQL query statement `stmt`that `langchain_pg_embedding` picks up `document` the  sum  field from a table named , `cmetadata` provided that `collection_id` the value of the field is included in the `ids` list of IDs provided by the parameter. 

By executing this query statement and passing in `ids` the parameter, the function retrieves the matching record from the database. Each record is used to create an `Document` object that contains the retrieved document content(`page_content`) and metadata (`metadata`). All of these `Document` objects are then collected into a list and serve as the return value of the function. 

**Note**:
- Make sure that the incoming list of IDs `ids` is not empty and that each ID is valid to ensure that the query can be executed correctly. 
- This function depends on `langchain_pg_embedding` the structure of the database table, specifically the fields it queries. If the database structure changes, you may need to update this function accordingly. 

**Example output**:
Suppose there are two records in the database `collection_id` that match a given list of IDs, the function might return a list like this:
```python
[
    Document(page_content="文档内容1", metadata={"作者": "张三", "发布日期": "2023-01-01"}),
    Document(page_content="文档内容2", metadata={"作者": "李四", "发布日期": "2023-02-01"})
]
```
This list contains two `Document` objects, each containing the content and metadata of the document retrieved from the database. 
***
### FunctionDef del_doc_by_ids(self, ids)
**del_doc_by_ids**: The function of this function is to delete documents based on the list of IDs provided. 

**Parameters**:
- ids: A list of strings containing the IDs of the documents to be deleted.

**Code Description**:
`del_doc_by_ids` The function takes as a parameter a list of strings `ids` containing the IDs of the documents that need to be deleted from the database. The function implements the delete operation by calling the method of its parent class `del_doc_by_ids` and `ids` passing the argument to the method. This suggests that the actual deletion logic is encapsulated in the parent class's methods, and that the current function is primarily responsible for forwarding the deletion request to the parent class for processing. 

**Note**:
- Make sure that the argument passed to this function `ids` contains a valid document ID, otherwise no documents may be deleted. 
- This function returns a Boolean value that indicates whether the deletion operation was successful or not. However, the specific success depends on the implementation details of the parent class method.
- Before using this function, you should understand `del_doc_by_ids` the implementation of the method in the parent class  and how it handles deletion operations in different cases. 

**Example output**:
A call `del_doc_by_ids(['doc1', 'doc2'])` may return `True`to indicate that the document with the specified ID has been successfully deleted. If the operation fails, it may be returned `False`. Note that the actual return value depends on the implementation of the parent class method. 
***
### FunctionDef do_init(self)
**do_init**: The function of this function is to initialize an instance of the PGKBService class. 

****Arguments: This function has no arguments. 

**Code Description**: `do_init`The method is an initialization method of the PGKBService class, which `_load_pg_vector`loads the PostgreSQL vector space search engine by calling the method. This process is an important step in the class instantiation process, ensuring that instances of the class are able to perform vector space search operations correctly. 

In the`do_init` method, the `_load_pg_vector`following key initialization steps are completed by calling the method:
1. Create an embedding function adapter `EmbeddingsFunAdapter`that is based on the properties of the class instance `embed_model`and is used to convert text into a vector representation. 
2. Specifies the collection name for the vector space search, using the attributes of the class instance`kb_name` as the collection name. 
3. Set the distance strategy to Euclidean distance, which is used to calculate the distance between vectors.
4. Use the class property `PGKBService.engine`as the database connection, which represents the connection engine to the PostgreSQL database. 
5. Gets the database connection string, which is used to establish a database connection.

With these steps, `_load_pg_vector`the method configures a PGVector instance for vector space search and saves it in the properties of the class instance`pg_vector`. This way, other methods of the class can take advantage of this PGVector instance to perform vector space search operations, such as finding documents that most closely resemble a given text vector. 

**Note**:
- No `do_init`special preparation is required before a method is called, as it is an initialization method that is automatically called during class instantiation. 
- You need to make sure that`embed_model` the and properties are set correctly before `kb_name`being called`_load_pg_vector`, as these properties are essential for initializing the PGVector instance. 
- `PGKBService.engine`It needs to be pre-configured to ensure a successful connection to the PostgreSQL database.
- Database connection strings should be kept private to avoid revealing sensitive information about the database.

In general, the`do_init` method `_load_pg_vector`completes the initialization of the PGKBService class instance by calling the method, which is ready for the subsequent vector space search operation. 
***
### FunctionDef do_create_kb(self)
**do_create_kb**: The function of this function is to create a knowledge base. 

****Arguments: This function has no arguments. 

**Code Description**: `do_create_kb` A function is `PGKBService` a method of a class that is responsible for the specific logic that creates a knowledge base. Currently, the implementation of this function is empty (using  a `pass` statement), which means it doesn't do anything. In practice, developers need to add code logic to this function to create a knowledge base, such as connecting to a database and performing database operations. 

**Note**: Although `do_create_kb` the current implementation of the function is empty, in future development, when adding specific implementation logic, you need to ensure the correctness of the database connection and the security of the operation. In addition, considering that the knowledge base can contain a large amount of data, attention needs to be paid to performance optimization and error handling. 
***
### FunctionDef vs_type(self)
**vs_type**: The function of the vs_type function is to return the vector storage type that is currently supported by the knowledge base service. 

**Parameters**: This function does not accept any parameters. 

**Code Description**: The vs_type function is a method of the PGKBService class, and its main purpose is to identify the types of vector stores supported by the knowledge base service instance. In this implementation, the vs_type method explicitly states that PostgreSQL (PG) is the vector storage type used by the service instance by returning a SupportedVSType.PG. SupportedVSType is an enumeration class that defines all the vector storage types supported in your project, including but not limited to FAISS, MILVUS, ZILLIZ, Elasticsearch (ES), ChromaDB, etc., and PG. By returning an enumerated value in SupportedVSType, the vs_type method provides the necessary information for the configuration and instantiation of the knowledge base service. This design makes the management and expansion of the knowledge base service more flexible and convenient, because different vector storage services can be dynamically selected and switched as needed. 

**Note**:
- When using the PGKBService class and its vs_type methods, you should be aware of the vector storage types defined in the SupportedVSType enumeration class to ensure that the vector storage type information returned by the method is properly understood and used.
- Since the vs_type method returns an enumerated member, you should pay attention to the use of the enumeration type when processing the returned value, such as obtaining specific information through the name or value attribute of the enumerated member.

**Example output**: Suppose the vs_type method of a PGKBService instance is called, and the possible return value is:
```
'pg'
```
This indicates that the current knowledge base service instance uses PostgreSQL as its vector storage service.
***
### FunctionDef do_drop_kb(self)
**do_drop_kb**: The function of this function is to delete the database records associated with the specified knowledge base name and the knowledge base directory in the file system. 

**Parameters**: This function doesn't have explicit arguments, but it depends on`self.kb_name` and `self.kb_path`both instance variables. 

**Code Description**:
`do_drop_kb`A function is `PGKBService`a method of a class that deletes data related to a particular knowledge base. In this method, you first delete the records associated with the knowledge base in the database through SQL statements, and then delete the corresponding knowledge base directory in the file system. The specific steps are as follows:

1. Use `Session`the context manager to create a database session, ensure that database operations complete in a session, and automatically close the session when the operation ends. 
2. Perform SQL deletion operations in a session. First, delete`langchain_pg_embedding` all`collection_id` matching records in the table that match the `langchain_pg_collection`records in the table that `name`match the fields`self.kb_name` in the table`uuid`. This means that all embedding information associated with the specified KB name will be deleted. 
3. Next, delete the records `langchain_pg_collection`in the table`name` that `self.kb_name`match the fields. This step deletes the collection record for the knowledge base. 
4. Perform `session.commit()`a commit database transaction to ensure that the above deletion is saved to the database. 
5. Use the function to `shutil.rmtree`delete the knowledge base directory in the file system. `self.kb_path`The variable specifies the path to the knowledge base directory, and the function recursively deletes the directory and all its contents. 

**Note**:
- Before executing this function, make sure that`self.kb_name` and `self.kb_path`have been set correctly to point to the name and path of the knowledge base you want to delete, respectively. 
- This operation is irreversible, and once executed, the associated database records and directories in the file system are permanently deleted. Therefore, before calling this function, make sure that you have made the appropriate backup or confirm that you no longer need the data.
- Since the database and file system are manipulated directly, ensure that the user who performs this operation has the appropriate permissions.
***
### FunctionDef do_search(self, query, top_k, score_threshold)
**do_search**: The function of this function is to perform a text query and filter out the documents with the highest similarity based on a given score threshold and an upper limit on the number of documents returned. 

**Parameters**:
- `query`: The text to be queried, and the data type is a string.
- `top_k`: The maximum number of documents to be returned, with data type as an integer.
- `score_threshold`: Score threshold, which is used to filter documents with similarity above this threshold, and the data type is floating-point.

**Code Description**:
`do_search`The function first passes through`EmbeddingsFunAdapter` an instance of the class`embed_func` and calls `embed_query`a method to convert the query text `query`into an embedding vector. This is done by converting the text into a vectorized representation for subsequent similarity searches. 

Next, the method used by`self.pg_vector` the function passes `similarity_search_with_score_by_vector`in the embedding vectors and parameters obtained in the previous step `top_k`to perform a similarity search. This method returns a list of documents and their similarity scores, sorted according to their similarity to the query vector. 

Finally, the function calls`score_threshold_process` the method, passes in`score_threshold`, `top_k`and the results of the similarity search, filters out the documents that meet the criteria according to the score threshold, and returns the previous `top_k`document. This step ensures that the returned document not only has a high similarity to the query text, but also that its similarity score exceeds the specified threshold. 

**Note**:
- Make sure you're passing in`query` a valid string, `top_k`a positive integer, and `score_threshold`a non-negative floating-point number. 
- `EmbeddingsFunAdapter`and `score_threshold_process`are the key components that this function depends on, ensuring that their implementation is as expected. 
- The performance and accuracy of this function depend on the quality of the embedded model and the efficiency of the similarity search algorithm.

**Example output**:
Let's say you call `do_search`a function, pass in the query text "Sample Query",`top_k` which is 3, `score_threshold`which is 0.5, and the possible return value is:
```
[("文档1", 0.8), ("文档3", 0.7), ("文档5", 0.6)]
```
This means that out of all documents, there are three documents that have a similarity score of 0.5 or greater and are the first three documents with the highest similarity.
***
### FunctionDef do_add_doc(self, docs)
**do_add_doc**: The function of this function is to add documents to the database and return a list of information containing document IDs and metadata. 

**Parameters**:
- `docs`: A list of documents that need to be added to the database, each document is an`Document` object. 
- `**kwargs`: Accepts a variable number of keyword arguments that can be passed to the underlying database operation as needed.

**Code Description**:
`do_add_doc`The function first calls`pg_vector` the object's`add_documents` method to `docs`add the documents in the list to the database. `add_documents`The method returns a list of each document ID. The function then iterates through these IDs and the original`docs` list to create a new list using list derivation`doc_infos`. Each element of this new list is a dictionary with two keys:`id` and`metadata`. `id`The key corresponds to the ID of the document, and the `metadata`key corresponds to the metadata of the document. Finally, the function returns a`doc_infos` list. 

**Note**:
- Make sure that `do_add_doc`the arguments passed to the function`docs` are a `Document`list of objects, and that each `Document`object should have valid metadata. 
- The keyword parameters you pass to `**kwargs`will directly affect the underlying database operations, so use caution to ensure you understand the impact of these parameters. 

**Example output**:
Suppose we `do_add_doc`pass two documents to a function, and both documents are successfully added to the database, the function might return a list like this:
```python
[
    {"id": "doc1_id", "metadata": {"title": "Document 1 Title", "author": "Author Name"}},
    {"id": "doc2_id", "metadata": {"title": "Document 2 Title", "author": "Another Author Name"}}
]
```
This list contains the ID and metadata of each document, which can be used for further processing or display.
***
### FunctionDef do_delete_doc(self, kb_file)
**do_delete_doc**: This function is used to remove the document vector associated with the specified knowledge file from the database. 

**Parameters**:
- `kb_file`: KnowledgeFile object, which represents the knowledge base file whose document vector needs to be deleted.
- `**kwargs`: Receive additional keyword arguments to extend functionality in future releases without impacting existing interfaces.

**Code Description**:
`do_delete_doc`The function first `kb_file`obtains the full path to the knowledge base file via the argument. To ensure that the file path string in the database query statement is formatted correctly, it replaces all backslashes () in the path`\` with double backslashes (`\\`). This is because in SQL queries, a backslash is a special character that needs to be escaped. 

Next, the function uses `Session`the context manager to create a database session and execute a SQL `DELETE`statement. `DELETE`The purpose of this statement is to`langchain_pg_embedding` remove from the table `cmetadata`all records in the field (stored in JSONB format) where the `source`value corresponding to the key matches the given file path. Here, it'`cmetadata::jsonb @> '{"source": "filepath"}'::jsonb`s a PostgreSQL JSONB query expression that looks for`cmetadata` records that contain a specific`source` key-value pair. 

After the delete operation is performed, the function `session.commit()`ensures that the deletion operation is saved to the database by committing the changes. 

**Note**:
- When you use this function, you need to make sure that the incoming`kb_file` object is valid and that its `filepath`properties correctly reflect the location of the file on disk. 
- This function directly manipulates the database and performs the deletion operation. Therefore, before calling this function, you should make sure that you have made a proper backup or confirmation of the data you want to delete in case of accidental data loss.
- Because this function involves database operations, its execution efficiency and scope of influence may be affected by the current state and configuration of the database. When dealing with large amounts of data or under high load, it is recommended to monitor database performance to avoid potential performance issues.
***
### FunctionDef do_clear_vs(self)
**do_clear_vs**: The function of this function is to clear and recreate the vector space. 

****Arguments: This function does not accept any arguments. 

**Code Description**: `do_clear_vs` A function is `PGKBService` a method of the class that manages the process of clearing and rebuilding vector spaces. In this function, the method is first called `self.pg_vector.delete_collection()` to delete the current vector space collection. This step is to clear all existing data and ensure that the vector space is empty. Next, `self.pg_vector.create_collection()` recreate a new collection of vector spaces by calling the method. The purpose of this is to provide a new environment for subsequent data insertion and management after the old data has been deleted. 

**Note**:  You `do_clear_vs` need to be cautious when using functions, as this will cause all existing vector space data to be permanently deleted and cannot be recovered. So, before you do this, make sure you have made adequate backups of your data or confirm that you no longer need it. In addition, after the vector space collection is recreated, any related settings or indexes need to be reconfigured to ensure proper use of the vector space and optimized performance. 
***
