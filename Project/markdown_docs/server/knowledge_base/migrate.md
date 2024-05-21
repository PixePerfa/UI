## FunctionDef create_tables
**create_tables**: The function of this function is to create a database table. 

****Arguments: This function does not accept any arguments. 

**Code Description**: `create_tables` A function is a key function used during database migration to create all tables defined in the database. It does this by calling `Base.metadata.create_all` a method and using  it `engine` as a binding parameter. Here `Base` is an ORM declaration base class that stores the metadata of all models (i.e., tables), and `engine` is  the connection engine of SQLAlchemy that performs the actual operations on the database. 

In the project,`create_tables` functions are called by multiple objects, showing their importance in different scenarios:
- When initializing the database (`init_database.py`) and server startup (`startup.py`), make sure that the required table structure has been created. 
- When you reset a table(`server/knowledge_base/migrate.py/reset_tables`), delete all the tables and then call this function again to create the table for testing or resetting the database environment. 
- In various test scenarios (e.g`tests/kb_vector_db/test_faiss_kb.py/test_init`., , ,`tests/kb_vector_db/test_milvus_db.py/test_init` ), `tests/kb_vector_db/test_pg_db.py/test_init`ensure that the database table structure is set correctly before testing. 

**Note**: When using this function, you need to ensure that`Base` the sum `engine`has been initialized correctly and that all table models have been `Base`defined. In addition, calling this function will create all tables that don't exist, and if the table already exists, it won't be modified, which means it won't update or modify the existing table structure. Therefore, caution should be exercised when using it in a production environment to avoid data loss. 
## FunctionDef reset_tables
**reset_tables**: The function of this function is to reset the database table. 

****Arguments: This function does not accept any arguments. 

**Code Description**: A `reset_tables` function is an important part of the database migration process and is used to reset the database environment. It first calls `Base.metadata.drop_all` the  method to delete all existing table structures, and then `create_tables` recreates the table structure by calling the function. This process is typically used for testing or in scenarios where the database needs to be cleaned up thoroughly and the table structure restructured. 

In this function,`Base.metadata.drop_all(bind=engine)` which is responsible for deleting all tables, where `Base` is the ORM declaration base class, which stores the metadata of all models (i.e. tables), is`engine` the SQLAlchemy connection engine, which is used to perform the actual operations on the database. Immediately after that,`create_tables()` it is called to recreate all the tables defined in the database. This ensures that the database environment can be reset to a clean initial state. 

**Note**: When calling `reset_tables` the function, you need to make sure that `Base`  and `engine` have been initialized correctly and that all table models have been `Base` defined. Also, because this function deletes all existing tables and recreates them, you should be extra careful when using them in a production environment to avoid unnecessary data loss. Using this function in a test or development environment can help you quickly reset the state of the database for cleanup and rebuilding of the environment. 
## FunctionDef import_from_db(sqlite_path)
**import_from_db**: The function of this function is to import data from the backup database to the info.db. 

**Parameters**:
- `sqlite_path`: String type, specifying the path to the SQLite database. The default is None.

**Code Description**:
`import_from_db` Functions are mainly used to import data from the backed up SQLite database to the current info.db database without any change in the knowledge base and vector library. This is usually the case when the structure of the info.db changes during a version upgrade, but the data itself does not need to be re-vectorized. At the beginning of the function, the necessary modules are imported, including `sqlite3` for  manipulating the SQLite database, and `pprint` for printing data. 

Internally, the function first gets a list of database models and then tries to connect to the specified SQLite database. By querying SQLite's `sqlite_master` tables, you can get and iterate through all the table names. For the table corresponding to each model, if the table exists in the database, all the data of the table is further read. For each row of data, the function filters out the required fields based on the column names defined by the model, and specifically processes `create_time` the  fields to parse them into the correct time format. After that, use the `session_scope` Context Manager to automatically manage the database session, adding the filtered and processed data to the session and finally committing it to the database. 

If any exceptions are encountered during the data import process, the function prints an error message and returns False indicating that the import failed. Otherwise, close the database connection after all data has been successfully processed and return True indicating that the import was successful.

**Note**:
- Make sure that you are passing in `sqlite_path` the correct SQLite database file path. 
- Make sure that the table names and field names in the backup database are consistent with the current database model.
- This function currently only supports SQLite databases.
- When you use this function to import data, you should ensure that no other operations are accessing the target database to avoid data conflicts.

**Example output**:
- When data is successfully imported, the function returns `True`. 
- If the backup database cannot be read or other errors are encountered, the function returns `False`. 
## FunctionDef file_to_kbfile(kb_name, files)
**file_to_kbfile**: The function of this function is to convert a list of files into a list of KnowledgeFile objects. 

**Parameters**:
- `kb_name`: String type, which represents the name of the knowledge base.
- `files`: A list of strings containing the names of the files that need to be converted.

