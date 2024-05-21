## FunctionDef bing_search(text, result_len)
**bing_search**: This function is used to do a text search through the Bing search engine and return the search results. 

**Parameters**:
- `text`: The text content that needs to be searched.
- `result_len`: The number of search results returned, default.`SEARCH_ENGINE_TOP_K` 
- `**kwargs`: Accepts additional keyword parameters for extended or custom search behavior.

**Code Description**:
`bing_search`The function first checks whether and are set in the environment variables`BING_SEARCH_URL``BING_SUBSCRIPTION_KEY`. If these two environment variables are not set, the function will return a dictionary with error messages that the user needs to set them. The error message consists of a tooltip, a title, and a link to the relevant help documentation. 

If the environment variable is set correctly, the function will create an`BingSearchAPIWrapper` instance, using the provided`BING_SUBSCRIPTION_KEY` sum`BING_SEARCH_URL`. Then, using this instance to call `results`the method, pass in the text that needs to be searched`text` () and the number of results (`result_len`). Finally, return to the search results. 

**Note**:
- Make sure that you have set the environment variable sum correctly before using this function`BING_SEARCH_URL``BING_SUBSCRIPTION_KEY`, otherwise you will not be able to perform the search operation. 
- `result_len`Parameters allow the caller to customize the number of search results returned, but the actual returned results are also limited by the Bing Search API.
- Additional `**kwargs`search options can be passed to the Bing Search API via parameters, but you need to make sure that these options are supported by the API. 

**Example output**:
```python
[
    {
        "snippet": "这是搜索结果的摘要",
        "title": "搜索结果标题",
        "link": "https://example.com/search-result"
    },
    {
        "snippet": "这是另一个搜索结果的摘要",
        "title": "另一个搜索结果标题",
        "link": "https://example.com/another-search-result"
    }
]
```
This example shows a list of search results that a function might return, each containing`snippet` (summary), `title`(title), and`link` (link). 
## FunctionDef duckduckgo_search(text, result_len)
**duckduckgo_search**: This function is used to perform a text search through the DuckDuckGo search engine and return the results. 

**Parameters**:
- `text`: The text that needs to be searched.
- `result_len`: The number of returned results, the default value is`SEARCH_ENGINE_TOP_K`, which is a preset constant that specifies the default number of returned results. 
- `**kwargs`: Accepts additional keyword parameters that can be used to extend or customize search behavior.

**Code Description**:
`duckduckgo_search`The function first creates an `DuckDuckGoSearchAPIWrapper`instance, which is a class that encapsulates the DuckDuckGo search API call. With this instance, the function performs`results` a search using a method. `text`A parameter is the text content that the user wants to search, while `result_len`a parameter specifies the number of search results that they want to return. If not specified at the time of call`result_len`, it will be used `SEARCH_ENGINE_TOP_K`as the default. In addition, the function also accepts any additional keyword arguments(`**kwargs`), which provides additional flexibility, allowing the caller to pass more arguments to the search API as needed. 

**Note**:
- Make sure that the class is properly set up and configured before using this function`DuckDuckGoSearchAPIWrapper`, including any necessary authentication information or API keys. 
- `SEARCH_ENGINE_TOP_K`is a predefined constant that needs to be defined before using this function. It determines the default number of results that are returned when the number of results is not explicitly specified.
- Due to `**kwargs`the additional parameter passing function, care should be taken to include only the parameters supported by the DuckDuckGo search API when using it to avoid errors. 

**Example output**:
```python
[
    {"title": "DuckDuckGo", "snippet": "DuckDuckGo是一个注重隐私的搜索引擎。", "url": "https://duckduckgo.com"},
    {"title": "DuckDuckGo隐私政策", "snippet": "了解DuckDuckGo如何保护您的隐私。", "url": "https://duckduckgo.com/privacy"}
]
```
This output example shows a possible return value with a list of search results. Each result is a dictionary containing the title (`title`), summary (`snippet`), and URL(`url`). The actual results returned will vary depending on the text searched and the number of results specified. 
## FunctionDef metaphor_search(text, result_len, split_result, chunk_size, chunk_overlap)
**metaphor_search**: The function of this function is to do a metaphorical search based on the given text and return a list of search results. 

**Parameters**:
- `text`: The text to be searched for, of type as a string.
- `result_len`: The maximum number of results to be returned, default.`SEARCH_ENGINE_TOP_K` 
- `split_result`: Whether to split search results into smaller chunks of text, defaults`False`. 
- `chunk_size`: Splits the size of the text block, which is 500 characters by default.
- `chunk_overlap`: The number of overlapping characters when splitting a block of text, defaults`OVERLAP_SIZE`. 

**Code Description**:
This function first checks if it is provided`METAPHOR_API_KEY`, and if it is not, it returns an empty list directly. If provided, the function will create a client with this API key`Metaphor` and use that client to search for the given text. The number of search results is controlled by`result_len` parameters, and autoprompts are enabled by default. 

