from typing import List, Optional
from datetime import datetime, date, timezone
from sqlalchemy import String, Text, ForeignKey, Date, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login_manager 

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    role: Mapped[str] = mapped_column(String(20), default='arayıcı')
    avatar_file: Mapped[str] = mapped_column(String(120), default='default.jpg')
    
    # İlişkiler
    customers: Mapped[List["Customer"]] = relationship(back_populates="assigned_user", cascade="all, delete-orphan")
    notes: Mapped[List["Note"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} (Role: {self.role})>'

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(64))
    surname: Mapped[str] = mapped_column(String(64))
    birth_date: Mapped[Optional[date]] = mapped_column(Date)
    district: Mapped[Optional[str]] = mapped_column(String(100))
    profession: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Foreign Key
    assigned_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'))
    
    # İlişkiler
    assigned_user: Mapped[Optional["User"]] = relationship(back_populates="customers")
    notes: Mapped[List["Note"]] = relationship(back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Customer {self.name} {self.surname} (Ref: {self.reference})>'

class Note(db.Model):
    __tablename__ = 'notes'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Foreign Keys
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    # İlişkiler
    customer: Mapped["Customer"] = relationship(back_populates="notes")
    user: Mapped["User"] = relationship(back_populates="notes")

    def __repr__(self):
        return f'<Note {self.id} for Customer {self.customer_id} by User {self.user_id}>'

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    message: Mapped[str] = mapped_column(String(255))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user: Mapped["User"] = relationship(back_populates="notifications")

    def __repr__(self):
        return f'<Notification {self.id} for User {self.user_id}>'
