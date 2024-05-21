## FunctionDef list_running_models(controller_address, placeholder)
**list_running_models**: The function of this function is to get the list of loaded models and their configuration items from the fastchat controller. 

**Parameters**:
- `controller_address`: String type, Fastchat controller server address. If it is not provided, an attempt is made to get the default address from the`fschat_controller_address()` function. 
- `placeholder`: String type, this parameter is not used, only as a placeholder.

**Code Description**:
`list_running_models`The function first `controller_address`checks whether the parameter is provided, and if not, the function is called`fschat_controller_address()` to get the default address of the Fastchat controller. The function then uses the`get_httpx_client()` function to create an HTTP client instance and `controller_address`sends a POST request to the specified address in the request path`/list_models`. After the request is successful, the model list is parsed from the response, and the function is called to`get_model_config()` obtain the configuration items for each model, and finally the model and its configuration items`BaseResponse` are wrapped in a dictionary and returned in an object. 

In terms of exception handling, if any exception is encountered during execution, the function logs an error message and returns an`code` object of 500`BaseResponse` with error `msg`details in the field. 

**Note**:
- Make sure that `controller_address`you are providing a valid Fastchat controller address, otherwise you will not be able to get the list of models successfully. 
- The function depends on`get_httpx_client()` and `get_model_config()`functions to ensure that these dependencies work properly. 
- The function uses a POST request to communicate with the Fastchat controller, ensuring that the controller supports`/list_models` the handling of the path. 
- When handling exceptions, the function logs detailed error information to help with debugging and problem localization.

**Example output**:
```python
{
    "code": 200,
    "msg": "success",
    "data": {
        "model1": {
            "model_version": "1.0",
            "language": "English",
            // 其他配置项
        },
        "model2": {
            "model_version": "2.0",
            "language": "Chinese",
            // 其他配置项
        }
        // 更多模型及其配置项
    }
}
```
This example illustrates the format of the response that might be returned when a function call succeeds, with`data` fields containing details about each model and its configuration items, and`code` a `msg`and field indicating that the request was successfully processed. 
## FunctionDef list_config_models(types, placeholder)
**list_config_models**: The function of this function is to get the list of models configured in configs locally. 

**Parameters**:
- `types`: The type is , `List[str]`and the default value is`["local", "online"]`. This parameter is used to specify the category of model configuration items to be obtained, such as`local` , ,`online` ,`worker` 
- `placeholder`: The type is , `str`and the default value is`None`. This parameter is used for placeholding, and has no practical effect when invoked, and is mainly used for the extensibility of API design. 

**Code Description**:
`list_config_models`The function first defines an empty dictionary `data`that stores the final model configuration information. Functions `list_config_llm_models`get different types of all configured large language models (LLMs) by calling functions. The function then iterates through these model types, and if the model type is present`types` in the arguments, it `get_model_config`obtains detailed configuration information for each model by calling the function and adds this information`data` to the dictionary. Finally, the function returns an`BaseResponse` object with fields containing the model configuration information `data`filtered according to`types` the parameters. 

**Note**:
- When using this function, you need to make sure that `types`the model type contained in the parameters has been correctly configured in the system, otherwise you may not be able to obtain the expected configuration information. 
- This function `BaseResponse`returns data through objects, ensuring consistency and standardization of API responses. The caller can`BaseResponse` judge the status and result of request processing by checking the sum`code` field in the object`msg`. 

**Example output**:
```python
{
    "code": 200,
    "msg": "success",
    "data": {
        "local": {
            "model1": {
                "config1": "value1",
                "config2": "value2"
            },
            "model2": {
                "config1": "value1",
                "config2": "value2"
            }
        },
        "online": {
            "model3": {
                "config1": "value1",
                "config2": "value2"
            },
            "model4": {
                "config1": "value1",
                "config2": "value2"
            }
        }
    }
}
```
This output example shows the format of the response that might be returned when a function call is successful, with`data` fields containing model configuration information filtered`types` based on parameters, `code`and a `msg`sum field indicating that the request was successfully processed. 
## FunctionDef get_model_config(model_name, placeholder)
**get_model_config**: The function of this function is to get the configuration items (merged) of the LLM model. 

**Parameters**:
- `model_name`: The string type, which is passed in through the body and describes as the name of the LLM model in the configuration, which is used to specify the name of the model for which the configuration needs to be obtained.
- `placeholder`: The string type, passed in via the Body, is described as "placeholder, no real effect", this parameter is not used inside the function, only as a placeholder for API design.

**Code Description**:
`get_model_config`The function first defines an empty dictionary `config`to store the filtered model configuration items. A function calls`get_model_worker_config` a function and passes `model_name`in parameters to obtain the working configuration items of the specified model. The function then iterates through these CIs, filters out sensitive information or CIs that don't need to be exposed through a series of criteria (excluding keys that contain "worker_class", "key", "secret", or ends in "id"), and adds the remaining CIs`config` to the dictionary. 

Finally, the function returns an`BaseResponse` object with fields `data`containing the filtered model configuration items. In this way, the caller can obtain the required model configuration information through the standard API response format. 

**Note**:
- When using this function, you need to ensure that the parameters passed in `model_name`are correct and the corresponding model configuration has been correctly configured in the system, otherwise you may not be able to obtain the expected configuration information. 
- This function protects the security of the model configuration by filtering sensitive information, so the returned configuration items do not contain information that could reveal the details of the model's internal implementation.
- The fields in `BaseResponse`the returned`code` object `msg`can be used to determine the status and result of request processing to ensure that the caller can correctly process the response data. 

