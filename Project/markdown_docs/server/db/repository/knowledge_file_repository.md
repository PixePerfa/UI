## FunctionDef list_file_num_docs_id_by_kb_name_and_file_name(session, kb_name, file_name)
**list_file_num_docs_id_by_kb_name_and_file_name**: The function of this function is to list all document IDs corresponding to a file in a knowledge base. 

**Parameters**:
- `session`: A database session instance that is used to execute database queries.
- `kb_name`: String type, specifies the name of the knowledge base.
- `file_name`: String type, specifies the name of the file.

**Code Description**:
`list_file_num_docs_id_by_kb_name_and_file_name`Functions receive database sessions, knowledge base names, and file names as parameters, and use these parameters to query tables in the database`FileDocModel`. The purpose of the query is to find out all the document IDs that match the given knowledge base name and file name. These document IDs are then converted into integer lists. This process involves filtering the`FileDocModel` model's `doc_id`fields to ensure that only eligible records are selected. Eventually, the function returns an integer list containing the IDs of all matching documents. 

**Note**:
- Ensure that you are passing in `session`a valid database session instance that is properly configured to connect to the target database. 
- `kb_name`and `file_name`parameters should be accurate to match the records in the database. Case sensitivity depends on the database configuration. 
- The returned list of document IDs is based on the records that actually exist in the database, and if no matching records are found, an empty list is returned.

**Example output**:
Suppose there are two documents with IDs 1 and 2 respectively, and both documents belong to File B.pdf in Knowledge Base A, a list will be returned after calling this function and passing in the corresponding knowledge base name and file name`[1, 2]`. 

Through this function, you can easily obtain the ID of the relevant document according to the knowledge base name and file name, and then support further document management or operation, for example, in the`MilvusKBService` `do_delete_doc`method, the list of document IDs obtained by this function is used to specify the deletion of the corresponding document record in the vector library. 
## FunctionDef list_docs_from_db(session, kb_name, file_name, metadata)
**list_docs_from_db**: The function of this function is to list all the documents corresponding to a file in a knowledge base. 

**Parameters**:
- `session`: A database session instance that is used to execute database queries.
- `kb_name`: String type, specifying the name of the knowledge base to be queried.
- `file_name`: String type, optional parameter, default is None, specifies the name of the file to be queried.
- `metadata`: Dictionary type, optional parameter, default is an empty dictionary, which is used to filter queries based on the metadata of the document.

**Code Description**:
The function first queries based on the knowledge base name`kb_name` pair`FileDocModel`, and if a parameter is provided`file_name`, further filters based on the file name. Then, iterate through `metadata`each item in the dictionary and filter the query results based on the key and value of the metadata. Eventually, the function returns a list, and each element in the list is a dictionary containing the document's ID()`id` and metadata(`metadata`). 

In terms of implementation, the`list_docs_from_db` function interacts with the database through the ORM model`FileDocModel`, and uses the query interface of SQLAlchemy to retrieve data. `FileDocModel.kb_name.ilike(kb_name)`and`FileDocModel.file_name.ilike(file_name)` the `ilike`use of methods for case-insensitive fuzzy matching, which enhances the flexibility of the query. For metadata queries,`FileDocModel.meta_data[k].as_string() == str(v)` conditional filtering of JSON fields is implemented. 

**Note**:
- When using this function, you should ensure that you are passing in`session` a valid database session instance. 
- Since `metadata`the parameter defaults to an empty dictionary, modifying this default value may affect the expected behavior of the function. It is recommended that you explicitly pass in the required parameters when calling a function`metadata` to avoid directly modifying the default values in the function definition. 
- When processing large amounts of data, you should consider query performance and optimization to avoid slow queries due to too many filtering operations.

**Example output**:
Suppose there are two records in the database with field values:
- id: 1, kb_name: "KB A", file_name: "File A.pdf", doc_id: "docA", metadata: {"author": "Zhang San", "year": "2021"}
- id: 2, kb_name: "KB A", file_name: "File B.pdf", doc_id: "docB", metadata: {"author": "Li Si", "year": "2022"}

