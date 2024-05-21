## ClassDef ApiRequest
**ApiRequest**: The function of the ApiRequest class is to encapsulate HTTP requests, simplifying the process of interacting with the API server. 

**Properties**:
- `base_url`: The base URL of the API server.
- `timeout`: The request timeout period, the default value is defined by `HTTPX_DEFAULT_TIMEOUT` . 
- `_use_async`: Whether to use asynchronous mode, default is False.
- `_client`: An instance of the httpx client used internally.

**Code Description**:
The ApiRequest class provides a simplified way to interact with the API server. It supports GET, POST, and DELETE HTTP methods, and can handle both synchronous and asynchronous requests. By managing the HTTPX client instance internally, it is able to efficiently reuse connections and improve request efficiency. In addition, the ApiRequest class provides support for streaming requests, as well as a convenient way to convert responses to JSON or other formats. 

- `client` Properties are responsible for creating and getting an HTTPX client instance. If the current instance is not created or is shut down, it is recreated according to the configuration.
- `get`, `post` , and `delete` methods correspond to HTTP GET, POST, and DELETE requests, respectively. These methods support a retry mechanism that automatically retries when a request fails. 
- `_httpx_stream2generator` The method converts the streaming response of httpx into a Python generator that makes it easy to process large amounts of data.
- `_get_response_value` Methods are used to process response data, and support converting responses to JSON or processing them through custom functions.
- Classes also contain a set of function-specific methods, such as `get_server_configs`, ,`list_search_engines` ,`get_prompt_template` , , 

In a project, the ApiRequest class is called by multiple modules, such as `dialogue_page`,`knowledge_base_page` , and , which `model_config_page` are used to interact with the backend API, including functions such as obtaining server configurations, executing dialogs, and managing knowledge bases. These calls demonstrate the practical use of the ApiRequest class in simplifying API calls. 

**Note**:
- When using the ApiRequest class, you need to make sure that `base_url` it  points to the API server correctly. 
- When dealing with asynchronous requests, you need to pay attention to `_use_async` the setting of the property and the corresponding asynchronous method calls. 

**Example output**:
Assuming the method is called `get_server_configs` , the possible return value is:
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "server_version": "1.0.0",
    "api_version": "1.0.0"
  }
}
```
This example shows a response to successfully get the server configuration with version information for the server and API.
### FunctionDef __init__(self, base_url, timeout)
**__init__**: The function of this function is to initialize the ApiRequest object. 

**Parameters**:
- `base_url`: String type, the default value is `api_address()`the return value of the function. The base URL used to specify the API request. 
- `timeout`: Floating-point number, default value.`HTTPX_DEFAULT_TIMEOUT` Specifies the timeout period for the request. 

**Code Description**: `__init__`A function is a `ApiRequest`constructor of a class that is responsible for initializing an instance of that class. During initialization, the property is first set`base_url`, and its value is obtained by default by calling `api_address`a function that returns the address of the API server. This step ensures that the`ApiRequest` object knows which server address to send the request to. Second, set `timeout`a property that defines the timeout period for network requests to avoid long hangs due to network issues. In addition, the function initializes two internally used properties:`_use_async` set to `False`indicate that asynchronous requests are not used by default; `_client`Initialization`None`, reserved as a storage location for HTTP client instances. 

From a functional point of view, `__init__`functions provide flexible initialization parameters (such as API server address and request timeout) that enable `ApiRequest`instances of the class to make customized network requests according to different needs. By calling`api_address` a function to obtain the API server address, the `ApiRequest`class shares a unified server address configuration with the rest of the project, which helps to maintain the consistency and configurability of the project. 

**Note**: When using `ApiRequest`classes, you need to make sure that the API server address in the project configuration file (obtained via`api_address` the function) is correct. In addition, considering that network requests may fail for various reasons,`ApiRequest` exception handling should be done when using classes for network requests. 
***
### FunctionDef client(self)
**client**: The function of this function is to get or create an instance of the httpx client. 

**Parameters**: This function does not accept any external parameters. 

**Code Description**: `client` The function first checks `_client` whether the property  is or `None` whether the client instance is closed (as determined by  the `is_closed` property). If any of these conditions are met, the function will `get_httpx_client` create a new instance of the httpx client by calling the function and assign it to the `_client` property. When you create a client instance, you pass several key parameters to `get_httpx_client` the  function, including `base_url`(base URL), `use_async`(whether to use an asynchronous client), and `timeout`(request timeout). The values of these parameters are derived from `ApiRequest` the properties of the class. If it `_client` already exists and is not closed, the function will return directly`_client`. 

**Note**:
- `_client` is `ApiRequest` a private property of the class that stores an instance of the httpx client. 
- `get_httpx_client` Functions are used to create and configure an HTTPX client instance and can be created as a synchronous or asynchronous client, depending on `use_async` the value of the parameter. 
- When the function is called multiple times `client` , if there is already an open client instance, the instance is reused to avoid creating new client instances frequently. 

**Output example**: Since the output of this function is an instance of an httpx client, the output example will depend on how to use that instance to make HTTP requests. For example, the code for making a GET request using this client instance might look like this:
```python
api_request = ApiRequest()  # Assume ApiRequest is an instance of the class containing the client function
httpx_client = api_request.client()
response = httpx_client.get('https://www.example.com')
print(response.text)
```
In this example, `ApiRequest` an instance of the class `api_request` is created, then  an httpx client instance `client`is called by calling `httpx_client`the function, and finally a GET request is made with that client instance and the response is printed. 
***
### FunctionDef get(self, url, params, retry, stream)
**get**: The function of this function is to get the data of the specified URL via an HTTP GET request. 

**Parameters**:
- `url`: String type, specifying the URL of the request.
- `params`: An optional parameter, dictionary, list (containing tuple), or byte type, to specify the query parameters for the request.
- `retry`: An integer, an optional parameter, with a default value of 3, specifies the number of retries when a request fails.
- `stream`: Boolean type, optional, default value is False, specifies whether to obtain the response content in the form of a stream.
- `**kwargs`: Receive any additional keyword arguments that will be passed directly to the request method of httpx.

**Code Description**:
This function is primarily used to perform HTTP GET requests. It first tries to`client` get an instance of the httpx client using a method, and then`stream` decides whether to call `client.stream`the method to get the response in the form of a stream, or to `client.get`call the method to get the full content of the response, based on the value of the parameter. If an exception occurs during the request, the function records an error message and`retry` decides whether to retry the request based on the value of the parameter. The number of retries `retry`is reduced by one after each exception is caught, until the number of retries is exhausted. If the request succeeds before the number of retries is exhausted, the function will return the response. Otherwise, it may be returned`None`. 

**Note**:
- Functions may encounter various exceptions during the request process, such as network connection issues, server errors, etc. These exceptions are caught and logged, but not thrown directly to avoid interrupting the execution of the program.
- Parameters allow `**kwargs`users to pass additional options to httpx requests, such as custom request headers, timeout settings, etc., which provides a high degree of flexibility. 
- The use of `stream`parameters can reduce memory consumption when working with large files or real-time data, as it allows the response content to be processed block by block. 

**Example output**:
Because the return value of this function depends on the response of the request, the output example will vary depending on the context in which it was called. For example, if the request is successful and no streaming response is used, a function might return an`httpx.Response` object whose properties and methods can be used to access information such as the response status code, response headers, and response content. If you use a streaming response, the function will return an iterator that allows the response to be read chunk-by-block. 
***
### FunctionDef post(self, url, data, json, retry, stream)
**post**: This function is used to perform HTTP POST requests. 

**Parameters**:
- `url`: String type, specifying the URL of the request.
- `data`: Dictionary type, default to None, used to specify the form data to be sent.
- `json`: Dictionary type, default to None, used to specify JSON data to send.
- `retry`: Integer, set to 3 by default, specifies the number of retries when the request fails.
- `stream`: Boolean type, default to False, specifies whether to receive the response content in the form of a stream.
- `**kwargs`: Receive any additional keyword arguments that will be passed directly to the request method of httpx.

**Code Description**:
This function first checks if the number of retries `retry`is greater than 0. If yes, try to perform a POST request. Depending on `stream`the value of the parameter, decide whether to call the method or method of the httpx client`stream` `post`to send the request. If an exception occurs during the request, the exception is caught, the error message is logged, and then the number of retries is reduced by one, and the attempt to send the request continues until it succeeds or the number of retries is exhausted. The logging of exception information depends on`logger.error` the method, which includes the exception type, error message, and optional exception information (depending on`log_verbose` the value of the variable). 

**Note**:
- The function is used internally `self.client`to obtain an httpx client instance, and the creation and configuration of the instance are detailed in`client` the function documentation. 
- When `stream`the parameter is True, the `client.stream`method is used to receive the response in a stream, which is suitable for processing large amounts of data. 
- You `**kwargs`can pass additional parameters to the httpx request method, such as custom request headers, timeout settings, etc. 
- The function catches and handles all exceptions, ensuring the robustness of network requests.

**Example output**:
Since the return value of this function depends on the response of the request, the specific output example will vary depending on the request URL and parameters. In most cases, if you do not use the streaming mode, the return value may be an `httpx.Response`object, through which you can access information such as response status codes, response headers, and response bodies. If you're using a stream pattern, the return value might be an iterator that processes the response content chunk-by-block. If the request fails and the number of retries is exhausted, None may be returned. 
***
### FunctionDef delete(self, url, data, json, retry, stream)
**delete**: The function of this function is to delete the specified resource through an HTTP delete request. 

**Parameters**:
- `url`: String type, specifying the URL of the resource to be deleted.
- `data`: Dictionary type, default to None, which is used to specify the body of data to be sent.
- `json`: Dictionary type, default to None, used to specify JSON data to send.
- `retry`: Integer, set to 3 by default, specifies the number of retries when the request fails.
- `stream`: Boolean type, default to False, specifies whether to receive response data in the form of a stream.
- `**kwargs`: Receive any additional keyword arguments that will be passed directly to the request method of httpx.

**Code Description**:
This function is mainly used to send HTTP DELETE requests to delete the specified resource. It first `retry`tries to send the request based on the number of times specified by the parameter. During the attempt, if`stream` the parameter is set to True, the method will `client.stream`be used to send a DELETE request in the form of a stream. Otherwise, use methods to`client.delete` send normal DELETE requests. Here'`client`s an instance of the httpx client that is fetched by`ApiRequest` a method of `client`the class, which is responsible for the actual network communication. During the request, if an exception is encountered, the exception is captured, the error message is recorded, and then`retry` the error is decided whether to try again based on the parameters. Before each retry,`retry` the value is reduced by 1 until it reaches 0. 

**Note**:
- When using this function, you need to make sure that the parameters passed in`url` are valid and that you have permission to perform the DELETE operation. 
- If the server responds with a large amount of content, setting`stream` it to True can reduce memory usage. 
- Through `**kwargs`parameters, you can pass additional request options, such as custom headers, timeout periods, etc., to meet different request requirements. 
- A function may return`httpx.Response` an object, `Iterator[httpx.Response]`an object (if `stream`true), or Never if the number of retries is exhausted and still fails. 

**Example output**:
Since the output of this function is dependent on the actual request and server response, here's an example of a possible return value:
```python
response = api_request.delete('https://www.example.com/resource')
if response:
    print(response.status_code)
else:
    print("Request failed, retried the specified number of times.")
