## FunctionDef config_aggrid(df, columns, selection_mode, use_checkbox)
**config_aggrid**: This function is used to configure the options of the AG Grid grid view to display and operate pandas DataFrame data.

**Parameter**:
- `df`: pd.DataFrame type, representing the data to be displayed in AG Grid.
- `columns`: dictionary type, empty dictionary by default. Used to customize the configuration of columns, the key is a tuple of column name and header, and the value is the configuration dictionary of the column.
- `selection_mode`: literal type, optional values ​​are "single", "multiple" or "disabled", default is "single". Used to configure the row selection mode.
- `use_checkbox`: Boolean type, indicating whether to use a checkbox when selecting rows.

**Code Description**:
This function first creates a GridOptionsBuilder instance based on the passed in DataFrame `df`. Next, configure the width of the number column "No" to 40. Then, iterates over each column configuration in the `columns` parameter and applies these custom configurations to the corresponding columns. In addition, the function configures the row selection function, including the selection mode, whether to use checkboxes, and pre-selected rows. Finally, the paging function is configured, including enabling paging, setting the automatic paging size to off, and the number of rows displayed per page to 10. The function returns the configured GridOptionsBuilder instance.

In the project, the `config_aggrid` function is called by the `knowledge_base_page` function to display the detailed information of the knowledge base files in the knowledge base page. By configuring AG Grid, users can view the list of knowledge base files on the web page, including information such as file name, document loader, number of documents, etc., and can select single or multiple files for operation according to the configuration.

**Note**:
- When using this function, make sure that the passed DataFrame `df` is properly prepared and the column names in the `columns` parameter match the column names in the DataFrame.
- Adjust the row selection mode and whether to use checkboxes according to actual needs to adapt to different user interaction scenarios.

**Output example**:
Since this function returns a GridOptionsBuilder instance instead of direct visual output, no specific visual example can be provided. However, it can be expected that the returned GridOptionsBuilder instance will be used in the AG Grid component to generate a table view with paging, custom column width and row selection functions.
## FunctionDef file_exists(kb, selected_rows)
**file_exists**: This function checks whether the specified document file exists in the local knowledge base folder and returns the name and path of the file.

**Parameter**:
- kb: string type, indicating the name of the knowledge base.
- selected_rows: list type, containing the selected row information, usually the metadata of the document.

**Code description**:
The `file_exists` function receives two parameters: `kb` and `selected_rows`. The `kb` parameter is used to specify the name of the knowledge base, while the `selected_rows` parameter contains the row information selected by the user on the interface, which usually contains the name of the file. The function first checks whether `selected_rows` is non-empty. If it is not empty, it extracts the file name (`file_name`) corresponding to the first row. Subsequently, the `get_file_path` function is called, passing in the knowledge base name `kb` and the file name `file_name` to obtain the full path of the file. If the file corresponding to the path does exist (that is, `os.path.isfile(file_path)` returns `True`), the function returns the file name and file path. If `selected_rows` is empty or the file does not exist, the function returns two empty strings.

**Note**:
- Before calling this function, you should ensure that the `selected_rows` parameter contains the correct file metadata information, especially the file name.
- This function relies on the `get_file_path` function to construct the full path of the file, so you need to ensure that the `get_file_path` function can be executed correctly and return a valid file path.
- The file path returned by this function is based on the file system structure of the server, so you need to pay attention to the validity and access rights of the path when using it on the client.

**Output example**:
Assuming that the name of the knowledge base is `my_knowledge_base`, the row selected by the user contains the file name `example.docx`, and the file does exist in the knowledge base folder on the server, the function call `file_exists('my_knowledge_base', [{'file_name': 'example.docx'}])` will return:
```
('example.docx', '/var/knowledge_bases/my_knowledge_base/content/example.docx')
```
This return value represents the file name and the full path of the file on the server. If the file does not exist or `selected_rows` is empty, the function call will return two empty strings: `("", "")`.
## FunctionDef knowledge_base_page(api, is_lite)
**knowledge_base_page**: This function is used to display and manage the knowledge base page in the Web UI.
**Parameters**:
- `api`: ApiRequest object, used to perform interaction with the backend API.
- `is_lite`: Boolean type, optional parameter, default is None, used to indicate whether it is in lightweight mode.

**Code description**:
The `knowledge_base_page` function first tries to obtain a detailed list of knowledge base information. If an exception occurs during the acquisition process, an error message is displayed and execution stops. Next, the index of the currently selected knowledge base is determined based on the name of the knowledge base selected in the session state. If there is no selected knowledge base information in the session state, the first knowledge base is selected by default. The function further provides a form for creating a new knowledge base, allowing users to enter the name, introduction, vector library type and embedding model of the new knowledge base. Users can upload files to the selected knowledge base and manage files in the knowledge base, such as adding, deleting files, or deleting files from the vector library. In addition, advanced functions such as rebuilding the vector library and deleting the knowledge base are also provided. Users can also perform keyword queries and set the number of matches through the sidebar.

**Note**:
- Before using this function, you need to ensure that the backend API service is running properly so that you can successfully obtain knowledge base information and perform other operations.
- When creating a new knowledge base, you need to ensure the uniqueness of the knowledge base name to avoid duplication with existing knowledge bases.
- The file upload and knowledge base management functions rely on user input and selection, so you should ensure good user experience and input validation when designing the UI.
- Operations such as rebuilding the vector library and deleting the knowledge base may affect the data integrity and availability of the knowledge base and should be used with caution.

**Output example**:
Since the `knowledge_base_page` function is mainly responsible for the display and interaction of the Web UI, its direct output is the change of the user interface rather than the specific data structure. For example, when a user successfully creates a new knowledge base, a prompt message such as "Knowledge base created successfully" will be displayed on the page, and the newly created knowledge base will appear in the knowledge base list. If the user tries to upload a file to the knowledge base, the upload progress will be displayed on the page, and the corresponding success or failure information will be displayed after completion.
### FunctionDef format_selected_kb(kb_name)
**format_selected_kb**: The function of this function is to format the selected knowledge base name.

**Parameter**:
- `kb_name`: string type, representing the name of the knowledge base.

**Code description**:
The `format_selected_kb` function accepts a parameter `kb_name`, which is a string representing the name of the knowledge base to be formatted. The function first tries to obtain the knowledge base information corresponding to `kb_name` from a predefined dictionary `kb_list`. If the corresponding knowledge base information is found, the function will return a formatted string containing the name of the knowledge base, its version type (`vs_type`), and the embedded model (`embed_model`). The format is `"knowledge base name (version type @ embedded model)"`. If the corresponding knowledge base information is not found in `kb_list`, the function will directly return the input knowledge base name.

**Note**:
- Make sure `kb_list` is a valid dictionary and has been correctly initialized and filled with the corresponding knowledge base information.
- The input knowledge base name `kb_name` should be an accurate key value that exists in `kb_list` to ensure that the knowledge base information can be correctly obtained.
- The string format returned by this function is particularly suitable for scenarios where detailed information of the knowledge base needs to be displayed, such as a drop-down menu or information display board in the user interface.

**Example output**:
Assuming there is an entry in the `kb_list` dictionary which is `{"example_kb": {"vs_type": "v1", "embed_model": "model123"}}`, and `format_selected_kb("example_kb")` is called, the function will return the string `"example_kb (v1 @ model123)"`. If `kb_name` is not in `kb_list`, such as calling `format_selected_kb("unknown_kb")`, the function will return `"unknown_kb"`.
***