from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from server.database import Base

class ModelStore(Base):
    __tablename__ = "model_store"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)