## ClassDef StructuredChatOutputParserWithRetries
**StructuredChatOutputParserWithRetries**: This class provides output parsing with a retry mechanism for structured chat agents. 

**Properties**:
- base_parser: The underlying parser used.
- output_fixing_parser: Output correction parser used, optional.

**Code Description**:
The StructuredChatOutputParserWithRetries class inherits from AgentOutputParser and is primarily used to parse the output of a structured chat agent. It fulfills its function by defining two main properties – base_parser and output_fixing_parser. base_parser is an instance of StructuredChatOutputParser for basic output parsing. output_fixing_parser is an optional instance of OutputFixingParser that is used to correct the output if necessary. 

The core method of this class is parse, which takes a string text as input and attempts to parse this string to generate an AgentAction or AgentFinish. The parsing process first tries to find the location of a special tag, such as "Action:" or ""<|observation|>", and then decides what to do with the text based on whether it contains a "tool_call" or not. If "tool_call" is included, it is further parsed to extract actions and parameters; Otherwise, the text is processed directly as the final answer. After the parsing is complete, select the corresponding parser for final parsing based on the presence or absence of output_fixing_parser. 

In the project, StructuredChatOutputParserWithRetries is used by the StructuredGLM3ChatAgent class as the default output parser. Using the _get_default_output_parser method of the StructuredGLM3ChatAgent class, it can be seen that StructuredChatOutputParserWithRetries is used to build a structured chat agent to process the output of a language model (LLM) and convert it into a format suitable for agent processing.

**Note**:
- When using the StructuredChatOutputParserWithRetries class, you need to make sure that the incoming text is formatted as expected, especially when it comes to special markup and tool call formats.
- If a output_fixing_parser is provided, it will be used for secondary resolution if the underlying resolution fails or if remediation is required.

**Example output**:
```json
Action:
```
{
  "action": "Final Answer",
  "action_input": "This is parsed text"
}
```
In this example, assuming the incoming text does not contain "tool_call", the parse method will directly treat the text as the final answer and build the corresponding JSON string as output.
### FunctionDef parse(self, text)
**parse**: The function of this function is to parse the text and generate the corresponding action or final answer.

**parameter**:
- `text`: The text to be parsed, type is string.

**Code description**:
This function first defines a list `special_tokens` containing special tokens that are used to find specific positions in the text. It then finds the first occurrence of these special tags and truncates the text to that location for further processing.

If the text contains "tool_call", it is considered an action that needs to be performed. The function will find the end position of the action description (that is, the position of "```") and extract the action name and parameters. Parameters are parsed into key-value pairs and stored in a dictionary. This information will then be organized into a JSON object, ready for further parsing.

If the text does not contain "tool_call", it is considered to be a final answer, the text is entered directly as an action, and the action name is set to "Final Answer".

Afterwards, the function will decide which parser to use for parsing based on whether `output_fixing_parser` exists. If present, the `output_fixing_parser` parser is used, otherwise the `base_parser` parser is used. The parsed results will be returned.

**Notice**:
- When using this function, you need to ensure that the text passed in is well-formatted, especially when the text contains action descriptions, a specific format needs to be followed (for example, correct separation of actions and parameters).
- If any exception is encountered during the parsing process, the function will throw an `OutputParserException` exception, and the exception message will contain the original text that cannot be parsed.

**Example output**:
Assuming that the text content is an action call, the possible return value after parsing is:
```json
{
  "action": "tool_call_example",
  "action_input": {
    "param1": "value1",
    "param2": "value2"
  }
}
```
If the text content is the final answer, the possible return value after parsing is:
```json
{
  "action": "Final Answer",
  "action_input": "Here is a sample text for a final answer."
}
```
***
### FunctionDef _type(self)
**_type**: The function of this function is to return a specific string. 

****Arguments: This function has no arguments. 

**Code Description**: `_type` The function is a very simple method, and its main purpose is to return a predefined string. This string represents a specific type identifier, the "structured_chat_ChatGLM3_6b_with_retries". This identifier is often used to distinguish between different processing logic or data formats. In this context, it may represent a conversation model that uses a specific configuration or policy, specifically a structured conversation output parser that is configured with a retry mechanism. This type of identification is important for maintaining code clarity and maintainability, as it allows developers to quickly identify and understand the purpose and behavior of blocks of code. 

