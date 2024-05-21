from sqlalchemy import Column, Integer, String, DateTime, JSON, func

from server.db.base import Base


class MessageModel(Base):
    """
    Chat recording model
    """
    __tablename__ = 'message'
    id = Column(String(32), primary_key=True, comment='Chat history ID')
    conversation_id = Column(String(32), default=None, index=True, comment='Dialog ID')
    chat_type = Column(String(50), comment='The type of chat')
    query = Column(String(4096), comment='User issues')
    response = Column(String(4096), comment='Model answers')
    # Record the knowledge base ID, etc., for subsequent expansion
    meta_data = Column(JSON, default={})
    # The higher the score out of 100, the better the review
    feedback_score = Column(Integer, default=-1, comment='User ratings')
    feedback_reason = Column(String(255), default="", comment='Reason for user rating')
    create_time = Column(DateTime, default=func.now(), comment='Creation time')

    def __repr__(self):
        return f"<message(id='{self.id}', conversation_id='{self.conversation_id}', chat_type='{self.chat_type}', query='{self.query}', response='{self.response}',meta_data='{self.meta_data}',feedback_score='{self.feedback_score}',feedback_reason='{self.feedback_reason}', create_time='{self.create_time}')>"
