## ClassDef SummaryAdapter
**SummaryAdapter**: The function of the SummaryAdapter class is to generate and process document summaries. 

**Properties**:
- `_OVERLAP_SIZE`: Overlap size, which is used to remove overlap when working on the document.
- `token_max`: The maximum number of tokens, which is used to limit the maximum length of the generated summary.
- `_separator`: Separator, which defaults to two line breaks and is used to connect documents.
- `chain`: MapReduceDocumentsChain object that is used to perform document mapping, specification, and summary merge operations.

**Code Description**:
The SummaryAdapter class provides the ability to generate, process, and optimize document summaries. It `form_summary`creates instances through a class method that accepts two language model-based parameters (`llm`and`reduce_llm`) for generating and merging summaries, and`overlap_size` and parameters `token_max`that control the size of the overlap and the maximum number of tokens for generating summaries, respectively. In addition, the class provides`summarize` and `asummarize`methods for synchronously and asynchronously generating document summaries, and`_drop_overlap` private `_join_docs`methods for handling overlaps in documents and connecting documents. 

From a functional point of view, the SummaryAdapter class is used in a project to process and generate summaries of knowledge base documents. It`form_summary` creates an instance by calling a method and uses the `summarize`method to generate a document summary. These summaries are then used to update or create summary information for the knowledge base, as shown in the`kb_summary_api.py` files `recreate_summary_vector_store`and `summary_file_to_vector_store`methods. 

**Note**:
- When using the SummaryAdapter class, you need to ensure that the language model (`llm`and`reduce_llm`) provided is able to generate and merge document summaries efficiently. 
- `overlap_size`and `token_max`parameters should be adjusted according to the actual requirements and the characteristics of the document to optimize the effect of summary generation. 
- In scenarios where a large number of documents are processed or high performance is required, methods for`asummarize` asynchronous summary generation should be considered to improve processing efficiency. 

**Example output**:
```python
[Document(page_content="这是生成的文档摘要。", metadata={"file_description": "文件描述", "summary_intermediate_steps": "摘要中间步骤", "doc_ids": "文档ID列表"})]
```
This output example shows `summarize`a list of document summaries returned by the method, each of which contains metadata information such as the content of the generated summary, a description of the file, an intermediate step in the generation of the summary, and a list of document IDs. 
### FunctionDef __init__(self, overlap_size, token_max, chain)
**__init__**: The function of this function is to initialize the SummaryAdapter object. 

**Parameters**:
- `overlap_size`: Integer, which represents the size of the overlap between blocks of text.
- `token_max`: Integer, which represents the maximum number of tokens processed.
- `chain`: MapReduceDocumentsChain object, which is used to process the chaining operation of documents.

**Code Description**:
This `__init__`method `SummaryAdapter`is the constructor of a class and is used to initialize an instance of that class. In this method, the incoming`overlap_size` parameters are first assigned to a private variable `_OVERLAP_SIZE`that defines how much overlap there should be between the text blocks during the text summarization process. This is to ensure smooth transitions and maintain contextual coherence when working with long texts. 

Second, a `token_max`parameter is assigned directly to an instance variable`token_max`, which limits the maximum number of tokens (e.g., words or characters) that can be processed during text processing. This is to control the complexity of processing and resource consumption. 

Finally, a `chain`parameter is an `MapReduceDocumentsChain`object that is assigned to an instance variable`chain`. This object represents a chain sequence of operations that process a document, allowing for complex processes such as word segmentation, summary generation, and so on. 

**Note**:
- When working with `SummaryAdapter`classes, you need to make sure that the sum`overlap_size` `token_max`parameters passed in are reasonable to avoid performance issues or inaccurate results when processing. 
- `chain`The parameter needs to be a valid `MapReduceDocumentsChain`instance, which means that the chained operation should be configured correctly before it can be used. 
***
### FunctionDef form_summary(cls, llm, reduce_llm, overlap_size, token_max)
**form_summary**: This function is used to form a text summary. 

**Parameters**:
- **LLM**: A language model used to generate summaries. 
- **reduce_llm**: A language model used to merge summaries. 
- **overlap_size**: The size of the text overlap. 
- **token_max**: The maximum number of tokens per digest block, which is 1300 by default. 

