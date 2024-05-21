from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, JSON, func

from server.db.base import Base


class SummaryChunkModel(Base):
    """
    Chunk Summary model to store chunk fragments for each doc_id in the file_doc,
    Source:
        User input: The user uploads the file, can fill in the description of the file, and the doc_id in the generated file_doc is stored in the summary_chunk
        The program automatically splits the page number information stored in the field information meta_data the file_doc table, divides it according to the page number of each page, generates a summary text by custom prompt, and stores the doc_id associated with the corresponding page number into the summary_chunk
    Follow-up tasks:
        Vector library construction: Create indexes to summary_context in the database table summary_chunk, build vector libraries, and meta_data metadata for vector libraries (doc_ids)
        Semantic association: Automatically segment the summary text and calculate the description entered by the user
        Semantic similarity
    """
    __tablename__ = 'summary_chunk'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    kb_name = Column(String(50), comment='The name of the knowledge base')
    summary_context = Column(String(255), comment='Summarize the text')
    summary_id = Column(String(255), comment='Summarize the vector id')
    doc_ids = Column(String(1024), comment="A list of associated vector library IDs")
    meta_data = Column(JSON, default={})

    def __repr__(self):
        return (f"<SummaryChunk(id='{self.id}', kb_name='{self.kb_name}', summary_context='{self.summary_context}',"
                f" doc_ids='{self.doc_ids}', metadata='{self.metadata}')>")
