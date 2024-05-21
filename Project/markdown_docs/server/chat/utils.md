## ClassDef History
**History**: The History class is used to represent the history of the conversation. 

**Properties**:
- `role`: Indicates the role of the speaker, and the type is a string.
- `content`: Indicates the content of the speech, and the type is a string.

**Code Description**:
The History class inherits from the BaseModel and is used to encapsulate a single piece of history in a conversation, including the speaking role and the content of the speech. It provides a way to convert history to a message tuple `to_msg_tuple`, and a way to convert history to a message template `to_msg_template`. In addition, a class method is provided `from_data`to create History instances from different types of data structures (lists, tuples, dictionaries). 

In projects, the History class is widely used to process and store conversation history. For example, in `agent_chat` `chat` features such as and , user input and historical conversations are passed to the model as parameters to generate the corresponding responses. These histories are managed and passed through instances of the History class, ensuring data consistency and ease of use. 

**Note**:
- When using `to_msg_tuple` a method, if  the property `role` is "assistant", the returned tuple is "ai" for the role part, otherwise "human", which helps to distinguish between the user and the assistant's speech when working on the conversation. 
- `to_msg_template` Methods allow you to format content based on whether or not you need the original content (`is_raw` parameters), which is useful when you need to format the content in a specific way. 
- `from_data` The class method provides flexible data transformation capabilities that allow history instances to be created from a variety of data sources, increasing the versatility and flexibility of your code.

**Example output**:
Let's assume that you have the following historical data:
```python
data = {"role": "user", "content": "你好"}
```
Use the History class to create an instance and convert to a message tuple:
```python
h = History.from_data(data)
print(h.to_msg_tuple())
```
The possible outputs are:
```
('human', '你好')
```
When converting to a message template, it is assumed that raw content processing is not required:
```python
print(h.to_msg_template(is_raw=False))
```
The output will format the content according to the actual template, where the roles and content will be replaced and processed accordingly.
### FunctionDef to_msg_tuple(self)
**to_msg_tuple**: The function of this function is to convert the message object into a tuple containing the role and content. 

**Arguments**: This function does not have an explicit parameter, but implicitly uses a self parameter, representing an instance of the History object that calls this function. 

**Code Description**: `to_msg_tuple`A function is a method of the History class that converts the role and content of a message object into a tuple. This function first checks the properties of the message object`role`. If the `role`property value is "assistant", the first element of the tuple is the string "ai"; Otherwise, the first element is the string "human". The second element of a tuple is the property value of the message object`content`, which is the content of the message. In this way, the `to_msg_tuple`role and content information of the message can be quickly obtained through the method, which is convenient for subsequent processing or display. 

**Note**: When using this function, you need to make sure that the instance of the History object calling it has the correct settings`role` and `content`properties, otherwise you may encounter an error that the property does not exist. 

**Output example**: Suppose an instance of the History object has`role` a property of "assistant" and a `content`property of "Hello, I'm an AI assistant. ", then `to_msg_tuple`the return value of the invoked method will be:

```python
("ai", "你好，我是AI助手。")
```

If the `role`property is another value, such as "user", and the `content`property is "This is a user message." ", then the return value will be:

```python
("human", "这是一个用户消息。")
```

This approach allows the role and content of the message to be quickly identified and used, which is very useful for message processing and presentation.
***
### FunctionDef to_msg_template(self, is_raw)
**to_msg_template**: The function of this function is to convert historical messages into a specific message template format. 

**Parameters**:
- `is_raw`: Boolean, which indicates whether the message content is processed as raw text. Defaults to True.

**Code Description**:
`to_msg_template`A function is `History`a method of a class that converts historical messages into `ChatMessagePromptTemplate`a format for further processing and use. The function first defines a character mapping dictionary`role_maps` that maps "AI" to "Assistant" and "Human" to "User". Then, the corresponding role is found based on`History` the object's `role`attributes, and if it is not found, `role`the original value of the attribute is used. 

Based on `is_raw`the value of the parameter, the function decides whether to wrap the message content in the "{% raw %}" and "{% endraw %}" tags. This is mainly used to handle Jinja2 template labels that may be included in the message content to avoid being incorrectly interpreted or executed in subsequent processing. If`is_raw` true, the message content is wrapped; Otherwise, leave it as it is. 

Finally, the function uses `ChatMessagePromptTemplate.from_template`methods to create and return an object with the processed content, the "jinja2" string (which indicates the type of template used), and the role as arguments`ChatMessagePromptTemplate`. 

In a project, `to_msg_template`methods are called by multiple asynchronous iterator functions that are responsible for handling different types of chat sessions, such as`chat_iterator` , `knowledge_base_chat_iterator`and `search_engine_chat_iterator`so on. In these functions, `to_msg_template`methods are used to convert historical messages or user input into a format suitable for model processing, which in turn generates a chat prompt or query template. 

**Note**:
- When using `to_msg_template`methods, you need to pay attention to the `is_raw`usage scenarios of parameters. If the message content contains a template label that needs to be retained, it should be`is_raw` set to True. 
- The method depends on the `ChatMessagePromptTemplate.from_template`method, so you need to ensure that `ChatMessagePromptTemplate`the class and its methods are implemented correctly. 

**Example output**:
Suppose you have an`History` object that `role`is "human" and `content`"Hello, AI!", and the call `to_msg_template(False)`might return something like this`ChatMessagePromptTemplate`:
```python
ChatMessagePromptTemplate(content="Hello, AI!", template_type="jinja2", role="user")
```
***
### FunctionDef from_data(cls, h)
**from_data**: This function is used to create a History object based on the data provided. 

**Parameters**:
- `h`: Can be a list, tuple, or dictionary type that is used to initialize the data for a History object.

**Code Description**:
`from_data`A function is a class method that creates a History object based on different types of input data. The function accepts a single parameter`h`, which can be a list, tuple, or dictionary type. If `h`it is a list or tuple, and it is at least 2 in length, then the first two elements of the list or tuple are initialized as the sum properties of the History object`role``content`. If `h`it is a dictionary type, the key-value pairs in the dictionary will be passed as arguments to the constructor of the History class by unwrapping to create a History object. Regardless of the type of input data, the function will eventually return a History object. 

In a project, `from_data`functions are called in multiple places to convert the user's input or historical conversation data into a History object for subsequent processing. For example, in functions`agent_chat` such as ,`chat_iterator` ,`file_chat` `knowledge_base_chat`, etc`search_engine_chat`., you can see `from_data`the call of the function, through which they convert the incoming list of historical conversations into a list of History objects for further processing and analysis. 

**Note**:
- When the input parameter `h`is a list or tuple, it needs to contain at least two elements, representing the role and content, otherwise the History object cannot be created correctly. 
- When the input parameter `h`is a dictionary, you need to make sure that the key contained in the dictionary matches the constructor parameter of the History class in order to initialize the object correctly. 

**Example output**:
Assuming that the input parameter`h` is a list`["user", "今天天气怎么样？"]`, the History object returned by the function will have the attributes`role="user"` and `content="今天天气怎么样？"`. If the input parameter`h` is a dictionary`{"role": "assistant", "content": "今天是晴天。"}`, the returned History object will have the same property value. 
***
