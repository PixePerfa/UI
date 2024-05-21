from sqlalchemy import Column, Integer, String, DateTime, func

from server.db.base import Base


class KnowledgeBaseModel(Base):
    """
    Knowledge base model
    """
    __tablename__ = 'knowledge_base'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='KBID')
    kb_name = Column(String(50), comment='KB Name')
    kb_info = Column(String(200), comment='Introduction to the Knowledge Base (for Agent)')
    vs_type = Column(String(50), comment='vector library type')
    embed_model = Column(String(50), comment='Embedding Model Name')
    file_count = Column(Integer, default=0, comment='Number of files')
    create_time = Column(DateTime, default=func.now(), comment='Created')

    def __repr__(self):
        return f"<KnowledgeBase(id='{self.id}', kb_name='{self.kb_name}',kb_intro='{self.kb_info} vs_type='{self.vs_type}', embed_model='{self.embed_model}', file_count='{ self.file_count}', create_time='{self.create_time}')>"
