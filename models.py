from datetime import datetime
from typing import Annotated, List
from sqlalchemy import func, ForeignKey, String
from sqlalchemy.orm import Mapped,mapped_column ,registry, relationship

table_registry = registry()
Base = table_registry.generate_base()

class user(table_registry.Base):
    __tablename__ = 'users'

    id: Mapped[int]= mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String(256))

    created_at: Mapped[Annotated[datetime, mapped_column(server_default=func.now())]]
    updated_at: Mapped[Annotated[datetime, mapped_column(server_default=func.now(), onupdate=func.now())]]

    receitas: Mapped[List["Receita"]] = relationship(back_populates="user")

class Receita(table_registry.Base):
    __tablename__ = 'receitas'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str]
    ingredientes: Mapped[str] = mapped_column(String(512)) 
    modo_de_preparo: Mapped[str] = mapped_column(String(2048))
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped["user"] = relationship(back_populates="receitas")