**Note**: When using this function, it is important to note that the string it returns is hard-coded, which means that if you need to change the type identifier in the future, you will need to modify the return value of this function directly. Therefore, care should be taken when maintaining this part of the code to ensure that any changes do not affect other code logic that relies on this identity. 

**Example output**: Calling  the `_type` function will return the following string:
```
"structured_chat_ChatGLM3_6b_with_retries"
```
***
## ClassDef StructuredGLM3ChatAgent
**StructuredGLM3ChatAgent**: The function of this class is to implement a structured chat agent for handling and responding to conversations based on the ChatGLM3-6B model. 

**Properties**:
- output_parser: The parser used to parse the proxy output, defaulting to the StructuredChatOutputParserWithRetries instance.
- observation_prefix: A prefix string to be added before the ChatGLM3-6B observation.
- llm_prefix: A prefix string to add before a Language model call.

**Code Description**:
The StructuredGLM3ChatAgent class inherits from the Agent class and provides an implementation of a structured chat agent. It handles interactions with language models (LLMs) by defining specific properties and methods, generates prompts, and parses the output of the LLMs. 

- **Attribute Definition**:
  - `output_parser` The property specifies the parser used to parse the proxy output, with the default value being an instance of the StructuredChatOutputParserWithRetries class, which provides output parsing capabilities with a retry mechanism.
  - `observation_prefix` The and `llm_prefix` properties define prefix strings that are added before the observation and the Language model call, respectively, to format the generated prompt. 

- **Methodology Analysis**:
  - `_construct_scratchpad` The method is used to build a draft of the agent, and it generates a string based on intermediate steps that records the agent's work process.
  - `_get_default_output_parser` The class method returns a default output parser instance that parses the output of the language model.
  - `create_prompt` A class method is used to generate a prompt template based on the provided tool and input variables, which formats the tool's information and other input variables into a string template that is used to generate input to the language model.
  - `from_llm_and_tools` The class method is used to build a StructuredGLM3ChatAgent instance based on a collection of language models and tools, which initializes the agent by combining the language model, tools, and other parameters.

**Note**:
- When using the StructuredGLM3ChatAgent class, you need to ensure that the tools and language models you provide match the agent's target tasks.
- The output parser (output_parser) should be able to parse the output of the language model accurately so that the agent can respond correctly to the user's input.
- When building prompts, you should take care to format the string templates to ensure that they can be understood and processed correctly by the language model.

**Example output**:
Assuming that the input received by the agent is a simple Q&A task, an example of the output might be as follows:
```
{
  "action": "Final Answer",
  "action_input": "This is the agent’s answer based on parsing the language model output."
}
```
In this example, the agent parses the output of the language model and generates a JSON object containing the final answer (Action) and the corresponding input (action_input).
### FunctionDef observation_prefix(self)
**observation_prefix**: The function of this function is to generate and return a prefix string observed by ChatGLM3-6B. 

****Arguments: This function does not accept any arguments. 

**Code Description**: `observation_prefix`A function is `StructuredGLM3ChatAgent`a method of a class, and its main purpose is to provide a uniform prefix for the observation of the ChatGLM3-6B model. This prefix is used to identify what is observed when processing chat or conversation data. In this function, the returned string is "Observation:", which means that all observations processed by this method will start with "Observation:". This helps the model identify and process the input data, ensuring consistency and accuracy in the data format. 

**Note**: When using this function, you need to note that the prefix string it returns is fixed. If you need different prefixes in different contexts or apps, you may need to modify or extend this function accordingly. 

**Example output**: Calling `observation_prefix`the function will return the following string:
```
Observation:
```
***
### FunctionDef llm_prefix(self)
**llm_prefix function function**: The function of this function is to generate and return a prefix string that is used to append when calling a large language model (LLM). 

****Arguments: This function has no arguments. 

**Code Description**: `llm_prefix`The function is defined in a `StructuredGLM3ChatAgent`class, is a simple member function that does not accept any arguments, and returns a fixed string`"Thought:"`. This string is prefixed with the purpose of appending a call to a large language model (LLM) before the actual query or command, as a way to potentially influence or specify how the model responds. This practice is common when interacting with large language models to guide the model's responses to be more in line with the desired context or style. 

**Note**: When using `llm_prefix`functions, it is important to note that the returned prefix string `"Thought:"`is hard-coded, which means that the return value of this function may need to be modified if different prefixes are needed to guide the response of the large language model in different application scenarios. In addition, the validity and applicability of this prefix may change with the different large language models or the update of the model training data, so it needs to be adjusted according to the specific performance of the model in practical applications. 

