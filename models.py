from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped
from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    age: Mapped[int] = mapped_column(Integer)
    password: Mapped[str] = mapped_column(String)