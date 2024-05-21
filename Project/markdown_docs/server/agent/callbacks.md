## FunctionDef dumps(obj)
**dumps**: The function of this function is to convert a dictionary object to a string in JSON format. 

**Parameters**:
- obj: A dictionary object that needs to be converted to a JSON string.

**Code Description**:
`dumps`A function is a simple but very core feature that takes a dictionary object as an input parameter and uses`json.dumps` methods to convert that dictionary into a string in JSON format. During the conversion process, `ensure_ascii=False`the parameters ensure that non-ASCII characters in the string are not escaped, maintaining the readability and integrity of the original data. 

In a project, `dumps`functions are called by methods in multiple asynchronous callback handlers, including`on_tool_start` ,`on_tool_end` ,`on_tool_error``on_llm_new_token``on_llm_start``on_chat_model_start``on_llm_end``on_llm_error``on_agent_finish`。 These methods typically require serializing the current tool's state or other relevant information into a JSON string when processing certain events (e.g., tool start, end, error, etc.) and queue it for further processing. Through the use`dumps` of functions, the format and accuracy of this information during the serialization process are ensured. 

**Note**:
- When using `dumps`functions, you need to make sure that the object you pass in is a dictionary type, because`json.dumps` methods can only process dictionary type data. 
- Considering `ensure_ascii=False`the use of parameters, make sure that non-ASCII characters are supported in environments that handle JSON strings. 

**Example output**:
Suppose you have a dictionary object`{"name": "test tool", "status": "running"}`, and the `dumps`output after processing with a function is an example:
```json
{"name": "Test Tool", "status": "Running"}
```
This output is a standard JSON string that can be further used for network transmission, storage, or other scenarios that require JSON format data.
## ClassDef Status
**The Status**: Status class is used to define constants for different states. 

**Properties**:
- `start`: Indicates the start state.
- `running`: indicates the running status.
- `complete`: Indicates the completion status.
- `agent_action`: indicates the status of the agent's execution.
- `agent_finish`: Indicates the agent completion status.
- `error`: indicates the error status.
- `tool_finish`: Indicates the completion status of the tool execution.

**Code Description**:
The Status class plays an important role in a project by defining a series of integer constants to represent different states, which are widely used in asynchronous callback processing to track and manage the execution of asynchronous tasks. For example, when handling events such as tool start, end, error, etc., the state of the current tool is updated based on different event types. These states not only help developers understand the current stage of the task, but also provide clear instructions for what to do if an error is made or a task is completed. 

In a project, the status value of the Status class is used to identify the different phases of an asynchronous operation, such as when the tool starts execution, `agent_action` when the tool ends,  when an `tool_finish`error is encountered, `error` and so on. These state values `CustomAsyncIteratorCallbackHandler` are referenced in various methods of the class to make it easier to manage and respond to different events during asynchronous operations. 

For example, in the `on_tool_start` method, use `Status.agent_action` to mark the state of the current tool as the state of the agent execution action; In the `on_tool_end` method, use `Status.tool_finish` to update the tool state to the Execution Complete state; In the `on_tool_error` method, use `Status.error` to mark the error state. This state management mechanism makes the management of asynchronous operations clearer and more orderly. 

**Note**:
- When using the Status class, developers need to make sure that the corresponding state constants are correctly referenced so that the state of asynchronous operations can be accurately tracked and managed.
- The update of the state value should match the actual asynchronous operation process to avoid logical errors caused by state inconsistencies.
- When dealing with asynchronous operations, you should decide the next operation based on the state value, such as whether to continue execution, whether to handle errors, etc., to ensure the robustness of the program.
## ClassDef CustomAsyncIteratorCallbackHandler
**CustomAsyncIteratorCallbackHandler**: The function of the CustomAsyncIteratorCallbackHandler class is to act as an asynchronous iterator callback handler for handling the start, end, error, and callbacks of various stages of the tool's interaction with long-term language models (LLMs). 

**Properties**:
- `queue`: An asynchronous queue used to store the results of a process.
- `done`: An event that marks the completion of a process.
- `cur_tool`: Tool information that is currently being processed.
- `out`: A flag used to control the output.

