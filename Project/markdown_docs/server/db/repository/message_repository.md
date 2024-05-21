## FunctionDef add_message_to_db(session, conversation_id, chat_type, query, response, message_id, metadata)
**add_message_to_db**: The function of this function is to add a new chat to the database. 

**Parameters**:
- `session`: A database session instance that is used to perform database operations.
- `conversation_id`: A string type that represents a unique identifier for a conversation.
- `chat_type`: The type of chat, such as normal chat, customer service chat, etc.
- `query`: A question or input from a user.
- `response`: The answer of the system or model, which is an empty string by default.
- `message_id`: The unique identification ID of the chat log, which is automatically generated if not provided.
- `metadata`: A dictionary type used to store additional information, which defaults to an empty dictionary.

**Code Description**:
This function first checks if it is provided`message_id`, and if not, then uses `uuid.uuid4().hex`to generate a unique ID. Next, create an `MessageModel`instance that contains all the relevant information about the chat history, such as the type of chat, user question, model answers, session ID, and metadata. This instance is then added to the database using the provided database session (`session`) and the changes are committed. Finally, the function returns the ID of the newly added chat history. 

**Note**:
- When you call this function, make sure that you are passing in`session` a valid instance of the database session. 
- `metadata`The parameters should be dictionary type and can contain data of any structure, but care should be taken to maintain the consistency of the data structure for subsequent processing.
- The auto-generated ones `message_id`are UUID-based, ensuring the uniqueness of each chat history. 
- When a function is successfully executed, a database transaction is committed, so you should make sure that other related database operations have been executed correctly before calling this function to avoid transaction conflicts.

**Example output**:
The calling `add_message_to_db`function may return the following chat history ID:
```
'4f5e8a7b9d314f5a8e7b9d2f4b8a9e2f'
```

The use cases of this function in projects include, but are not limited to, recording chats when users interact with the system, and recording and backtracking chat history in automated tests or data analysis. By persisting chat logs, projects can provide a richer user experience and deeper data insights.
## FunctionDef update_message(session, message_id, response, metadata)
**update_message**: The function of this function is to update existing chats. 

**Parameters**:
- `session`: A database session instance that is used to perform database operations.
- `message_id`: The unique ID of the chat history that you want to update.
- `response`: (Optional) New reply content, string type.
- `metadata`: (Optional) New metadata, dictionary type.

**Code Description**:
`update_message`The function first invokes the`get_message_by_id` corresponding chat history based on the `message_id`query. If a corresponding record is found, the function will update the reply content () and metadata () of the chat record based on the parameters passed in`response``metadata`. If the `response`parameter is not empty, the reply content of the record is updated. If `metadata`the parameter is a dictionary type, the metadata of the record is updated. Once the update is complete, the record is added to the database session and the changes are committed. If the update is successful, the function returns the ID of the update record. 

**Note**:
- Ensure that you are passing in `session`a valid database session instance and that it has been properly configured to connect to the target database. 
- `message_id`Make sure that the ID is valid and exists in the database so that you can find the corresponding chat history and update it.
- When updating metadata(`metadata`), the argument passed in must be of dictionary type, otherwise it will not be updated. 
- After the function is successfully executed, the ID of the update record is returned. If the chat history is not found, the update will not be performed and the ID will not be returned.

**Example output**:
Suppose there is a `123`chat history with a message ID and `update_message(session, '123', response='新的回复内容', metadata={'key': 'value'})`if the update is successful, the function will return it after the call`123`. This means that `123`the reply content and metadata of the chat history with the ID have been successfully updated. 

In the project, a `update_message`function is called by `on_llm_end`a method that updates the content of the reply to the chat history after the language model has finished processing. This shows `update_message`an important use case in the real-world scenario, which is to update the chat history in the database in a timely manner to keep the data up-to-date after a new reply or message is obtained. 
## FunctionDef get_message_by_id(session, message_id)
**get_message_by_id**: The function of this function is to query the chat history based on the message ID. 

**Parameters**:
- `session`: A database session instance that is used to execute database queries.
- `message_id`: The unique identifier ID of the chat history you want to query.

**Code Description**:
`get_message_by_id`The function uses a database session (`session`) and a message ID(`message_id`) as parameters to query `MessageModel`the records in the model. It first constructs a query that `filter_by`specifies the message ID as a filter criterion by a method, and then calls `first()`the method to try to get the first matching record. If there is a record that meets the criteria, the record will be returned; Otherwise, return`None`. This process allows the caller to quickly retrieve the chat history based on a specific message ID. 

