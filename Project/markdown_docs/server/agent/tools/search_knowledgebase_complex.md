## FunctionDef search_knowledge_base_iter(database, query)
**search_knowledge_base_iter**: This function is used to search the knowledge base and get relevant information asynchronously and iteratively. 

**Parameters**:
- `database`: String type, specifying the name of the knowledge base to be searched.
- `query`: String type, the user's query string.

**Code Description**:
`search_knowledge_base_iter` A function is an asynchronous function that takes two arguments:`database` and `query`. This function interacts `knowledge_base_chat` with the knowledge base primarily by calling the function. When called `knowledge_base_chat` , relevant parameters are passed in, including the knowledge base name, query string, model name, temperature parameters, history, top_k value of the vector search, maximum number of tokens, prompt name, score threshold, and whether it is output as a stream. The specific values of these parameters are derived in part from global variables or variables outside of the function. 

Internally, the function processes `response.body_iterator` the returned data one by one through asynchronous iteration. The resulting data for each iteration is a JSON string that contains the answers and related documentation information. The function adds up these answers and returns the summed string at the end. 

**Note**:
- The function is asynchronous, so you need to use a keyword when you call `await` it. 
- The function handles the JSON data internally, so the module needs to be imported `json` . 
- Before you can use the function, you need to make sure that  the `knowledge_base_chat` function and its required environment and parameters are properly configured and initialized. 

**Example output**:
 `search_knowledge_base_iter` An example of a string that might be returned by calling a function:
```
"This is an answer generated based on your query. Source [1] [Document name] (Document link) \n\nDocument content\n\nNo relevant document found. This answer is based on the large model's own capabilities!"
```
The string contains the cumulative results of all responses, along with a link to the document and its content, if there is a related document. If you can't find the relevant document, you'll get a message.
## FunctionDef search_knowledge_multiple(queries)
**search_knowledge_multiple**: This function is used to asynchronously search multiple knowledge bases and get relevant information. 

**Parameters**:
- `queries`: A list of multiple tuples, each containing a database name and a query string.

**Code Description**:
`search_knowledge_multiple` A function is an asynchronous function that takes as arguments a list of multiple tuples (database name, query string). Internally, an asynchronous task is first created for each query in the list, which is implemented by calling `search_knowledge_base_iter` the  function, which is responsible for interacting with the specified knowledge base and getting the query results. After that, `asyncio.gather` use functions to execute these asynchronous tasks in parallel and wait for all tasks to complete, collecting their results. 

For the result of each query, the function generates a string containing the custom message and the results of the query. This custom message includes the name of the knowledge base, as well as a hint indicating from which knowledge base the information was queried. All of these generated strings are collected into a list and served as the return value of the function.

**Note**:
- Since `search_knowledge_multiple` is an asynchronous function, you need to use a keyword when calling it `await` . 
- The execution of functions depends on `search_knowledge_base_iter` functions, which need to be properly configured and initialized, including access settings and query parameters for the knowledge base. 
- The design of this function makes it possible to query multiple knowledge bases at the same time, which improves the query efficiency.

**Example output**:
 `search_knowledge_multiple` An example of a list that might be returned by calling a function:
```
[
"\nQuery related information of database1 knowledge base:\nThis is the answer generated based on your query. Source [1] [Document name] (Document link) \n\nDocument content\n\nNo relevant document found ,This answer is based on the ability of the large model itself! ",
 "\nQuery related information of database2 knowledge base:\nThis is the answer generated based on your query. Source [1] [Document name] (Document link) \n\nDocument content\n\nNo relevant document found ,This answer is based on the ability of the large model! "
]
```
This example of output shows that when two different knowledge bases are queried, each query result is preceded by a custom message indicating the source of the knowledge base, followed by the specific information queried.
## FunctionDef search_knowledge(queries)
Doc is waiting to be generated...
## ClassDef LLMKnowledgeChain
Doc is waiting to be generated...
### ClassDef Config
**Config**: The function of the Config class is to define a strict configuration pattern for pydantic objects. 

**Properties**:
- `extra`: Controls how extra fields are handled.
- `arbitrary_types_allowed`: Allows the use of any type of field.

**Code Description**:
The Config class is a configuration class that is specifically designed to define the configuration of a model when using the pydantic library. In this class, two important configuration items are defined:

1. `extra = Extra.forbid`: This parameter item is used to specify what should be done when the incoming data contains fields that are not declared by the model. By setting it to `Extra.forbid`disallow the incoming of additional fields, an error will be thrown if you try to pass in a field that is not declared in the model. This helps ensure strict match and type security of the data, avoiding problems caused by data errors or mismatches. 

2. `arbitrary_types_allowed = True`: This configuration item allows any type of field to be used in the model. By default, pydantic requires all field types to be predefined, but with this option turned on, any type of field can be used, including custom types. This provides more flexibility and allows developers to use a variety of complex or custom data types in their models as needed.