**Code Description**:
The CustomAsyncIteratorCallbackHandler class inherits from AsyncIteratorCallbackHandler and provides a range of asynchronous methods to handle different events such as the start (on_tool_start), end (on_tool_end), error (on_tool_error), new token interacting with the LLM (on_llm_new_ token), LLM initiation (on_llm_start) and end (on_llm_end), etc. These methods`cur_tool` `queue`record the results of each event by updating the dictionary and adding information to the queue. 

When a tool starts an event, the class preprocesses the input string, removes specific stop words that may be causing processing interruptions, and then queues the processed information. When the tool ends or an error occurs, the dictionary is also updated accordingly`cur_tool` and the results are queued. For LLM interactions, the class is able to handle the receipt of new tokens, LLM start and end events, and error handling, again by updating`cur_tool` dictionaries and queues to record state. 

This class is used in projects to handle callbacks during interactions with long-term language models (LLMs), and in particular, `server/chat/agent_chat.py/agent_chat/agent_chat_iterator`it is used as a callback handler to manage the state of asynchronous chat iterators. In this way, it is able to collect and organize the output derived from LLMs and other tools to provide the necessary information for the end user interaction. 

**Note**:
- When using this class, you need to be aware of its asynchronous nature and ensure that its methods are called in the appropriate asynchronous environment.
- Since the information it processes may come from different sources (such as LLMs or other tools), it is necessary to ensure that the data entered is formatted correctly to avoid errors in the processing process.

**Example output**:
Suppose the start and end events of a tool are processed, and an example of a possible output in the queue is:
```json
{
  "tool_name": "Example tool",
  "input_str": "Input before processing",
  "output_str": "Processed output",
  "status": "tool_finish",
  "run_id": "Example run ID",
  "llm_token": "",
  "final_answer": "",
  "error": ""
}
```
This indicates that a tool has completed its task, and contains information such as the tool's name, input and output strings, status, and run ID.
### FunctionDef __init__(self)
**__init__**: This function is used to initialize an instance of the CustomAsyncIteratorCallbackHandler class. 

**Parameters**: The function does not accept any external parameters. 

**Code Description**: 
This function is the constructor of the CustomAsyncIteratorCallbackHandler class and is responsible for initializing the class instance. In this initialization process, `super().__init__()`the initialization logic of the parent class is first inherited by calling the constructor of the parent class. Next, the function creates an asynchronous queue`self.queue` that stores the results of the asynchronous operation. In addition,`self.done` it is an asynchronous event () `asyncio.Event`that marks when the asynchronous operation is complete. `self.cur_tool`is a dictionary that stores the state or data of the current tool. Finally,`self.out` it is set to True, which may indicate some kind of output state or flag. 

**Note**:
- Before using the CustomAsyncIteratorCallbackHandler class, `asyncio`it is important to understand the basic concepts of asynchronous programming and libraries, as the implementation of this class relies on the asynchronous programming features of Python. 
- `self.queue`Used for communication between asynchronous tasks, ensuring that the data in the queue is processed correctly when used.
- `self.done`Events are used to control asynchronous processes, especially when you need to wait for some asynchronous operation to complete.
- `self.cur_tool`The specific purpose and structure of dictionaries should be defined and used according to the actual application scenarios.
- `self.out`The specific meaning and purpose may vary depending on the actual code logic, and developers should understand and use it according to the context.
***
### FunctionDef on_tool_start(self, serialized, input_str)
**on_tool_start**: The function of this function is to initialize and preprocess the tool when it starts executing. 

**Parameters**:
- serialized: A dictionary containing serialized tool information.
- input_str: A string type that represents the input text for the tool.
- run_id: UUID type, which represents the unique identifier of the current run.
- parent_run_id: UUID type or None, a unique identifier for the parent run, and an optional parameter.
- tags: String list or None, which indicates the tags related to the current run, and optional parameters.
- metadata: Dictionary or None, containing metadata related to the current run, optional parameters.
- **kwargs: Accepts any additional keyword arguments.

**Code Description**:
`on_tool_start`A function is `CustomAsyncIteratorCallbackHandler`a method of a class that is called when the tool starts executing. The method first preprocesses the input string `input_str`and removes specific stop words that may cause processing interruptions, such as "Observation:", "Thought", etc. This step is to ensure that the input string is not interrupted prematurely in subsequent processing because it contains a specific vocabulary. 

Next, the method uses `serialized`the tool name in the parameters and the processed tool`input_str`, as well as other relevant information (such as run ID, status, etc.), to build a dictionary that represents the current tool state`cur_tool`. This dictionary includes key information such as tool name, input and output strings, status, run ID, and more. 