**Example output**: Calling `llm_prefix`a function will return a string`"Thought:"`. 

Through the above analysis, developers and beginners can understand `llm_prefix`what functions do, how to use them, and what to pay attention to. This helps to `StructuredGLM3ChatAgent`guide the model's response more effectively when using classes to interact with large language models, improving the quality and effectiveness of interactions. 
***
### FunctionDef _construct_scratchpad(self, intermediate_steps)
**_construct_scratchpad**: The function of this function is to construct and return a string that represents an intermediate step. 

**Parameters**:
- **intermediate_steps**: A list of tuples, each consisting of an AgentAction and a string, representing intermediate action steps. 

**Code Description**:
`_construct_scratchpad` The function first calls the method of its parent class `_construct_scratchpad` , passes in the data of the intermediate step (),`intermediate_steps` and receives the returned string (`agent_scratchpad`). This string represents the progress of the work so far. The function then checks `agent_scratchpad` whether it is a string type, and if not, throws an `ValueError` exception to ensure that the data type of the subsequent operation is correct. 

If `agent_scratchpad` it is not empty, the function will return a formatted string that presents the user with previous work in a friendly way, even though the function does not actually have direct access to the work, but only passes the information through the arguments. If `agent_scratchpad` is  empty, the empty string is returned. 

**Note**:
- Make sure that the parameters you pass in `intermediate_steps` are formatted correctly, that is, the elements in the list are tuples, and the tuples contain `AgentAction` and  strings. 
- This function assumes that the parent class's `_construct_scratchpad` method is implemented correctly and returns a string. If the implementation of the parent class method changes, you may need to adjust this function accordingly. 

**Example output**:
If  contains `intermediate_steps` a series of action steps, and the parent class method returns a string representation of those steps, for example, "Step 1: Do something; Step 2: Do something else; ", then an example of a string that this function might return is:

```
"This was your previous work (but I haven't seen any of it! I only see what you return as final answer):
Step 1: Do something; Step 2: Do something else;"
```
***
### FunctionDef _get_default_output_parser(cls, llm)
**_get_default_output_parser**: The function of this function is to get the default output parser. 

**Parameters**:
- `llm`: An optional parameter of type that `BaseLanguageModel`indicates the underlying language model. 
- `**kwargs`: Accepts any number of keyword arguments.

**Code Description**: `_get_default_output_parser` A function is `StructuredGLM3ChatAgent` a class method of the class that gets the default output parser. The method accepts an optional instance of the language model `llm` and any number of keyword arguments `**kwargs`. Inside the function body, it creates and returns an `StructuredChatOutputParserWithRetries` instance to which it passes `llm` as a parameter. `StructuredChatOutputParserWithRetries` Classes are output parsers designed specifically for structured chat agents, with a retry mechanism that processes the output of a language model and converts it into a format suitable for agent processing. 

In the project, the`_get_default_output_parser` method is called by  the `from_llm_and_tools` method to get the default output parser instance. If you `StructuredGLM3ChatAgent` don't explicitly specify an output parser when you create an instance, you `_get_default_output_parser` get a default output parser instance by calling the method and use it to process the output of your Language model. 

**Note**:
- When using `_get_default_output_parser` methods, you need to make sure that the parameters you pass in `llm` , if any, are a valid instance of the language model. 
- The method is designed to flexibly accept any number of keyword arguments `**kwargs`, but these extra arguments are not directly used in the current implementation. Developers can take advantage of these parameters as needed when extending or modifying methods. 

**Output example**: Since `_get_default_output_parser` the method returns an `StructuredChatOutputParserWithRetries` instance, the output example will depend on the specific implementation of that instance. Assuming `llm` the argument is , `None`calling `_get_default_output_parser` the method will return an instance without an instance of the Language model `StructuredChatOutputParserWithRetries` . 
***
### FunctionDef _stop(self)
**Function of _stop function**: `_stop`The purpose of the function is to end the current session and return a specific list of tags. 

****Arguments: This function has no arguments. 

**Code Description**: `_stop`A function is `StructuredGLM3ChatAgent`a private method of a class that is used to mark an endpoint in a chat agent's session. When this function is called, it returns a list of individual string elements`"<|observation|>"`. This return value is often used to indicate that the conversation model has ended, or that some form of reset or observation is required. In the context of a chat agent, this particular string may be used as a signal or tag to trigger a specific behavior or processing logic. 

