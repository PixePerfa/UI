## FunctionDef add_kb_to_db(session, kb_name, kb_info, vs_type, embed_model)
**add_kb_to_db**: The function of this function is to add or update knowledge base information to the database. 

**Parameters**:
- `session`: A database session instance that is used to perform database operations.
- `kb_name`: The name of the knowledge base, which is used as a unique identifier for the knowledge base.
- `kb_info`: An introduction to the knowledge base, providing a basic description of the knowledge base.
- `vs_type`: Vector library type, specifies the type of vector library used by the knowledge base.
- `embed_model`: Embedding model name, specifying the embedding model to be used for the knowledge base.

**Code Description**:
This function first attempts to query the database if there is a knowledge base instance that matches the given knowledge base name. If it doesn't exist, the function creates a new `KnowledgeBaseModel`instance, populates its properties with the provided parameters, and then adds this new instance to the database. If a knowledge base with the same name already exists, the function will update the information about the knowledge base (`kb_info`), the vector library type (`vs_type`), and the embedding model (`embed_model`). Whether you're adding a new knowledge base or updating an existing one, this function will eventually return`True`, indicating that the operation was successful. 

**Note**:
- Make sure that you're passing in `session`a valid database session instance to allow the function to perform database operations. 
- Before calling this function, you should make sure that `kb_name`it is unique to avoid unnecessary overwriting of knowledge base information. 
- This function is not responsible for submitting the database session, and the caller needs to decide whether to submit the session based on their own needs after calling this function.

**Example output**:
Because the return value of this function is a Boolean type, it will return after a successful add or update operation`True`. For example, whether a new knowledge base is created or an existing knowledge base information is updated, a function call`add_kb_to_db(session, '技术文档库', '存储技术相关文档', 'ElasticSearch', 'BERT')` will be returned`True`. 
## FunctionDef list_kbs_from_db(session, min_file_count)
**list_kbs_from_db**: The function of this function is to list a list of knowledge base names from the database that meet certain criteria. 

**Parameters**:
- `session`: A database session object that is used to execute database queries.
- `min_file_count`: The minimum number of files, which is -1 by default, indicates that there is no limit on the number of files.

**Code Description**:
 The function `list_kbs_from_db` queries the  name of the knowledge base `session` in by passing in the database session object  .`KnowledgeBaseModel` It uses a filter that will only be included in the results list if the number of files in the knowledge base is greater than  the `min_file_count` value specified by the parameter. The query result starts with a list of multiple tuples, and the first element in each tuple is the knowledge base name. Then, using list inference, these tuples are converted into a list that contains only the name of the knowledge base. Eventually, the function returns this list of knowledge base names. 

**Note**:
- When using this function, you need to ensure that the incoming `session` object is a valid database session object and that the database connection has been configured correctly. 
- `min_file_count` Parameters allow callers to filter the knowledge base based on the number of files, and their values can be adjusted according to actual needs. If you don't need to filter the knowledge base based on the number of files, you can leave its default values.

**Example output**:
Suppose there are three knowledge bases in the database, the number of files is 0, 10, 20, and  the `min_file_count` value of the parameter is 5, then the return value of the function might be as follows:
```
['知识库B', '知识库C']
```
This means that only Knowledge Base B and Knowledge Base C with more than 5 files are included in the results list.
## FunctionDef kb_exists(session, kb_name)
**kb_exists**: The function of this function is to check if there is a knowledge base with the specified name in the database. 

**Parameters**:
- `session`: A database session object that is used to execute database queries.
- `kb_name`: The name of the knowledge base to be checked.

**Code Description**:
`kb_exists` The function checks if a knowledge base with that name exists in the database by taking a database session object and a knowledge base name as parameters. Internally, the function first executes a query using the incoming session object, which uses the model to`KnowledgeBaseModel` filter the tables in the database`knowledge_base` to find knowledge base records whose names match the`kb_name` parameters. Here methods are used `ilike`to make case-insensitive matches to improve the flexibility of the query. If there is at least one matching record in the query result, the function returns`True`, indicating that the knowledge stock of the specified name is there. If no matching record is found, it is returned`False`, indicating that the knowledge base does not exist. 

**Note**:
- When using `kb_exists`functions, you need to ensure that the incoming `session`object is a valid database session object and that the database connection is configured correctly. 
- The input `kb_name`should be of type string, and it is a good idea to do the necessary formatting or validation to ensure the accuracy of the query before calling this function. 
- The return value of this function is a Boolean type and can be used directly for conditional judgment.

**Example output**:
Suppose there is a knowledge base called Technical Documentation Library in the database, and the call`kb_exists(session, "技术文档库")` will be returned`True`. If you query for a non-existent knowledge base name, such as`kb_exists(session, "不存在的库")` , it is returned`False`. 

The use scenarios of this function in a project include, but are not limited to, checking whether a knowledge base with the same name already exists before adding a new knowledge base, or verifying the existence of a knowledge base before performing knowledge base-related operations to ensure data consistency and the validity of operations.
## FunctionDef load_kb_from_db(session, kb_name)
**load_kb_from_db**: The function of this function is to load the knowledge base information of the specified name from the database. 

