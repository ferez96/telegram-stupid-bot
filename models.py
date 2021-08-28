import enum
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String, DateTime, func, Enum

Base = declarative_base(bind=None)
Session = sessionmaker(bind=None)
db_session = scoped_session(Session)


class AuditMixin(object):
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Group(AuditMixin, Base):
    __tablename__ = "groups"

    class Status(enum.Enum):
        inactive = 0
        active = 1

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.inactive)