**Note**: While `_stop`the implementation of a function may seem simple, it may play a key role in the logic of the chat agent. When used, you need to ensure that the dialog model or processing logic is able to correctly recognize and process the returned tags`"<|observation|>"`. Also, because `_stop`it is a private method, it is only `StructuredGLM3ChatAgent`called inside the class and should not be accessed or called directly from outside the instance of the class. 

**Example output**: A `_stop`call to a function might return a list like this:
```python
["<|observation|>"]
```
This list contains a string element `"<|observation|>"`that represents the end of a chat session or the state that needs to be observed. 
***
### FunctionDef create_prompt(cls, tools, prompt, input_variables, memory_prompts)
**create_prompt**: The function of this function is to build a chat prompt template based on the provided tools and template parameters. 

**Parameters**:
- `tools`: A sequence of objects that implements the BaseTool interface, representing tools that can be used by chat agents.
- `prompt`: A string template that is used to format the final tooltip.
- `input_variables`: A list of strings specifying the name of the input variable, defaulting to None.
- `memory_prompts`: A list of BasePromptTemplate objects that provide a memory hint, defaulting to None.

**Code Description**:
`create_prompt`The function first iterates through `tools`each tool in the arguments, extracts its name, description, and parameter schema, and formats the information into a simplified JSON structure. This structure includes the tool's name, description, and parameters. The function then formats the tool information into a string, with each tool information on a single line, including its name, description, and parameters. This formatted string, along with other provided template parameters such as tool name list, history, input, and proxy drafts, is used to populate the`prompt` template string. 

If `input_variables`not specified, it defaults`["input", "agent_scratchpad"]`. `memory_prompts`Parameters allow additional hints to be added to the final prompt template, which can be previous conversation history or other important information. 

Finally, the function creates an object with the formatted prompt and a list of input variables`ChatPromptTemplate`, and returns it. This returned object can be used directly to generate prompts for chat agents. 

In a project, `create_prompt`functions are called by `from_llm_and_tools`methods that are used to build a chat agent based on a language model (LLM) and a collection of tools. This suggests that `create_prompt`functions play a central role in the initialization process of building chat agents, especially in preparing prompt templates for chat agents. 

**Note**:
- Make sure that `prompt`the template string provided by the parameter uses all the expected variables correctly to avoid errors when formatting. 
- `tools`The tool objects in the parameters need to implement`BaseTool` the interface to ensure that they have`name` , `description`and `args_schema`properties. 

**Example output**:
Suppose you have two tools, "Calculator" and "Translator", and the `prompt`parameter is "Available tools: {tools}\nInput: {input}", the properties in the objects that the function may return`ChatPromptTemplate` may `messages`contain the following strings:

```
Available tools:
Calculator: A simple calculator, args: {'number1': 'Number', 'number2': 'Number'}
Translator: Translates text from one language to another, args: {'text': 'String', 'target_language': 'String'}
Input: {input}
```
***
### FunctionDef from_llm_and_tools(cls, llm, tools, prompt, callback_manager, output_parser, human_message_template, input_variables, memory_prompts)
**from_llm_and_tools**: The function of this function has the function of building a chat agent from a language model (LLM) and a collection of tools. 

**Parameters**:
- `cls`: The first argument of the class method, which refers to the current class.
- `llm`: , `BaseLanguageModel`which represents the underlying language model. 
- `tools`: Implements `BaseTool`the object sequence of the interface, representing the tools that can be used by chat agents. 
- `prompt`: String type, used to format the final tooltip, defaults to None.
- `callback_manager`:  , `BaseCallbackManager`which is used to manage callback functions, which defaults to None. 
- `output_parser`:  , `AgentOutputParser`which is used to parse proxy output, defaults to None. 
- `human_message_template`: String type, which represents a human message template, defaults`HUMAN_MESSAGE_TEMPLATE`. 
- `input_variables`: A list of strings that specifies the name of the input variable, which defaults to None.
- `memory_prompts`:  A `BasePromptTemplate`list of objects to provide a memory hint, which defaults to None. 
- `**kwargs`: Accepts any number of keyword arguments.

**Code Description**:
`from_llm_and_tools`The function first verifies that the provided set of tools is valid. It then calls `create_prompt`methods to create a chat prompt template, which is based on the provided tools, prompts, input variables, and memory prompts. Next, use`llm`, generate,`prompt` and `callback_manager`create an `LLMChain`instance. In addition, the function extracts the tool name from the tool collection and tries to get the default output parser, and if no arguments are provided`output_parser`, the `_get_default_output_parser`method is called to get the default parser. Finally, use these components to build and return an`StructuredGLM3ChatAgent` instance. 