**Code Description**:
`form_summary`A function is `SummaryAdapter`a method of a class that is responsible for creating a workflow for creating a text digest. The process involves using the language model to generate summaries, merging summaries, and processing blocks of text to ensure that each digest block is not longer than the specified maximum number of tokens. The function first defines a template for document formatting, and then defines a processing chain`llm_chain` that is used to generate a summary. Next, another processing chain is defined`reduce_llm_chain` to merge these summaries. Finally, by `MapReduceDocumentsChain`combining the processes that generate and merge summaries, a configured instance of the digest processing process is returned. 

In a project, `form_summary`functions are called in a number of places, including scenarios such as reconstructing the knowledge base digest vector store, converting a file digest to a vector store, and converting a digest to a vector store based on a document ID. These call scenarios show that`form_summary` functions are the core function of processing knowledge base document summaries, which can generate and merge document summaries according to different needs to support the construction and update of knowledge bases. 

**Note**:
- Make sure that the incoming`llm` `reduce_llm`and parameters are valid instances of the language model. 
- `overlap_size`and `token_max`parameters should be set reasonably according to actual needs to optimize the effect and performance of summary generation. 
- This function returns a configured digest processing process instance whose methods need`summarize` to be called to perform digest generation and merge operations. 

**Example output**:
Since `form_summary`the function returns a configured digest processing process instance rather than a direct digest result, there is no direct output example. However, after calling the method with the returned instance`summarize`, you can get a summary result in the following format:
```json
{
  "code": 200,
  "msg": "摘要生成成功",
  "summarize": [
    {
      "doc_id": "文档ID1",
      "summary": "这里是文档摘要内容..."
    },
    {
      "doc_id": "文档ID2",
      "summary": "这里是另一个文档的摘要内容..."
    }
  ]
}
```
This example shows the summary result format returned by the summary processing process instance after the document has been processed, which contains the ID of the document and the corresponding summary content.
***
### FunctionDef summarize(self, file_description, docs)
**summarize**: The function of this function is to synchronously call the method that generates a document summary asynchronously. 

**Parameters**:
- `file_description`: The type of string that describes the contents of the file.
- `docs`: `DocumentWithVSId` A list of types, which is an empty list by default. These documents will be used to generate summaries. 

**Code Description**:
`summarize` A function is `SummaryAdapter` a method of the class that is used to synchronously call an asynchronous method  to `asummarize` generate a summary of a document. The function first decides how to fetch or create an event loop based on the Python version check. If the Python version is earlier than 3.10, it will use `asyncio.get_event_loop()` to get the current event loop; For Python 3.10 and above, it tries to use `asyncio.get_running_loop()` Get Running Event Loop, and if it fails, creates a new event loop and sets it to the current event loop. After that, the function calls the method synchronously through the event loop's `run_until_complete` method `asummarize` , passing in a file description and a list of documents as arguments, and finally returns a `Document` list of objects. 

**Note**:
- This function is a synchronous wrapper that is used to call asynchronous methods in synchronous code `asummarize`, ensuring that asynchronous methods are executed correctly in a synchronous environment. 
- If the incoming document list `docs` is empty, the`asummarize` method will simply return an empty list of `Document` objects. 
- When using this function, you need to be aware of compatibility issues with your Python version to ensure that event loops can be fetched or created correctly.

**Example output**:
Calling  a `summarize` function might return a list in the following format:
```python
[
    Document(
        page_content="这里是合并后的摘要内容。",
        metadata={
            "file_description": "文件描述信息",
            "summary_intermediate_steps": "中间步骤的信息",
            "doc_ids": "文档ID列表"
        }
    )
]
```
This list contains an `Document` object with  a `page_content` property containing the generated summary content, and a `metadata` property containing a file description, information about the intermediate steps, and a list of document IDs. 
***
### FunctionDef asummarize(self, file_description, docs)
**asummarize**: The function of this function is to asynchronously generate a summary of the document. 

**Parameters**:
- `file_description`: The type of string that describes the contents of the file.
- `docs`: `DocumentWithVSId` A list of types, which is an empty list by default. These documents will be used to generate summaries. 

**Code Description**:
`asummarize` A function is `SummaryAdapter`an asynchronous method of a class that handles the generation of document summaries. The process is divided into two main parts: first, each document is processed to obtain a summary of each document; Second, these summaries are combined into a final one, and the information for the intermediate steps can be returned. 

When processing document summaries, the function first records log information that starts generating summaries. Then, a `chain.combine_docs`summary of the document is generated by calling the method, passing in a list of documents and a brief description of the task. This method returns the combined summary and information about the intermediate steps. The function prints out the combined summary and information about the intermediate steps for easy debugging and review. 