**Note**:
- When used`extra = Extra.forbid`, you need to ensure that all incoming data closely matches the fields defined by the model, otherwise an error will be thrown. This requires developers to be more careful and precise when designing models and working with data. 
- Enabling allows for greater `arbitrary_types_allowed = True`flexibility in the model, but it also requires developers to ensure that custom types are used and handled correctly to avoid type errors or other potential issues. 
***
### FunctionDef raise_deprecation(cls, values)
**raise_deprecation**: The function of this function is to warn when an LLMKnowledgeChain is instantiated using a deprecated method, and automatically convert to the recommended instantiation method if appropriate. 

**Parameters**:
- `cls`: The first argument of the class method, representing the class itself.
- `values`: A dictionary containing the parameters passed when instantiating an LLMKnowledgeChain.

**Code Description**:
`raise_deprecation` The function first checks if the incoming `values` dictionary contains a key `"llm"`. If it exists, it means trying to instantiate directly via arguments using the deprecated method `llm` `LLMKnowledgeChain`. At this point, the function issues a warning that the instantiation method is deprecated and suggests that a `llm_chain` parameter or `from_llm` class method be used instead. 

If there `values` is no `"llm_chain"` key  in and the `"llm"` value of the key is not , `None`the function will process it further. It tries to `values` get `"prompt"` the value of the key from , and if it doesn't exist, uses `PROMPT` the value of the global variable . Then, `llm` `prompt` create an instance with the value of `LLMChain` and  assign that instance to `values` the key  in the dictionary `"llm_chain"` . 

Finally, the function returns the updated `values` dictionary. 

**Note**:
- When using this function, you should make sure that `values` the value corresponding to the key in the incoming  dictionary `"llm"` (if it exists) is valid, as this will affect `LLMChain` the creation of the instance. 
- You should avoid using deprecated instantiation methods directly to avoid compatibility issues in future releases.

**Example output**:
Assuming that the incoming `values` dictionary is `{"llm": some_llm_object}`  and `PROMPT` is the default prompt text, the function might return a dictionary like this:
```python
{
"llm": some_llm_object,
 "llm_chain": LLMChain(llm=some_llm_object, prompt=default prompt text)
}
```
This means that even if you initially try to instantiate with the deprecated method, the function automatically adjusts to ensure that it is instantiated in the recommended way `LLMKnowledgeChain`. 
***
### FunctionDef input_keys(self)
**Function function**: `input_keys` The function is to return the desired list of input keys. 

****Arguments: This function has no arguments. 

**Code Description**:  A `input_keys` function is `LLMKnowledgeChain` a method of a class that returns a list of individual elements that are properties of that instance `input_key` . This method is marked as private, meaning that it is only `LLMKnowledgeChain` used inside the class, and it is not recommended to call it directly outside the class. This design is often used to encapsulate and hide the internal implementation details of the class, ensuring the simplicity and stability of the class's public interface. 

**Note**: Since `input_keys` the method is marked as private (indicated by `:meta private:` comments),  you `LLMKnowledgeChain` should avoid calling this method directly when using the class. Instead, the value of should be accessed or modified indirectly through other public methods provided by the class `input_key` . 

**Example output**:
```python
["example_input_key"]
```
In this example, assuming that `LLMKnowledgeChain` the value of the Instance `input_key` property is  , `"example_input_key"`then calling  the Method `input_keys` will return a list of the strings. This indicates that the instance expects only one input key, i.e`"example_input_key"`. . 
***
### FunctionDef output_keys(self)
**output_keys**: The function of this function is to return a list of output keys. 

****Arguments: This function has no arguments. 

**Code Description**:  A `output_keys` function is `LLMKnowledgeChain` a member method of a class that returns a list of elements that contain an element. `self.output_key` Here `self.output_key` is `LLMKnowledgeChain` a property of the instance, which represents the keyword of some kind of output. This function is marked as a private method (via `:meta private:` annotation), which means that it is primarily intended for other methods inside the class to be called, rather than designed for external use. 

**Note**: Since this function is marked as private, when using `LLMKnowledgeChain` a  class, you should avoid calling  the `output_keys` method directly, and instead indirectly get the required output key information through other public interfaces provided by the class. 

**Example output**:
```python
['desired_output_key']
```
In this example,`'desired_output_key'` the value of is `self.output_key` the output key that this instance expects. The return value is a list, and even if there is only one output key, it will be returned as a list, which keeps the interface consistent and extensible. 
***
### FunctionDef _evaluate_expression(self, queries)
Doc is waiting to be generated...
***
### FunctionDef _process_llm_result(self, llm_output, run_manager)
Doc is waiting to be generated...
***
### FunctionDef _aprocess_llm_result(self, llm_output, run_manager)
Doc is waiting to be generated...
***
### FunctionDef _call(self, inputs, run_manager)
Doc is waiting to be generated...
***
### FunctionDef _acall(self, inputs, run_manager)
Doc is waiting to be generated...
***
### FunctionDef _chain_type(self)
**Function name**: _chain_type

