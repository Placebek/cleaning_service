from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, String, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), default="", nullable=True)
    last_name = Column(String(50), default="", nullable=True)
    username = Column(String(50), unique=True)
    tg_id = Column(Integer)
    phone_number = Column(String(30))
    cleaning_date = Column(Date)
    created_at = Column(TIMESTAMP, default=datetime.now)

    city_name_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'), nullable=True)
    street_name_id = Column(Integer, ForeignKey('streets.id', ondelete='CASCADE'), nullable=True)
    house_number_id = Column(Integer, ForeignKey('houses.id', ondelete='CASCADE'), nullable=True)
    apartment_number_id = Column(Integer, ForeignKey('apartments.id', ondelete='CASCADE'), nullable=True)

    city_name = relationship("City", back_populates="user")
    street_name = relationship("Street", back_populates="user")
    house_number = relationship("House", back_populates="user")
    apartment_number = relationship("Apartment", back_populates="user")
    orders = relationship("Order", back_populates="user")

    admin_user = relationship("AdminUser", back_populates="user", uselist=False)


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String(20))

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    user = relationship("User", back_populates="admin_user")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String(50))

    user = relationship("User", back_populates="city_name")


class Street(Base):
    __tablename__ = "streets"

    id = Column(Integer, primary_key=True, index=True)
    street_name = Column(String(50))

    user = relationship("User", back_populates="street_name")


class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    house_number = Column(Integer)

    user = relationship("User", back_populates="house_number")


class Apartment(Base):
    __tablename__ = "apartments"

    id = Column(Integer, primary_key=True, index=True)
    apartment_number = Column(Integer)

    user = relationship("User", back_populates="apartment_number")
    

class TypeOfPremises(Base):
    __tablename__ = "types_of_premises"

    id = Column(Integer, primary_key=True, index=True)
    type_of_premises = Column(String(100))


class TypeOfCleaning(Base):
    __tablename__ = "types_of_cleaning"

    id = Column(Integer, primary_key=True, index=True)
    surface_cleaning = Column(Boolean, default=False)
    deep_cleaning = Column(Boolean, default=False)
    sanitizing = Column(Boolean, default=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    user = relationship("User", back_populates="orders")

    types_of_cleaning_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    types_of_cleaning = relationship("User", back_populates="orders")

    types_of_premises_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    types_of_premises = relationship("User", back_populates="orders")