The call `list_docs_from_db(session, "知识库A")`will return the following list:
```python
[
    {"id": "docA", "metadata": {"author": "张三", "year": "2021"}},
    {"id": "docB", "metadata": {"author": "李四", "year": "2022"}}
]
```
This output example shows how a function can return the IDs and metadata of all documents under a given knowledge base name.
## FunctionDef delete_docs_from_db(session, kb_name, file_name)
**delete_docs_from_db**: The function of this function is to delete all documents corresponding to a file in a knowledge base and return the information of the deleted documents. 

**Parameters**:
- `session`: A database session instance that is used to perform database operations.
- `kb_name`: String type, specifying the name of the knowledge base from which you want to delete the document.
- `file_name`: String type, optional, default is None, specifies the name of the file to delete the document.

**Code Description**:
`delete_docs_from_db`The function first calls `list_docs_from_db`the function, listing all the corresponding documents based on the knowledge base name`kb_name` and the file name `file_name`(if provided). Then, construct a query object, get through`session.query(FileDocModel)` `FileDocModel`the query interface, and use `filter`methods to filter based on the knowledge base name. If a parameter is provided`file_name`, it is further filtered based on the file name. Next, use the `query.delete(synchronize_session=False)`method to delete all the documents that meet the criteria, and `session.commit()`ensure that the changes are saved to the database by committing the transaction. Finally, the function returns`list_docs_from_db` a list of deleted documents that were previously retrieved by the function. 

**Note**:
- Before calling this function, you should ensure that you are passing in `session`a valid instance of the database session and that it has been configured correctly. 
- Deletion operations are irreversible, so make sure you really need to delete these documents before you execute this function.
- Since this function returns information about the deleted document, it can be used for logging or subsequent processing.

**Example output**:
Suppose there are two document records in the database with knowledge base names of Knowledge Base A and file names of File A.pdf and File B.pdf, respectively, and`delete_docs_from_db(session, "知识库A", "文件A.pdf")` the following list may be returned when called:
```python
[
    {"id": "docA", "metadata": {"author": "张三", "year": "2021"}}
]
```
This output example shows how the function returns the ID and metadata information of a deleted document.
## FunctionDef add_docs_to_db(session, kb_name, file_name, doc_infos)
**add_docs_to_db**: The function of this function is to add all the document information corresponding to a file in a knowledge base to the database. 

**Parameters**:
- `session`: A database session instance that is used to perform database operations.
- `kb_name`: String type, specifying the name of the knowledge base to which you want to add document information.
- `file_name`: String type, specifies the name of the file to which you want to add document information.
- `doc_infos`: A list of document information, each element is a dictionary containing the ID and metadata of the document.

**Code Description**:
`add_docs_to_db`Functions are primarily used to add document information to the database in bulk. It takes a database session, a knowledge base name, a file name, and a list of document information as parameters. The document information list`doc_infos` is formatted in such a way `[{"id": str, "metadata": dict}, ...]`that each dictionary represents the information of a document, including the ID and metadata of the document. 

The function first checks`doc_infos` if it is`None`, and if so, prints an error message and returns `False`an added failure. This is to handle possible error cases and ensure the robustness of the function. 

Next, the function iterates through `doc_infos`the list and creates an instance for each document in the list`FileDocModel`. `FileDocModel`is an ORM model that maps tables in a database `file_doc`that contains basic document information fields, such as knowledge base name, file name, document ID, and metadata. `FileDocModel`When an instance is created, the information about the document that is currently traversed is populated into the appropriate fields. 

Then, use `session.add(obj)`Add Instance `FileDocModel`to a database session so that you can save the document information to the database. When the traversal is complete, the function returns`True` that all document information has been successfully added to the database. 

**Note**:
- Make sure that you are passing in `session`a valid database session instance and that the database connection is configured correctly. 
- `doc_infos`The parameter cannot be empty, and the dictionary inside it needs to contain`id` and `metadata`key. 
- In practice, you may need to handle `session.add(obj)`exceptions that may be thrown by operations, such as database constraint violations. 

