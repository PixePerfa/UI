from datetime import datetime
from sqlalchemy import Column, DateTime, String, Integer


class BaseModel:
    """
    Base model
    """
    id = Column(Integer, primary_key=True, index=True, comment="Primary key ID")
    create_time = Column(DateTime, default=datetime.utcnow, comment="Creation time")
    update_time = Column(DateTime, default=None, onupdate=datetime.utcnow, comment="Updated")
    create_by = Column(String, default=None, comment="Created by")
    update_by = Column(String, default=None, comment="Renewer")