```
In this example, you first try to delete the resource at the specified URL, and then determine whether the request is successful based on the return value. If the request is successful, print out the status code of the response. If the request fails and the number of retries is exhausted, the failure message is printed.
***
### FunctionDef _httpx_stream2generator(self, response, as_json)
**_httpx_stream2generator**: The function of this function is to convert the GeneratorContextManager returned by httpx.stream into a normal generator in order to handle asynchronous or synchronous HTTP stream responses. 

**Parameters**:
- `response`: contextlib._GeneratorContextManager type, which indicates the response flow of an httpx request.
- `as_json`: Boolean type, which is set to False by default, specifies whether to parse the data in the stream to JSON format.

**Code Description**:
_httpx_stream2generator function is designed to process HTTP stream responses from the httpx library. It provides both asynchronous and synchronous processing methods, depending on the _use_async properties of the ApiRequest object. When working with an asynchronous flow, it`async with` uses statements to manage the response context and `aiter_text`responds to the content by iterating asynchronously. For synchronous flows,`with` use statements and `iter_text`methods to iterate over the response content. Either way, the function checks each chunk and if the `as_json`argument is True, it tries to parse the chunk as a JSON object; Otherwise, the data block is returned directly. 

When parsing JSON, the function specifically handles chunks of data that start with "data:"", which is typically used for server send events (SSE). If the datablock starts with ":", it is considered a comment line of SSE and skipped. If an exception is encountered during parsing the JSON, the function logs the error message and proceeds to the next chunk.

In addition, the function handles several exceptions, including failure to connect to the API server, API communication timeouts, and other communication errors, logs these exceptions, and generates a JSON object containing error codes and messages as output from the generator.

In a project, _httpx_stream2generator functions are called by multiple API request methods, such as`chat_chat` , ,`agent_chat``knowledge_base_chat` `file_chat`,`search_engine_chat` These methods interact with backend services through APIs to get real-time data streams. By using _httpx_stream2generator functions, these methods are able to process streaming data from back-end services in a unified and efficient way. 

**Note**:
- When using this function, you need to make sure that the response parameter passed in is a valid httpx response stream object.
- When processing large amounts of data or requiring real-time responses, the right choice of asynchronous or synchronous mode can have a significant impact on performance.

**Example output**:
```python
# If as_json is True and the data in the stream is in JSON format
{"name": "example", "value": 123}

