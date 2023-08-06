from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)

from ...database import Base


class AssistantSearchCopilotModel(Base):
    __tablename__ = "assistant_search_copilot"

    id = Column(Integer, primary_key=True)
    assistant_user_query_id = Column(
        Integer,
        ForeignKey("assistant_user_queries.id"),
        nullable=True,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
