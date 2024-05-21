## FunctionDef launch_api(args, args_list, log_name)
**launch_api**: The function of this function is to start an API service. 

**Parameters**:
- args: An object that contains the parameters required for API startup and should have the ability to access properties such as api_host and api_port.
- args_list: A list of strings, with a default value of api_args, specifying the key names that need to be converted to command-line arguments.
- log_name: The name of the log file. If not provided, it is dynamically generated based on the hostname and port of the API.

**Code Description**:
`launch_api` The function first prints out a prompt message for starting the API service, which is available in both Chinese and English. Then, if no arguments are provided`log_name`, the function generates the name of the log file based on the hostname and port number of the API service and stores it in a predefined log path. The function then`string_args` calls the function `args`to convert the parameters in the object into a string format that is acceptable to the command line. `string_args`The detailed functions and usage of the function are described in the relevant documentation. 

After that, the `launch_api`function constructs a shell command string for starting the API service, which contains the name of the startup script (),`api.py` the converted parameter string, and the path to the log file. Finally, use `subprocess.run`the method to execute the built shell command to start the API service in the background and redirect the stdout and stds to the log file. 

During the process, the `launch_api`function also prints out the location information of the log file, so that the user can easily find and view the log file when the API service starts abnormally. 

**Invocation relationships in the project**:
`launch_api` Functions are responsible for initiating the core functionality of the API service in the project. It`string_args` handles the conversion of command-line arguments by calling functions, which shows`launch_api` `string_args`a direct dependency on with. `string_args`Functions provide the `launch_api`ability to string parameters, making it `launch_api`possible to efficiently construct shell commands that start API services. 

**Note**:
- Make sure that the object passed to`launch_api` the function `args`contains all the necessary API startup parameters, such as`api_host` and`api_port` . 
- If the `log_name`parameters are not provided, the naming of the log file will depend on the hostname and port number of the API service, so make sure that this information is accurate. 
- When using `launch_api`functions, you should ensure that the relevant API startup script(`api.py`) exists under the expected path and that the arguments passed through the command line are handled correctly. 
## FunctionDef launch_webui(args, args_list, log_name)
**launch_webui**: The function of this function is to start the WebUI service. 

**Parameters**:
- args: An object that contains the parameters required to launch the WebUI. This object should have the ability to access the values of each parameter.
- args_list: A list of parameters, default to web_args, which specifies which parameters need to be included in the resulting command line string.
- log_name: The name of the log file. If this is not provided, the webui in the LOG_PATH path is used as the log file name by default.

**Code Description**:
`launch_webui` Functions are primarily responsible for starting the WebUI service. First, the function prints out a prompt to start the webUI, both in English and Chinese, to ensure that the user understands the current operation. Next, the function checks to see if the parameters are provided`log_name`, and if not, uses the default log file name. 

Next, the function calls`string_args` the function to `args`convert the arguments in the object into a string format that is acceptable to the command line. This step generates`args` the final parameter string by checking the parameters in the object and`args_list` the parameter key names specified in the list. 

Based on `args`the parameter values`nohup` in the object, the `launch_webui`function decides whether to start the WebUI service in background mode. If `nohup`true, then construct a command-line string that redirects the output of the webui service to the specified log file and runs in the background. Otherwise, construct a command-line string directly to run the WebUI service in foreground mode. 

Finally, use the `subprocess.run`method to execute the constructed command line string to start the webui service. The function prints out a completion message after the WebUI service is started. 

**Invocation relationships in the project**:
`launch_webui` Functions are responsible for the task of starting the WebUI service in the project. It relies on`string_args` functions to handle the generation of command-line arguments. `string_args`Based on the provided parameter object and the list of parameters, the function generates a parameter string suitable for the command line. This design allows`launch_webui` the function to flexibly handle different startup parameters while maintaining a centralized and consistent command line argument generation logic. 

**Note**:
- Make sure that the object passed to`launch_webui` the function `args`contains all the necessary parameters, especially `nohup`the parameters, as it determines whether the WebUI service is running in foreground or background mode. 
- If you are running the WebUI service in background mode, be sure to check the specified log file to facilitate troubleshooting possible startup exceptions.
