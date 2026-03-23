from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class WorkoutModel(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    workout_type = Column(String(100), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    calories_burned = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class MealModel(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    meal_type = Column(String(50), nullable=False)
    meal_date = Column(Date, nullable=False, index=True)
    notes = Column(String(1000), nullable=True)


class MealItemModel(Base):
    __tablename__ = "meal_items"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    quantity = Column(String(100), nullable=False)
    calories = Column(Integer, nullable=True)


class WaterLogModel(Base):
    __tablename__ = "water_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    log_date = Column(Date, nullable=False, index=True)
    amount_ml = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class DailyTargetModel(Base):
    __tablename__ = "daily_targets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    target_date = Column(Date, nullable=False, index=True)
    calories_target = Column(Integer, nullable=False)
    water_target_ml = Column(Integer, nullable=False)
    protein_target_g = Column(Integer, nullable=False)
    carbs_target_g = Column(Integer, nullable=False)
    fat_target_g = Column(Integer, nullable=False)