**Parameters**:
- `session`: A database session instance that is used to execute database queries.
- `kb_name`: The name of the knowledge base to be loaded.

**Code Description**:  The `load_kb_from_db` function takes a database session and a knowledge base name as parameters, and uses this session to query `KnowledgeBaseModel` the first knowledge base record in the table with a name that matches the given name. Ignore the case of the name when querying. If a corresponding knowledge base record is found, the function will extract the name of the knowledge base (`kb_name`), the vector library type (), `vs_type`and the embedding model name () from that record`embed_model`. If no corresponding record is found, the three variables will be set to `None` . Finally, the function returns these three values. 

**Note**:
- Before calling this function, make sure that the incoming  is `session` a valid database session instance and that it has been configured correctly. 
- The incoming knowledge base name `kb_name` should be a string with a corresponding record in the database, otherwise the function will return `None` a  value. 
- This function is not case-sensitive, that is, it is not case-sensitive.

**Example output**:
Suppose there is a knowledge base in the database called Technical Documentation Library, with a vector library type of "ElasticSearch" and an embedding model name of "BERT", then the call `load_kb_from_db(session, "技术文档库")` will return:
```
("技术文档库", "ElasticSearch", "BERT")
```
If a knowledge base with the specified name does not exist in the database, calling `load_kb_from_db(session, "不存在的库")` will  return:
```
(None, None, None)
```
## FunctionDef delete_kb_from_db(session, kb_name)
**delete_kb_from_db**: The function of this function deletes the specified knowledge base from the database. 

**Parameters**:
- `session`: A database session instance that is used to perform database operations.
- `kb_name`: The name of the knowledge base to be deleted.

**Code Description**:
 The function first uses `delete_kb_from_db`the `session` method to query  whether there is a knowledge base with the specified name `kb_name` in the table by passing in the `query` parameters and knowledge base name `KnowledgeBaseModel` . When querying, the method is used `ilike` to implement case-insensitive matching to improve user experience and fault tolerance. If the target knowledge base is queried, use `session.delete` the method to remove it from the database. Regardless of whether the knowledge base is found and deleted, the function will eventually return `True`to indicate that the operation is complete. 

**Note**:
- When you call this function, you need to make sure that you are passing `session` in a valid database session instance and that the database connection is configured correctly. 
- The incoming knowledge base name `kb_name` should be a string type that uniquely identifies a knowledge base in the database. 
- The database transaction is not automatically committed after the function is executed, and the caller needs to decide whether to commit the transaction based on the actual situation.

**Example output**:
Because the return value of this function is fixed `True`, no concrete output example is provided. When this function is called, you can confirm that the operation has been performed based on the return value, but you will need to verify that the knowledge base was indeed successfully deleted by other means, such as querying the database. 

The application scenarios of this function in a project include, but are not limited to, in the knowledge base management service, when a user or administrator requests the deletion of a knowledge base, this function is called to perform the deletion operation. For example, in `KBService` the method of the class`drop_kb`, the knowledge base is  deleted by calling  the function `delete_kb_from_db` . This design allows the deletion of the knowledge base to be used independently or easily integrated into more complex service processes. 
## FunctionDef get_kb_detail(session, kb_name)
**get_kb_detail**: The function of this function is to get the details of the specified knowledge base. 

**Parameters**:
- `session`: A database session instance that is used to execute database queries.
- `kb_name`: String type, specifying the name of the knowledge base to be queried.

**Code Description**:
`get_kb_detail` The function takes a database session instance and a knowledge base name as parameters, and uses this session instance to query `KnowledgeBaseModel` the table for records whose names match the given knowledge base name. Ignore case when querying to improve query flexibility. If a matching knowledge base record is found, the function returns a dictionary containing the knowledge base name (`kb_name`), the knowledge base introduction (),`kb_info` the vector library type (`vs_type`), the embedding model name (`embed_model`), the number of files (`file_count`), and the creation time (`create_time`). If no matching record is found, an empty dictionary is returned. 

This function is called in several places in the project, including, but not limited to, loading knowledge base embedding vectors and getting a knowledge base detail list. These call scenarios show that `get_kb_detail` functions are an important bridge between database knowledge base information and the rest of the project. 

**Note**:
- Ensure that the parameter passed in `session` is a valid database session instance and that it is properly configured and connected to the database before calling this function. 
- The incoming  should `kb_name` be of type string, and try to make sure that it is accurate so that it can correctly match the records in the database. 

**Example output**:
Suppose you have a knowledge base in your database called Technical Documentation Library, the details of which are as follows:
```python
{
    "kb_name": "技术文档库",
    "kb_info": "存储技术相关文档的知识库",
    "vs_type": "ElasticSearch",
    "embed_model": "BERT",
    "file_count": 100,
    "create_time": "2023-04-01T12:00:00"
}
```
If the name of the queried knowledge base is Technical Documentation Library, the  function `get_kb_detail` returns the above dictionary. If no matching knowledge base is found, the function returns `{}`. 