**Note**:
- Make sure that the`llm` sum `tools`parameters provided are valid instances, and`tools` that each tool implements`BaseTool` the interface. 
- If not specified at the time of call`output_parser`, the default output parser is automatically used. 
- `**kwargs`Parameters provide additional flexibility, allowing additional configuration options to be passed when creating an agent.

**Example output**:
Since `from_llm_and_tools`the function returns an `StructuredGLM3ChatAgent`instance, the output example will depend on the specific implementation of that instance. For example, if you call this function with default parameters, it will return an instance with the underlying Language model configured, the specified set of tools, and the default output parser`StructuredGLM3ChatAgent`. This instance can be used directly to process chat conversations, execute tool commands, and parse the output of the language model. 
***
### FunctionDef _agent_type(self)
**_agent_type**: The function of this function is to throw a ValueError exception. 

****Arguments: This function does not accept any arguments. 

**Code Description**:  A `_agent_type` function is `StructuredGLM3ChatAgent` a private method of a class that is designed to be overridden in a subclass to specify or return a specific proxy type string. In its original form, this function directly throws an `ValueError` exception, which suggests that this would be explicitly indicated if the method was called directly without proper rewriting in the subclass. This is a common programming pattern used to enforce that subclasses implement specific methods. 

**Note**: When working with `StructuredGLM3ChatAgent` a class or any of its subclasses, developers need to ensure that  the `_agent_type` method is properly overridden to avoid runtime errors. The existence of this method underscores the design principle that certain methods are designed specifically for child classes and not directly for use in parent classes. So if you run into `ValueError` a development process, it's probably because you tried to call a method that should be overridden by a subclass, but didn't do so. 
***
## FunctionDef initialize_glm3_agent(tools, llm, prompt, memory, agent_kwargs)
**initialize_glm3_agent**: The function of this function is to initialize a chat agent based on the GLM3 model. 

**Parameters**:
- `tools`: Implements `BaseTool`the object sequence of the interface, representing the tools that can be used by chat agents. 
- `llm`: , `BaseLanguageModel`which represents the underlying language model. 
- `prompt`: String type, used to format the final tooltip, defaults to None.
- `memory`:  , `ConversationBufferWindowMemory`which is used to store chat history, which defaults to None. 
- `agent_kwargs`: Dictionary type, which contains additional parameters required to create a chat agent, and defaults to None.
- `tags`: A sequence of strings used to tag or categorize proxies, defaulting to None.
- `**kwargs`: Accepts any number of keyword arguments, providing additional configuration options.

**Code Description**:
`initialize_glm3_agent`The function first checks if `tags`the arguments are provided and converts them into a list form. Then, check `agent_kwargs`if the parameter is None, and if it is, initialize it as an empty dictionary. Next, use the`StructuredGLM3ChatAgent.from_llm_and_tools` class method to create an `StructuredGLM3ChatAgent`instance based on the provided Language model, toolset, prompts, and`agent_kwargs` other parameters in . Finally, use `AgentExecutor.from_agent_and_tools`the method to create and return an `AgentExecutor`instance that contains the chat agent, tool collection, chat history, and tags you just created. 

**Note**:
- When using `initialize_glm3_agent`functions, make sure that`tools` the sum `llm`arguments provided are valid instances, and`tools` that each tool implements the`BaseTool` interface. 
- `prompt`Parameters allow you to customize the chat agent's prompts, which can be provided as needed.
- `memory`Parameters are used to store and manage chat history, helping to achieve a more coherent conversation.
- `agent_kwargs`and `**kwargs`provides additional flexibility, allowing additional configuration options to be passed when creating a chat agent. 

**Example output**:
Assuming that a function is called `initialize_glm3_agent`and the necessary parameters are provided, an instance like the following might be returned`AgentExecutor`:
```
AgentExecutor(
    agent=StructuredGLM3ChatAgent(...),
    tools=[...],
    memory=ConversationBufferWindowMemory(...),
    tags=['example_tag']
)
```
In this example, the `AgentExecutor`instance contains a configured `StructuredGLM3ChatAgent`chat agent, along with the associated collection of tools, chat history, and tags. This instance can be used directly to process chat conversations, execute tool commands, and parse the output of the language model. 