**Function function**: Returns a string representation of the chain type. 

****Arguments: This function has no arguments. 

**Code Description**: `_chain_type`A function is `LLMKnowledgeChain`a private method of a class that returns a string representing the type of the chain. In this context, the chain type is defined fixedly`"llm_knowledge_chain"`, which means that the string returned by the function is used to identify or represent a chain of knowledge based on the Long-term Language Model (LLM). This identifier can be used to distinguish LLM-based knowledge chains when dealing with different types of knowledge chains. Since this is a private method, it is primarily called by other methods inside the class, rather than directly by the outside of the class. 

**Note**: Since `_chain_type`it is a private method, it should only `LLMKnowledgeChain`be used inside the class. Attempting to call this method directly from outside the class may result in access control errors or undesirable behavior. 

**Example output**: 
```python
"llm_knowledge_chain"
```
This output example shows `_chain_type`the string that is returned when a method is called. This string can be thought of as an identifier that can be used to identify a particular LLM-based chain of knowledge when there may be multiple types of chains of knowledge. 
***
### FunctionDef from_llm(cls, llm, prompt)
**from_llm**: The function of this function is to create a chain of knowledge object from the language model. 

**Parameters**:
- `cls`: The first argument of the class method, which refers to the current class and is used to create an instance of the class.
- `llm`: BaseLanguageModel, which represents the language model to be used.
- `prompt`: An instance of BasePromptTemplate, which is set to PROMPT by default, and is used to generate a prompt template for queries.
- `**kwargs`: Accepts any number of keyword arguments that will be passed to the constructor of LLMKnowledgeChain.

**Code Description**:
`from_llm`is a class method that accepts a language model instance and an optional prompt template, as well as any other arbitrary keyword parameters. This method starts by creating an`LLMChain` instance that encapsulates the details of the language model and prompt template. It then uses this`LLMChain` instance and any other provided keyword arguments to create and return an `LLMKnowledgeChain`instance. This process allows the language model and associated configurations to be encapsulated into a chained object that can be used to perform complex knowledge search tasks. 

In a project, `from_llm`a method is `search_knowledgebase_complex`called by a function. In this call, it creates an instance of the model taken from the model container and a`verbose` keyword parameter`LLMKnowledgeChain`. This instance is then used to run an operation on a query to get an answer. This shows `from_llm`how the approach allows for the flexibility to build knowledge chains for use in complex knowledge search tasks. 

**Note**:
- Make sure that the argument you pass to`from_llm` `llm`is a valid `BaseLanguageModel`instance, as it is required to perform a knowledge search. 
- `prompt`Although the parameters are optional, they can significantly affect the performance of knowledge search when set correctly, so it is recommended to configure them appropriately according to specific application scenarios.
- Any `**kwargs`extra arguments passed through should be compatible with`LLMKnowledgeChain` the constructor to ensure that they can be used correctly. 

**Example output**:
Assuming the `from_llm`method is called correctly, it might return an instance of the following`LLMKnowledgeChain`:
```
LLMKnowledgeChain(llm_chain=LLMChain(llm=<BaseLanguageModel instance>, prompt=<BasePromptTemplate instance>), verbose=True)
```
This instance can then be used to perform specific knowledge search tasks.
***
## FunctionDef search_knowledgebase_complex(query)
Doc is waiting to be generated...
## ClassDef KnowledgeSearchInput
**KnowledgeSearchInput**: The function of the KnowledgeSearchInput class is to define an input model for searching the knowledge base. 

**Properties**:
- location: The query string used for searching.

**Code Description**:
The KnowledgeSearchInput class inherits from BaseModel, which indicates that it is a model class that defines data structures and types. In this class, a property called is defined`location`, which is labeled as a string type. By using`Field` a function, an `location`additional description of the property is provided, i.e., "query to be searched for". This makes the KnowledgeSearchInput class more than just a data container, but also enhances the readability and ease of use of the code through property descriptions. 

Although`server/agent/tools/__init__.py` there `server/agent/tools_select.py`is no direct mention of the use of the KnowledgeSearchInput class in the project, it can be inferred that the KnowledgeSearchInput class, as a data model, may be called by the part of the project that is responsible for searching the knowledge base function. Specifically, it may be used to encapsulate a user-fed search query, which is then passed to a function or method that performs the search to`location` retrieve relevant knowledge base entries based on the value in the property. 

**Note**:
- When using the KnowledgeSearchInput class, you need to make sure that `location`the value passed to the property is a valid string, as this will directly affect the results of the search. 
- Since the KnowledgeSearchInput class inherits from BaseModel, you can take advantage of the data validation capabilities provided by the Pydantic library to ensure the validity of the input data. This means that when instantiating a KnowledgeSearchInput object, an error will be thrown if the data type passed is not as expected, helping developers to identify and fix problems early.
