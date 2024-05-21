## FunctionDef get_messages_history(history_len, content_in_expander)
**get_messages_history**: The function of this function is to get the message history. 

**Parameters**:
- `history_len`: Specifies the length of the message history to fetch.
- `content_in_expander`: A boolean value that controls whether or not to return the contents of the expander element, defaulting to False.

**Code Description**:
`get_messages_history`The function is used to filter and return message history for a specified length from the chat box. It accepts two parameters:`history_len` and`content_in_expander`. `history_len`The parameter specifies the number of historical messages that need to be fetched, and the `content_in_expander`parameter controls whether or not to include the content in the expander element. This feature is especially useful when exporting message history, as the user can choose whether or not they want additional information from the expander. 

Inside the function, an `filter`internal function called an internal function is defined to filter the content that meets the criteria in each message. It first filters out the content in the message element with the output method of "markdown" or "text", and then`content_in_expander` decides whether to include the content in the expander based on the value of the parameter. Finally, the filtered content is concatenated into a string and returned as the content of the message. 

`get_messages_history`Functions return a filtered message history by calling`chat_box.filter_history` a method and passing in`history_len` and `filter`functions as parameters. Each record contains the role (sender) and content of the message. 

In a project, this function is `dialogue_page`called by a function to get a record of historical conversations when the user interacts with the system. This allows the system to provide more personalized and contextual responses based on past exchanges. 

**Note**:
- When `content_in_expander`set to True, the returned message history will contain the contents of the expander element, which may increase the size of the returned data. 
- This function relies on`chat_box` the object's `filter_history`method, so you need to make sure that `chat_box`the object is properly initialized and contains valid message history data. 

**Example output**:
```python
[
    {
        "role": "user",
        "content": "Hello, I would like to know more about AI."
    },
    {
        "role": "ai",
        "content": "Of course, AI is short for artificial intelligence, and it can perform many complex tasks."
    }
]
```
This example shows a possible output with two message records, one from the user and one from the AI, each containing the sender's role and message content.
### FunctionDef filter(msg)
**filter**: The function of this function is to filter and organize the message content. 

**Parameters**:
- msg: A dictionary containing message elements, where "elements" is a list, and each element in the list is an object that contains information such as the content of the message and how it is output.

**Code Description**:
This function first iterates through`msg["elements"]` the list to filter out `_output_method`the elements in which the property value is "markdown" or "text". This step ensures that only message content output in Markdown or plain text is selected. Then, if`content_in_expander` the variable does not exist or its value is`False` (the definition not shown in the code here`content_in_expander`, it may be an external variable or defined above), the message content is further filtered out for content that is not in the expander. Finally, the contents of the filtered elements (`x.content`) are extracted to form a new list. 

The function returns a dictionary containing two key-value pairs:
- "role": Directly `msg`obtains its "role" value from the entered dictionary, which indicates the role of the message. 
- "content": concatenate the elements in the content list with two line breaks`\n\n` to represent the final message content. 

**Note**:
- Make sure that the dictionary you enter `msg`contains the "elements" key, and that its value is a list of elements and attributes in the list`_output_method``content`. 
- This function does not handle `content_in_expander`cases where a variable may not be defined, and you need to use it to ensure that the variable is clearly defined and valued in context. 
- The processing logic of the function depends on the properties of the message element, ensuring that the message element object has`_output_method` and`_in_expander` `content`properties. 

**Example output**:
Let's say the dictionary you enter looks`msg` like this:
```python
{
    "role": "user",
    "elements": [
        {"_output_method": "markdown", "content": "Hello, world!", "_in_expander": False},
        {"_output_method": "text", "content": "How are you?", "_in_expander": True}
    ]
}
```
The return value of the function might be:
```python
{
    "role": "user",
    "content": "Hello, world!"
}
```
This means that only messages that are not in the collapsed area and whose output is markdown or text are sorted out and returned are filtered.
***
## FunctionDef upload_temp_docs(files, _api)
**upload_temp_docs**: This function is used to upload files to a temporary directory, is used for file conversations, and returns a temporary vector library ID. 

**Parameters**:
- `files`: A list of files that need to be uploaded.
- `_api`: An instance of the ApiRequest class that performs an interaction with an API server.