# If as_json is False
"data: example stream data\n"
```
#### FunctionDef ret_async(response, as_json)
**ret_async**: The function of this function is to process HTTP responses asynchronously, decide whether to parse the response content as JSON based on the parameters, and return the data in the form of a generator. 

**Parameters**:
- `response`: An asynchronous HTTP response object that supports asynchronous context management and asynchronous iteration.
- `as_json`: A boolean value indicating whether the response content should be parsed to JSON.

**Code Description**:
`ret_async` A function is an asynchronous generator that processes responses from HTTP requests. It first attempts to interact asynchronously with the response object. By iterating over each block of text that responds to the content, the function can`as_json` determine how it is processed based on the value of the parameter. 

- When `as_json`True, the function attempts to parse each block into JSON. If the block `data: `starts with it, it tries to parse the JSON after removing the prefix and suffix; If the block starts with a colon`:`, it is treated as an SSE (Server-Sent Events) comment line and skipped; Otherwise, just try to parse the entire block as JSON. After the parsing is successful, the parsed data is used as the next value of the generator. If parsing fails, an error message is logged and the next block is processed. 

- When `as_json`False, the text block is directly used as the next value of the generator, and no JSON parsing is performed. 

The function also handles several exceptions, including connection errors (`httpx.ConnectError`), read timeouts (`httpx.ReadTimeout`), and other exceptions. When these exceptions are encountered, the corresponding error message is logged and a dictionary containing the error code and message is generated as the next value of the generator. 

**Note**:
- When using this function, you need to make sure that the incoming`response` object supports asynchronous operations. 
- There are a number of exceptions that are caught and handled internally by the function, and the caller should be careful to handle the dictionary of error messages that the generator may produce.
- Because the function uses an asynchronous feature, it needs to be used in an asynchronous environment to get the data when you call it`async for`. 
- The error log of a function depends on external`logger` objects and `log_verbose`variables, and you need to ensure that these dependencies are properly configured in the context in which they are called. 
***
#### FunctionDef ret_sync(response, as_json)
**ret_sync**: This function is used to synchronously process HTTP responses and convert the response content to JSON or direct text as needed. 

**Parameters**:
- `response`: An HTTP response object that should support a context management protocol as well as a way to iterate over the content of the text.
- `as_json`: Boolean value indicating whether the response content should be parsed to JSON.

**Code Description**:
`ret_sync` The function first tries to process the incoming HTTP response. Use `response`the object's context manager to ensure that responses are handled securely. The function iterates over each chunk of text of the response content, skipping any empty chunks, which is to handle the null bytes that some APIs might send at the beginning and end. 

If `as_json`the argument is true, the function attempts to parse the text block into JSON. In particular, if a block of text starts with "data:", the function will try to parse the JSON after removing the prefix and the last two characters; If the text block starts with ":", it is considered a comment line of SSE (Server-Sent Events) and skipped; Otherwise, directly try to parse the entire block of text into JSON. If any exceptions are encountered during parsing, error messages are logged, and`log_verbose` detailed exception information is decided based on the value of the variable. 

If `as_json`the argument is false, the function returns the text block directly as part of the iterator without JSON parsing. 

The function also handles several specific exceptions, including connection errors (`httpx.ConnectError`), read timeouts (`httpx.ReadTimeout`), and other exceptions. In these cases, the appropriate error message is logged and an iterator is returned with a dictionary containing the error code and message. 

**Note**:
- When you use this function, you need to ensure that the incoming `response`object supports the desired action, including context management and text iteration. 
- When choosing to parse a response in JSON format, care should be taken to handle possible parsing errors and be prepared to receive error messages.
- The Exception Handling section shows how to handle specific connection and timeout errors, which is useful for debugging and error handling.
- This function is designed with responses in SSE (Server-Sent Events) format, which is very common in real-time data transmission.
***
***
### FunctionDef _get_response_value(self, response, as_json, value_func)
**_get_response_value**: The function of this function is to transform the HTTP response object and return the processed data according to the specified parameters. 

**Parameters**:
- `response`: httpx. Response object, which represents an HTTP response.
- `as_json`: Boolean, defaults to False. When set to True, the function attempts to parse the response body to JSON.
- `value_func`: A callable object, which defaults to None. This parameter allows the user to pass in a function, which receives a parameter (the response body or its JSON parsing result) and returns the processed data.

**Code Description**:
This function is primarily used to process response data for API requests. It provides flexible processing methods, including direct return of the response body, return the JSON parsing result of the response body, or`value_func` customize the processing logic through parameters. Inside the function, an internal function is defined to `to_json`try to parse the response body into JSON, and if parsing fails, the error message is logged and a dictionary containing the error code and information is returned. Then, according to the`_use_async` attributes, determine whether the asynchronous mode is currently used, and choose the synchronous or asynchronous processing mode accordingly. If`as_json` the parameter is True, the `to_json`response body is processed using a function; If the user `value_func`provides a custom handler via a parameter, the final returned data is processed by that function. 

In a project, `_get_response_value`a function is called by multiple API request functions that are used to process the HTTP responses obtained by these functions. For example, this function is used to process response data in scenarios such as getting server configurations, listing search engines, and getting hint templates, and parse responses to JSON or further processing through custom functions as needed. This design makes the processing of response data more flexible and uniform. 

**Note**:
- When using `as_json`parameters, you need to make sure that the response body can be successfully parsed to JSON, otherwise an error message will be returned. 
- If parameters are provided`value_func`, you need to ensure that the incoming function can correctly process the input data (the response body or its JSON parsing result) and return the desired result. 

**Example output**:
Assuming that the response body is`{"code": 200, "msg": "success", "data": {"key": "value"}}` and `as_json`the parameter is True, and no argument is provided`value_func`, the return value of the function might be:
```python
{"code": 200, "msg": "success", "data": {"key": "value"}}
```
#### FunctionDef to_json(r)
**to_json**: The function of this function is to convert the response object to JSON format. 

**Parameters**:
- r: The response object that needs to be converted to JSON format.

**Code Description**:
`to_json`Functions are designed to process API responses, attempting to convert the response object`r` to JSON format. In this process, the function first tries to `r.json()`parse the response using a method. If any exception is encountered during parsing (e.g., the response content is not in valid JSON format), the exception is caught and a JSON object containing the error code 500, the error message, and empty data is constructed to return. Error messages are appended with exception information for easy debugging and error tracking. If verbose logging is enabled (`log_verbose`true), error messages and exception types are logged to the log for subsequent analysis. 

In a project, `to_json`functions are `ret_async`called by functions and are used to process API responses asynchronously. In`ret_async` , the `as_json`value of the parameter decides whether the response needs to be converted to JSON. If needed,`ret_async` the obtained response object is processed using`to_json` a function`await`, and then the converted JSON data is passed to the `value_func`function for further processing. This shows that `to_json`functions play a key role in processing asynchronous API responses. 

**Note**:
- When using `to_json`functions, you need to make sure that the incoming response object has a`.json()` method, which usually means that the object is an HTTP response object. 
- Exceptions caught inside a function are extensive, so when calling this function, you should be careful with exception handling to avoid hiding potential errors.

**Example output**:
If the response content is valid JSON, for example`{"name": "test"}`, the `to_json`function will return this JSON object.
If the response content is not valid JSON, assuming a parsing exception occurs, the function may return a JSON object in the following format:
```json
{
  "code": 500,
  "msg": "The API failed to return the correct JSON. Parsing error message",
  "data": None
}
```
***
#### FunctionDef ret_async(response)
**ret_async**: The function of this function is to process the API response asynchronously and convert it to JSON format or return it directly as needed. 

**Parameters**:
- response: The asynchronous response object that needs to be processed.

**Code Description**:
`ret_async`Functions are designed to handle API responses asynchronously. It accepts a `response`parameter, which is an asynchronous response object. The function internally first decides whether the response needs to be converted to JSON format, which is determined by checking`as_json` the value of the variable. If `as_json`true, the function is called `to_json`to convert the response to JSON format; Otherwise, the response content is returned directly. 

In the process of converting to JSON format, the`ret_async` function uses `await`the keyword to wait for `response`the asynchronous operation of the object to complete, and then passes the result to the `to_json`function for processing. Once the processing is complete, the converted JSON data is passed to the`value_func` function for further processing. 

If you don't need to convert the response to JSON format, the`ret_async` function also uses `await`the keyword to wait for the asynchronous operation of the response content to complete, and then passes the result directly to the`value_func` function. 

This function demonstrates the application of asynchronous programming when handling API responses, especially when it comes to the need to convert response data or perform other processing.

**Note**:
- When you call `ret_async`a function, you need to make sure that the incoming`response` object supports asynchronous operations. 
- `as_json`Variables and `value_func`functions are not defined in the code snippet and need to be `ret_async`provided in the context in which the function is called. 
- `to_json`The function is used to convert the response object to JSON format, so when `as_json`it is true, you need to make sure that the response object can be successfully converted. 

**Example output**:
- If `as_json`true, and the response content is valid JSON, for example`{"name": "test"}`, a `ret_async`function may return `value_func`a processed JSON object. 
- If `as_json`false, assuming the response content is the string "response content", the`ret_async` function will return `value_func`the processed string "response content". 
***
***
### FunctionDef get_server_configs(self)
**get_server_configs**: This function is used to get server configuration information. 

**Parameters**:
- `**kwargs`: A variablekey argument that allows you to pass any number of parameter names and their corresponding values, which will be passed directly to the internal`post` method. 

**Code Description**:
`get_server_configs`The function `post`sends an HTTP POST request to the server by calling a method with the URL of the request`"/server/configs"`. The function accepts any number of keyword arguments ()`**kwargs` that will be passed directly to the `post`method. After sending the request, the function processes the response by calling`_get_response_value` a method, converting the response body to a dictionary in JSON format and returning it. `_get_response_value`The method supports parsing the response body to JSON, and the processing logic can be customized through the input parameters to meet different data processing needs. 

**Note**:
- When you use this function, you can`**kwargs` pass additional parameters to `post`the method, such as custom request headers and timeout settings, which provides flexible request configuration capabilities. 
- Functions depend on `post`methods to send HTTP requests, so their performance and exception handling capabilities are`post` closely tied to the implementation of methods. 
- The returned data is in JSON format, and the caller should ensure that the data in JSON format is processed.

**Example output**:
`get_server_configs`Here's an example of what a function might return by calling a function:
```python
{
    "code": 200,
    "msg": "success",
    "data": {
        "config1": "value1",
        "config2": "value2",
        // More configuration items...
    }
}
```
This example shows a standard response structure with status codes, messages, and data, with `data`fields that contain details of the server configuration. The actual data structure returned may vary depending on the configuration of the server. 
***
### FunctionDef list_search_engines(self)
**list_search_engines**: This function is used to make a list of available search engines. 

**Parameters**:
- `**kwargs`: Receive any additional keyword arguments that will be passed directly to the internal POST request method.

**Code Description**:
`list_search_engines` The function `/server/list_search_engines`fetches a list of available search engines by sending an HTTP POST request to the path. It uses`post` a method to execute this request, and can accept any additional keyword arguments ()`**kwargs` that will be passed directly to the `post`method. After the response is obtained, the function processes `_get_response_value`the response data using a method that parses the response body into JSON format and extracts`data` the value of the field from it as the final result. 

**Note**:
- Functions internally depend on `post`methods to send HTTP requests, so ensuring that `post`methods execute correctly is a prerequisite for using this function. 
- Functions also rely on `_get_response_value`methods to process response data, ensuring that the method correctly parses the response body and extracts the required data. 
- Since this function can accept any additional keyword parameters, this provides some flexibility, such as customizing the HTTP request header or setting timeouts.

**Example output**:
Assuming that the response body returned by the server side is`{"code": 200, "msg": "success", "data": ["Google", "Bing", "DuckDuckGo"]}`, the `list_search_engines`return value of the function will be a list as follows:
```python
["Google", "Bing", "DuckDuckGo"]
```
This list contains all available search engine names.
***
### FunctionDef get_prompt_template(self, type, name)
**get_prompt_template**: This function is used to get a prompt template of the specified type and name. 

**Parameters**:
- `type`: String type, default value is llm_chat, which is used to specify the prompt template type for the request.
- `name`: String type, default is "default", which is used to specify the name of the prompt template for the request.
- `**kwargs`: Receives any additional keyword arguments that will be passed directly to the internal`post` method. 

**Code Description**:
`get_prompt_template`The function first constructs a`type` dictionary containing`name` the sum`data`, and then uses `post`the method to send a request to the server with the URL of the request`/server/get_prompt_template`, and passes the `data`dictionary as JSON data. In addition, any `**kwargs`additional arguments passed through are passed directly to the`post` method. The received response is processed through`_get_response_value` a method that allows `value_func`the processing logic of the response value to be customized via parameters. In this function, `value_func`it is set up as a lambda function that receives the response object and returns its textual content. As a result, the`get_prompt_template` function ends up returning the textual content of the server's response. 

**Note**:
- Functions send HTTP POST requests internally through `post`methods, so it is necessary to ensure the stability of the network connection. 
- `_get_response_value`Methods are used to process response data, and the processing logic can be customized as needed, but only the text content of the response is returned in this function.
- Through `**kwargs`parameters, you can `post`pass additional request parameters to the method, such as custom request headers, timeout settings, etc., which increases the flexibility of the function. 

**Example output**:
Assuming that the server returns text content for the requested prompt template`"Welcome to the chat!"`, the function might return a value of:
```
"Welcome to the chat!"
```
This output example shows what the function might return if it successfully fetches a prompt template. The actual content returned will vary depending on the server's response.
***
### FunctionDef chat_chat(self, query, conversation_id, history_len, history, stream, model, temperature, max_tokens, prompt_name)
**chat_chat**: This function is used to handle API requests related to chats. 

**Parameters**:
- `query`: String type, the content of the user's query.
- `conversation_id`: A string type, which defaults to None, and represents a unique identifier for a session.
- `history_len`: Integer, which is -1 by default, indicates the number of historical messages to be considered.
- `history`: List type, default is empty list, a list containing the content of historical conversations, each element is a dictionary.
- `stream`: Boolean type, which is True by default, specifies whether to receive the response content in a streaming mode.
- `model`: String type, which defaults to the first element of the LLM_MODELS list, specifying the Language model used.
- `temperature`: The floating-point type, which defaults to TEMPERATURE, controls the creativity of the generated text.
- `max_tokens`: Integer, optional, defaults to None, specifies the maximum number of tokens for generating text.
- `prompt_name`: String type, default is default, specifies the name of the prompt template to use.
- `**kwargs`: Receive any additional keyword parameters.

**Code Description**:
The function first constructs a dictionary containing all the parameters required for the request`data`, and then uses the `self.post`method to send a POST request to the "/chat/chat" path, which is a`data` dictionary. When requesting, the `stream`parameter is set to True, which means that the response content is received in a stream. Finally, the function calls `self._httpx_stream2generator`a method that converts the stream response returned by the httpx library into a normal generator, specifying that the data in the stream is parsed in JSON format, and finally returns the generator. 

**Note**:
- A method is called inside the function `post`to send an HTTP POST request, and the detailed description of the method can be found`post` in the function's documentation. 
- The function also calls `_httpx_stream2generator`a method to handle the streaming response, and a detailed description of the method can be found`_httpx_stream2generator` in the function's documentation. 
- Parameters`**kwargs` allow you to `post`pass additional HTTP request parameters to a method, such as custom request headers or timeout settings. 
- Functions are designed to support streaming responses and are suitable for scenarios that work with real-time data or large amounts of data.

**Example output**:
Since the function returns a generator, the exact output depends on the content of the response. Here's an example of a possible output, assuming the data in the stream is in JSON format:
```python
{
    "text": "This is the response generated by the model.",
    "message_id": "123456789"
}
```
In practice, the generator will gradually generate such JSON objects, each containing information such as text and message IDs generated by the model.
***
### FunctionDef agent_chat(self, query, history, stream, model, temperature, max_tokens, prompt_name)
**agent_chat**: This function is used to process requests for agent chats and send queries to backend services. 

**Parameters**:
- `query`: String type, the content of the user's query.
- `history`: A list type, which defaults to an empty list and contains a dictionary-type element that is used to pass the conversation history.
- `stream`: Boolean type, which is True by default, specifies whether to receive the response content in a streaming mode.
- `model`: String type, which defaults to the `LLM_MODELS`first element of the list and is used to specify the model for handling the request. 
- `temperature`: Floating-point type, default, `TEMPERATURE`which controls the diversity of generated text. 
- `max_tokens`: Integer, an optional parameter, that specifies the maximum number of tokens for which text can be generated.
- `prompt_name`: String type, default is "default", which specifies the name of the prompt template to use.

**Code Description**:
`agent_chat`The function first constructs a dictionary containing the request parameters`data`, and then uses the `self.post`method to send a POST request to the `/chat/agent_chat`endpoint. The request receives the response in a stream. The function finally calls `_httpx_stream2generator`a method that converts the stream response to httpx into a normal generator to facilitate the processing of asynchronous or synchronous HTTP stream responses and uses them as return values. 

**Note**:
- This function depends on `post`the method to send HTTP POST requests, and `post`the detailed behavior of the method is described in`post` the function documentation. 
- `agent_chat`The return value of a function is a generator that allows the caller to stream response data from a backend service. This is especially useful for scenarios that deal with large amounts of data or require real-time responses.
- `LLM_MODELS``TEMPERATURE`and are used in the function and these two global variables, which need to be defined outside the function. 

**Example output**:
Since `agent_chat`the function returns a generator, its output depends on the response of the backend service. Assuming that the data returned by the backend service is in JSON format and`as_json` the parameter is True, the possible output example is:
```python
{
    "answer": "This is a sample answer.",
    "confidence": 0.95
}
```
If `as_json`the parameter is false, the original text data returned by the backend service may be directly output. 
***
### FunctionDef knowledge_base_chat(self, query, knowledge_base_name, top_k, score_threshold, history, stream, model, temperature, max_tokens, prompt_name)
**knowledge_base_chat**: This function is used to have a chat conversation through the knowledge base. 

**Parameters**:
- `query`: String type, the user's query statement.
- `knowledge_base_name`: String type, specifying the name of the knowledge base to be queried.
- `top_k`: Integer, the default value is VECTOR_SEARCH_TOP_K, specifies the upper limit of the number of related knowledge items to be returned.
- `score_threshold`: Floating-point type, the default value is SCORE_THRESHOLD, and sets the score threshold for returning knowledge entries.
- `history`: List type, which is an empty list by default, contains historical conversation records of the dictionary type.
- `stream`: Boolean type, which is True by default, specifies whether to receive the response content in a streaming mode.
- `model`: String type, which defaults to the first element of the LLM_MODELS list, specifying the Language model used.
- `temperature`: floating-point type, the default value is TEMPERATURE, which controls the diversity of generated text.
- `max_tokens`: Integer, optional, specifies the maximum number of tokens for which text can be generated.
- `prompt_name`: String type, default is default, specifies the name of the prompt template to use.

**Code Description**:
The function first constructs a dictionary with all the input parameters`data`, and then uses `self.post`the method to `/chat/knowledge_base_chat`send a POST request to the path and passes `data`it as JSON data. The response to the request is received as a stream, and `self._httpx_stream2generator`the response stream of httpx is converted into a normal generator by calling the method to facilitate the processing of asynchronous or synchronous HTTP stream responses. The method returns a generator that iteratively fetches the processed response data. 

**Note**:
- The function calls a `self.post`method internally to send an HTTP POST request, and the detailed behavior of this method can be found`post` in the function documentation. 
- The response stream is processed by `self._httpx_stream2generator`a method, and the detailed behavior of the method can be found in`_httpx_stream2generator` the function's documentation. 
- The behavior of a function is influenced by the parameters passed in, in particular the`stream` parameters that determine how the content of the response is received. 
- When using this function, you need to make sure that the `knowledge_base_name`knowledge base specified by the parameter already exists and is available. 

**Example output**:
Since the function returns a generator, the output example will depend on the specific response content. Assuming that the content of the response is data in JSON format, a possible output example would be:
```python
{
    "answer": "This is the answer retrieved from the knowledge base based on your query.",
    "docs": [
        {"title": "Document 1", "content": "Contents of Document 1", "score": 0.95},
        {"title": "Document 2", "content": "Contents of Document 2", "score": 0.90}
    ]
}
```
In practice, the generator will gradually generate data blocks in the above format until all relevant response data has been processed.
***
### FunctionDef upload_temp_docs(self, files, knowledge_id, chunk_size, chunk_overlap, zh_title_enhance)
**upload_temp_docs**: This function is used to upload temporary documents to the knowledge base. 

**Parameters**:
- `files`: A list of files, which can be a list of strings, paths, or bytes of data.
- `knowledge_id`: String type, specifying the ID of the knowledge base, which is Never by default.
- `chunk_size`: Integer, specifies the size of each block when uploading in parts, and the default value is determined by`CHUNK_SIZE` a constant. 
- `chunk_overlap`: Integer, specifies the size of the overlap between blocks when uploaded in parts, and the default value is determined by`OVERLAP_SIZE` a constant. 
- `zh_title_enhance`: Boolean, specifies whether to enhance the Chinese title, the default value is determined by`ZH_TITLE_ENHANCE` the constant. 

**Code Description**:
This function first defines an internal function `convert_file`that converts the input file into a format suitable for uploading. If the file is byte data, it is encapsulated in `BytesIO`an object; If the file is a readable object, it is used directly; If the file is the path, the file is opened and read as binary data. After that, all files are converted through `convert_file`functions and a dictionary of uploaded data is constructed, including knowledge base ID, tile size, block overlap size, and Chinese title enhancement options. Finally, use the`post` method to `/knowledge_base/upload_temp_docs`send a POST request to the path, upload the file, and process the response through`_get_response_value` the method, returning the response data in JSON format. 

This function is closely related to`post` the and`_get_response_value` method. `post`The method is responsible for executing HTTP POST requests, sending files and data to the server; `_get_response_value`Methods are used to process the server's response, converting it to JSON format or other user-defined formats. This design enables modularity of functions, making the process of uploading files clear and manageable. 

**Note**:
- Make sure that `files`the file path in the incoming parameters exists or that the file data is valid to avoid errors during the upload process. 
- `chunk_size`and `chunk_overlap`parameters should be set reasonably according to the server's acceptance capacity and network conditions to optimize upload performance. 
- Functions rely on `post`the implementation of methods to ensure that `post`they can properly handle requests for file uploads. 
- When using `_get_response_value`processing responses, make sure that the server's response can be parsed correctly into JSON format. 

**Example output**:
Assuming that the upload is successful, the server responds with the following JSON data:
```python
{
    "code": 200,
    "msg": "Upload success",
    "data": {
        "file_ids": ["file1_id", "file2_id"]
    }
}
```
In this case, `upload_temp_docs`the return value of the function might be:
```python
{
    "code": 200,
    "msg": "Upload success",
    "data": {
        "file_ids": ["file1_id", "file2_id"]
    }
}
```
#### FunctionDef convert_file(file, filename)
**convert_file**: The function of this function is to convert the incoming file into the form of a file name and a file object. 

**Parameters**:
- **file**: This can be a byte string, a file object with a read method, or a local file path. 
- **filename**: An optional parameter that specifies the file name. If not provided, the file name is automatically determined based on the file object or path. 

**Code Description**:
This function first examines `file`the type of the parameter to determine whether it is a byte string, a file object, or a file path, and processes accordingly:
- If `file`it is a byte string (`bytes`type), it is converted `BytesIO`to a file object using it. 
- If `file`you have `read`a method (that is, it's a file object), you use that object directly. If `filename`the parameter is not provided, an attempt will be made to get the file name from the properties of the file object`name`. 
- If `file`it's neither a byte string nor a `read`method, it's assumed to be a local file path. The function will try to open the file that the path points to (in binary read mode) and set the file name as needed. 

When processing is complete, the function returns a tuple containing the file name and the file object.

**Note**:
- Make sure that the incoming file path is valid, otherwise an exception will be thrown when trying to open the file.
- If you're passing in a file object, make sure it's already open in the appropriate mode, such as binary read mode.

**Example output**:
Suppose there is a file located in`/path/to/document.pdf`, and the call `convert_file('/path/to/document.pdf')`will return:
```
('document.pdf', <_io.BufferedReader name='/path/to/document.pdf'>)
```
If a string of bytes is passed, the call may return, assuming no file name is provided`convert_file(b'some binary data')`
```
(None, <_io.BytesIO object at 0x7f4c3b2f1e50>)
```
Note that since byte strings don't have an explicit file name, the file name in this case may be`None` specified outside of the function or depending on the context. 
***
***
### FunctionDef file_chat(self, query, knowledge_id, top_k, score_threshold, history, stream, model, temperature, max_tokens, prompt_name)
**file_chat**: This function is used to process file dialog requests by sending queries to the backend and receiving the processing results. 

**Parameters**:
- `query`: String type, the content of the user's query.
- `knowledge_id`: String type, which specifies the unique identifier of the knowledge file.
- `top_k`: Integer, default is`VECTOR_SEARCH_TOP_K`, specifies the number of most relevant results returned. 
- `score_threshold`: floating-point type, the default value is to `SCORE_THRESHOLD`specify the score threshold for returning results. 
- `history`: List type, which is an empty list by default, contains historical conversation records of the dictionary type.
- `stream`: Boolean type, which is True by default, specifies whether to receive the response content in a streaming mode.
- `model`: String type, default, `LLM_MODELS[0]`specifies the language model to use. 
- `temperature`: Floating-point, default`TEMPERATURE`, controls how innovative the text is generated. 
- `max_tokens`: Integer, optional, specifies the maximum number of tokens for which text can be generated.
- `prompt_name`: String type, default is default, specifies the name of the prompt template to use.

**Code Description**:
`file_chat`The function first constructs a data dictionary with all the necessary information, then`self.post` uses the method to `/chat/file_chat`send a POST request to the endpoint and passes the data dictionary as JSON data. Requests are sent in a stream in order to process potentially large amounts of data. The response received by the function `self._httpx_stream2generator`is converted into a generator by a method to facilitate asynchronous processing of the response data. This method allows the response to be processed block by block in JSON format, which is suitable for scenarios where real-time data streams are used. 

**Note**:
- When using `file_chat`functions, you need to make sure that `knowledge_id`you are correctly pointing to a valid knowledge file identifier. 
- `history`Parameters allow historical conversations to be passed, which helps the model better understand the context to generate more accurate responses.
- With adjustments`top_k` and `score_threshold`parameters, you can control the quantity and quality of the returned results. 
- `stream`The default parameter is True, which means that the response is processed in a stream mode, which is suitable for scenarios with large data volumes.

**Example output**:
Since `file_chat`the output of a function is a generator processed by `self._httpx_stream2generator`a method, the specific output example will depend on the response of the backend service. In general, you might get a JSON data stream in a format similar to the following:
```json
{
  "answer": "This is an answer generated based on your query and the file content provided.",
  "docs": [
    {
      "title": "Related Document 1",
      "content": "Document content summary.",
      "score": 0.95
    },
    {
      "title": "Related Document 2",
      "content": "Document content summary.",
      "score": 0.90
    }
  ]
}
```
This example shows a list of possible responses along with the most relevant documents for the query and their matching scores.
***
### FunctionDef search_engine_chat(self, query, search_engine_name, top_k, history, stream, model, temperature, max_tokens, prompt_name, split_result)
**search_engine_chat**: This function is used for chat-style search through search engines. 

**Parameters**:
- `query`: String type, the user's query statement.
- `search_engine_name`: String type, specifying the name of the search engine to use.
- `top_k`: Integer, defaults`SEARCH_ENGINE_TOP_K`, specifies the number of search results to be returned. 
- `history`: A list type, which defaults to an empty list and contains a dictionary-type element that is used to pass the conversation history.
- `stream`: Boolean type, which is True by default, specifies whether to receive the response content in a streaming mode.
- `model`: String type, default, `LLM_MODELS[0]`specifies the language model to use. 
- `temperature`: Floating-point type, default, `TEMPERATURE`which adjusts the randomness of the generated text. 
- `max_tokens`: Integer, optional, specifies the maximum number of tokens for which text can be generated.
- `prompt_name`: String type, default is "default", which specifies the name of the prompt template to use.
- `split_result`: Boolean type, set to False by default, specifies whether to split the returned result.

**Code Description**:
This function first constructs a dictionary with all input parameters`data`, and then uses `self.post`a method to `/chat/search_engine_chat`send a POST request to the path, passing `data`it as the request body. The response to the request is received as a stream and `self._httpx_stream2generator`converted to a normal generator by a method to facilitate the processing of asynchronous or synchronous HTTP stream responses. This enables the function to process the real-time data stream and parse the chunks into JSON format or return them directly as needed. 

**Note**:
- Functions depend on `self.post`a method to send HTTP POST requests, and the specific implementation and behavior of that method can affect`search_engine_chat` the behavior and performance of the function. 
- Calling a method with `stream=True`a parameter `self.post`means that the response content will be received as a stream, which is suitable for processing large amounts of data or real-time data streams. 
- `self._httpx_stream2generator`The method is used to process the HTTP stream response returned by the httpx library and`as_json=True` parse the data in the stream into JSON format according to the parameters. 

**Example output**:
Assuming that the search engine returns two results for the query "Python programming", the function might return generator output in the following format:
```python
[
    {"title": "Python official documentation", "url": "https://docs.python.org", "snippet": "The official Python documentation provides a detailed language reference..."},
    {"title": "Python Tutorial", "url": "https://www.learnpython.org", "snippet": "This Python tutorial is for programmers of all levels..."}
]
```
This output example shows the search results returned in JSON format, with the title, URL, and summary information for each result. The actual output will vary depending on the search engine's response and processing logic.
***
### FunctionDef list_knowledge_bases(self)
**list_knowledge_bases**: The function of this function is to list all available knowledge bases. 

****Arguments: This function has no arguments. 

**Code Description**:  The function fetches a list of all available knowledge bases `list_knowledge_bases` by sending an HTTP GET request to `/knowledge_base/list_knowledge_bases` the  path. The function first calls  the `get` method to send a request and receives a response in return. It then `_get_response_value` processes this response using a method, parses the response body into JSON format, and extracts `data` the value of the field from it. If  the field `data` does not exist, an empty list is returned by default. This process allows the function to return a list of knowledge bases in a structured way, which is easy to process and use later. 

**Note**:
- Functions rely on `get` methods to send HTTP requests, so you need to make sure that the network connection is healthy and that the destination server is able to respond to `/knowledge_base/list_knowledge_bases` requests from the path. 
- The list of knowledge bases returned by the function is provided in JSON format, which requires the caller to be able to work with data in JSON format.
- When processing a server response, if the response body cannot be successfully parsed to JSON, or if `data` the field does not exist, the function will return an empty list instead of throwing an exception. This means that the caller needs to check the returned list to confirm that the knowledge base list was successfully fetched. 

**Example output**:
Assuming that the server responds successfully and returns information from both knowledge bases, the function might return data in the following format:
```python
[
    {"id": "kb1", "name": "Knowledge Base 1", "description": "This is the description of the first knowledge base"},
    {"id": "kb2", "name": "Knowledge Base 2", "description": "This is the description of the second knowledge base"}
]
```
If the server doesn't return any knowledge base information, or if the request fails, the function returns an empty list:
```python
[]
```
***
### FunctionDef create_knowledge_base(self, knowledge_base_name, vector_store_type, embed_model)
**create_knowledge_base**: This function is used to create a new knowledge base. 

**Parameters**:
- `knowledge_base_name`: String type, specifying the name of the knowledge base you want to create.
- `vector_store_type`: String type, `DEFAULT_VS_TYPE`defaults, specifies the type of vector storage. 
- `embed_model`: String type, defaults`EMBEDDING_MODEL`, specifies the model to use for embedding. 

**Code Description**:
`create_knowledge_base`Functions are primarily responsible for creating a new knowledge base through the API interface. The function first constructs a data dictionary that contains the knowledge base name, vector storage type, and embedding model. Then, use the`post` method to `/knowledge_base/create_knowledge_base`send a POST request to the path, and the request body is the above data dictionary. Finally,`_get_response_value` the response is processed by calling the method, and if specified`as_json=True`, the response body is attempted to parse into JSON format and returned. 

**Note**:
- Make sure that the incoming knowledge `knowledge_base_name`base name is not empty and unique to avoid creating duplicate knowledge bases. 
- `vector_store_type`and `embed_model`parameters should be selected according to the actual needs of the appropriate type and model, which will affect the performance and effect of the knowledge base. 
- Functions rely on `post`methods to send HTTP requests, which provide a retry mechanism and exception handling to ensure the stability of network requests. 
- The return value of a function depends on the response result of the API, and typically contains the status code and message of the operation, and possibly the details of the knowledge base created.

**Example output**:
Assuming that a knowledge base named "ExampleKB" is successfully created, and the default vector storage type and embedding model are used, the function might return data in JSON format as follows:
```python
{
    "code": 200,
    "msg": "New knowledge base ExampleKB",
    "data": {
        "knowledge_base_name": "ExampleKB",
        "vector_store_type": "DEFAULT_VS_TYPE",
        "embed_model": "EMBEDDING_MODEL"
    }
}
```
If you try to create an existing knowledge base name, the following data may be returned:
```python
{
    "code": 404,
    "msg": "A knowledge base with the same name ExampleKB already exists"
}
```
***
### FunctionDef delete_knowledge_base(self, knowledge_base_name)
**delete_knowledge_base**: This function is used to delete the specified knowledge base. 

**Parameters**:
- `knowledge_base_name`: String type, specifying the name of the knowledge base to be deleted.

**Code Description**:
`delete_knowledge_base` The function sends an HTTP POST request to `/knowledge_base/delete_knowledge_base`the endpoint to delete the knowledge base with the specified name. The function receives a parameter `knowledge_base_name`that specifies the name of the knowledge base to be deleted. When the request is sent, the name is sent as part of the JSON data body. The response to the request is handled by calling`_get_response_value` the function to ensure that the response content is parsed correctly in JSON format. If the response is successful, the function will return the parsed JSON data. 

**Note**:
- Make sure that the incoming one `knowledge_base_name`actually exists in the system, otherwise it may cause the deletion to fail. 
- Deleting a knowledge base is an irreversible operation, and once executed, all data in the knowledge base will be permanently deleted.
- Before calling this function, it is recommended that you have a proper acknowledgment process in place to prevent accidental deletion of important data.

**Example output**:
Assuming that the knowledge base named is successfully deleted`example_kb`, the function may return data in JSON format as follows:
```python
{
    "code": 200,
    "msg": "success",
    "data": None
}
```
This output indicates that the request has been successfully processed and the knowledge base has been deleted. `code`The field indicates the status code of the operation, and 200 indicates the success of the operation. `msg`The field provides a short description of the operation. `data`The field is usually empty in this operation because the delete operation does not return additional data. 
***
### FunctionDef list_kb_docs(self, knowledge_base_name)
**list_kb_docs**: The function of this function is to list the files in the specified knowledge base. 

**Parameters**:
- `knowledge_base_name`: String type, specifying the name of the knowledge base to be queried.

**Code Description**:
`list_kb_docs`The function`get` sends an HTTP GET request to the endpoint by calling a method`/knowledge_base/list_files` to get a list of files for the specified knowledge base. When requested, it is `knowledge_base_name`passed as a query parameter. After receiving the response, the response data is processed by using`_get_response_value` a method that supports parsing the response body into JSON format, and `value_func`further processing the parsed data through the functions provided by the parameters, and finally returns an array containing a list of files. 

**Note**:
- Make sure that the parameters passed in `knowledge_base_name`are correct so that you can query the correct list of KB files. 
- This function depends on`get` and `_get_response_value`methods to ensure that these dependencies work correctly. 
- The response data format for function processing depends on the design of the backend API to ensure that`/knowledge_base/list_files` the response format of the backend endpoint matches the processing logic of this function. 

**Example output**:
Assuming that a file exists in the knowledge base`["document1.pdf", "document2.pdf"]`, a function might return an array like this:
```python
["document1.pdf", "document2.pdf"]
```
This output example shows an array of file lists that are returned when a function call is successful. The actual data returned will vary depending on the files that are actually included in the specified knowledge base.
***
### FunctionDef search_kb_docs(self, knowledge_base_name, query, top_k, score_threshold, file_name, metadata)
**search_kb_docs**: This function is used to search for documents in the knowledge base. 

**Parameters**:
- `knowledge_base_name`: String type, specifying the name of the knowledge base to be searched.
- `query`: String type, which defaults to an empty string and specifies the content of the search query.
- `top_k`: Integer, defaults`VECTOR_SEARCH_TOP_K`, specifies the maximum number of documents to be returned. 
- `score_threshold`: Integer, defaults`SCORE_THRESHOLD`, specifies the score threshold for the search results. 
- `file_name`: String type, default is an empty string, specifies the name of the file to be searched.
- `metadata`: Dictionary type, default to empty dictionary, specifies the metadata to be searched.

**Code Description**:
This function first constructs a dictionary containing search parameters`data`, and then uses`post` a method to `/knowledge_base/search_docs`send a POST request to the path, which is a `data`dictionary. After the request is successful, the `_get_response_value`response is processed using a method, parsed into JSON format, and returned. This process involves interaction with the backend API for searching for documents based on the given query criteria in a specified knowledge base. 

**Note**:
- The function calls a `post`method internally to execute an HTTP POST request, and the detailed behavior of this method can be found`post` in the function documentation. 
- The function also calls `_get_response_value`a method to handle HTTP responses, and the detailed behavior of this method can be found`_get_response_value` in the function's documentation. 
- When using this function, you need to make sure that `knowledge_base_name`you are correctly pointing to an existing knowledge base that has documents that match your search criteria. 
- `top_k`and `score_threshold`parameters can be used to adjust the quantity and quality of search results, depending on the actual needs. 

**Example output**:
Assuming that the search query returns two documents, the return value of the function might be as follows:
```python
[
    {
        "doc_id": "123",
        "title": "Document title 1",
        "content": "Document content example 1",
        "score": 0.95,
        "metadata": {"author": "作者1", "date": "2023-01-01"}
    },
    {
        "doc_id": "456",
        "title": "Document Title 2",
        "content": "Document Content Example 2",
        "score": 0.90,
        "metadata": {"author": "作者2", "date": "2023-02-01"}
    }
]
```
This example output shows the structure of the search results, including document ID, title, content, match score, and metadata. The actual output will vary depending on the search query and the documents in the knowledge base.
***
### FunctionDef update_docs_by_id(self, knowledge_base_name, docs)
**update_docs_by_id**: This function is used to update documents in the knowledge base based on the document ID. 

**Parameters**:
- `knowledge_base_name`: String type, specifying the name of the knowledge base for which you want to update the document.
- `docs`: A dictionary type that contains the ID of the document to be updated and its corresponding updated content.

**Code Description**:
`update_docs_by_id`The function mainly sends an HTTP POST request to `/knowledge_base/update_docs_by_id`the interface to update the Chinese file of the specified knowledge base. The function takes two arguments:`knowledge_base_name` and`docs`. `knowledge_base_name`A parameter specifies the name of the knowledge base in which the document is to be updated, while`docs` a parameter is a dictionary that contains the document ID and its corresponding update. 

Inside the function, a `knowledge_base_name`dictionary containing`docs` and `data`then the `post`method is called to send a POST request. `post`A method `ApiRequest`is a member method of a class that is used to perform an HTTP POST request. When a method is called`post`, it will `/knowledge_base/update_docs_by_id`be used as the URL of the request, and the `data`dictionary will be passed to the method as JSON data. 

After the request is successfully sent and a response is received, the function calls`_get_response_value` the method to process the response data. `_get_response_value`is `ApiRequest`another member method of the class that is responsible for transforming the HTTP response object and returning the processed data according to the specified parameters. In this function, the`_get_response_value` method is used to parse the response data and return the result of the processing. 

**Note**:
- Ensure that the input`knowledge_base_name` and `docs`parameters are formatted correctly and that `docs`the document ID in exists in the specified knowledge base. 
- The return value of this function depends on `_get_response_value`the processing result of the method, which is usually a Boolean value and indicates whether the update operation was successful or not. 

**Example output**:
Assuming the update operation succeeds, the function may return`True`. If the update operation fails, `False`a specific error message may be returned. The exact return value depends on `_get_response_value`the implementation details of the method and the content of the server's response. 
***
### FunctionDef upload_kb_docs(self, files, knowledge_base_name, override, to_vector_store, chunk_size, chunk_overlap, zh_title_enhance, docs, not_refresh_vs_cache)
**upload_kb_docs**: This function is used to upload documents to the knowledge base and optionally add the document content to the vector store. 

**Parameters**:
- `files`: A list of files, which can be a list of strings, path objects, or byte data.
- `knowledge_base_name`: Knowledge base name, specifying the target knowledge base to upload the document.
- `override`: Boolean, defaults to False. If True, the file with the same name is overwritten when the file is uploaded.
- `to_vector_store`: Boolean, which defaults to True. Decide whether to add the uploaded document content to the vector store.
- `chunk_size`: An integer that specifies the size of the document chunk, with a default value of CHUNK_SIZE.
- `chunk_overlap`: An integer that specifies the size of the overlap between tiles, with a default value of OVERLAP_SIZE.
- `zh_title_enhance`: Boolean, specifies whether to enable Chinese title enhancement, the default value is ZH_TITLE_ENHANCE.
- `docs`: A dictionary that can be used to provide additional metadata for a document, defaulting to an empty dictionary.
- `not_refresh_vs_cache`: Boolean, defaults to False. Specifies whether to refresh the cache of the vector store after adding a document to the vector store.

**Code Description**:
This function first converts `files`each file in the argument into a format suitable for uploading. For byte data, wrap it as`BytesIO` an object; For file objects that have `read`methods, use them directly; For the file path, turn it on to binary read mode. Then, construct a dictionary that contains all the necessary information`data`, including the knowledge base name, whether to overwrite, whether to add to the vector store, tile size, tile overlap, Chinese title enhancement, document metadata, and whether to refresh the vector store's cache. If`docs` the argument is a dictionary, it is converted to a JSON string. Finally, use`post` the method to `/knowledge_base/upload_docs`send a POST request to the path, upload the file and related data, and process the response through`_get_response_value` the method, returning the response data in JSON format. 

**Note**:
- When uploading large amounts of data or large files, consider appropriate adjustments`chunk_size` and `chunk_overlap`parameters to optimize processing performance. 
- If `to_vector_store`the parameter is set to True, make sure that the knowledge base is configured to support vector storage. 
- `docs`When passing additional document metadata with parameters, make sure it's formatted correctly for successful parsing. 

**Example output**:
Assuming that the upload operation is successful, the function may return data in the following format:
```python
{
    "code": 200,
    "msg": "Upload success",
    "data": {
        "failed_files": []
    }
}
```
If there are files that fail during the upload process for various reasons, the`failed_files` list will contain information about those files. 
#### FunctionDef convert_file(file, filename)
**convert_file**: The function of this function is to convert different types of file inputs into the form of file names and file objects. 

**Parameters**:
- **file**: This can be a byte string, a file object with a read method, or a local file path. 
- **filename**: An optional parameter that specifies the file name. If not provided, the file name is automatically determined based on the file object or path. 

**Code Description**:
This function handles three types of inputs:
1. If the input is a byte string (`bytes`), it is converted to `BytesIO`an object so that it can operate like a file. 
2. If the input has a `read`method (for example, an open file object), the object is used directly. If a parameter is provided`filename`, the parameter value is used; If it is not provided, an attempt is made to get the file name from the properties of the file object`name`. 
3. If the input is neither a byte string nor a `read`method (i.e., assumed to be a local file path), an attempt is made to open the file that the path points to (in binary read mode) and the file name is automatically determined. If a parameter is provided`filename`, the parameter value is used; If not provided, the file name is extracted from the path. 

**Note**:
- The entered file path should be valid and accessible, otherwise an exception will be thrown when trying to open the file.
- When the input is a byte string, the file name is not automatically determined, so it `filename`is especially important to provide parameters in this case. 

**Example output**:
Suppose there is a local file path`"/path/to/document.pdf"`, and the call`convert_file("/path/to/document.pdf")` will return:
```
("document.pdf", <_io.BufferedReader name='/path/to/document.pdf'>)
```
This means that the function returns the file name `"document.pdf"`and a file object, which can be used for further file operations. 
***
***
### FunctionDef delete_kb_docs(self, knowledge_base_name, file_names, delete_content, not_refresh_vs_cache)
**delete_kb_docs**: This function is used to delete the specified document from the knowledge base. 

**Parameters**:
- `knowledge_base_name`: String type, specifying the name of the knowledge base to be manipulated.
- `file_names`: List of strings, specifying a list of file names to be deleted.
- `delete_content`: Boolean type, default is False, specifies whether to delete the file content at the same time.
- `not_refresh_vs_cache`: Boolean type, default to False, specifies whether to not flush the cache of vector search.

**Code Description**:
This function first constructs a dictionary that contains the knowledge base name, a list of file names, whether to delete content, and whether to refresh the vector search cache`data`. Then, the invoked`post` method `/knowledge_base/delete_docs`sends a POST request to the path, and the request body is a`data` dictionary. Finally, the method is called `_get_response_value`to process the response and return the result in JSON format. 

**Note**:
- When calling this function, you need to make sure that`knowledge_base_name` the sum arguments `file_names`correctly point to the knowledge base and files that exist, otherwise the deletion may fail. 
- `delete_content`The parameter controls whether the actual contents of the file are deleted, and if set to True, the file will be deleted completely; If False, only the file is removed from the knowledge base's index, and the file itself remains.
- `not_refresh_vs_cache`The parameter is used to control whether to refresh the cache of vector search, if true, the cache will not be refreshed after the file is deleted, which may affect the accuracy of subsequent search results.

**Example output**:
Assuming that the specified file is successfully deleted, the function may return a JSON object like this:
```python
{
    "code": 200,
    "msg": "success",
    "data": {
        "failed_files": []
    }
}
```
If the specified files do not exist or the deletion fails, the returned JSON object`failed_files` will contain the names of those files in the list. 
***
### FunctionDef update_kb_info(self, knowledge_base_name, kb_info)
**update_kb_info**: This function is used to update the information in the knowledge base. 

**Parameters**:
- `knowledge_base_name`: String type, specifying the name of the knowledge base to be updated.
- `kb_info`: A string type that provides new information about the knowledge base.

**Code Description**:
`update_kb_info`Functions are primarily responsible for sending requests to the backend to update information about a specified knowledge base. It first constructs a dictionary containing the knowledge base name (`knowledge_base_name`) and the new knowledge base information (`kb_info`).`data` Then, `post`use the method to send an HTTP POST request to`/knowledge_base/update_info` the endpoint, carrying the above `data`as JSON data. Once the request is successful, the `_get_response_value`response is processed by calling the method, and if specified`as_json=True`, an attempt is made to parse the response body into JSON format and return. 

**Note**:
- When calling this function, you need to make sure that the knowledge base name provided (`knowledge_base_name`) already exists in the system, otherwise it may not be updated successfully. 
- The updated information(`kb_info`) should be in string format and can contain information such as a description of the knowledge base, metadata, etc. 
- The specific implementation and exception handling mechanism of the internal methods`post` of the function sends HTTP requests through methods `_get_response_value`and processes the responses through methods are important for understanding the behavior of functions. 

**Example output**:
Assuming that the update of the knowledge base information is successful, the returned JSON response might look like this:
```python
{
    "code": 200,
    "msg": "Knowledge base information update success",
    "data": {
        "knowledge_base_name": "example_kb",
        "kb_info": "Updated knowledge base description"
    }
}
```
This output example shows a typical success response with a status code`200`, a success message, and an updated knowledge base name and description. The actual data structure returned may vary depending on the backend implementation. 
***
### FunctionDef update_kb_docs(self, knowledge_base_name, file_names, override_custom_docs, chunk_size, chunk_overlap, zh_title_enhance, docs, not_refresh_vs_cache)
**update_kb_docs**: This function is used to update documents in the knowledge base. 

**Parameters**:
- `knowledge_base_name`: String type, specifying the name of the knowledge base for which you want to update the document.
- `file_names`: A list of strings containing the names of the files that need to be updated.
- `override_custom_docs`: Boolean type, default is False, specifies whether to overwrite the custom document.
- `chunk_size`: Integer, specifies the size of the document chunk, the default value is determined by`CHUNK_SIZE` the constant. 
- `chunk_overlap`: Integer, specifies the size of the overlap between document tiles, the default value is determined by`OVERLAP_SIZE` a constant. 
- `zh_title_enhance`: Boolean type, specifies whether to enhance the Chinese title, the default value is determined by`ZH_TITLE_ENHANCE` the constant. 
- `docs`: A dictionary type that contains the content of the document to be updated, which is an empty dictionary by default.
- `not_refresh_vs_cache`: Boolean type, default is False, specifies whether to not refresh the vector search cache.

**Code Description**:
This function first constructs a dictionary with all the parameters`data` that is used as the payload for the HTTP request. If `docs`the parameter is a dictionary type, it is converted to a JSON string. Then, the invoked`post` method `/knowledge_base/update_docs`sends a POST request to the path, and the request body is a`data` dictionary. Finally, the method is called`_get_response_value` to process the response, and if specified `as_json`as True, the response data in JSON format is returned. 

**Note**:
- Before calling this function, make sure that the knowledge base name and file name are correct to avoid updating the wrong document.
- When `override_custom_docs`True, the custom document in the knowledge base will be overwritten, and this option should be used with caution. 
- `chunk_size`and `chunk_overlap`parameters affect how the document is chunked, and inappropriate values can affect the search performance. 
- If the `docs`parameter is non-empty, the function will update the specified document content; Otherwise, only the files in the file name list are updated. 
- `not_refresh_vs_cache`If this parameter is true, the vector search cache is not refreshed after the document is updated, which may affect the real-time performance of the search results.

**Example output**:
```python
{
    "code": 200,
    "msg": "Document update success",
    "data": {
        "failed_files": []
    }
}
```
This example indicates that the update operation was performed successfully and all the specified files were successfully updated with no failed files.
***
### FunctionDef recreate_vector_store(self, knowledge_base_name, allow_empty_kb, vs_type, embed_model, chunk_size, chunk_overlap, zh_title_enhance)
**recreate_vector_store**: This function is used to reconstruct the vector store in the knowledge base. 

**Parameters**:
- `knowledge_base_name`: String type, specifying the name of the knowledge base to be reconstructed for the vector store.
- `allow_empty_kb`: Boolean type, which defaults to True, specifies whether to allow empty knowledge bases.
- `vs_type`: String type, `DEFAULT_VS_TYPE`defaults, specifies the type of vector storage. 
- `embed_model`: String type, defaults`EMBEDDING_MODEL`, specifies the model to use for embedding. 
- `chunk_size`: Integer, `CHUNK_SIZE`defaults, specifies the size of the text block. 
- `chunk_overlap`: Integer, defaults`OVERLAP_SIZE`, specifies the size of the overlap between blocks of text. 
- `zh_title_enhance`: Boolean type, defaults to `ZH_TITLE_ENHANCE`specifies whether to enhance Chinese titles. 

**Code Description**:
The function first constructs a dictionary containing all parameters`data`, and then sends a POST request to the path by calling `self.post`the method`/knowledge_base/recreate_vector_store`, which is a `data`dictionary. The purpose of this request is to rebuild the vector store of the specified knowledge base in the backend service. The response to the request is`self._httpx_stream2generator` converted into a generator by a method so that the response data can be processed in a streaming fashion. If`as_json` the parameter is True, the response data will be parsed into JSON format. 

**Note**:
- This function depends on `self.post`the method to send HTTP POST requests, and `self.post`the detailed behavior of the method can be found in its documentation. 
- `self._httpx_stream2generator`Methods are used to process streaming responses, and their detailed behavior can be found in their documentation.
- The execution result of a function depends on the implementation and state of the backend service, and whether the provided parameters meet the requirements of the backend service.

**Example output**:
```python
[
    {"code": 200, "msg": "Vector storage reconstruction success"},
    {"finished": 1, "total": 10, "msg": "Processing..."},
    ...
]
```
This output example shows the possible form of a function return value, which contains multiple dictionaries, each representing a state or result of the rebuild process. `code`A field of 200 indicates that the operation was successful,`finished` and a `total`field that indicates the current processing progress, `msg`provides additional status information or error messages. 
***
### FunctionDef list_running_models(self, controller_address)
**list_running_models**: This function is used to get a list of models that are running in Fastchat. 

**Parameters**:
- `controller_address`: String type, optional, default is None. Lets you specify the address of the controller.

**Code Description**: 
`list_running_models`The function mainly sends an HTTP POST request to `/llm_model/list_running_models`the endpoint to get the list of models that are currently running in Fastchat. The function first constructs a containing`controller_address` dictionary as the requested data. If `log_verbose`the variable is true, the data sent is recorded through the logger. Subsequently,`post` the request is sent using a method, and the `_get_response_value`response is processed through the method, which finally returns a list of models in JSON format. If the "data" key is not present in the response, an empty list is returned by default. 

**Note**:
- The function calls a `post`method internally to execute an HTTP POST request, and the detailed behavior of this method can be found`post` in the method's documentation. 
- The function also calls a `_get_response_value`method to handle HTTP responses, which supports custom processing logic, please refer to the`_get_response_value` method's documentation for details. 
- The execution of the function depends on `controller_address`a parameter that specifies the address of the controller, which defaults to None if not provided. 
- The return value of a function is the result of processing by `_get_response_value`the method, and is usually a list containing information about the running model. 

**Example output**:
```python
[
    {
        "model_name": "model1",
        "status": "running",
        "controller_address": "192.168.1.100"
    },
    {
        "model_name": "model2",
        "status": "running",
        "controller_address": "192.168.1.101"
    }
]
```
This example shows the possible return value of a function, which contains information about two running models, each with model name, state, and controller address.
***
### FunctionDef get_default_llm_model(self, local_first)
**get_default_llm_model**: The function of this function is to get the name of the currently running LLM (large language model) model and where it is running (local or online) from the server. 

**Parameters**:
- `local_first`: Boolean, which defaults to True. When set to True, the function will return the locally running model first. When set to False, the model is returned in the order in which the LLM_MODELS is configured.

**Code Description**:
`get_default_llm_model`A function first defines the sum of two intrinsic functions`ret_sync` `ret_async`that are used to obtain the default LLM model in both synchronous and asynchronous environments. The function `self._use_async`chooses which intrinsic function to use based on the value. The logic of the two intrinsic functions is basically the same, except that`ret_async` they use an asynchronous approach to get a list of running models. 

The function logic is as follows:
1. Get a list of models that are currently running.
2. Traverse through the LLM models (LLM_MODELS) in the configuration to check if each model is in the running list.
3. If a model is found in the running list, the model is selected based on `local_first`the parameters and whether the model is local (judging by checking`online_api` the field). 
4. If no model is found according to the above logic, the first model in the run list is selected as the default model.
5. Returns information about the name of the selected model and whether the model is local.

In the project, `get_default_llm_model`functions are used in different scenarios, such as `test_get_default_llm`verifying the type of the function return value in a test case, and `dialogue_page`getting the default LLM model in a function and displaying the currently running model information on the user interface. This indicates that the function plays a key role in the project to obtain the information of the currently valid LLM model, so that other parts can be further manipulated or displayed based on this information. 

**Note**:
- When using this function, you need to make sure that`LLM_MODELS` the configuration is correct and that the `list_running_models`method correctly returns a list of currently running models. 
- The asynchronous version of the function`ret_async` needs to run in an async-capable environment. 

**Example output**:
```python
("gpt-3", True)
```
This output indicates that the default LLM model currently running is "gpt-3" and that the model is running locally.
#### FunctionDef ret_sync
**ret_sync**: This function is used to synchronously return the name of the currently available local or online model and its type. 

****Arguments: This function does not accept any arguments. 

**Code Description**: The `ret_sync`function first calls `list_running_models`a method to get a list of currently running models. If no model is running, an empty string and False are returned. Next, the function iterates through the list of predefined models `LLM_MODELS`to check if each model is in the list of running models. If a model is found in the running list, it is further checked to see if the model is local (i.e., not a model run through the online API). If the `local_first`variable is true and the current model is not local, then proceed to check the next model. If a model that matches the criteria is found, a Boolean value is returned for the model name and whether it is a local model. If`LLM_MODELS` none of the models in the running model list are listed, the first model in the running list is selected by default, and a Boolean value is returned for its name and whether it is a local model. 

**Note**:
- `list_running_models`The return value of the method is key, as it determines `ret_sync`whether the function can find a valid model. For more information on the behavior of this method, please refer to its documentation. 
- `local_first`Variable control prefers local or online models, but its definition is not shown in the code snippet, and should generally be defined outside of the function.
- This function assumes `LLM_MODELS`a predefined list of model names that specify the order of models to prioritize. 
- The name of the model returned by the function and whether it is a local model can be used for subsequent operations, such as initializing the model or deciding which model to use to provide services.

**Example output**:
```python
("model1", True)
```
This example shows that the function returns a model named "model1" that is run locally.
***
#### FunctionDef ret_async
**ret_async**: This function is used to asynchronously get the most suitable language model for the moment and where to run it. 

**Parameters**: This function does not accept any external parameters. 

**Code Description**: `ret_async`The function first `list_running_models`gets the list of currently running models asynchronously by calling the method. If no model is running, the function returns an empty string and False. Next, the function iterates through the list of predefined language models`LLM_MODELS` to check if each model is in the list of running models. For each running model, the function checks if the model is marked as running locally (i.e., not running through the online API). If`local_first` the variable is true and the model is not run locally, the model is skipped. Once a model that matches the criteria is found, the function returns it as a result. If`LLM_MODELS` none of the models in the list are in the list of running models, the `running_models`first model in the selection is returned as the result. Finally, depending on whether the model is run through an online API, the function returns the model name and a Boolean value that indicates whether it runs locally or not. 

This function `list_running_models`is closely related to the method, which is responsible for providing a list of models that are currently running. This design enables`ret_async` intelligent selection of the most appropriate model for operation based on the real-time model running status. 

**Note**: 
- The function is asynchronous and needs to be run in an environment that supports asynchronous operations.
- `local_first`The variable controls whether to prefer the model that runs locally, but the definition and assignment of this variable is outside the code snippet and needs to be configured according to the actual use case.
- The model name returned by the function is an empty string and a boolean value of False, indicating that no available model was found.

**Example output**:
```python
("model1", True)
```
This example shows that the function returns a model named "model1" that is run locally.
***
***
### FunctionDef list_config_models(self, types)
**list_config_models**: This function is used to get a list of models configured in the server. 

**Parameters**:
- `types`: A list of strings, the default value is["local", "online"]. Lets you specify the type of model that needs to be obtained. 

**Code Description**:
`list_config_models`Functions are primarily used to get a list of configured models from the server. It accepts a parameter`types`, which is a list of strings that specifies the type of model to fetch. By default, this list includes two types, "local" and "online", representing the local model and the online model, respectively. 

The function first constructs a containing`types` dictionary`data`, and then uses `self.post`the method to send a POST request to the server, with the URL of the request being "/llm_model/list_config_models" and the request body being a`data` dictionary. `self.post`The method is a function that executes HTTP POST requests, please refer to the`post` function documentation for details. 

After the request is successfully returned, the function processes the response using`self._get_response_value` a method. `self._get_response_value`is a function that transforms an HTTP response object to return the processed data based on the specified parameters. In this function, it is used to parse the response body and try to parse it into JSON format. If the parsing is successful, the function will return a dictionary with the structure of the model`{"type": {model_name: config}, ...}`, where `type`is the type of the model,`model_name` the name of the model, and `config`the configuration information of the model. 

**Note**:
- The function depends on`self.post` and `self._get_response_value`two methods, ensuring that both methods are implemented correctly before use. 
- The specific structure of the returned model list and configuration information may vary depending on the implementation on the server side.

**Example output**:
```python
{
    "local": {
        "model1": {"config1": "value1"},
        "model2": {"config2": "value2"}
    },
    "online": {
        "model3": {"config3": "value3"},
        "model4": {"config4": "value4"}
    }
}
```
This example shows the possible return value of a function, which contains two types of models ("local" and "online") and their configuration information.
***
### FunctionDef get_model_config(self, model_name)
**get_model_config**: This function is used to obtain configuration information for a specified model on the server. 

**Parameters**:
- `model_name`: String type, specifying the name of the model to be queried for configuration. The default value is None.

**Code Description**:
`get_model_config`The function first constructs a dictionary containing the name of the model`data`, and then uses `post`the method to send a request to the server with the URL of the request`"/llm_model/get_model_config"`. The method here`post` is `ApiRequest`a member method of the class that is used to perform HTTP POST requests. The response returned by the request is processed through`_get_response_value` a method to obtain the response data in JSON format. `_get_response_value`is a `ApiRequest`member method of another class that is responsible for transforming the HTTP response object and returning the processed data based on the specified parameters. In this function,`_get_response_value` the method uses as a parameter a lambda function`value_func` that attempts to get `"data"`the value of the field from the response data and returns an empty dictionary if it does not exist. 

**Note**:
- The function `post`sends an HTTP POST request through a method, so you need to make sure that the network connection is working and that the server is able to process the request correctly. 
- The returned model configuration information is provided in the form of a dictionary, and the specific configuration items contained depend on the implementation details of the server-side model configuration.
- If the server response does not contain`"data"` a field, or if the `model_name`model specified by the parameter does not exist, the function returns an empty dictionary. 

**Example output**:
Assuming that there is a model named on the server`"example_model"`, and its configuration information includes the version number of the model and the supported languages, the return value of the function might look like this:
```python
{
    "version": "1.0",
    "supported_languages": ["English", "Chinese"]
}
```
In practice, the returned dictionary will contain specific configuration information for the specified model on the server.
***
### FunctionDef list_search_engines(self)
**list_search_engines**: The function of this function is to get a list of search engines supported by the server. 

****Arguments: This function has no arguments. 

**Code Description**:  The `list_search_engines` function first `post` sends an HTTP POST request to the server by calling the method, and the URL of the request is "/server/list_search_engines". This request does not require any additional data or parameters. After receiving a response from the server, the function uses `_get_response_value` the method to  process the response. `_get_response_value` The method is configured to parse the response content in JSON format and extract the "data" field in the response JSON via a lambda function. If the "data" field does not exist, an empty dictionary is returned by default. Eventually, this function returns a list of strings containing the name of the search engine. 

**Note**:
- Functions rely on `post` methods to send HTTP requests, which provide a retry mechanism and exception handling to ensure the stability of network requests. 
- `_get_response_value` Methods are used to parse HTTP responses, support synchronous or asynchronous modes, and allow further processing of parsed data through custom functions.
- The list of search engines returned depends on server configuration and availability and may change over time or with changes in server settings.

**Example output**:
```python
["Google", "Bing", "DuckDuckGo"]
```
This example shows a list of search engine names that a function might return. The actual list returned depends on the search engines currently supported by the server.
***
### FunctionDef stop_llm_model(self, model_name, controller_address)
**stop_llm_model**: This function is used to stop an LLM model. 

**Parameters**:
- `model_name`: String type, specifying the name of the LLM model to be stopped.
- `controller_address`: String type, default to None, specifies the address of the controller.

**Code Description**:
`stop_llm_model`Functions are mainly used to stop a specified LLM model. In the implementation of Fastchat, this usually means stopping the LLM model`model_worker`. The function receives two parameters:`model_name` the name of the model to be stopped, and the `controller_address`address of the controller, the latter being optional. 

The function first constructs a`model_name` dictionary containing`controller_address` and then sends a POST request to the path `data`by calling `post`the method`/llm_model/stop`, and the requested data body is a`data` dictionary. `post`A method `ApiRequest`is a member method of the class that is used to execute HTTP POST requests and is able to handle retry logic, exception catching, and so on. 

After sending a POST request and receiving a response, the function calls`_get_response_value` a method to process the response. `_get_response_value`Methods are able to convert HTTP response objects to JSON format (if`as_json` the parameter is True) or `value_func`customize the processing logic based on the provided functions. In this function, the `as_json`parameter is set to True, which means that the response body is expected to be parsed into JSON format. 

**Note**:
- When using this function, you need to make sure that the provided`model_name` function actually exists and that there is a corresponding`model_worker` one running. 
- If `controller_address`not specified, the default controller address will be used. Ensure that the default address is correct or explicitly provide address parameters. 
- The execution of a function depends on the success of the network request and the state of the LLM model. Therefore, after calling this function, you should check the returned JSON data to confirm whether the model was successfully stopped.

**Example output**:
Assuming that the LLM model named is successfully stopped`example_model`, the function might return data in JSON format as follows:
```python
{
    "code": 200,
    "msg": "Model stops success",
    "data": {
        "model_name": "example_model",
        "status": "stopped"
    }
}
```
This output example shows a successful stop operation with `code`a field indicating that the operation was successful, a `msg`field that provides a message that the operation was successful, and a`data` field containing the name and new state of the model that was stopped. 
***
### FunctionDef change_llm_model(self, model_name, new_model_name, controller_address)
**change_llm_model**: This function is used to request a switch from a currently running large language model (LLM) to another model. 

**Parameters**:
- `model_name`: String type, which indicates the name of the model that is currently running.
- `new_model_name`: String type, which represents the name of the new model you want to switch to.
- `controller_address`: String type, optional parameter, default is None, indicating the address of the controller.

**Code Description**:
`change_llm_model` The function first checks`model_name` and `new_model_name`if it is specified, and if not, returns a dictionary containing the error code and message. Then, depending on `self._use_async`the value, decide whether to execute the model switching logic synchronously or asynchronously. 

In the synchronous(`ret_sync`) or asynchronous(`ret_async`) execution logic, first get the list of models that are currently running and the list of models in the configuration. If the name of the new model is the same as the name of the current model, or if the new model is already running, a message is returned that does not need to be switched. If the specified current model is not running, or if the new model is not in the configuration, the appropriate error message is returned. 

If the check passes, a data dictionary containing the model name and controller address is constructed, and a request is sent to the endpoint through a POST request`/llm_model/change` to switch the model. Finally, the response value of the request is returned. 

In a project, `change_llm_model`a function is `webui_pages/dialogue/dialogue.py/dialogue_page`called by an object to handle the user's choice to switch LLM models through the interface. When a user selects a new model and triggers a model switch, this function is responsible for sending a request to the backend to switch models and handling responses, such as displaying a success or error message. 

**Note**:
- Ensure and`model_name` `new_model_name`correctly specify, and that the new model is defined in the system configuration. 
- Asynchronous execution needs to run in an asynchronous-enabled environment.

**Example output**:
```json
{
    "code": 200,
    "msg": "Model switching success"
}
```
Or in the case of an error:
```json
{
    "code": 500,
    "msg": "The specified model 'example_model' is not running. The current running model：['model1', 'model2']"
}
```
#### FunctionDef ret_sync
**ret_sync**: This function is used to synchronously switch models and return the results of the switch. 

**Parameters**: This function does not accept any external parameters. 

**Code Description**: The `ret_sync`function first calls `list_running_models`a method to get a list of currently running models. It then checks`new_model_name` if it is equal to `model_name`or if it already exists in the list of running models, and if it is, returns a dictionary with a status code of 200 and the message "No need to switch". If the specified `model_name`model is not in the running model list, a dictionary containing status code 500 and the corresponding error message is returned indicating that the specified model is not running. Next, the function call`list_config_models` method gets the list of models in the configuration, and if `new_model_name`it is not in the configuration model list, it returns a dictionary with status code 500 and an error message indicating that the model to be switched is not set in the configuration. 

If all of the above checks pass, construct a`model_name` data dictionary`new_model_name` that contains,`controller_address` and uses`post` methods to `/llm_model/change`send a request to the endpoint to switch models. Finally, the method is called`_get_response_value` to process the response and return the result in JSON format. 

**Note**:
- The internal logic of the function depends on`list_running_models` the four`list_config_models` methods of , `post`, , and `_get_response_value`to ensure that these methods are implemented correctly before they are used. 
- The `model_name`and `new_model_name`variables used in the function `controller_address`should be defined outside of the function and passed to the function, and the source and how these variables are defined are not shown in this document. 
- The returned status code and message are used to indicate the outcome of the operation, including whether the model needs to be switched, whether the model is running, and whether the model to switch is found in the configuration.

**Example output**:
```python
{
    "code": 200,
    "msg": "No need to switch"
}
```
or
```python
{
    "code": 500,
    "msg": "The specified model 'model_name' is not running. Currently running model:['model1', 'model2']"
}
```
or
```python
{
    "code": 500,
    "msg":"The model 'new_model_name' to switch to is not configured in configs."
}
```
This example shows the possible return values of a function, including situations where no switching is required, the specified model is not running, and the model to be switched is not configured.
***
#### FunctionDef ret_async
**ret_async**: This function is used to asynchronously switch the currently running Language model. 

**Parameters**: This function does not accept any external parameters. 

**Code Description**: `ret_async` The function first `list_running_models` gets a list of currently running models by calling the method. It then checks if the name of the new model requesting the switch `new_model_name` is already the current model or already exists in the list of running models, and if so, it returns a message with a status code of 200 indicating that there is no need to switch. If the specified current model `model_name` is not in the running model list, a message with status code 500 is returned, indicating that the specified model is not running. Then, the function calls  the method to `list_config_models` get the list of models in the configuration, check whether the new model name is in the configuration list of models, and if not, it returns a message with a status code of 500, indicating that the model to be switched is not found in the configuration. 

If all of the above checks pass, the function constructs a data dictionary containing the model name, the new model name, and the controller address, and then uses `post` the  method to `/llm_model/change` send a request to the endpoint to perform the model switch. Finally,  the `_get_response_value` response is processed by calling the method and the result is returned in JSON format. 

**Note**:
- Internally, the function uses `self.list_running_models` the and `self.list_config_models` methods to get a list of currently running models and a list of configured models, ensuring that these methods return the required data correctly. 
- Use `self.post` a method to send HTTP requests, and for more information about the behavior of this method, please refer to `post` the method's documentation. 
- Use `_get_response_value` a method to process HTTP responses, which supports parsing the response body into JSON format, please refer to the `_get_response_value` method documentation for details. 
- The execution of the function depends on `model_name` the correct setting of the ,`new_model_name` , and  these `controller_address` variables need to be correctly assigned before the function is called. 

**Example output**:
Assuming that the new model requesting the switch already doesn't exist in the run or configuration, the function might return JSON-formatted data for one of the following examples:
```python
{
    "code": 200,
    "msg": "No need to switch"
}
```
or
```python
{
    "code": 500,
    "msg": "The specified model 'model_name' is not running. Currently running model:['model1', 'model2']"
}
```
or
```python
{
    "code": 500,
    "msg": "The model 'new_model_name' to switch to is not configured in configs."
}
```
***
***
### FunctionDef embed_texts(self, texts, embed_model, to_query)
**embed_texts**: This function is used to vectorize text, using a local embedding model or an online embedding model. 

**Parameters**:
- `texts`: A list of strings, which represents a list of text that needs to be vectorized.
- `embed_model`: String type, `EMBEDDING_MODEL`defaults, specifies the embedding model to use. 
- `to_query`: Boolean type, defaults to False, and indicates whether the results are used for the query.

**Code Description**:
`embed_texts`The function first constructs a`texts` `embed_model`dictionary containing`to_query` and and`data` and then sends a POST request to the path by calling`post` the method`/other/embed_texts`, and the request body is a `data`dictionary. The purpose of this request is to obtain a vectorized representation of the specified text. `post`Methods are responsible for executing HTTP POST requests, including retry logic and exception handling, to ensure the robustness of network requests. After the request is successfully sent and the response is received, the`embed_texts` function processes the response by calling`_get_response_value` the method. `_get_response_value`The method is responsible for transforming the HTTP response, and can return the JSON parsing result of the response body as needed or further processing through a custom function. In this function,`_get_response_value` a lambda function is used as `value_func`a parameter, which receives the JSON parsing result of the response and returns the fields in it`data`, i.e., the vectorized text data. 

**Note**:
- Make sure that the parameters you pass in`texts` are valid text lists, and that the `embed_model`model specified by the parameters supports text vectorization. 
- `to_query`The parameters should be set according to the actual usage scenario to ensure the correct application of the vectorization results.
- Function dependencies`post` and `_get_response_value`methods to ensure that these methods can handle HTTP requests and responses correctly. 

**Example output**:
Assuming two texts are `["Hello", "world"]`vectorized and the function is executed successfully, the possible return value is:
```python
[
    [0.1, 0.2, 0.3, ...],  
    [0.4, 0.5, 0.6, ...]   
]
```
This output example shows a list of floating-point numbers after each text is vectorized, depending on the embedding model used.
***
### FunctionDef chat_feedback(self, message_id, score, reason)
**chat_feedback**: This function is used to submit a conversation feedback review. 

**Parameters**:
- `message_id`: String type, specifying the ID of the message to be fed back.
- `score`: Integer, which represents the rating of the conversation.
- `reason`: String type, default is an empty string, providing the reason for the rating.

**Code Description**:
`chat_feedback`Functions are primarily used to collect user feedback on chat messages, including ratings and reasons. It constructs a`message_id` `score`dictionary containing`reason` , and `data`then calls methods to send a POST request `post`to the server's `/chat/feedback`path to submit user feedback. `post`The method is responsible for executing the HTTP POST request and sending the data according to the provided parameters. After the request is successfully sent and the response is received, the`chat_feedback` function processes the response data by calling `_get_response_value`a method that is responsible for transforming the HTTP response object and returning the processed data according to the specified parameters. Eventually, the`chat_feedback` function returns the processed response data. 

**Note**:
- Make sure and`message_id` `score`parameters are correct, as they are key information for submitting feedback. 
- `score`The parameter should be an integer that represents how satisfied the user is with the message.
- `reason`While parameters are optional, providing specific feedback reasons can help improve the quality of the service or conversation.
- The execution of this function depends on the server's response, so you need to ensure that the feedback request is handled correctly on the server side.

**Example output**:
Since the return value of this function depends on the server's response, the specific output example will vary depending on the request URL and parameters. In general, if the server processes successfully, it may return an integer value containing the result of the processing, for example,`200` indicating success. 
***
## ClassDef AsyncApiRequest
**AsyncApiRequest**: The function of the AsyncApiRequest class is to provide encapsulation of asynchronous API requests. 

**Properties**:
- `base_url`: The base URL of the API server.
- `timeout`: The request timeout period, the default value is defined by `HTTPX_DEFAULT_TIMEOUT` . 
- `_use_async`: Indicates whether to use asynchronous mode, which defaults to True in this class.

**Code Description**:
The AsyncApiRequest class inherits from the ApiRequest class and is specifically designed to handle asynchronous API requests. It takes the base URL and timeout as parameters via the constructor, and sets  the `_use_async` property to True on initialization, which indicates that all requests will be made asynchronously. This design makes the AsyncApiRequest class more efficient and responsive when it comes to processing large or long-running network requests. 

In the project, the AsyncApiRequest class and the ApiRequest class together form the core processing mechanism of API requests. The ApiRequest class provides basic synchronous and asynchronous request processing capabilities, including encapsulation of GET, POST, and DELETE methods, as well as features such as request retries, streaming requests, and response data processing. The AsyncApiRequest class focuses on the processing of asynchronous requests by inheriting from the ApiRequest class, making it easier for developers to achieve efficient network communication in scenarios that require asynchronous processing of network requests.

**Note**:
- When using the AsyncApiRequest class, you need to ensure that the parameters passed in `base_url` are correctly pointed to the target API server. 
- Since the AsyncApiRequest class handles asynchronous requests, you need to use keywords in the corresponding calls when calling its methods `await` to ensure that the asynchronous operation is executed correctly and the result is obtained. 
- In the process of processing asynchronous requests, you may encounter network latency or server response timeouts, so  it `timeout` is important to set the parameters reasonably to improve the robustness and user experience of the program. 
### FunctionDef __init__(self, base_url, timeout)
**__init__**: The function of this function is to initialize an asynchronous API request object. 

**Parameters**:
- `base_url`: A string type that represents the base URL of the API server. The default value is obtained by calling`api_address` the function. 
- `timeout`: Floating-point number, which represents the request timeout period. The default value is`HTTPX_DEFAULT_TIMEOUT`. 

**Code Description**: `__init__`A function is `AsyncApiRequest`a constructor of a class that is used to create a new asynchronous API request object. In this function, the base URL and timeout are first initialized by calling the constructor of the parent class`super().__init__(base_url, timeout)`. By `base_url`default, the arguments here are obtained by calling `api_address`a function that reads from the project configuration and returns the address of the API server. `timeout`The parameter specifies the timeout period for network requests, which is `HTTPX_DEFAULT_TIMEOUT`a preset constant that represents the default request timeout time in the HTTP library. 

Next, the function sets a private property`_use_async` to which `True`indicates that the request object will be asynchronously network-requested. This is`AsyncApiRequest` one of the main differences between the class and the synchronous request class`ApiRequest`, namely that it supports asynchronous operations and is able to send network requests and receive responses without blocking the main thread. 

**Note**: When using `AsyncApiRequest`classes, you need to make sure that `api_address`the function returns the address of the API server correctly, which requires that the sum of the API server has been set correctly in the project's configuration file`host``port`. In addition, given the nature of asynchronous requests, developers should be familiar with Python's asynchronous programming patterns, such as usage and keywords, when using this type of network request`async``await`. 
***
## FunctionDef check_error_msg(data, key)
**check_error_msg**: The function of this function is to check whether the data returned by the API request contains an error message, and return the corresponding error message. 

**Parameters**:
- `data`: This can be a string, dictionary, or list, representing the data returned by the API request.
- `key`: The string type, the default value is "errorMsg", which indicates the key name of the error information in the dictionary data.

**Code Description**:
`check_error_msg`Functions are mainly used to process the response data after an API request to determine if an error has occurred. It first checks`data` the type of parameter. If `data`it is a dictionary and contains the specified `key`(the default is "errorMsg"), the value corresponding to the key is returned as an error message. If the dictionary contains a "code" key and its value is not equal to 200, this usually means that the request was unsuccessful and the function will return the value corresponding to the "msg" key as an error message. If none of the above conditions are met, the function will return an empty string, indicating that no error occurred. 

In a project, `check_error_msg`functions are called in multiple places to handle responses to different API requests. For example, in AND`dialogue_page``knowledge_base_page`, the function is used to check the results of API requests related to conversation management, knowledge base operations, so that an appropriate error message is displayed to the user when an error occurs. This helps improve the user experience by helping users understand why an action failed with instant feedback. 

**Note**:
- When using `check_error_msg`functions, you need to make sure that the parameters you pass in`data` are properly formatted and match the function's internal processing logic. 
- The return value of a function is a string, which may be a specific error message or an empty string. The caller needs to determine whether further processing is required based on the return value.

**Example output**:
- If the data returned by the API is`{"errorMsg": "Invalid request parameters"}`, the `check_error_msg`function will return an "invalid request parameter". 
- If the data returned by the API is`{"code": 404, "msg": "Resource not found"}`, the function will return "Resource Not Found". 
- If the data returned by the API does not contain error information, the function will return an empty string "".
## FunctionDef check_success_msg(data, key)
**check_success_msg**: The function of this function is to check if the data returned by the API request contains a success message. 

**Parameters**:
- `data`: can be a string, dictionary, or list, representing the data returned by the API request.
- `key`: The string type, the default value is "msg", which represents the key to look for a success message in the returned data.

**Code Description**:
`check_success_msg`Functions are mainly used to process the returned data of an API request to confirm whether the request was successfully executed. The function first checks whether`data` the type of the parameter is a dictionary and whether the dictionary contains the `key`specified key and the "code" key. If these conditions are met, and the value of "code" is 200, indicating that the request was successful, the function will return `key`the corresponding value, usually a message indicating success. If either condition is not met, the function will return an empty string indicating that there is no success message. 

In the project, `check_success_msg`functions are used to handle the return value of API requests in different scenarios. For example, in AND`dialogue_page``knowledge_base_page`, this function is used to check the return results of actions such as changing the LLM model, uploading a knowledge base document, etc., to give feedback to the user whether the operation was successful. By checking the value corresponding to the "msg" key in the returned data, you can show the user a success or error message, thereby improving the user experience. 

**Note**:
- Ensure that the format of the returned data of the API request meets the expectations of the function processing, especially when the expected returned data is a dictionary, which needs to include "code" and`key` the specified key. 
- The function returns a string, which may be an empty string or a string containing a success message. When you use this function, you should use the return value to determine the subsequent action or display logic.

**Example output**:
- If the API request is successful and the data returned is included`{"code": 200, "msg": "Operation success"}`, the `check_success_msg`function will return "Operation Successful". 
- If the API request fails, or if the returned data does not contain a "code" of 200, the function will return an empty string.
