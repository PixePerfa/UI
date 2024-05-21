from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, JSON, func

from server.db.base import Base


class KnowledgeFileModel(Base):
    """
    Knowledge file model
    """
    __tablename__ = 'knowledge_file'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='Knowledge File ID')
    file_name = Column(String(255), comment='filename')
    file_ext = Column(String(10), comment='File Extension')
    kb_name = Column(String(50), comment='Name of the knowledge base to which it belongs')
    document_loader_name = Column(String(50), comment='Document loader name')
    text_splitter_name = Column(String(50), comment='Text splitter name')
    file_version = Column(Integer, default=1, comment='File Version')
    file_mtime = Column(Float, default=0.0, comment="File modified time")
    file_size = Column(Integer, default=0, comment="file size")
    custom_docs = Column(Boolean, default=False, comment="Custom docs")
    docs_count = Column(Integer, default=0, comment="Split the number of documents")
    create_time = Column(DateTime, default=func.now(), comment='Created')

    def __repr__(self):
        return f"<KnowledgeFile(id='{self.id}', file_name='{self.file_name}', file_ext='{self.file_ext}', kb_name='{self.kb_name}', document_loader_name='{self.document_loader_name}', text_splitter_name='{self.text_splitter_name}', file_version='{self.file_version}', create_time='{self.create_time}')>"


class FileDocModel(Base):
    """
    File-vector library document model
    """
    __tablename__ = 'file_doc'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    kb_name = Column(String(50), comment='KB Name')
    file_name = Column(String(255), comment='filename')
    doc_id = Column(String(50), comment="Vector Library Document ID")
    meta_data = Column(JSON, default={})

    def __repr__(self):
        return f"<FileDoc(id='{self.id}', kb_name='{self.kb_name}', file_name='{self.file_name}', doc_id='{self.doc_id}', metadata='{self.meta_data}')>"