**Code Description**:
`upload_temp_docs` The function receives a list of files and an instance of the ApiRequest class as arguments. It `_api` `upload_temp_docs` uploads files to the server's temporary directory by calling the instance's method and is used for subsequent file dialog processing. After the upload is successful, the server will return a response with the temporary vector library ID. The function `.get("data", {}).get("id")` extracts the temporary vector library ID from the response by chaining and returns it. 

In a project,`upload_temp_docs` functions are called by `dialogue_page` functions and are used to implement file conversations. Users can upload a file and use it as part of their knowledge base, and then refer to the file content in the conversation for Q&A. This is useful in conversation scenarios where you need to reference a lot of document content. 

**Note**:
- Ensure that `_api` the parameter is a valid ApiRequest instance and that the underlying URL of the API server is configured correctly. 
- The uploaded file list `files` should contain a valid file path or file object so that the function can process and upload the file correctly. 

**Example output**:
Assuming that the file is successfully uploaded, the server returns the following response:
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "id": "temp_vector_library_id_123456"
  }
}
```
The return value of the function will be a string, `"temp_vector_library_id_123456"`representing the ID of the temporary vector library. 
## FunctionDef parse_command(text, modal)
**parse_command**: This function is used to parse a custom command entered by the user and perform the corresponding action based on the command. 

**Parameters**:
- text: Text entered by the user, of type as a string.
- modal: A modal object that is used to display modal dialogs when needed.

**Code Description**:
`parse_command`Functions are primarily responsible for handling specific commands that the user enters in the dialog interface. These commands include Create New Session (`/new`), Delete Session (`/del`), Clear Session Content (`/clear`), and View Help Information (`/help`). The function first matches the command format entered by the user with a regular expression, and if the match is successful, the corresponding action is performed according to the command type. 

- `/help`The command triggers the opening of a modal dialog box that displays help information about the available commands.
- `/new`The command is used to create a new session. If the user does not specify a session name, a default name is automatically generated. If the specified session name already exists, an error message is displayed.
- `/del`The command is used to delete a specified session. If no session name is specified, the current session is deleted by default. If the last session or the specified session does not exist, an error message is displayed.
- `/clear`The command is used to clear the chat history for a specified conversation. If no session name is specified, the chat history of the current session is cleared by default.

This function is closely related to the function in the project`dialogue_page`. `dialogue_page`In a function, the user's input is first processed by `parse_command`the function to determine whether it is a custom command. If so, follow the command and re-render the page; If it's not a custom command, the user's input continues to be processed as follows the normal dialog flow. 

**Note**:
- When using this function, you need to make sure that `modal`the object is properly initialized so that modal dialogs such as help information can be displayed when needed. 
- Functions rely on global states, such as `st.session_state`to manage session information, so you should make sure that the relevant states are set correctly before calling this function. 

**Example output**:
Assuming that the user enters a `/help`command, the function will return `True`and trigger a modal dialog with help information displayed. If the user enters non-command text, such as "Hello", the function will return`False`. 
## FunctionDef dialogue_page(api, is_lite)
**dialogue_page**: This function is used to handle the logic of the conversation page, including initializing the session, processing user input, displaying the conversation history, and so on. 

**Parameters**:
- `api`: An instance of the ApiRequest class that performs an interaction with an API server.
- `is_lite`: Boolean type, default is False, indicating whether it is in lightweight mode.

**Code Description**:
`dialogue_page`Functions are at the heart of the dialog system and are responsible for handling the user's interaction with the system. The function first initializes the session state, including the session ID and file chat ID. Then, depending on whether it's the first visit or not, the welcome message is displayed and the chat box is initialized. Next, the function handles the help information of the custom command, and provides configuration options such as dialog mode, LLM model selection, and Prompt template selection in the sidebar. 

Functions also contain logic for processing different dialog modes (e.g., LLM conversations, knowledge base Q&A, file conversations, etc.), as well as user input. The text entered by the user is first checked whether it is a custom command, and if so, the corresponding command is executed; If not, the corresponding API is called according to the current dialog mode for processing, and the reply is displayed.

In addition, functions handle functions such as displaying conversation history, collecting feedback, and exporting conversation records. After all the logic has been processed, the function triggers a re-rendering of the page if needed.

**Note**:
- Make sure that the parameters you pass in `api`are valid ApiRequest instances and that the address of the API server is correctly configured. 
- Functions depend on multiple global variables and functions, such as`chat_box` , , etc., `get_messages_history`and you need to make sure that these dependencies `dialogue_page`are properly initialized before being called. 
- The implementation of UI elements such as modal dialogs, sidebar configurations, and dialog history display in functions relies on the Streamlit library to ensure that the Streamlit environment is properly set up when using this function.

**Example output**:
Since `dialogue_page`functions are primarily responsible for handling the page logic and interacting directly with the user, rather than returning data directly, there is no specific example of a return value. The result of the function execution is to display the dialog interface on the web UI, process user input, and display corresponding replies or execute corresponding commands according to different dialog modes and user actions. 
### FunctionDef on_feedback(feedback, message_id, history_index)
**on_feedback**: This function is used to process feedback from the user. 

**Parameters**:
- `feedback`: The content of user feedback is a dictionary that contains at least`text` a key that indicates the reason for the feedback. 
- `message_id`: String type, default is an empty string, specifying the ID of the message to be fed back.
- `history_index`: Integer, which is -1 by default, indicates the index position in the chat history.

**Code Description**:
`on_feedback`Functions are primarily responsible for handling user feedback on chat conversations. It first`feedback` extracts the user's feedback reasons from the parameters and stores them in variables`reason`. Then, a `chat_box.set_feedback`method is called, passing the user's feedback content and historical index as parameters, and this method returns an integer`score_int` that represents the rating of the feedback. Next, the function uses`api.chat_feedback` the method`message_id` to submit ,`score_int` (score), and `reason`(feedback reason) as parameters to the server. In this process, the `api.chat_feedback`method is used to send a POST request to the server to submit feedback from the user, including the message ID, rating, and reason for the rating. Finally, the function is set`st.session_state["need_rerun"]` to `True`notify the system that it needs to be re-run in order to update the user interface or perform other necessary update operations. 

**Note**:
- Make sure that `feedback`the parameters include a valid reason for feedback. 
- `message_id``history_index`Although there are default values for the and parameters, specific values should be provided as needed in actual use to ensure that feedback can be accurately associated with a specific message. 
- The execution of this function triggers an interaction with the server, so you need to pay attention to the network state and the server response.
- It is`st.session_state["need_rerun"]` set `True`to ensure that the user interface is updated with the latest feedback, and developers should take this into account when using this function. 
***
### FunctionDef on_mode_change
**on_mode_change**: This function is used to handle the response logic when the dialog mode changes. 

****Arguments: This function does not accept any arguments. 

**Code Description**: `on_mode_change` The function first `st.session_state` gets the current dialog mode () from and `dialogue_mode`generates a prompt based on this pattern. If the current mode is Knowledge Base Q&A, the function further checks that the knowledge base () has been selected`selected_kb`. If a knowledge base is selected, the prompt contains the name of the currently selected knowledge base. Finally, use the `st.toast` method to display this tooltip. 

Specifically, the steps to execute the function are as follows:
1. The  value of is `st.session_state` obtained from  , `dialogue_mode` which represents the current conversation pattern. 
2. Based on the acquired pattern, a basic prompt is generated in the format "Switched to {mode} mode.".
3. If the current mode is Knowledge Base Q&A, try to `st.session_state` get `selected_kb` the value from , which is the currently selected knowledge base. 
4. If there is a selected knowledge base, the tooltip will append "Current knowledge base:`{cur_kb}`." to inform the user of the knowledge base they are currently using. 
5. Use `st.toast` the method to display the final tool. 

**Note**: 
- This function relies on  to `st.session_state` get the current conversation mode and the selected knowledge base, so make sure that `dialogue_mode`  and `selected_kb`(if in knowledge base Q&A mode) are set correctly before calling this function. 
- `st.toast` The method is used to display a temporary message on the interface, which means that the prompt message will disappear automatically after a short period of time and will not interfere with the normal operation of the user.
***
### FunctionDef on_llm_change
**on_llm_change**: This function is used to handle Language model change events. 

****Arguments: This function does not accept any arguments. 

**Code description**: When a large language model (LLM) changes, the `on_llm_change`function first checks whether the currently selected model (`llm_model`) exists. If it exists, it `api.get_model_config(llm_model)`obtains the configuration information for that model through a call. The function here`api.get_model_config` is `webui_pages/utils.py/ApiRequest/get_model_config`called from it, and its main function is to get the configuration information of the specified model on the server. 

If the field does not exist in the obtained model configuration information`"online_api"`, that is, only the local `model_worker`model can be switched, the function will save the current model name`llm_model` to `st.session_state["prev_llm_model"]`the previous model. Regardless of whether the model can be switched or not, the currently selected model name will be saved to`st.session_state["cur_llm_model"]` the system, which ensures that the user's most recent selection is recorded. 

**Note**:
- This function relies on `st.session_state`storing and tracking the changed state of the Language model, so you need to make sure that it is properly initialized before calling this function`st.session_state`. 
- The execution of a function depends on the response of an external API, so network conditions and server status may affect the execution result of a function.
- Since there is no direct error-handling logic inside the function, if the `api.get_model_config`call fails or the configuration information returned does not meet expectations, it may be necessary to handle the error in the upper logic of the invocation of the function. 
***
### FunctionDef llm_model_format_func(x)
**llm_model_format_func**: The function of this function is to format the model name and add a "(Running)" tag after the model name if the model is running. 

**Parameters**:
- **x**: String type, representing the name of the model. 

**Code Description**:
`llm_model_format_func` The function receives a parameter `x`, which is a string that represents the name of the model. The function first checks if the name exists in the `running_models` list, which contains the name of the model that is currently running. If `x` Exists `running_models` in , the function returns the model name with a string appended to "(Running)" to indicate that the model is currently running. If `x` not in `running_models` the list, the function returns the model name passed in directly. 

**Note**:
- Make sure that the`running_models` list has been properly initialized and contains all currently running model names before calling this function. 
- The return value of this function depends on `running_models` the current state of the list, so make sure the `running_models` list is up-to-date before using this function to format the model name. 

**Example output**:
- Assuming `running_models` that contains  "Model_A", the call `llm_model_format_func("Model_A")` will return "Model_A (Running)". 
- If  it `running_models` doesn't contain Model_B, the call `llm_model_format_func("Model_B")` will return Model_B. 
***
### FunctionDef prompt_change
**prompt_change**: The function of this function is to display a prompt message informing the user that the specified template has been successfully switched. 

****Arguments: This function has no arguments. 

**Code Description**:  The `prompt_change` function first defines a text variable `text`that contains a formatted message indicating the name of the template to which it has been switched. This uses a variable that is not defined directly in the code snippet`prompt_template_name`, which should be defined before the function call and contains the name of the template. Next, the function uses `st.toast` the method to display a brief notification with the content of a `text` message in a variable. `st.toast` The method is a way to display temporary messages on the interface, and is often used to feedback the results of the operation to the user. 

**Note**: Before using `prompt_change` functions, make sure that the variables `prompt_template_name` are properly defined and contain a valid template name. In addition, this function relies on `st.toast` methods, which are part of the Streamlit library, so make sure that Streamlit is installed and imported correctly in your project. This function is suitable for scenarios where you need to provide feedback to the user on the result of the template switching operation. 
***
### FunctionDef on_kb_change
**on_kb_change**: The function of this function is to display a notification when the knowledge base changes. 

****Arguments: This function does not accept any arguments. 

**Code Description**: `on_kb_change` A function is a function with no arguments that is used to display a temporary notification on the user interface. This function is triggered when the Knowledge Base (KB) changes. It uses `st.toast` a method to display a notification that includes "Knowledge base loaded:" and the name of the currently selected knowledge base. Here `st.session_state.selected_kb` is a session state variable that stores the currently selected knowledge base name. `st.toast` The method is a simple yet effective way to provide instant feedback to the user on the user interface. 

**Note**: When using this function, you need to make sure that `st.session_state` `selected_kb` there is an item in and that its value is the name of the currently selected knowledge base. Also, considering that `st.toast` the notifications displayed are temporary, make sure this type of feedback is appropriate for your use case. If you need a more persistent way to be notified, you may want to consider other UI elements. 
***
