## ClassDef CustomPromptTemplate
**CustomPromptTemplate**: The function of the CustomPromptTemplate class is to format and generate a customized prompt string based on the list of templates and tools provided. 

**Properties**:
- `template`: A string type that defines the template for the prompt.
- `tools`: A list of Tool objects, each containing the name and description of the tool.

**Code Description**:
The CustomPromptTemplate class inherits from StringPromptTemplate and is mainly used to generate customized prompts. It`format` receives keyword arguments via a method, which `intermediate_steps`is a list of tuples of actions and observations. The method first `intermediate_steps`formats the information in as a string, then adds it to the template, along with the name and description of the tool, and finally returns the formatted string. 

In the project, the CustomPromptTemplate class is used `server/chat/agent_chat.py/agent_chat/agent_chat_iterator`to generate prompts for user interaction. With the provided template and tool list, CustomPromptTemplate is able to generate prompts with instructions for using the tool and descriptions of intermediate steps, which is useful for guiding the user on how to interact with the agent. Especially in an asynchronous chat environment, accurate and detailed prompts can greatly improve the user experience. 

**Note**:
- When using CustomPromptTemplate, you need to make sure that the parameters passed to`format` the method are `intermediate_steps`properly formatted, i.e., a tuple list containing actions and observations. 
- The list of tools `tools`should contain all the tools that may be mentioned in the tooltip, and each tool should have a name and description. 

**Example output**:
Suppose you have the following list of templates and tools:
- Template:`"Please use the following tools：{tools}\n{agent_scratchpad}"`
- List of tools:`[Tool(name="Tool1", description="This is tool 1"), Tool(name="Tool2", description="This is tool 2")]`
- `intermediate_steps`：`[("action1", "observation1"), ("action2", "observation2")]`

When a method is called`format`, the string that may be returned is:
```
Please use the following tools：
Tool1: This is tool 1
Tool2: This is tool 2
action1
Observation: observation1
Thought: action2
Observation: observation2
Thought: 
```
### FunctionDef format(self)
**Function**:  The `format` function of the function is to format and return a string based on the provided parameters and internal logic. 

**Parameters**:
- `**kwargs`: A keyword argument that can accept multiple named arguments and is used to dynamically pass to templates and internal logic processing.

**Code Description**:
The function first extracts the argument from the incoming keyword argument (`kwargs`).`intermediate_steps` `intermediate_steps`It should be a tuple list of actions and observations. The function iterates through the list, formatting the log of each action and the corresponding observations into a string and concatenating it into`thoughts` a string. 

Next, the function adds the`thoughts` string to `kwargs`the dictionary with the key name`agent_scratchpad`. In addition, it is `self.tools`processed, which is a list of tool objects. The function formats the name and description of each tool as strings, and concatens these strings with line breaks, and assigns the result to`kwargs` a key in the dictionary`tools`. At the same time, the names of all tools are extracted, concatenated with commas and spaces into a string, and assigned to`kwargs` the keys in the dictionary`tool_names`. 

Finally, the function uses `self.template.format(**kwargs)`a statement to pass the processed `kwargs`dictionary as an argument to the template's`format` method and returns the formatted string. 

**Note**:
- Make sure that the key`kwargs` is included in `intermediate_steps`the pass and that its values are formatted correctly. 
- `self.tools`It should be a list of objects that contain`name` and `description`attributes. 
- The function relies on`self.template` a `format`method that ensures it `self.template`has been initialized correctly and can be accepted`kwargs` as a parameter. 

**Example output**:
```plaintext
Action: Move Forward
Observation: Wall detected
Thought: 
Tool1: Used for cutting
Tool2: Used for digging
Tool Names: Tool1, Tool2
```
***
## ClassDef CustomOutputParser
**CustomOutputParser**: The function of the CustomOutputParser class is to parse the output of a large model and decide the next operation based on the output content. 

**Properties**:
- `begin`: A boolean value that indicates whether the parsing process should start or stop.

**Code Description**:
The CustomOutputParser class, which inherits from AgentOutputParser, is a parser dedicated to parsing the output of large models. It analyzes the output of the model to decide whether to continue with certain actions or end the session. Specifically, it checks if the model output contains a specific keyword or phrase, such as "Final Answer:" or "Action:", and returns the corresponding action instructions accordingly. 

