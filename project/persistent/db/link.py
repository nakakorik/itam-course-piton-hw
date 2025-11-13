import uuid
from datetime import UTC, datetime
from utils.utc_now import utcnow

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def _uuid4_as_str()-> str:
    return str(uuid.uuid4())



class Link(Base):
    __tablename__ = "link"

    id = Column(Text, default = _uuid4_as_str, primary_key = True)
    created_at = Column(DateTime(timezone=True), default = utcnow, nullable = False)

    short_link = Column(Text, nullable = False, unique = True)
    real_link = Column(Text, nullable = False)


class Link_Usage(Base):
    __tablename__ = "link_usage"

    id = Column(Text, default = _uuid4_as_str, primary_key = True)
    usedlink_id = Column(Text, nullable = False)
    user_agent = Column(Text, nullable = False)
    created_at = Column(DateTime(timezone=True), default = utcnow, nullable = False)
    short_link = Column(Text, nullable = False)