Each entry in the search results transforms `markdownify`its summary section through a function for better presentation. 

If `split_result`the parameter is`True`, the function will split the content of each search result to produce smaller chunks of text. These blocks of text are`RecursiveCharacterTextSplitter` split by a given splitter sum and`chunk_size` arguments`chunk_overlap`. Then, based on the similarity to the original search text, the text block with the highest similarity is selected`result_len` as the final result. 

If yes`split_result``False`, the summary, links, and titles of the search results are returned directly. 

**Note**:
- Make sure you have set it up correctly before using this function`METAPHOR_API_KEY`. 
- `SEARCH_ENGINE_TOP_K`and `OVERLAP_SIZE`need to be pre-defined according to the actual situation. 
- The function of splitting results is suitable for scenarios that require further analysis of long texts.

**Example output**:
```python
[
    {
        "snippet": "这是搜索结果的一个示例文本片段。",
        "link": "https://example.com/link-to-source",
        "title": "示例文本标题"
    },
    # 更多搜索结果...
]
```
This output example shows`split_result` `False`the format of the search results that a function might return when it is. Each result contains a text fragment (`snippet`), a source link (),`link` and a title (`title`). 
## FunctionDef search_result2docs(search_results)
**search_result2docs**: The function of this function is to convert the search results into a list of documents. 

**Parameters**:
- search_results: A list of search results, each of which is a dictionary containing at least one "snippet", "link", and "title" key.

**Code Description**:
`search_result2docs`The function takes a list of search results as input, iterates through the list, and creates an object for each result`Document`. This `Document`object contains the content of the page (provided by the "snippet" key in the result, an empty string if it does not exist), a source link (provided by the "link" key, an empty string if it does not exist), and a file name (provided by the "title" key, an empty string if it does not exist). This information is stored in`Document` the object's`page_content` sum `metadata`properties. Finally, all created `Document`objects are collected into a list and returned. 

In a project, `search_result2docs`a function is `lookup_search_engine`called by a function to process the search results returned from a particular search engine. `lookup_search_engine`The function first obtains the search results through the search engine based on the given query parameters and the name of the search engine, and then calls`search_result2docs` the function to convert these search results into`Document` a list of objects for further processing or display. 

**Note**:
- Make sure that the incoming list of search results is properly formatted and that each result dictionary contains at least three keys: "snippet", "link", and "title".
- The output of a function depends on the quality and completeness of the input search results.

**Example output**:
Let's say `search_results`the parameters are the following list:
```python
[
    {"snippet": "这是搜索结果的摘要", "link": "https://example.com", "title": "示例标题"},
    {"snippet": "第二个搜索结果的摘要", "link": "https://example2.com", "title": "第二个示例标题"}
]
```
The return value of the function might be a`Document` list of two objects, each with `page_content`"This is the summary of the search result" and "The summary of the second search result",`metadata` with the corresponding "source" and "filename" information. 
## FunctionDef lookup_search_engine(query, search_engine_name, top_k, split_result)
**lookup_search_engine**: The function of this function is to asynchronously query the specified search engine and return a list of documents after the search results have been converted. 

**Parameters**:
- `query`: A string type that represents the keyword to be queried in a search engine.
- `search_engine_name`: String type, specifying the name of the search engine to be queried.
- `top_k`: Integer, the default value is the `SEARCH_ENGINE_TOP_K`maximum number of search results returned. 
- `split_result`: Boolean type, default, `False`indicates whether to split the search results. 

**Code Description**:
`lookup_search_engine`The function first`search_engine_name` `SEARCH_ENGINES`obtains the corresponding search engine function from the dictionary through arguments. It then`run_in_threadpool` uses the function to run the search engine function asynchronously, passing in`query`, `result_len=top_k`and `split_result=split_result`as arguments to get the search results. The obtained search results are then passed to a`search_result2docs` function, which converts the search results into `Document`a list of document() objects. Eventually, this list of documents is returned. 

In a project, `lookup_search_engine`functions are called by `search_engine_chat_iterator`functions to get the results of search engine queries and convert those results into a list of documents to generate chat replies based on search engine results in the chat iterator. 

**Note**:
- Make sure that `search_engine_name`the search engine for the parameter has been`SEARCH_ENGINES` defined in the dictionary. 
- `top_k`Parameters control the number of search results returned, adjusting as needed for the optimal search experience.
- `split_result`Parameters can control whether the search results need to be split or not, depending on the specific implementation and needs of the search engine function.

**Example output**:
Assuming that the search query returns two results, the return value of the function might be a list of documents in the following format:
```python
[
    Document(page_content="这是搜索结果的摘要", metadata={"source": "https://example.com", "filename": "示例标题"}),
    Document(page_content="第二个搜索结果的摘要", metadata={"source": "https://example2.com", "filename": "第二个示例标题"})
]
```
Each object in this list `Document`contains a summary of the search results, a link to the source, and a title that can be used for further processing or presentation. 
## FunctionDef search_engine_chat(query, search_engine_name, top_k, history, stream, model_name, temperature, max_tokens, prompt_name, split_result)
**search_engine_chat**: This function is used to retrieve information through a search engine and generate responses in conjunction with historical conversations and LLM models. 