**Example output**:
There is no direct output example for this function, as its main role is to affect the state of the database. However, after a successful execution, you can expect that the table in the database`file_doc` will add a corresponding record, and the field value of the record will reflect the parameter value provided when the function is called. 
## FunctionDef count_files_from_db(session, kb_name)
**count_files_from_db**: The function of this function is to count the number of files in a specified knowledge base. 

**Parameters**:
- `session`: A database session instance that is used to execute database queries.
- `kb_name`: String type, specifying the name of the knowledge base for which you want to count the number of files.

**Code Description**:
 The function uses the ORM model to query the number of files in a given knowledge base `count_files_from_db`by receiving a database session instance and a knowledge base name as parameters`KnowledgeFileModel`. In this process, the function first constructs a query for the`KnowledgeFileModel` model, using `filter`methods to filter based on the knowledge base name (`kb_name`), and here using `ilike`methods to achieve case-insensitive matching to enhance the flexibility of the query. Finally, use the `count`method to calculate and return the number of records that meet the criteria, that is, the number of files in the specified knowledge base. 

**Note**:
- When you call this function, make sure that the argument you pass in`session` is a valid instance of the database session and that `kb_name`the argument correctly specifies the name of the target knowledge base. 
- Due to `ilike`the fuzzy matching method, the knowledge base names can be flexibly matched, but the accuracy of the names should be paid attention to when using them to avoid erroneous statistical results. 

**Example output**:
If you specify that the knowledge base name is "DefaultKB" and there are 10 files in the knowledge base, the call`count_files_from_db(session, "DefaultKB")` returns an integer `10`indicating that the number of files in the "DefaultKB" knowledge base is 10. 

The use scenarios of this function in a project include, but are not limited to, that a knowledge base service (such as`KBService` a method in a class`count_files`) calls this function to obtain the total number of files in a specific knowledge base to support functions such as knowledge base management and data analysis. 
## FunctionDef list_files_from_db(session, kb_name)
**list_files_from_db**: The function of this function is to list all the file names that belong to a particular knowledge base from the database. 

**Parameters**:
- `session`: A database session object that is used to execute database queries.
- `kb_name`: The name of the knowledge base, which is used to filter the files for a specific knowledge base.

**Code Description**:
`list_files_from_db`The function takes a database session object and a knowledge base name as arguments, and uses the session object to perform a query. This query is model-based`KnowledgeFileModel` and filters out `kb_name`all records whose fields match the incoming KB name. Methods are used here`ilike`, which allow for case-insensitive comparisons, increasing the flexibility of the query. The result of the query is `KnowledgeFileModel`a list of instances, representing all the files found. The function then iterates through this list, extracts the properties of each instance`file_name`, i.e., the file names, and collects those file names into a list. Finally, return to this list with all the file names that match the criteria. 

**Note**:
- Ensure that the incoming `session`object is a valid database session instance and that the connection to the database is properly configured. 
- The incoming knowledge base name `kb_name`should ensure its accuracy, as the query results are directly dependent on this parameter. 
- Queries use `ilike`methods that are not case sensitive, but this can affect query performance, especially in large databases. 

**Example output**:
If there are files in the database that belong to a knowledge base named "GeneralKB", and the file names are "document1.pdf", "report2.docx", respectively, then the call`list_files_from_db(session, "GeneralKB")` returns the following list:
```
["document1.pdf", "report2.docx"]
```
## FunctionDef add_file_to_db(session, kb_file, docs_count, custom_docs, doc_infos)
**add_file_to_db**: The function of this function is to add file information to the database and update the information and version number of the file if the file already exists. 

**Parameters**:
- `session`: A database session instance that is used to perform database operations.
- `kb_file`: Type `KnowledgeFile` , which represents the knowledge file to be added to the database. 
- `docs_count`: Integer, which is set to 0 by default, indicates the number of documents contained in the file.
- `custom_docs`: Boolean, which is set to False by default, indicates whether the document in the file is a custom document.
- `doc_infos`: A list of document information, each element is a dictionary in the format that`[{"id": str, "metadata": dict}, ...]` contains the ID and metadata of the document. 