The function also records the document ID and encapsulates the file description, intermediate step information, and document ID as metadata along with the merged digest into an`Document` object. Finally, the function returns a`Document` list of the objects. 

**Note**:
- The function is asynchronous and needs to be called in an asynchronous environment.
- If the incoming list of documents is empty, the function will simply return an empty list of`Document` objects. 
- There is a comment piece of code in the function that states that the summary may need to be regenerated in some cases, and this part of the logic is not enabled in the current version.

**Example output**:
Calling `asummarize`a function might return a list in the following format:
```python
[
    Document(
        page_content="这里是合并后的摘要内容。",
        metadata={
            "file_description": "文件描述信息",
            "summary_intermediate_steps": "中间步骤的信息",
            "doc_ids": "文档ID列表"
        }
    )
]
```
This list contains an`Document` object with `page_content`properties containing the generated summary content, properties `metadata`containing a file description, information about intermediate steps, and a list of document IDs. 
***
### FunctionDef _drop_overlap(self, docs)
**_drop_overlap**: The function of this function is to remove the overlapping parts of the page content sentences in the document list. 

**Parameters**:
- `docs`: A list of instances of DocumentWithVSId, each representing a document containing the content of the page.

**Code Description**:
`_drop_overlap` The function receives as input a list of documents, which are represented by instances of the DocumentWithVSId class, each containing a page content property. The purpose of this function is to process the document list and remove the overlapping parts of the page content sentences, so as to facilitate the subsequent document processing or summary generation process and reduce the interference of redundant information. 

The function first initializes an empty list `merge_docs`that stores the processed document contents. Then, process each document one by one by iterating through the list of documents entered`docs`. For the first document in the list, its page content is added directly to `merge_docs`the list as a starting point for processing. For subsequent documents, the function checks whether there is any overlap between the beginning of the page content of the current document and the end of the page content of the previous document. If there is an overlap, the function removes the overlap from the page content of the current document and adds only the non-overlapping parts to the`merge_docs` list. 

Overlap detection and removal is achieved by iteratively reducing the length of the content of the previous document page and comparing it with the beginning of the content of the current document page until the overlapping part is found or a certain iteration condition is reached. Here two properties are used`self._OVERLAP_SIZE` `self._separator`to help determine the conditions and processing logic of overlap detection. 

**Note**:
- `_drop_overlap`Functions rely on `DocumentWithVSId`the properties of the class `page_content`to get the page content of the document. Therefore, make sure that each instance in the incoming document list contains valid page content. 
- The effect and performance of function processing can be affected by`self._OVERLAP_SIZE` the sum `self._separator`values, and adjusting these values appropriately can optimize the processing results. 

**Example output**:
Let's say you have two documents that say "It's a nice day, it's a good day to hang out." Good for going out and don't forget to bring an umbrella. "And" is good for going out and playing, don't forget to bring an umbrella. Tomorrow will be good weather as well. `_drop_overlap`After being processed by the function, the returned`merge_docs` list may be as follows:
```
["今天天气不错，适合出去玩。适合出去玩，不要忘记带伞。", "明天也是好天气。"]
```
This means that the overlapping portions of the second document that overlap with the first document have been successfully removed.
***
### FunctionDef _join_docs(self, docs)
**_join_docs**: The function of this function is to concatenate a list of strings into a string and return Zero if necessary. 

**Parameters**:
- `docs`: A list of strings, which is a list of documents to connect to.

**Code Description**:
`_join_docs` The function receives a list of strings as arguments. It uses instance variables `_separator` as delimiters to concatenate these strings into a new string. It then strips out the whitespace characters at both ends of the new string. If the processed string is empty (i.e., 0 in length), the function will return `None`; Otherwise, the processed string is returned. 

This function is designed to take into account the possible list of empty strings or full whitespace characters, ensuring that in this case not an empty string is returned, but `None` rather , which in many cases is helpful for subsequent logical judgments. 

**Note**:
- `_separator` It should be defined in the rest of the class, which determines how to insert separators between strings. If `_separator` is  not defined correctly, this function may not work as expected. 
- The incoming `docs` list must not be empty, otherwise the function will return `None` . 

**Example output**:
Assuming that  is `_separator` defined as a comma `,`and  the `docs` argument is  , `["Hello", "world", "!"]`then the return value of the function will be `"Hello,world,!"` . If  is `docs` an empty list, or if all strings in the list are empty or contain only whitespace characters, the function will return `None` . 
***
