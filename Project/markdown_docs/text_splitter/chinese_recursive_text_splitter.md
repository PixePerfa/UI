## FunctionDef _split_text_with_regex_from_end(text, separator, keep_separator)
**_split_text_with_regex_from_end**: The function of this function is to use regular expressions to split the text from the end of the text. 

**Parameters**:
- text: The text that needs to be split, of type str.
- separator: A regular expression used as a splitter, of type str.
- keep_separator: A boolean value that indicates whether to keep the delimiter in the returned list.

**Code Description**:
This function accepts a string`text` and a regular expression `separator`as arguments, as well as a boolean value `keep_separator`that controls whether the delimiter is retained after the split. If it`separator` is not empty, the function will split the text according to`separator` it. If `keep_separator`true, the delimiter is also kept in the returned list. This is achieved by splitting the text along with the delimiter, and then reassembling the split text and the delimiter into a new list item. If the length of the split list is odd, it means that there is no separator after the last element, and the last element will be added to the result list. If`keep_separator` false, the text is simply split according to the delimiter and the separator is not kept. If `separator`empty, the text is split into a list of individual characters. Finally, the function returns a list of non-null split results. 

In the project, this function is called by`ChineseRecursiveTextSplitter` a class`_split_text` method. `_split_text`The method is used to recursively split the text, gradually splitting the text into smaller chunks based on a series of separators. `_split_text_with_regex_from_end`Functions are responsible for splitting from the end of the text using regular expressions in this process, which is one of the key steps in achieving recursive text segmentation. By adjusting `keep_separator`the parameters, you can flexibly control how well the separator is retained in the segmentation result, which is very useful for maintaining the original structure information of the text. 

**Note**:
- Make sure that you are passing in`separator` a valid regular expression, otherwise`re.split` the split may not be performed correctly. 
- If the text is very long, using complex regular expressions as delimiters can impact performance.

**Example output**:
Suppose you have the following call:
```python
_split_text_with_regex_from_end("hello,world,this,is,a,test", ",", True)
```
The possible return values are:
```python
["hello,", "world,", "this,", "is,", "a,", "test"]
```
In this example, the text is separated by commas, and the commas are retained for each segmented part.
## ClassDef ChineseRecursiveTextSplitter
**ChineseRecursiveTextSplitter**: The function of this class is to recursively split Chinese text. 

**Properties**:
- `separators`: A list of delimiters to specify rules for text segmentation.
- `keep_separator`: Boolean, which specifies whether to keep the delimiter in the split text.
- `is_separator_regex`: Boolean, which specifies whether the element in the delimiter list is a regular expression.

**Code Description**:
The ChineseRecursiveTextSplitter class inherits from RecursiveCharacterTextSplitter and is specifically designed to handle recursive segmentation of Chinese text. It allows the user to customize the list of delimiters, as well as control whether delimiters are kept and whether delimiters are treated as regular expressions. The default separator list includes common Chinese and English sentence end symbols, such as periods, question marks, exclamation marks, and so on. This class`_split_text` can effectively split long text into smaller fragments through recursive invocation methods, while ensuring that the segmented text fragments are not too long or too short, which is suitable for further text processing or analysis. 

When splitting text, the `_split_text`method first determines the separator to use, and then divides the text into small pieces based on this separator. If the length of a fragment exceeds a preset threshold, the method recursively splits the fragment until all segments are within the required length. Eventually, the method returns a list of text fragments that have been cleaned (stripped of extra line breaks and whitespace). 

**Note**:
- When using custom delimiters, if`is_separator_regex` set to`False`, you need to make sure that the elements in the delimiter list do not contain any regular expression special characters, or are used`re.escape` for escape. 
- This class is suitable for processing Chinese text, but also supports text segmentation containing English sentences, and can flexibly respond to different text segmentation needs by providing an appropriate separator list.

