from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    contact_info = Column(String, index=True)
    is_active = Column(Boolean, default=True)

    # dogs = relationship("Dog", back_populates="owner")
    dogs = relationship("Dog", back_populates="owner",
                        cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', contact_info='{self.contact_info}', is_active={self.is_active}, dogs={self.dogs})>"


class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    breed = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="dogs")