**Code Description**:
`add_file_to_db` The function first querelieves whether the specified knowledge base exists in the database, and if so, it continues to check whether a file with the same name already exists in the knowledge base. If a file already exists, the function updates the file's last modified time, file size, number of documents, whether it is a custom document flag, and file version number. If the file does not exist, create a new `KnowledgeFileModel` instance and set the corresponding file information, including the file name, file extension, knowledge base name, document loader name, text splitter name, file modification time, file size, number of documents, and custom document flag. Then, add a new file instance to the database session and increase the file count for the knowledge base. Regardless of whether the file already exists, `add_docs_to_db` the function is called  to add all the document information corresponding to the file to the database. 

**Note**:
- Make sure that the incoming `session` is a valid database session instance. 
- `kb_file` The parameter must be an `KnowledgeFile` instance of type and its properties should be set correctly to reflect the actual information of the file. 
- `doc_infos` Each dictionary in a parameter must contain `id`  a `metadata` and key. 
- In practice, you may need to handle exceptions that may be thrown by database operations, such as violating uniqueness constraints.

**Example output**:
There is no direct output example for this function, as its main role is to affect the state of the database. However, after a successful execution, you can expect that the table in the database `knowledge_file` will add or update the corresponding records, and the field values of the records will reflect the parameter values provided when the function is called. 
## FunctionDef delete_file_from_db(session, kb_file)
**delete_file_from_db**: The function of this function deletes the specified knowledge file from the database and updates the file count of the related knowledge base. 

**Parameters**:
- `session`: A database session instance that is used to perform database operations.
- `kb_file`: `KnowledgeFile`An object of type that represents a knowledge file that needs to be removed from the database. 

**Code Description**:
`delete_file_from_db`The function first constructs a query condition through the input`session` and `kb_file`objects to query whether the target knowledge file exists in the`KnowledgeFileModel` table. If it exists, the function will do the following:
1. Use `session.delete(existing_file)`the method to delete found file records from the database. 
2. Call `delete_docs_from_db`the function to delete all documents and records corresponding to the knowledge file based on the name of the knowledge file and the name of the knowledge base to which it belongs. 
3. Commit a database transaction to ensure that the above delete operations are saved to the database.
4. Query `KnowledgeBaseModel`the table, find the knowledge base record to which the knowledge file belongs, subtract the `file_count`(file count) of the knowledge base by 1, and commit the database transaction again to save the changes. 

**Note**:
- Before performing a delete operation, make sure that you are passing in`session` a valid database session instance and that it has been configured correctly. 
- The deletion operation is irreversible, so before you execute this function, make sure that you really need to delete the specified knowledge file and its related documents.
- The function updates the file count of the knowledge base after the file and related documents are successfully deleted. This step is important to maintain the accuracy of the knowledge base.

**Example output**:
There is no direct output example for this function, as it primarily performs a database deletion operation. After the function is executed successfully, it is returned`True`, indicating that the knowledge file and its related documents have been successfully deleted, and the file count of the related knowledge base has been updated. If you need to verify the results of an operation, you can query the database to confirm that the specified knowledge files and documents have been deleted, and that the file count of the corresponding knowledge base has been reduced. 
## FunctionDef delete_files_from_db(session, knowledge_base_name)
**delete_files_from_db**: The function of this function is to delete all file records for a specified knowledge base from the database. 

**Parameters**:
- `session`: A database session instance that is used to perform database operations.
- `knowledge_base_name`: String type, specifying the name of the knowledge base where you want to delete the file.

**Code Description**:
`delete_files_from_db` The function first queries `KnowledgeFileModel` the table and deletes all file records that match the specified knowledge base name. The function then queries `FileDocModel` the table and also deletes all the documents that match the specified knowledge base name. Both operations use `ilike` the case insensitive matching method to ensure that all related records are matched. After that, the function queries `KnowledgeBaseModel` the table, finds the corresponding knowledge base instance, and if it does, sets the file count of the knowledge base to 0, indicating that the knowledge base no longer contains any files. Finally, the function commits all changes to the database and returns `True`, indicating that the operation completed successfully. 