**Example output**:
```python
{
    "code": 200,
    "msg": "success",
    "data": {
        "model_version": "1.0",
        "language": "English",
        // Other non-sensitive configuration items

    }
}
```
This example shows the format of the response that might be returned when a function call is successful, with`data` fields containing filtered model configuration items and`code` a AND `msg`field indicating that the request was successfully processed. 
## FunctionDef stop_llm_model(model_name, controller_address)
**stop_llm_model**: The function of this function is to request the fastchat controller to stop a certain LLM model. 

**Parameters**:
- `model_name`: The name of the LLM model to be stopped, this parameter is required.
- `controller_address`: The address of the Fastchat controller server, this parameter is optional. If it is not provided, the`fschat_controller_address` function is used to get the default address. 

**Code Description**:
`stop_llm_model`Functions are mainly used to stop a specified LLM model. First, if no arguments are provided,`controller_address` the function is called `fschat_controller_address`to get the address of the Fastchat controller. Then, use `get_httpx_client`the function to get an instance of the httpx client, and send a POST request to the Fastchat controller through this client, the URL of the request is composed of the controller address and `/release_worker`path, and the request body contains the name of the model to be stopped. If the request is successful, the function returns the content of the controller's response. In exceptional cases, the function logs the error message and returns an object containing the error message`BaseResponse`. 

**Note**:
- When calling this function, make sure that the model name provided is correct and is currently running. If the model name is wrong or the model is not running, it may cause the stop operation to fail.
- If the connection to the Fastchat controller fails or the controller fails to process the request, the function returns an object with an error message`BaseResponse`, where `code`500 indicates an internal server error. 
- Because of the way Fastchat is implemented, stopping the LLM model is actually stopping the model_worker the model is in.

**Example output**:
Assuming that the LLM model named "example_model" is successfully stopped, the function might return an object like this`BaseResponse`:
```python
{
    "code": 200,
    "msg": "success",
    "data": null
}
```
If you try to stop a model that doesn't exist, or if communication with the Fastchat controller fails, the returned`BaseResponse` object might look like this:
```python
{
    "code": 500,
    "msg": "failed to stop LLM model example_model from controller: http://127.0.0.1:8080。The error message is： ConnectionError",
    "data": null
}
```
## FunctionDef change_llm_model(model_name, new_model_name, controller_address)
**change_llm_model**: The function of this function is to request the fastchat controller to switch the LLM model. 

**Parameters**:
- `model_name`: String type, which indicates the name of the currently running model.
- `new_model_name`: String type, which represents the name of the new model you want to switch to.
- `controller_address`: String type, which indicates the address of the Fastchat controller server. If it is not provided, the`fschat_controller_address` function is used to get the default address. 

**Code Description**:
`change_llm_model`The function first checks `controller_address`whether the parameter is provided, and if not, the `fschat_controller_address`function is called to obtain the address of the Fastchat controller. Then, use `get_httpx_client`the function to get an httpx client instance that sends an HTTP POST request to the endpoint of the controller address`/release_worker`. The JSON body of the request contains`model_name` and `new_model_name`fields that represent the current model and the new model to be switched to, respectively. The request timeout is defined by `HTTPX_DEFAULT_TIMEOUT`a constant. If the request is successful, the function will return the controller's response JSON. When an exception is encountered, the function logs an error log and returns an object with the error message`BaseResponse`. 

**Note**:
- Make sure to `controller_address`point to the Fastchat controller server correctly, otherwise the request will fail. 
- When using this function, you should ensure that`model_name` the correct and `new_model_name`corresponding model is available on the server. 
- The function `get_httpx_client`is used to get an HTTPX client instance, ensuring that proxy settings and timeout configurations are applied correctly, as well as supporting exception handling and logging. 

**Example output**:
When a model is successfully switched, an example of a possible return value is:
```json
{
  "code": 200,
  "msg": "Model switched successfully",
  "data": {
    "previous_model": "old_model_name",
    "current_model": "new_model_name"
  }
}
```
When an error is encountered, an example of a return value is:
```json
{
  "code": 500,
  "msg": "failed to switch LLM model from controller: http://127.0.0.1:8080。The error message is：ConnectionError"
}
```
## FunctionDef list_search_engines
**list_search_engines**: The function of this function is to list the search engines supported by the server. 

****Arguments: This function has no arguments. 

**Code Description**: `list_search_engines` The function first `server.chat.search_engine_chat` imports  a `SEARCH_ENGINES` variable from the module, which contains a list of all search engines supported by the server. The function then `BaseResponse` constructs a response object using a class where the `data` Field is set to `SEARCH_ENGINES` the contents of the list. `BaseResponse` A class is a standardized API response format that contains `code` three fields, namely , ,`msg` and  , `data` representing the API's status code, status message, and returned data content, respectively. In this function, just focus on `data` the field, which is used to hold the list of search engines. 

**Note**:
- `list_search_engines` The function returns an `BaseResponse` object, so when you call this function, you should process the object to get the data in it. 
- Since `SEARCH_ENGINES` is imported from another module, make sure that the variable is properly defined and initialized before importing. 
- This function does not receive any arguments, so it can be called directly without providing additional information.

**Example output**:
 `list_search_engines` An example response that might be returned by calling the function is as follows:
```python
{
    "code": 200,
    "msg": "success",
    "data": ["Google", "Bing", "DuckDuckGo"]
}
```
In this example, the`code` and `msg` field indicates that the request was successfully processed, while `data` the field  contains a list of the names of the search engines supported by the server. 
