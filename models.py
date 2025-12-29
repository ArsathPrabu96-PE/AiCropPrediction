from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Crop(Base):
    __tablename__ = 'crops'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))  # e.g., cereal, vegetable, fruit
    optimal_ph_min = Column(Float)
    optimal_ph_max = Column(Float)
    optimal_temperature_min = Column(Float)
    optimal_temperature_max = Column(Float)
    optimal_rainfall_min = Column(Float)
    optimal_rainfall_max = Column(Float)
    average_yield_per_hectare = Column(Float)
    market_price_per_kg = Column(Float)

class SoilType(Base):
    __tablename__ = 'soil_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    ph_level = Column(Float)
    nitrogen_content = Column(Float)
    phosphorus_content = Column(Float)
    potassium_content = Column(Float)
    texture = Column(String(50))  # sandy, clay, loam

class State(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    state_id = Column(Integer, ForeignKey('states.id'))
    soil_type_id = Column(Integer, ForeignKey('soil_types.id'))
    state = relationship('State')
    soil_type = relationship('SoilType')

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Float)
    humidity = Column(Float)
    rainfall = Column(Float)
    location = relationship('Location')

class Recommendation(Base):
    __tablename__ = 'recommendations'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    crop_id = Column(Integer, ForeignKey('crops.id'))
    predicted_yield = Column(Float)
    predicted_profit = Column(Float)
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    location = relationship('Location')
    crop = relationship('Crop')

# Create engine
engine = create_engine('sqlite:///crop_recommendation.db')
Base.metadata.create_all(engine)