**Note**:
- Before calling this function, make sure that the incoming  is `session` a valid database session instance and that it has been configured correctly. 
- This function will permanently delete all file records in the specified knowledge base, which is irreversible and should be used with caution.
- When a file record is deleted, the file count of the associated knowledge base is reset to 0, which means that the knowledge base will no longer contain any files.

**Example output**:
Because the return value of this function is a Boolean type, it returns after a successful delete operation `True`. For example:
```
操作成功完成后返回值: True
```
## FunctionDef file_exists_in_db(session, kb_file)
**file_exists_in_db**: This function is used to check if the specified file already exists in the database. 

**Parameters**:
- `session`: A database session instance that is used to execute database queries.
- `kb_file`: An `KnowledgeFile` object of type that represents the knowledge base file to be examined. 

**Code Description**:
 The function checks whether the specified file already exists in the database `file_exists_in_db` by taking a database session(`session`) and an `KnowledgeFile` object(`kb_file`s) as arguments. It starts by `session.query` constructing a query using a method that is made against a `KnowledgeFileModel` table, filtering out `filter` records with file  name(s)`file_name` and knowledge base name(s`kb_name`) that match the incoming `kb_file` object. The method is used here `ilike` to make a case-insensitive match. If at least one record exists in the result of the query, i.e., the `first()` method returns a non-null value, the file is considered to exist in the database, and the function returns `True`; Otherwise, return . `False` 

**Note**:
- Ensure that the incoming `session` parameter is a valid database session instance and that the database connection is configured correctly. 
- The incoming `kb_file` object should contain valid `filename`  and attributes `kb_name` , which will be used for matching criteria in the database query. 
- This function does not make any modification operations to the database, and is only used to check the existence of files.

**Example output**:
Suppose there is already a record in the database with the file name "example.pdf" and the knowledge base name "DefaultKB", and when an object is passed in `kb_file` with  a property `filename` value of "example.pdf" and a `kb_name` property value of "DefaultKB", the function will return  .`True` If there are no records in the database that meet the criteria, the function will return `False` . 
## FunctionDef get_file_detail(session, kb_name, filename)
**get_file_detail**: This function is used to get the details of a specific file in the specified knowledge base. 

**Parameters**:
- `session`: A database session instance that is used to execute database queries.
- `kb_name`: String type, specifying the name of the knowledge base to be queried.
- `filename`: String type, specifying the name of the file to be queried.

**Code Description**:
`get_file_detail`First, the function `session`uses the query interface of SQLAlchemy to query the model based on`kb_name` (knowledge base name) and `filename`(file name) as filter conditions`KnowledgeFileModel` through the input parameters. The query condition uses `ilike`methods, which means that the query is case-insensitive, which improves the flexibility of the query. If the specified file is queried, the function extracts the details of the file from the query results and returns them in dictionary form. This information includes the knowledge base name, file name, file extension, file version, document loader name, text splitter name, creation time, last modified time of the file, file size, whether it is a custom document, number of documents, etc. If no file is queried, the function will return an empty dictionary. 

**Note**:
- When using this function, you need to make sure that you are passing in`session` a valid database session instance. 
- The sum of `kb_name`query conditions `filename`is case-insensitive, which means that the results can be queried correctly regardless of whether they are passed in uppercase or lowercase. 
- The returned dictionary contains several properties of the file whose values are derived directly from the records in the database, so you should be mindful of their data type and meaning when using these values.

**Example output**:
```json
{
  "kb_name": "SampleKB",
  "file_name": "example.pdf",
  "file_ext": ".pdf",
  "file_version": 1,
  "document_loader": "PDFLoader",
  "text_splitter": "SpacyTextSplitter",
  "create_time": "2023-04-01 12:00:00",
  "file_mtime": 1617184000,
  "file_size": 1024,
  "custom_docs": false,
  "docs_count": 10
}
```
This example shows a dictionary of information returned by a function when a file is queried`get_file_detail`. It contains information such as the name of the knowledge base, file name, file extension, file version, document loader name, text splitter name, file creation time, last modified time, file size, whether it is a custom document, and the number of documents. 
