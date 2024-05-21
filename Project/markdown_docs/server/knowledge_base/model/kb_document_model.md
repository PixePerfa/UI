## ClassDef DocumentWithVSId
**DocumentWithVSId**: The function of the DocumentWithVSId class is to represent a document that has been vectorized.

**Attributes**:
- `id`: The unique identifier of the document, of type string.
- `score`: The score of the document, with an initial default value of 3.0, of type floating point.

**Code Description**:
The DocumentWithVSId class inherits from the Document class and is used to represent a document that has been vectorized. This class is mainly used in knowledge base systems. After the document is vectorized, the processing result is represented by an instance of this class. Two attributes are defined in the class: `id` and `score`. The `id` attribute is used to store the unique identifier of the document, while the `score` attribute is used to store the score or relevance measure of the document in certain operations (such as searching or sorting).

In the project, instances of the DocumentWithVSId class are mainly used in the following scenarios:
1. When searching for knowledge base documents, the search results returned will contain a series of DocumentWithVSId instances, each of which represents a searched document, and its `score` attribute indicates the degree of match between the document and the search query.
2. When listing knowledge base documents, if you need to filter based on specific file names or metadata, the returned results may also contain DocumentWithVSId instances.
3. In the document summary generation process, DocumentWithVSId instances are used to represent documents that need to be summarized, and the `id` attribute is used to identify specific documents.

**Note**:
- When using the DocumentWithVSId class, you need to pay attention to the uniqueness of the `id` attribute to ensure that each instance can accurately correspond to a specific document in the knowledge base.
- The value of the `score` attribute may change depending on different operations or contexts, so you should pay attention to its meaning and calculation method when using it.