Finally, the`on_tool_start` method call`dumps` function `cur_tool`serializes the dictionary into a JSON-formatted string and `queue.put_nowait`uses the method to asynchronously put it into the queue. This step is used to pass information about the status of the current tool to other parts of the process, such as for monitoring, logging, or further data processing. 

Throughout the process, `Status.agent_action`states are used to mark the state of the current tool, indicating that the agent is performing an action. This, along`Status` with other states defined in the class, helps the system track and manage the flow of execution of asynchronous tasks. 

**Note**:
- When using `on_tool_start`the method, make sure that the parameters you pass in `serialized`contain the necessary tool information, such as the tool name. 
- The input string `input_str`may be truncated based on a predefined stop word, which needs to be considered when designing the input. 
- The method is asynchronous, so keywords need to be used when called`await`. 
- Arguments `**kwargs`allow methods `on_tool_start`to flexibly receive and process additional keyword arguments, which provides more flexibility, but also requires the caller to pay attention to the correctness and relevance of the arguments. 
***
### FunctionDef on_tool_end(self, output)
**on_tool_end**: The function of this function is to update the state of the tool and process the output at the end of the tool execution. 

**Parameters**:
- `output`: A string type that represents the output of the tool's execution.
- `run_id`: UUID type, which represents the unique identifier of the current run.
- `parent_run_id`: UUID type or None, a unique identifier for the parent run, optional.
- `tags`: String list or None, which indicates the label related to the current run, and can be used as an optional parameter.
- `**kwargs`: Receive any additional keyword parameters.

**Code Description**:
`on_tool_end`A function is `CustomAsyncIteratorCallbackHandler`an asynchronous method of a class that handles the logic after the execution of a tool. The function first sets the instance variable`out` to True, indicating that the output is ready. Then, use the `cur_tool.update`method to update the current tool's status to indicate `Status.tool_finish`that the tool's execution is complete, and replace the "Answer:" part of the tool's output string with an empty string. Finally, the function serializes the state of the current tool and the updated output through`dumps` the function into a JSON-formatted string and `queue.put_nowait`uses the method to queue it for further processing. 

This function is directly related to `dumps`the function and`Status` the class. `dumps`The function is used to convert the dictionary object to a string in JSON format, ensuring that the tool state and output information are formatted consistently and accurately during the serialization process. `Status`Classes provide a series of state constants that represent the `Status.tool_finish`state in which the tool execution is complete, and are used to update the state of the current tool at the end of the tool execution. 

**Note**:
- When calling `on_tool_end`a function, you must ensure that the`output` sum argument passed in is `run_id`valid and `run_id`should be a unique identifier. 
- Optional parameters`parent_run_id` and `tags`can be passed in as needed to provide more contextual information about the current run. 
- When processing the output string, the `output.replace("Answer:", "")`operation is to remove the possible prefix "Answer:" to get the pure output content. 
- The function is asynchronous, so you need to use a keyword when you call`await` it. 
- When using `queue.put_nowait`methods to put information into a queue, you should ensure that the queue is properly initialized and ready to receive data. 
***
### FunctionDef on_tool_error(self, error)
**on_tool_error**: The function of this function is to handle errors that occur during the execution of the tool. 

**Parameters**:
- `error`: An instance of an exception or keyboard interruption that indicates an error that occurred.
- `run_id`: UUID format, which represents the unique identifier of the current run.
- `parent_run_id`: UUID format, or None, which represents the unique identity of the parent run, if one exists.
- `tags`: A list of strings, or None, that represents the tag associated with the current error.
- `**kwargs`: Accept any additional keyword arguments.

**Code Description**:
`on_tool_error`A function is an `CustomAsyncIteratorCallbackHandler`asynchronous method in a class that handles errors that occur during the execution of a tool. This method is called when an exception or keyboard interruption is encountered during tool execution. The function first`self.cur_tool.update` uses the method to update the current tool's state to and `Status.error`logs the error message. It then serializes the current tool's state and error messages into a JSON-formatted string, and uses`self.queue.put_nowait` methods to queue the string for later processing. 

This function is directly related to `dumps`the function and`Status` the class. `dumps`Functions are used to convert dictionary objects to JSON-formatted strings, ensuring that error messages and tool states are serialized and transmitted in the correct format. `Status`Classes provide a `error`state constant that unambiguously identifies that the tool is currently in an error state. This design makes the error handling process both clear and efficient, and facilitates subsequent error tracking and handling. 