**Example output**:
```python
text_splitter = ChineseRecursiveTextSplitter()
text = "This is a test text. Contains multiple sentences! There are also English sentences. Yes, it works well."
split_texts = text_splitter.split(text)
# Output may be: ['This is a test text. ', 'Contains multiple sentences! ', 'There are also English sentences.', 'Yes, it works well.']
```
In this example, the `split`method splits the entered text based on sentence ending symbols in Chinese and English, returning a list of four separate sentences. This shows the flexibility and effectiveness of the ChineseRecursiveTextSplitter class when working with mixed-language text. 
### FunctionDef __init__(self, separators, keep_separator, is_separator_regex)
**__init__**: The function of this function is to create a new text splitter. 

**Parameters**:
- **separators**: An optional parameter of type`List[str]`. A list of delimiters used to specify the split text. If not provided, the default delimiter list is used. 
- **keep_separator**: Boolean type parameter, default value`True`. Specifies whether to retain the separator after splitting the text. 
- **is_separator_regex**: Boolean type parameter, the default value is`True`. Specifies whether a delimiter in the delimiter list should be considered a regular expression. 
- **kwargs**: Receives any additional keyword arguments that will be passed to the parent class's initialization method. 

**Code Description**:
This function is `ChineseRecursiveTextSplitter`the constructor of the class and is used to initialize an instance of a text splitter. It first calls the parent class's initialization method, passing,`keep_separator` and any other keyword arguments (`**kwargs`). It then initializes the internal variables based on the provided parameters. If the `separators`parameter is not provided, a default list of separators is used, which includes common Chinese and English sentence closing symbols, such as periods, question marks, exclamation marks, and their respective space combinations, as well as commas and semicolons in Chinese. `_is_separator_regex`Variables are used to mark whether an element in a delimiter list should be treated as a regular expression for use when splitting text. 

**Note**:
- When using the default separator, you can match a variety of common sentence closing symbols and the spaces that follow them due to the inclusion of regular expressions, which is useful for working with text that contains multiple types of punctuation marks.
- If you select Do not keep the delimiter (`keep_separator=False`), the split text will not contain any delimiters. This may have an impact on certain application scenarios that require precise control over the output format. 
- When`is_separator_regex` set, `False`the strings in the delimiter list will be used directly as the basis for splitting the text, rather than as a regular expression, which may be more useful when dealing with very specific delimiter needs. 
***
### FunctionDef _split_text(self, text, separators)
**_split_text**: The function of this function is to recursively split the text based on a series of delimiters and return a list of the divided text blocks. 

**Parameters**:
- text: The text that needs to be split, of type str.
- separators: A list of delimiters used to split text, of type List[str]. 

**Code Description**:
`_split_text`The function first determines which separator to use to split the text. It does this by iterating through `separators`the list and checking if each delimiter is present in the text. Once the first matching delimiter is found, the function uses this delimiter to split the text and updates the subsequent delimiter list to a new`new_separators` list for subsequent recursive splitting. 

The actual operation of splitting the text is done by calling `_split_text_with_regex_from_end`a function that uses a regular expression to split the text starting from the end of the text. This step allows you to keep or remove the delimiter, depending on`_keep_separator` the value. 

Next, the function checks the length of each text block after splitting. If the length of the text block is less than the set one`_chunk_size`, it is added to the results list. For blocks of text that are longer than`_chunk_size` that, the function attempts to `new_separators`recursively split those blocks of text using the next delimiter in the list. 

Finally, the function returns a cleaned list of text blocks with all blank text blocks removed and successive line breaks replaced with single line breaks.

**Note**:
- Make sure that `separators`the separators in the list are valid and in order from highest to least first. 
- Functions internally use regular expressions for text segmentation, so the delimiter needs to be a valid regular expression, or if not split with a regular expression, the delimiter will be automatically escaped.
- Recursive splitting can result in a large number of function calls, especially when dealing with large texts or complex delimiter patterns, and you should be aware of the risk of performance and stack overflow.

**Example output**:
Suppose you have the following call:
```python
_split_text("This is a test text. This is still a test text!", [".", "!"])
```
The possible return values are:
```python
["This is a test text", "This is still a test text"]
```
In this example, the text is "". "And"! "Separator splitting, where each split part is a separate block of text.
***