**Parameters**:
- `query`: The query entered by the user, of type as a string.
- `search_engine_name`: Specifies the name of the search engine to use, of type as a string.
- `top_k`: The number of search results, of type an integer.
- `history`: A list of historical conversations, each element of which is an`History` object. 
- `stream`: Whether to output the result as a stream, and the type is Boolean.
- `model_name`: Specifies the name of the LLM model to be used, of type String.
- `temperature`: The sampling temperature of the LLM model, which is used to control the diversity of the generated text, and is of type floating-point number.
- `max_tokens`: Limit the number of tokens generated by LLMs, of type integer or None.
- `prompt_name`: The name of the prompt template used, of type String.
- `split_result`: Whether to split the search results, mainly used in the metaphor search engine, the type is Boolean.

**Code Description**:
This function first checks whether the specified search engine supports it, and returns an error message if it is not supported or the required configuration items are not set. Then, convert the data from the list of historical conversations into`History` a list of objects. Next, an asynchronous iterator is defined `search_engine_chat_iterator`to perform search operations and generate answers. In this iterator, the values are first adjusted based on the conditions`max_tokens`, then an instance of the LLM model is created, and a search engine query is executed. Query results and historical dialogs will be used to build input prompts for the LLM model to generate answers. Depending on `stream`the value of the parameter, the function will output the result in different ways: if it is True, it will output each generated token and the final document list in streaming form; If false, all generated tokens will be concatenated into a complete answer and output at one time, with a list of documents attached. Finally, an object is returned`EventSourceResponse` that contains the execution result of the asynchronous iterator. 

**Note**:
- When using this function, you need to ensure that the specified search engine is supported in the project and that the relevant configuration items (such as API keys) are set correctly.
- `history`The parameter should be `History`a list of objects, each representing a historical conversation. 
- This function supports streaming output and is suitable for scenarios that need to display the generated results in real time.
- The execution of functions depends on external LLM models and search engine services, so the execution time may be affected by network conditions and service response time.

**Example output**:
```json
{
  "answer": "根据您的查询，这里是生成的回答。",
  "docs": [
    "出处 [1] [来源链接](http://example.com)\n\n相关文档内容。\n\n",
    "出处 [2] [来源链接](http://example.com)\n\n相关文档内容。\n\n"
  ]
}
```
If `stream`True, the output will be sent in steps as multiple json strings, each containing a token or list of documents. If False, a json string containing the full answer and document list will be output. 
### FunctionDef search_engine_chat_iterator(query, search_engine_name, top_k, history, model_name, prompt_name)
**search_engine_chat_iterator**: The function of this function is to asynchronously iterate over search engine query results and generate chat replies based on those results. 

**Parameters**:
- `query`: String type, the user's query request.
- `search_engine_name`: String type, specifying the name of the search engine to be queried.
- `top_k`: Integer, which specifies the maximum number of search results to be returned.
- `history`: An optional `List[History]`type that represents conversation history. 
- `model_name`: String type, defaults`LLM_MODELS[0]`, specifies the name of the language model to use. 
- `prompt_name`: String type, specifying the name of the prompt template to use.

**Code Description**:
`search_engine_chat_iterator`The value that the function checks first`max_tokens`, and if it's a non-positive integer, it sets it to`None`. Next, `get_ChatOpenAI`a function initializes an `ChatOpenAI`instance that is used to generate a language model-based chat response. The function uses `lookup_search_engine`an asynchronous query of the specified search engine, takes the search results, and converts those results into a text context. 

Next, the function `get_prompt_template`constructs a complete chat prompt by obtaining the specified prompt template and combining it with the conversation history. This prompt will be used as input to the language model to generate a chat response. The function creates an asynchronous task and`wrap_done` wraps the task with the function to notify you if the task completes or an exception occurs. 

The function also processes the document source information of the search results, formatting them into a specific list of strings. If no related document is found, a specific message is added indicating that the relevant document was not found.

Finally, depending on `stream`the value of the variable, the function may stream chat replies one by one, or merge all replies and return them all at once. In streaming mode, each generated reply is sent to the client immediately, while in non-streaming mode, it waits for all replies to be generated and returned uniformly. 

**Note**:
- When using this function, you need to make sure that the provided`search_engine_name` corresponds to the configured search engine. 
- `history`Parameters allow for the inclusion of a history of the conversation, which is important for generating more coherent and contextual responses.
- The function takes advantage of the asynchronous programming pattern, so you should be careful to use keywords when calling this function`await`. 
- Functions can take longer to execute when dealing with large or complex queries, so the user interface and interaction logic should be designed with potential latency in mind.
***