**Code Description**: `file_to_kbfile`The function takes a list of knowledge base names and file names as input parameters, iterates through the list of files, and creates an instance for each file`KnowledgeFile`. During instantiation`KnowledgeFile`, if any exceptions are encountered, the file is skipped and exception information is logged. The function eventually returns a `KnowledgeFile`list of objects that contain information about the file's association with the name of the knowledge base and other`KnowledgeFile` file handling capabilities provided by the class. 

**Note**:
- Before you call this function, you need to make sure that the files in the incoming file list are all present on disk.
- If the file format is not supported, or if `KnowledgeFile`there are other problems during the creation of the instance, the file will be skipped and an error message will be logged. 
- The level of detail of logging depends on the settings in the global log configuration`log_verbose`. 

**Example output**:
Assuming you have a list of files`["document1.md", "document2.txt"]` and a knowledge base name`"demo_kb"`, the call`file_to_kbfile("demo_kb", ["document1.md", "document2.txt"])` might return a `KnowledgeFile`list of objects (depending on the file content and`KnowledgeFile` the implementation of the class):
```python
[
    KnowledgeFile(filename="document1.md", knowledge_base_name="demo_kb"),
    KnowledgeFile(filename="document2.txt", knowledge_base_name="demo_kb")
]
```
Each object in this list `KnowledgeFile`represents a file associated with the knowledge base`demo_kb`, which can be further used for operations such as file processing, document loading, and text segmentation of the knowledge base. 

In a project, `file_to_kbfile`functions are used in several scenarios, including but not limited to converting files in a local folder to a knowledge base file, updating a file in a knowledge base, deleting a file from the knowledge base, and so on. For example, in a`folder2db` function, it is used to convert files in a specified folder into `KnowledgeFile`objects, which can then be used to create or update vector libraries; In a `prune_db_docs`function, it is used to identify and delete knowledge base files that no longer exist in the local folder. 
## FunctionDef folder2db(kb_names, mode, vs_type, embed_model, chunk_size, chunk_overlap, zh_title_enhance)
**folder2db**: The function of this function is to populate the database and/or vector storage with existing files in the local folder. 

**Parameters**:
- `kb_names`: A list of knowledge base names of type `List[str]`. 
- `mode`: Migration mode, the optional value is `"recreate_vs"`, `"update_in_db"`, `"increment"`and the type is `Literal["recreate_vs", "update_in_db", "increment"]` . 
- `vs_type`: Vector storage type, optional values are `"faiss"`, `"milvus"`, `"pg"`, `"chromadb"`, and the default value is `DEFAULT_VS_TYPE` , type is `Literal["faiss", "milvus", "pg", "chromadb"]` . 
- `embed_model`: Embedding model name, default value is `EMBEDDING_MODEL` , type is `str` . 
- `chunk_size`: Chunk size, default value is `CHUNK_SIZE` , type is `int` . 
- `chunk_overlap`: tile overlap size, default value is `OVERLAP_SIZE` , type is `int` . 
- `zh_title_enhance`: Whether to enhance the Chinese title, the default value is `ZH_TITLE_ENHANCE` , the type is `bool` . 

**Code Description**:
Based on the parameters provided, this function reads the file from the local folder and populates the file information into the database and/or vector store according to the specified migration pattern. Supported migration modes include:
- `recreate_vs`: Recreates all vector stores and populates the database information with existing files in the local folder.
- `update_in_db`: Updates vector storage and database information with local files that already exist in the database.
- `increment`: Creates vector storage and database information for local files that do not exist in the database.

The function first checks to see if a list of knowledge base names is provided, and if not, it calls  the function `list_kbs_from_folder` to get all knowledge base directory names. Then, according to the specified vector storage type and embedding model name, the `KBServiceFactory.get_service` corresponding knowledge base service instance is obtained through the method. Depending on the migration mode, the function performs corresponding operations, such as clearing the vector store, creating a knowledge base, updating the vector store, and so on. 

**Note**:
- Before using this function, make sure that the relevant files for the target knowledge base exist in the local folder.
- Depending on the migration mode, operations may involve rebuilding vector storage or updating database information, which may have an impact on existing data.
- Internally, a function does this by calling multiple helper functions and service instance methods, ensuring that the helper functions and methods are implemented correctly and are available.

In the project,`folder2db` functions are used to initialize the database (`init_database.py`) and test the migration feature (`tests/test_migrate.py`), including testing the recreation of the vector store (`test_recreate_vs`) and incremental update (`test_increment`). These calls show that functions`folder2db` are a key component in the knowledge base migration and management process to update or rebuild databases and vector stores based on files in local folders. 
### FunctionDef files2vs(kb_name, kb_files)
**files2vs**: The function of this function is to batch convert and add files to the vector library. 

**Parameters**:
- `kb_name`: String type, which represents the name of the knowledge base.
- `kb_files`: `KnowledgeFile`A list of objects, representing a list of files to be processed and added to the vector library. 

**Code Description**:
`files2vs`The function is mainly responsible for batching and adding a given list of files`kb_files` () to the specified knowledge base(`kb_name`). This process involves the following steps:

1. A function is called`files2docs_in_thread`, which uses multithreading to convert each file in the file list into a document list. In this process, it will be processed according to the content of the file and a series of parameters such as document tile size`chunk_size`, tile overlap size`chunk_overlap`, whether to enhance Chinese titles,`zh_title_enhance` etc. 

2. For `files2docs_in_thread`each returned result of a function, first check if the transformation was successful. If successful, the converted file name and document list are obtained. 

3. For each successfully converted file, create a new `KnowledgeFile`instance and set the file name, knowledge base name, and split document list (`splited_docs`) to this instance. 

4. invocation`KBService` to add `add_doc`the instance created in the previous step `KnowledgeFile`to the knowledge base. During this process, the vector library cache () is not flushed`not_refresh_vs_cache=True`. 

5. If the conversion fails, an error message is printed.

Through the above steps, this function implements batch conversion of file content and adds it to the vector library of the knowledge base to support the subsequent search and retrieval functions.

**Note**:
- When using `files2vs`functions, you need to make sure that the sum arguments passed in`kb_name` are `kb_files`correct and valid. `kb_files`Each `KnowledgeFile`object should be a file that can be processed correctly. 
- `files2docs_in_thread`Multithreading of functions can improve the efficiency of file conversion, but it is also necessary to pay attention to thread safety when using it.
- `add_doc`The call to the method does not flush the vector library cache, which means that after adding a large number of documents, you may need to manually flush the cache to ensure that the vector library's data is up to date.
***
## FunctionDef prune_db_docs(kb_names)
**prune_db_docs**: The function of this function is to delete documents in the database that do not exist in the local folder. 

**Parameters**:
- `kb_names`: A list of strings containing the names of the knowledge bases that need to be cleaned up.

**Code Description**:  The function `prune_db_docs`performs the following operations on each knowledge base`kb_names` by iterating through the incoming list of knowledge base names:
1. Use `KBServiceFactory.get_service_by_name` the method to obtain the corresponding knowledge base service instance based on the knowledge base name. If the instance exists, the execution continues. If it doesn't exist, the current knowledge base is skipped. 
2. Call the method of the knowledge base service instance `list_files` to get a list of files in the database. 
3. Call  the `list_files_from_folder` function to get a list of files in the local folder. 
4. Calculates a list of files that exist in the database but not in the local folder.
5. Use `file_to_kbfile` the function to convert the list of files obtained in step 4 to a `KnowledgeFile` list of objects. 
6. Traverse through `KnowledgeFile` the list of objects, call the method of the knowledge base service instance on each object `delete_doc` to delete the document in the database, and print the document information that was successfully deleted. 
7. Invoke the knowledge base service instance's `save_vector_store` method to save the state of the vector library. 

**Note**:
- Ensure that each knowledge base in the incoming list of knowledge base names `kb_names` is registered and correctly configured in the database before calling this function. 
- This function is used to synchronize the state of documents in the local folder and database, especially if you need to delete certain document files from the database after you delete them in the file browser.
- When deleting a document in the database,`delete_doc` the method's `not_refresh_vs_cache` parameter is set to  , `True`which means that the vector library cache is not refreshed immediately after the deletion operation. The state of the vector library will be saved by the method after all deletion operations are completed `save_vector_store` . 
- During function execution, information about each successfully deleted document is printed, including the knowledge base name and file name, so that the operation result can be tracked.

With the above steps,`prune_db_docs` the function can effectively delete those documents from the database that no longer exist in the local folder, thus keeping the database content accurate and up-to-date. 
## FunctionDef prune_folder_files(kb_names)
**prune_folder_files**: The function of this function is to delete document files in the local folder that do not exist in the database, which is used to free up local disk space by deleting unused document files. 

**Parameters**:
- `kb_names`: A list of strings that represents the name of the knowledge base that needs to be processed.

**Code Description**:
`prune_folder_files` The function receives a list of knowledge base names as arguments. For each knowledge base name in the list, the function first uses `KBServiceFactory.get_service_by_name` methods to try to get the corresponding knowledge base service instance. If you successfully get the service instance, proceed with the following steps:

1. Call the method of the knowledge base service instance `list_files` to get a list of files stored in the database. 
2. Use `list_files_from_folder` the function to get a list of files in your local folder. 
3. Set operations are performed to find out the files that exist in the local folder but are not in the database file list, and these files are considered unused.
4. For each unused file, use the method to `os.remove` delete the file and print a message that the deletion was successful. 

This process optimizes the use of storage resources by ensuring that local storage space is not taken up by files that no longer exist in the database.

**Note**:
- Before you call this function, you need to ensure that each name in the list of knowledge base names provided is valid and that the corresponding knowledge base service instance can be successfully obtained.
- This function depends on `KBServiceFactory.get_service_by_name`,`list_files_from_folder` , and `get_file_path` , so you need to make sure that these depend on functions work correctly. 
- Deleting a file is irreversible, so you should make sure that you have properly backed up your important data before executing this function.
- During the execution of the function, the information of each deleted file is printed, and the execution of the deletion operation can be tracked through this information.