**Note**:
- When you call this function, you must ensure that the argument you pass in `error`is an instance of an exception or keyboard break so that the error message is properly logged. 
- `run_id`and `parent_run_id`parameters should be in a valid UUID format to ensure that the specific running instance and its parent instance (if any) can be accurately traced. 
- `tags`Parameters can be used to provide additional error context information to aid in error classification and analysis.
- The function is asynchronous and needs to be called with`await` a keyword. 
***
### FunctionDef on_llm_new_token(self, token)
**on_llm_new_token**: The function of this function is to process the token generated by the new LLM (Large Language Model). 

**Parameters**:
- token: A string type that represents a new token generated by the LLM.
- **kwargs: Receives any number of keyword arguments that can be used in the body of the function but are not directly used in the current function implementation.

**Code Description**:
`on_llm_new_token`A function is `CustomAsyncIteratorCallbackHandler`an asynchronous method of a class that is primarily used to process new tokens generated by a large language model. The function first defines a list called`special_tokens` a specific token string such as "Action" and "<|observation|>". These special tokens are used to identify whether a specific action or observation is included in the token generated by the LLM. 

The function then iterates through`special_tokens` the list to check if the pass `token`contains any of the special tokens in the list. If `token`a special token is found to be included, the function will do the following:
1. Use `split`the method of splitting`token`, bounded by a special token, and take the first part after the split`before_action`. 
2. The invoking `self.cur_tool.update`method updates the current tool's state to and`Status.running` sets it `before_action`to after adding a line break.`llm_token` 
3. Use `dumps`a function `self.cur_tool`to convert an object to a string in JSON format and`self.queue.put_nowait` put it in a queue via a method. 
4. Set `self.out`to and terminate the`False` loop. 

If it`token`'s not empty and`self.out` is `True`(i.e., no special token found), it will be`token` `llm_token`updated directly into `self.cur_tool`it and put into the queue after serialization as well. 

This function decides whether to update the state and content of the current tool by checking whether the token generated by the LLM contains a specific action or observation, and puts the updated information into a queue for subsequent processing.

**Note**:
- Functions are used `dumps`to serialize dictionary objects into JSON strings, which is a step to ensure that the data in the queue is formatted uniformly for subsequent processing and transmission. 
- `Status.running`is a `Status`state value referenced from a class that indicates that the current tool or task is running. When updating a tool state, you need to make sure that you are using the correct status value. 
- The asynchronous nature of functions requires the caller to use `await`keywords to ensure the correct execution of asynchronous operations. 
- Arguments are not used directly in the function implementation`**kwargs`, which means that the function is designed to allow for additional keyword arguments to be received for future extension or flexible use in different contexts. 
***
### FunctionDef on_llm_start(self, serialized, prompts)
**on_llm_start**: The function of this function is to update the state of the current tool when the Long-Term Learning Model (LLM) starts, serialize it and put it into the queue. 

**Parameters**:
- `serialized`: A dictionary containing serialized information of type`Dict[str, Any]` . 
- `prompts`: A list of strings containing a hint of type`List[str]` . 
- `**kwargs`: Receives any number of keyword arguments of type .`Any` 

**Code Description**:
`on_llm_start`A function is `CustomAsyncIteratorCallbackHandler`an asynchronous method of a class that is primarily used to handle the logic of a long-term learning model (LLM) when it starts. In this method, the`self.cur_tool.update` current tool's state is first updated to be by calling the method`Status.start`, and it will `llm_token`be set to an empty string. This means that the current tool has started execution, but no LLM tokens have been generated or received. 

Next, the method uses`dumps` a function to `self.cur_tool`serialize the object into a string in JSON format. `dumps`Functions are a core feature that takes a dictionary object as input and converts it to a string in JSON format, ensuring the readability and integrity of non-ASCII characters. In this method, the`dumps` use of functions ensures that the serialized information of the current tool state is formatted uniformly and accurately. 

Finally, the serialized string is `self.queue.put_nowait`immediately placed in a queue via the method for further processing. This step is part of the asynchronous operation and ensures that a large number of tasks can be handled efficiently, even in high-concurrency environments. 

