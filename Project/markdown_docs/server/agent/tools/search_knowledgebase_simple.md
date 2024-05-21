## FunctionDef search_knowledge_base_iter(database, query)
**search_knowledge_base_iter**: This function is used to search the knowledge base asynchronously and iteratively and get answers. 

**Parameters**:
- `database`: The name of the knowledge base, of type String.
- `query`: The content of the user's query, of type as a string.

**Code Description**:
`search_knowledge_base_iter` A function is an asynchronous function that takes two arguments:`database` and `query`. This function first calls `knowledge_base_chat` the function, passing in the appropriate parameters, including the knowledge base name, query content, model name, temperature parameters, history, top_k value of the vector search, the maximum number of tokens, the prompt name, the score threshold, and the flag of whether or not to stream the output. `knowledge_base_chat` The function is responsible for processing the user's query request and interacting with the knowledge base to return a response object. 

Internally, the function processes `response.body_iterator` the data in the response body through asynchronous iteration. The result for each iteration is `data` a JSON string that represents a subset of the query results. Functions use `json.loads` methods to parse JSON strings into dictionary objects, from which they extract answers and related documentation information. Eventually, the function returns the content of the answer obtained from the last iteration. 

**Note**:
- Since  is `search_knowledge_base_iter` an asynchronous function, you need to use a keyword when you call `await` it. 
- The function returns the answer content obtained from the last iteration, and if you need to process the data obtained from each iteration, you need to add the corresponding processing logic during the iteration.
- Make sure that the incoming knowledge base name already exists in the system, otherwise the query request may not be processed correctly.

**Example output**:
 `search_knowledge_base_iter` An example of what might be returned by calling the function:
```json
"This is an answer generated based on your query"
```
This output example only represents the format of the answer content that the function may return, and the actual content will vary depending on the query content and the data in the knowledge base.
## FunctionDef search_knowledgebase_simple(query)
**search_knowledgebase_simple**: This function is used to simplify the search of the knowledge base and get answers. 

**Parameters**:
- `query`: The content of the user's query, of type as a string.

**Code Description**:
`search_knowledgebase_simple` A function is a simplified interface for searching the knowledge base. It accepts a single parameter`query`, which is what the user is querying. Inside the function, `search_knowledge_base_iter` the  knowledge base is searched by calling the function. `search_knowledge_base_iter` is an asynchronous function that is responsible for iteratively searching the knowledge base and getting answers asynchronously. `search_knowledgebase_simple` Functions run `asyncio.run` asynchronous functions by using methods `search_knowledge_base_iter` , which can be called synchronously. 

Since `search_knowledge_base_iter` the function requires the database name and the query content as arguments, but `search_knowledgebase_simple` only the query content is provided in the function `query`, this means that in `search_knowledge_base_iter` the implementation of the function, the database name may be preset or obtained by other means. 

**Note**:
- `search_knowledgebase_simple` Functions provide a simplified interface that allows developers to search the knowledge base without having to deal with the complexity of asynchronous programming directly, but with a simple synchronous function call.
- Since the asynchronous function is called internally `search_knowledge_base_iter`, ensure that the relevant asynchronous environment and configuration are set up correctly when using this function. 
- Given `search_knowledge_base_iter` the asynchronous nature of functions and the possible iterative processing,  you `search_knowledgebase_simple` should be aware of possible delays or the impact of asynchronous execution when calling functions. 

**Example output**:
 `search_knowledgebase_simple` An example of what might be returned by calling the function:
```
"This is an answer generated based on your query."
```
This example of output represents the format of the answer content that the function might return, and the actual content will vary depending on the content of the query and the data in the knowledge base.
