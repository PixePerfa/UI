## FunctionDef get_keyword_embedding(bert_model, tokenizer, key_words)
**get_keyword_embedding**: The function of this function is to get the embedding representation of the keyword. 

**Parameters**:
- **bert_model**: A pre-trained BERT model for generating embedding representations. 
- **tokenizer**: A tokenizer that matches the BERT model and is used to convert keywords into a format that the model can understand. 
- **key_words**: A list of strings containing the keywords that need to be represented by the embedding. 

**Code Description**:
`get_keyword_embedding`The function first uses the incoming`tokenizer` keyword list `key_words`into an input format that the model can handle. This step involves converting keywords to corresponding input IDs, and filling and truncating the inputs to meet the requirements of the model. Subsequently, the function`tokenizer` extracts from the output `input_ids`and removes the special tags at the beginning and end of each sequence, as these tags are not necessary for the embedded representation of the keyword. 

Next, the function uses`bert_model` the `embeddings.word_embeddings`properties to obtain the `input_ids`corresponding embedding representation. Since multiple keywords may be passed in, the function averages the embedding representations of all keywords to obtain a unified representation. 

In the project, `get_keyword_embedding`functions are called by `add_keyword_to_model`functions that are used to add embedding representations of custom keywords to the pre-trained BERT model. This process involves reading the keyword file, generating an embedding representation of the keyword, extending the embedding layer of the model to include these new keywords, and finally saving the modified model to the specified path. This allows the model to understand and effectively process these new keywords, improving the model's performance on specific tasks. 

**Note**:
- Make sure that the`bert_model` sum passed in `tokenizer`matches that they come from the same pretrained model. 
- The list of keywords `key_words`should be carefully selected, as these keywords will have a direct impact on the comprehension and performance of the model. 
- Before calling this function, you should have prepared the keyword file and made sure that it is formatted correctly.

**Example output**:
Assuming two keywords are passed in`["AI", "machine learning"]`, the function might return a`(2, embedding_size)` tensor of shape, where `embedding_size`is the dimension of the model embedding layer, representing the average embedding representation of the two keywords. 
## FunctionDef add_keyword_to_model(model_name, keyword_file, output_model_path)
**add_keyword_to_model**: The function of this function is to add custom keywords to the pre-trained embedding model. 

**Parameters**:
- **model_name**: String type, defaults`EMBEDDING_MODEL`. Specify the name of the pretrained embedding model to use. 
- **keyword_file**: String type, default is an empty string. Specify the path of the file that contains the custom keyword. 
- **output_model_path**: String type, which can be`None`. Specify the path to save the model after keywords are added. 

**Code Description**:
First, the function reads `keyword_file`the file and adds each line in the file to the list as a keyword`key_words`. Next, `model_name`load a sentence transformer model (SentenceTransformer model) using the specified and extract the first module from it as the word embedding model. Through this word embedding model, the BERT model and its tokenizer can be obtained. 

The function then calls `get_keyword_embedding`the function, passing in the BERT model, tokenizer, and keyword list to get the embedding representation of these keywords. Next, the function adds these new keyword embeddings to the embedding layer of the BERT model. This step involves extending the tokenizer to include new keywords, adjusting the embedding layer size of the BERT model to accommodate the new keywords, and assigning the embedding representation of the keywords directly to the embedding layer weights of the model. 

Finally, if the parameters are provided`output_model_path`, the function creates the necessary directories under that path and saves the updated word embedding model as well as the BERT model to the specified location. This process ensures that the model is able to understand and effectively process these new keywords in subsequent use. 

**Note**:
- Make sure the `keyword_file`file exists and is properly formatted, and each line should contain a keyword. 
- Because the size of the embedding layer of the model adjusts for the new keywords, the size of the model may increase after the keywords are added.
- When saving the model, the `safetensors`BERT model is saved in the format to ensure the compatibility and security of the model. 
- Adding keywords to a model is an operation that affects the performance of the model, so keywords should be chosen carefully and given consideration for their practical application to a specific task.
## FunctionDef add_keyword_to_embedding_model(path)
**add_keyword_to_embedding_model**: The function of this function is to add custom keywords to the specified embedding model. 

**Parameters**:
- **path**: String type, defaults`EMBEDDING_KEYWORD_FILE`. Specify the path of the file that contains the custom keyword. 

**Code Description**:
This function starts by `os.path.join(path)`getting the full path of the keyword file. It then reads the name and path of the model from the configurations, which are obtained through`MODEL_PATH["embed_model"][EMBEDDING_MODEL]`. Next, the function calculates the parent directory where the model is located and generates a new model name with the current timestamp, in the format to`EMBEDDING_MODEL Merge Keywords_Current time` ensure the uniqueness of the output model name. 

Next, there's the function call`add_keyword_to_model`, which is an important call relation, because it'`add_keyword_to_model`s responsible for actually adding keywords to the embedding model. When calling`add_keyword_to_model`, pass in the name of the model currently in use, the path to the keyword file, and the path where the new model will be saved. This step completes the core functionality of integrating custom keywords into the pre-trained embedded model. 

**Note**:
- Make sure that the parameters you pass `path`in point to a valid keyword file, that the file is properly formatted, and that each line contains a keyword to add. 
- This function relies on `add_keyword_to_model`the function, which is responsible for the actual keyword addition logic, including reading keywords, updating the embedding layer of the model, and saving the updated model. Therefore, it`add_keyword_to_model` is very important to understand the specific implementation to understand the entire keyword addition process. 
- The new model name generated contains a timestamp, which helps distinguish between model versions generated at different points in time.
- When using this function, you should consider that the model size may increase as new keywords are added, which may have an impact on the performance of the model when it loads and runs.