**Note**:
- Ensure that you are passing in `session`a valid database session instance that is properly configured to connect to the target database. 
- `message_id`You should ensure that it is a valid ID and that it exists in the database so that the query can successfully return results.
- This function returns an `MessageModel`instance, or if no matching record is found`None`. Therefore, you should check the return value after calling this function to determine if the record was successfully retrieved. 

**Example output**:
For example, if there is a chat record with a message ID in the database`123`, the call `get_message_by_id(session, '123')`may return the following`MessageModel` instance:
```
<message(id='123', conversation_id='456', chat_type='普通聊天', query='用户的问题', response='模型的回答', meta_data='{}', feedback_score=80, feedback_reason='详细的反馈理由', create_time='2023-04-01 12:00:00')>
```
If the specified `message_id`does not exist in the database, the function will return`None`. 
## FunctionDef feedback_message_to_db(session, message_id, feedback_score, feedback_reason)
**feedback_message_to_db**: The function of this function is to update the user feedback information of the chat history. 

**Parameters**:
- `session`: A database session instance that is used to perform database operations.
- `message_id`: The unique identifier ID of the chat history, which is used to locate the chat history for which feedback needs to be updated.
- `feedback_score`: The user's rating of the chat answer out of 100.
- `feedback_reason`: Reason for user rating.

**Code Description**:
`feedback_message_to_db`The function first queries `session.query(MessageModel).filter_by(id=message_id).first()`the instance of the chat history with the specified ID. If the record exists, the function updates the sum field of the record`feedback_score` `feedback_reason`to the parameter value passed in. After that, `session.commit()`make the changes to the database by committing. If the update is successful, the function returns the ID of the update record. 

This function is one of the core features related to user feedback, which allows users to rate and give feedback on chat history, which can then be used to improve the quality of answers in the chat system or perform other relevant analysis.

**Note**:
- Before calling this function, make sure that `session`it is properly initialized and that database operations are available. 
- The incoming `message_id`should ensure that it exists in the database, otherwise the update operation will not be possible. 
- `feedback_score`It should be between 0 and 100, representing the percentage of user satisfaction.
- In practice, it may be necessary to `feedback_reason`validate the length or content of the user's feedback justification to avoid storing invalid or inappropriate information. 

**Example output**:
If the update operation is successful, the function will return the ID of the chat record, for example:
```
'1234567890abcdef1234567890abcdef'
```
This ID can be used for follow-up actions or logging so that the results of the feedback action can be tracked.
## FunctionDef filter_message(session, conversation_id, limit)
**filter_message**: The function of this function is to filter the chat history based on the dialog ID and return the last few records. 

**Parameters**:
- `session`: A database session instance that is used to execute database queries.
- `conversation_id`: String type, specifying the ID of the dialog to be queried.
- `limit`: Integer, optional, default value of 10, specifies the maximum number of records to be returned.

**Code Description**:
`filter_message`First, the function `session`uses the query interface of SQLAlchemy to`conversation_id` filter out `MessageModel`the chat records that match the specified dialog ID from the model through the input sum parameters. During the query, it also applies two filter criteria:
1. Ignore records with empty responses, i.e., select only those chat records that the system or model has already answered.
2. Sorts the results in descending order by creation time, and`limit` limits the number of records returned by parameters. 

Once the query is complete, the function does not directly return`MessageModel` a list of objects, but instead builds a new list`data` in which each element is a dictionary`query` containing `response`and two key-value pairs, corresponding to the user query and the system answer for each record. 

**Note**:
- When using this function, you need to make sure that you are passing`session` in a valid database session instance and that the`conversation_id` parameters are in the correct dialog ID format. 
- The data structure returned by the function is to simplify the content of the record, and only contains the query and answer information, if you need more chat history information, you may need to modify the function accordingly.

**Example output**:
The calling `filter_message`function may return a list of data in the following format:
```
[
    {"query": "用户的问题1", "response": "系统的回答1"},
    {"query": "用户的问题2", "response": "系统的回答2"},
    ...
]
```
This list contains the largest number `limit`of records, each of which is a dictionary of user queries and system answers. 