On initialization, the `begin`property is set to True, indicating that the parser is ready to start parsing the output. In`parse` the method, first check that all supported surrogate models are not in the model container and `begin`are True. If the conditions are met, it looks for stop words in the output (such as "Observation:") and truncates the output based on those stop words in preparation for further parsing. 

If the output contains "Final Answer:", it means that the large model has given a final answer, and the parser will reset `begin`to True and return an AgentFinish object containing the final answer. If the output contains "Action:", the parser parses out the corresponding action and input, attempts to execute the action, and returns an AgentAction object. If an exception is encountered during parsing, or if the output is not in the expected format, the parser will return an AgentFinish object with an error message. 

**Note**:
- When using CustomOutputParser, you need to ensure that the output format of the large model matches the format expected by the parser, otherwise the operation instructions may not be parsed correctly.
- The parser relies on a specific keyword or phrase in the output to decide on an action, so this needs to be considered when designing the output format for a large model.

**Example output**:
Suppose the output of a large model is "Final Answer: 42", and the object that may be returned after CustomOutputParser is as follows:
```
AgentFinish(return_values={"output": "42"}, log="Final Answer: 42")
```
If the output of the large model is "Action: Calculate Action Input: 42 + 1", the objects that may be returned after parsing are:
```
AgentAction(tool="Calculate", tool_input="42 + 1", log="Action: Calculate Action Input: 42 + 1")
```

In a project, CustomOutputParser is used to parse the output of the large model during interaction with the user to determine whether a specific tool or service needs to be invoked to assist in fulfilling the user's request. This enables the entire system to handle a wide range of different user needs more intelligently and flexibly.
### FunctionDef __init__(self)
**__init__**: This function is used to initialize the CustomOutputParser object. 

**Parameters**: The function does not accept any external parameters. 

**Code description**: In the __init__ method of the CustomOutputParser class, `super().__init__()`first make sure that the parent class is properly initialized by calling the constructor of the parent class. Next, the method sets an instance variable `self.begin`and initializes it to True. This variable may be used to mark the start of parsing, or to control certain operations that only need to be performed at initialization. 

**Note**: When using the CustomOutputParser class, you do not need to manually pass any parameters to the __init__ method. After the object is created, the value can be modified according to the actual needs`self.begin`, but in general, the initial value of the variable is true enough for most use cases. In addition, if the CustomOutputParser class inherits from a parent class with complex initialization logic,`super().__init__()` this ensures that this logic is not missed. 
***
### FunctionDef parse(self, llm_output)
**parse**: The function of this function is to parse the text output from the large language model (LLM) and decide what to do next based on the output. 

**Parameters**:
- `llm_output`: A string type that represents the output text received from a large language model (LLM).

**Code Description**:
This function first checks to see if a supported surrogate model exists `model_container.MODEL`in and if it is to start parsing. If it is a surrogate model that starts parsing and does not have support, it looks for a stop word in the output (e.g., "Observation:") and takes the text before the first stop word as the new output text. 

If the output text contains "Final Answer:", it means that the large language model has given a final answer. At this point, the function takes the text after "Final Answer:" as output and marks the end of parsing.

If the output text contains "Action:", it means that a specific action needs to be performed. The function parses out the action name and action input, and then attempts to execute the action. If the execution is successful, an`AgentAction` object is returned, containing the action name, action input, and raw log. 

If none of the above conditions are met, or if an exception is encountered while parsing the action, the function returns an`AgentFinish` object indicating the end of parsing, along with an error message or the large model's own answers. 

**Note**:
- When using this function, you need to make sure that and`model_container.MODEL` `SUPPORT_AGENT_MODEL`have been set up correctly so that the function can correctly determine if there is a supported proxy model. 
- The return value type of the function may be`AgentFinish` , `tuple[dict[str, str], str]`or`AgentAction`, and the caller needs to handle it accordingly depending on the return value type. 

**Example output**:
Assuming `llm_output`"Final Answer: 42", an example of what a function might return is:
```python
AgentFinish(return_values={"output": "42"}, log="Final Answer: 42")
```

If `llm_output`it's "Action: Email Action Input: john.doe@example.com", the example that the function might return is:
```python
AgentAction(tool="Email", tool_input="john.doe@example.com", log="Action: Email Action Input: john.doe@example.com")
```
***
