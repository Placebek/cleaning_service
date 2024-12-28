from dataclasses import Field
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, String, Integer, Float, ForeignKey, Date, func
from sqlalchemy.orm import relationship

from database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), default="", nullable=True)
    last_name = Column(String(50), default="", nullable=True)
    phone_number = Column(String(30), nullable=True)
    tg_username = Column(String(50), nullable=True)
    tg_id = Column(Integer, nullable=True)

    address_id = Column(Integer, ForeignKey('addresses.id', ondelete='CASCADE'), nullable=True)
    
    created_at: Optional[datetime] = Column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    address = relationship("Address", back_populates="user", uselist=False)
    worker = relationship("Worker", back_populates="user")
    admin = relationship("Admin", back_populates="user")
    request = relationship("Request", back_populates="user")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    user = relationship("User", back_populates="admin")
    order = relationship("Order", back_populates="admin")


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    photo = Column(String)
    experience = Column(Integer)
    is_active = Column(Boolean)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)

    created_at: Optional[datetime] = Column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
    updated_at: Optional[datetime] = Column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    user = relationship("User", back_populates="worker")
    order = relationship("Order", back_populates="worker")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)

    city_name_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'), nullable=True)
    street_name_id = Column(Integer, ForeignKey('streets.id', ondelete='CASCADE'), nullable=True)
    house_number = Column(Integer, nullable=True)
    apartment_number = Column(Integer, nullable=True)

    created_at: Optional[datetime] = Column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    user = relationship("User", back_populates="address")

    city_name = relationship("City", back_populates="address")
    street_name = relationship("Street", back_populates="address")


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    volume_work_id = Column(Integer, ForeignKey('volume_works.id', ondelete='CASCADE'), nullable=True)
    date = Column(Date)

    user = relationship("User", back_populates="request")
    volume_work = relationship("VolumeWork", back_populates="request")
    order = relationship("Order", back_populates="request")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    worker_id = Column(Integer, ForeignKey('workers.id', ondelete='CASCADE'), nullable=True)
    admin_id = Column(Integer, ForeignKey('admins.id', ondelete='CASCADE'), nullable=True)
    request_id = Column(Integer, ForeignKey('requests.id', ondelete='CASCADE'), nullable=True)
    status_id = Column(Integer, ForeignKey('statuses.id', ondelete='CASCADE'), nullable=True)

    worker = relationship("Worker", back_populates="order")
    admin = relationship("Admin", back_populates="order")
    request = relationship("Request", back_populates="order")
    status = relationship("Status", back_populates="order")


class VolumeWork(Base):
    __tablename__ = "volume_works"

    id = Column(Integer, primary_key=True, index=True)
    worker_count = Column(Integer)
    cleaning_type_id = Column(Integer, ForeignKey('cleaning_types.id', ondelete='CASCADE'), nullable=True)
    premises_type_id = Column(Integer, ForeignKey('premises_types.id', ondelete='CASCADE'), nullable=True)

    cleaning_type = relationship("CleaningType", back_populates="volume_work")
    premises_type = relationship("PremisesType", back_populates="volume_work")
    request = relationship("Request", back_populates="volume_work")


class PremisesType(Base):
    __tablename__ = "premises_types"

    id = Column(Integer, primary_key=True, index=True)
    premises_type = Column(String(100))

    volume_work = relationship("VolumeWork", back_populates="premises_type")


class CleaningType(Base):
    __tablename__ = "cleaning_types"

    id = Column(Integer, primary_key=True, index=True)
    cleaning_type = Column(String(50))

    volume_work = relationship("VolumeWork", back_populates="cleaning_type")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String(50))

    address = relationship("Address", back_populates="city_name")


class Street(Base):
    __tablename__ = "streets"

    id = Column(Integer, primary_key=True, index=True)
    street_name = Column(String(50))

    address = relationship("Address", back_populates="street_name")


class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True, index=True)
    status_name = Column(String(50))

    order = relationship("Order", back_populates="status")
