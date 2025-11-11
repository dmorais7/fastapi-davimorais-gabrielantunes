from datetime import datetime
from typing import Annotated
from sqlalchemy import func 
from sqlalchemy.orm import Mapped,mapped_column,registry

table_registry = registry()

class user(table_registry.Base):
    __tablename__='users'

    id: Mapped[int]= mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[Annotated[datetime, mapped_column(server_default=func.now())]]=mapped_column(init=False)