**Note**:
- When using `on_llm_start`methods, you need to make sure that the arguments you pass in`serialized` are properly formatted dictionaries and that the `prompts`arguments are a list of strings. These parameters are critical for the execution of the method. 
- The method is asynchronous, so keywords need to be used when called`await`. 
- Update state and serialization operations should match the actual LLM startup logic to ensure state accuracy and information integrity.
- When dealing with asynchronous tasks, you should pay attention to exception handling to ensure that the program can run smoothly even in the event of an error.
***
### FunctionDef on_chat_model_start(self, serialized, messages)
**on_chat_model_start**: The function of this function is to initialize the setup at the beginning of the conversation model. 

**Parameters**:
- `serialized`: A dictionary-type parameter that contains serialization information.
- `messages`: A list-type parameter that contains a list of messages.
- `run_id`: A UUID parameter that represents the unique identifier of the run.
- `parent_run_id`: An optional UUID type parameter that represents the unique identifier of the parent run.
- `tags`: An optional string list type parameter that contains tag information.
- `metadata`: An optional dictionary-type parameter that contains metadata information.
- `**kwargs`: Receive any additional keyword parameters.

**Code Description**:
`on_chat_model_start`A function is `CustomAsyncIteratorCallbackHandler`a method of a class that is primarily used to handle initialization at the beginning of a conversation model. In this method,`self.cur_tool.update` the current tool's state is first updated via the method to and`Status.start` set to `llm_token`an empty string. This indicates that the chat model is executing and there are currently no long-lived model tokens. Then,`self.queue.put_nowait` the serialized information (converted to`self.cur_tool` `dumps`a JSON-formatted string by a function) using the method is immediately placed in a queue for subsequent processing. 

There are two important objects called in this method:`Status` and`dumps`. `Status`Classes are used to define different state constants, which represent the`Status.start` start state, which is used to identify the start of the conversation model. `dumps`The function is used to convert a dictionary object to a string in JSON format, and here it is used to serialize`self.cur_tool` information so that it can be queued as a string. 

**Note**:
- When calling `on_chat_model_start`a method, you need to make sure that the parameters passed in meet the requirements, especially the`run_id` UUID must be valid. 
- `serialized`The parameters should contain all the necessary serialization information to ensure that the dialog model can be initialized correctly.
- Usage`tags` and `metadata`parameters can provide additional contextual information, but they are optional. 
- The method is asynchronous, so keywords need to be used when called`await`. 
- In practice, attention should be paid to `**kwargs`the use of parameters to ensure that no unexpected keyword parameters are passed in to avoid potential errors. 
***
### FunctionDef on_llm_end(self, response)
**on_llm_end**: The function of this function is to update the state of the current tool at the end of the LLM (Large Language Model) task and put it in a queue. 

**Parameters**:
- `response`: LLMResult type, which indicates the result of the LLM task.
- `**kwargs`: Accepts any additional keyword arguments, providing flexibility for function calls.

**Code Description**:
`on_llm_end`A function is an `CustomAsyncIteratorCallbackHandler`asynchronous method of a class that is called at the end of a large language model (LLM) task. This function first uses`self.cur_tool.update` the method to update the current tool's status to indicate`Status.complete` that the task is complete, and sets `llm_token`it to a line break ("\n"). This step is to mark that the tool or task you are currently working on has been completed and is ready for the next step. 

The function then uses the`self.queue.put_nowait` method to put `self.cur_tool`the JSON string representation (obtained by calling `dumps`the function transformation) into a queue for later processing. `dumps`The function converts the `self.cur_tool`dictionary object into a string in JSON format, ensuring the consistency and accuracy of the information during the serialization process. This step is a key part of the asynchronous process, ensuring that task status updates and information delivery are done in a timely and accurate manner. 

Functions`dumps` and `Status`classes are `on_llm_end`two objects that are closely related to functions throughout the project. `dumps`Functions are responsible for serializing dictionary objects into JSON strings, while `Status`classes provide a set of predefined state constants that identify the different stages of asynchronous operations. Together, these tools and mechanisms support`on_llm_end` the implementation of functions, making it possible to effectively manage and pass the end state of LLM tasks. 

