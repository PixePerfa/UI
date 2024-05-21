from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from server.db.base import Base


class ConversationModel(Base):
    """
    Chat recording model
    """
    __tablename__ = 'conversation'
    id = Column(String(32), primary_key=True, comment='Dialog ID')
    name = Column(String(50), comment='The name of the dialog box')

    chat_type = Column(String(50), comment='The type of chat')
    create_time = Column(DateTime, default=func.now(), comment='Creation time')

    def __repr__(self):
        return f"<Conversation(id='{self.id}', name='{self.name}', chat_type='{self.chat_type}', create_time='{self.create_time}')>"
