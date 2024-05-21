## FunctionDef list_kbs
**list_kbs**: The function of this function is to get a list of knowledge bases. 

****Arguments: This function does not accept any arguments. 

**Code Description**: `list_kbs` A function is a parameterless function that is used to get a list of knowledge bases from a database. It does this by calling `list_kbs_from_db` the function. `list_kbs_from_db` The function queries the database for a list of knowledge base names that meet certain criteria and returns those names. The function then`list_kbs` encapsulates these names in `ListResponse` an instance of the class. `ListResponse` A class is a class designed to encapsulate the data response of a list, and it inherits from  the `BaseResponse` class to provide status codes, status messages, and a list of data. This design makes the API's response format consistent and easy for front-end developers to understand and use. 

**Note**:
- `list_kbs` The function relies on  the `list_kbs_from_db` function to correctly get the list of knowledge base names from the database. Therefore, ensuring that the database connection and query logic are correct is a prerequisite for using this function. 
- The list of `ListResponse` data contained in the returned instance should correctly reflect the knowledge base in the database. This requires the `list_kbs_from_db` function to be able to execute its query logic accurately. 
- In the actual deployment and use, you should pay attention to the performance and response time of the database, especially when the number of knowledge bases is large, to ensure a good user experience.

**Example output**:
Suppose there are three knowledge bases in the database, named "Knowledge Base A", "Knowledge Base B", "Knowledge Base C", the possible examples of the function would look `ListResponse` like this:
```
{
    "code": 200,
    "msg": "success",
    "data": ["知识库A", "知识库B", "知识库C"]
}
```
This indicates that the API call was successful and a list of three knowledge base names was returned.
## FunctionDef create_kb(knowledge_base_name, vector_store_type, embed_model)
**create_kb**: This function is used to create a new knowledge base. 

**Parameters**:
- `knowledge_base_name`: The name of the knowledge base, of type String. Example parameters provide default example values.
- `vector_store_type`: Vector storage type, the type is a string, and the default value is "faiss".
- `embed_model`: The name of the embedding model, the type is a string, and the embedding model configured by the project is used by default.

**Code Description**:
This function first `validate_kb_name`verifies the legitimacy of the knowledge base name by calling the function. If the name is invalid or empty, the 403 and 404 status codes are returned`BaseResponse`, and an error message is displayed. Next, use the method to `KBServiceFactory.get_service_by_name`check whether a knowledge base with the same name exists, and if it exists, it returns an object with a 404 status code`BaseResponse` to indicate that the knowledge base already exists. If the verification is successful, the function `KBServiceFactory.get_service`obtains the corresponding knowledge base service instance through a method and calls the method of the instance `create_kb`to create a knowledge base. If an exception occurs during the creation process, an error message is recorded and a 500 status code is returned`BaseResponse`. After the knowledge base is created, the object with a status code of 200 is returned`BaseResponse`, indicating that the knowledge base has been added. 

**Note**:
- Before calling this function to create a knowledge base, you need to ensure that the knowledge base name is not empty and does not contain illegal characters to avoid security risks.
- The vector storage type and embedding model should be selected according to the project needs and configuration to ensure the correct creation of the knowledge base and the effectiveness of subsequent operations.
- When handling exceptions, attention should be paid to recording detailed error information to facilitate the location and resolution of the problem.

**Example output**:
If you successfully create a knowledge base named Technical Documentation Library, the function returns the following`BaseResponse` object:
```
{
    "code": 200,
    "msg": "已新增知识库 技术文档库"
}
```
If you try to create an existing knowledge base, for example named "Technical Library", the function will return:
```
{
    "code": 404,
    "msg": "已存在同名知识库 技术文档库"
}
```
If the knowledge base name is invalid, it returns:
```
{
    "code": 403,
    "msg": "Don't attack me"
}
```
## FunctionDef delete_kb(knowledge_base_name)
**delete_kb**: The function of this function is to delete the specified knowledge base. 

**Parameters**:
- `knowledge_base_name`: String type, which represents the name of the knowledge base to be deleted. This parameter is passed in through the request body and an example value of "samples" is provided.

**Code Description**:
`delete_kb` The function first verifies the validity of the knowledge base name. If the name is invalid, i.e. it does not pass `validate_kb_name` the validation of the function, an object with status code 403 will be returned with the `BaseResponse` message "Don't attack me", indicating that the request was rejected. Next, the function decodes the URL of the knowledge base name to ensure that the name is correct. 

Use  the method to `KBServiceFactory.get_service_by_name` obtain the corresponding knowledge base service instance based on the knowledge base name. If the instance is `None` , i.e., the knowledge base does not exist, an object with status code 404 will be returned with the `BaseResponse` message "Knowledge base not found {knowledge_base_name}". 

If the knowledge base service instance is successfully obtained, the function tries to call the method of the knowledge base service instance `clear_vs` to clear the vector data in the knowledge base, and then calls  the method to `drop_kb` delete the knowledge base. If the deletion operation is successful, an object with status code 200 will be returned with the `BaseResponse` message "Successfully deleted knowledge base {knowledge_base_name}". 

If an exception occurs during the deletion process, the exception is caught, an error log is recorded, and an object with status code 500 is returned with the `BaseResponse` message "An accident occurred while deleting the knowledge base: {e}", where `{e}` is the  exception information. 

**Note**:
- Before calling this function, make sure that the incoming knowledge base name is URL-encoded.
- This function relies on `validate_kb_name` the function to verify the legitimacy of the knowledge base name to prevent potential security risks. 
- Deleting a knowledge base is an irreversible operation, and once executed, all data in the knowledge base will be permanently deleted.

**Example output**:
If you try to delete a non-existent knowledge base "unknown_kb", the following object might be returned by the function `BaseResponse` :
```
{
    "code": 404,
    "msg": "未找到知识库 unknown_kb"
}
```
If the knowledge base named "samples" is successfully deleted, the following possible objects may be returned by the function `BaseResponse` :
```
{
    "code": 200,
    "msg": "成功删除知识库 samples"
}
```
