# models/text_simplification/simplification_log.py

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base

class SimplificationLog(Base):
    __tablename__ = "simplification_logs"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    simplified_text = Column(Text, nullable=False)
    language = Column(String(2), nullable=True)  # ISO 639-1 code
    complexity_level = Column(Integer, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<SimplificationLog id={self.id} language={self.language} timestamp={self.timestamp}>"
