## FunctionDef list_summary_from_db(session, kb_name, metadata)
**list_summary_from_db**: This function lists the chunk summary information in a knowledge base. 

**Parameters**:
- `session`: A database session instance that is used to execute database queries.
- `kb_name`: String type, specifying the name of the knowledge base to be queried.
- `metadata`: Dictionary type, which defaults to an empty dictionary and is used to filter summaries with specific metadata.

**Code Description**:
`list_summary_from_db` A function queries summary information in a particular knowledge base by receiving a database session, a knowledge base name, and an optional metadata dictionary as parameters. First, the function uses the incoming knowledge base name to filter the `SummaryChunkModel`model to get all the summary information under the knowledge base. If a metadata dictionary is provided, the function will further filter this summary information based on the key-value pairs of the metadata. Eventually, the function formats the query results into a list, each element is a dictionary containing the id, summary_context, summary_id, doc_ids, and metadata of the summary, and then returns the list. 

**Note**:
- When using `list_summary_from_db`functions, make sure that you are passing in`session` a valid database session instance. 
- `kb_name`The parameter should ensure that it matches the name of the knowledge base stored in the database, and the parameter supports case-insensitive matching.
- `metadata`When using parameters for a filtered query, ensure that the keys and values in the dictionary`SummaryChunkModel` `meta_data`match the key-value pairs stored in the fields in . 

**Example output**:
The calling `list_summary_from_db`function might return a list in the following format:
```
[
    {
        "id": "1",
        "summary_context": "这是一个关于AI技术的摘要",
        "summary_id": "summary123",
        "doc_ids": "['doc1', 'doc2']",
        "metadata": {}
    },
    {
        "id": "2",
        "summary_context": "这是第二个摘要的示例文本",
        "summary_id": "summary456",
        "doc_ids": "['doc3', 'doc4']",
        "metadata": {"page": "1-2"}
    }
]
```
This example shows information about two summaries, each containing the id, the content of the summary (summary_context), the digest ID (summary_id), a list of associated document IDs (doc_ids), and additional metadata.
## FunctionDef delete_summary_from_db(session, kb_name)
**delete_summary_from_db**: This function deletes the chunk summary of the specified knowledge base and returns the deleted chunk summary information. 

**Parameters**:
- `session`: A database session instance that is used to perform database operations.
- `kb_name`: String type, specifying the name of the knowledge base from which you want to delete the summary.

**Code Description**:
`delete_summary_from_db` The function first calls `list_summary_from_db` the function to `kb_name` list all chunk summary information in the knowledge base based on the name of the knowledge base. Next, the function constructs a query that `session.query` uses methods  and `SummaryChunkModel` models  to `filter` filter the knowledge base names to match the case insensitive knowledge base names. Then, use the `query.delete` method to delete all the records that match, and `session.commit` commit the changes to the database via the method. Finally, the function returns `list_summary_from_db` a list of deleted chunk summary information that was previously obtained through the function. 

**Note**:
- Before calling this function, make sure that you are passing `session` in a valid database session instance and that it has been configured correctly. 
- `kb_name` The parameter should match the name of the knowledge base stored in the database, and it supports case-insensitive matches to ensure that the target knowledge base is found correctly.
- Functions commit changes as soon as they delete them, so use them sparingly to avoid accidentally deleting important data.

**Example output**:
Calling  the `delete_summary_from_db` function might return a list in the following format:
```
[
    {
        "id": "1",
        "summary_context": "这是一个关于AI技术的摘要",
        "doc_ids": "['doc1', 'doc2']"
    },
    {
        "id": "2",
        "summary_context": "这是第二个摘要的示例文本",
        "doc_ids": "['doc3', 'doc4']"
    }
]
```
This example shows the information of two deleted summaries, each containing the ID, the content of the summary (summary_context), and the associated document ID list (doc_ids).
## FunctionDef add_summary_to_db(session, kb_name, summary_infos)
**add_summary_to_db**: The function of this function is to add summary information to the database. 

**Parameters**:
- `session`: A database session instance that is used to perform database operations.
- `kb_name`: String type, specifying the name of the knowledge base to which you want to add summary information.
- `summary_infos`: A list of dictionaries, each containing a summary information, including summary text, document identifiers, and other information.

**Code Description**:
`add_summary_to_db` The function receives a database session, a knowledge base name, and a list of summarized information. Each summary message is a dictionary containing the summary text (`summary_context`), the summary ID (),`summary_id` the document ID list (`doc_ids`), and additional metadata (`metadata`). The function iterates through the list, creates an instance for each summary message`SummaryChunkModel`, and adds it to the database session. When all the summary information is added, the function commits the session to save the changes and returns`True` a statement that the operation was successful. 

In this process, `SummaryChunkModel`the model used to map the summary information table in the database defines how to store information such as knowledge base name, summary text, summary ID, document ID list, and metadata. 

**Note**:
- Make sure that you are passing `session`in a valid instance of the database session and that it is properly configured before calling this function. 
- `summary_infos`Each dictionary in the list must contain`summary_context` ,`summary_id` , `doc_ids`and `metadata`keys. 
- `metadata`Fields should be passed in the correct JSON format to avoid errors when serializing or deserializing.
- After the function is executed, you need to check the return value to ensure that the summary information has been successfully added to the database.

**Example output**:
Instead `add_summary_to_db`of returning a specific instance of the data, the calling function typically returns a Boolean value`True` indicating that all summary information has been successfully added to the database. 
## FunctionDef count_summary_from_db(session, kb_name)
**count_summary_from_db**: The function of this function is to count the number of summary information under the specified knowledge base name. 

**Parameters**:
- `session`: A database session instance that is used to execute database queries.
- `kb_name`: String type, specifying the name of the knowledge base for which you want to query for the number of summaries.

**Code Description**:
`count_summary_from_db` The function takes a database session instance and a knowledge base name as parameters, and uses this session instance to query `SummaryChunkModel` the table for the number of summary information that matches the given knowledge base name. During the query, the method is used `ilike` to achieve case-insensitive matching, which means that the corresponding record is correctly matched regardless of the case of the incoming knowledge base name. This function returns an integer that represents the number of summary information matched. 

In the hierarchy of a project,`count_summary_from_db` functions belong to `knowledge_metadata_repository.py` files, which serve as part of the database repository layer and are primarily responsible for handling data operations related to knowledge base metadata. `count_summary_from_db` Functions `SummaryChunkModel`  interact directly with the classes `knowledge_metadata_model.py` defined in `SummaryChunkModel` the associated with the  query. `SummaryChunkModel` A class defines the data model for summary information, including fields such as knowledge base name, summary text, and more, and is a mapping of the table structure in which the summary information is stored in the database. 

**Note**:
- When calling this function, make sure that the argument passed in `session` is a valid instance of the database session and `kb_name` that the argument is a non-empty string. 
- Because  of `ilike` the fuzzy matching method used, the performance impact should be considered when calling this function, especially when dealing with large amounts of data. 

**Example output**:
Suppose there are 3 pieces of summary information in the database that belong to the Technical Documentation knowledge base, and calling `count_summary_from_db(session, "技术文档")` will  return an integer`3`. 