**Note**:
- When you call `on_llm_end`a function, you need to make sure that the parameters you pass in`response` are `LLMResult`of type to ensure that the function can correctly handle the results of the LLM task. 
- Functions are internally used `**kwargs`to accept arbitrary additional keyword arguments, which provides flexibility when calling, but callers should be careful to pass only the arguments they need to avoid unnecessary confusion. 
- Updating state and putting into queue operations are performed asynchronously, and you should be careful when calling this function to handle issues related to asynchronous execution that may arise, such as concurrency control and exception handling.
***
### FunctionDef on_llm_error(self, error)
**on_llm_error**: The function of this function is to handle LLM error events. 

**Parameters**:
- `error`: Receives an exception object, which can be`Exception` of or `KeyboardInterrupt`type, indicating an error that has occurred. 
- `**kwargs`: Receive any number of keyword arguments, providing additional flexibility to handle different error cases.

**Code Description**:
`on_llm_error`A function is `CustomAsyncIteratorCallbackHandler`a method of a class that is specifically designed to handle errors encountered by LLMs (long-lived models) during execution. This function is triggered when an error occurs during LLM execution. 

Inside the function, the current `self.cur_tool.update`tool's state is first updated via a method`Status.error`, and the error message is logged. Here`Status.error` is a `Status`constant defined from the class, which indicates that the current tool is in an error state. Error messages are recorded by`error` converting the parameters to strings. 

Next, the function uses `self.queue.put_nowait`methods to asynchronously put the current tool's state information into the queue. Use `dumps`a function to serialize tool state information into a string in JSON format before putting it into a queue. `dumps`Functions are a key function that converts dictionary objects into JSON-formatted strings, ensuring consistent formatting and accuracy of information during network transmission or storage. 

**Note**:
- When handling LLM errors, make sure that `on_llm_error`the arguments passed to the function `error`contain enough error information for accurate documentation and subsequent processing. 
- Using `**kwargs`parameters provides additional flexibility, but care needs to be taken when calling that the keyword arguments passed should match the error handling logic. 
- When updating tool state and serialization state information, you should ensure the atomicity of operations and error handling mechanisms to avoid further errors caused by improper exception handling.
- Consider `dumps`the use of functions, make sure that the incoming objects meet the requirements for JSON serialization, and be careful to handle non-ASCII characters. 
***
### FunctionDef on_agent_finish(self, finish)
**on_agent_finish**: The function of this function is to update the state of the current tool when the agent execution completes and put its final result into the queue. 

**Parameters**:
- `finish`: An `AgentFinish`object of type that contains the end result of an agent's execution. 
- `run_id`: An `UUID`object of type that represents a unique identifier of the current run. 
- `parent_run_id`: An optional `UUID`type of object that represents the unique identity of the parent run. 
- `tags`: An optional list of strings containing tags related to the current run.
- `**kwargs`: Accept any additional keyword arguments.

**Code Description**:
`on_agent_finish`A function is `CustomAsyncIteratorCallbackHandler`an asynchronous method of a class that is called when the proxy execution is complete. The method first uses`finish.return_values["output"]` the Get Proxy Execution Final Output and updates the current tool's state to`Status.agent_finish` while setting the final answer to the Agent's output. It then `dumps`uses a function to serialize the state of the current tool into a JSON-formatted string, and uses`put_nowait` methods to queue this string for later processing. Finally, `cur_tool`it is reset to an empty dictionary in preparation for the next proxy execution. 

In this process, `dumps`the function is responsible for converting the dictionary object into a string in JSON format, ensuring that the information is formatted consistently and accurately during the serialization process. `Status`Classes provide `agent_finish`status that identifies that agent execution has completed, which is critical for tracking and managing the execution process of asynchronous tasks. 

**Note**:
- Make sure that `finish`the parameters provide a valid proxy execution result, especially that the`finish.return_values["output"]` output is correctly obtained. 
- When using `dumps`functions, you need to make sure that the object passed in is a dictionary type to avoid serialization errors. 
- When putting information into a queue, you `put_nowait`can use this method to avoid blocking, but you need to make sure that the queue is processed fast enough to handle the speed of the placement and avoid queue overflow. 

**Example output**:
Since `on_agent_finish`the method doesn't return a value, its main role is to update the state and put the information into the queue, so there's no direct output example. However, it can be assumed that after the agent execution is complete, the queue will contain a JSON-formatted string similar to the following:
```json
{"status": 5, "final_answer": "Output results of agent execution"}
```
This indicates that the status of the current tool has been updated to the Agent Complete status and the final answer has been set to the output of the agent.
***
