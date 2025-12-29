import sys
sys.path.append('..')
from models import Crop, SoilType, State, Location, WeatherData, Recommendation, engine
from sqlalchemy.orm import sessionmaker
import random

Session = sessionmaker(bind=engine)
session = Session()

# Sample crops
crops_data = [
    {'name': 'Wheat', 'category': 'Cereal', 'optimal_ph_min': 6.0, 'optimal_ph_max': 7.5, 'optimal_temperature_min': 15, 'optimal_temperature_max': 25, 'optimal_rainfall_min': 300, 'optimal_rainfall_max': 600, 'average_yield_per_hectare': 3000, 'market_price_per_kg': 21},
    {'name': 'Rice', 'category': 'Cereal', 'optimal_ph_min': 5.5, 'optimal_ph_max': 6.5, 'optimal_temperature_min': 20, 'optimal_temperature_max': 30, 'optimal_rainfall_min': 1000, 'optimal_rainfall_max': 2000, 'average_yield_per_hectare': 4000, 'market_price_per_kg': 25},
    {'name': 'Maize', 'category': 'Cereal', 'optimal_ph_min': 5.8, 'optimal_ph_max': 7.0, 'optimal_temperature_min': 18, 'optimal_temperature_max': 27, 'optimal_rainfall_min': 500, 'optimal_rainfall_max': 800, 'average_yield_per_hectare': 3500, 'market_price_per_kg': 17},
    {'name': 'Tomato', 'category': 'Vegetable', 'optimal_ph_min': 6.0, 'optimal_ph_max': 6.8, 'optimal_temperature_min': 15, 'optimal_temperature_max': 25, 'optimal_rainfall_min': 500, 'optimal_rainfall_max': 700, 'average_yield_per_hectare': 20000, 'market_price_per_kg': 42},
    {'name': 'Potato', 'category': 'Vegetable', 'optimal_ph_min': 5.0, 'optimal_ph_max': 6.5, 'optimal_temperature_min': 15, 'optimal_temperature_max': 20, 'optimal_rainfall_min': 500, 'optimal_rainfall_max': 700, 'average_yield_per_hectare': 25000, 'market_price_per_kg': 25},
]

# Sample soil types
soil_data = [
    {'name': 'Loam', 'ph_level': 6.5, 'nitrogen_content': 0.15, 'phosphorus_content': 0.08, 'potassium_content': 0.12, 'texture': 'loam'},
    {'name': 'Clay', 'ph_level': 7.0, 'nitrogen_content': 0.12, 'phosphorus_content': 0.06, 'potassium_content': 0.10, 'texture': 'clay'},
    {'name': 'Sandy', 'ph_level': 6.0, 'nitrogen_content': 0.08, 'phosphorus_content': 0.04, 'potassium_content': 0.06, 'texture': 'sandy'},
]

# Sample states
states_data = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
    'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
    'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
]

# Sample locations (villages)
locations_data = [
    # Andhra Pradesh
    {'name': 'Vijayawada Village', 'latitude': 16.5062, 'longitude': 80.6480, 'state_name': 'Andhra Pradesh', 'soil_type_name': 'Loam'},
    {'name': 'Tirupati Village', 'latitude': 13.6288, 'longitude': 79.4192, 'state_name': 'Andhra Pradesh', 'soil_type_name': 'Sandy'},
    {'name': 'Guntur Village', 'latitude': 16.3067, 'longitude': 80.4365, 'state_name': 'Andhra Pradesh', 'soil_type_name': 'Clay'},
    # Arunachal Pradesh
    {'name': 'Itanagar Village', 'latitude': 27.0844, 'longitude': 93.6053, 'state_name': 'Arunachal Pradesh', 'soil_type_name': 'Loam'},
    {'name': 'Tawang Village', 'latitude': 27.5861, 'longitude': 91.8594, 'state_name': 'Arunachal Pradesh', 'soil_type_name': 'Clay'},
    # Assam
    {'name': 'Guwahati Village', 'latitude': 26.1445, 'longitude': 91.7362, 'state_name': 'Assam', 'soil_type_name': 'Clay'},
    {'name': 'Dibrugarh Village', 'latitude': 27.4728, 'longitude': 94.9119, 'state_name': 'Assam', 'soil_type_name': 'Loam'},
    {'name': 'Silchar Village', 'latitude': 24.8333, 'longitude': 92.7789, 'state_name': 'Assam', 'soil_type_name': 'Sandy'},
    # Bihar
    {'name': 'Patna Village', 'latitude': 25.5941, 'longitude': 85.1376, 'state_name': 'Bihar', 'soil_type_name': 'Sandy'},
    {'name': 'Gaya Village', 'latitude': 24.7955, 'longitude': 84.9994, 'state_name': 'Bihar', 'soil_type_name': 'Loam'},
    {'name': 'Bhagalpur Village', 'latitude': 25.2425, 'longitude': 86.9842, 'state_name': 'Bihar', 'soil_type_name': 'Clay'},
    # Chhattisgarh
    {'name': 'Raipur Village', 'latitude': 21.2514, 'longitude': 81.6296, 'state_name': 'Chhattisgarh', 'soil_type_name': 'Clay'},
    {'name': 'Bilaspur Village', 'latitude': 22.0797, 'longitude': 82.1391, 'state_name': 'Chhattisgarh', 'soil_type_name': 'Sandy'},
    # Goa
    {'name': 'Panaji Village', 'latitude': 15.4909, 'longitude': 73.8278, 'state_name': 'Goa', 'soil_type_name': 'Sandy'},
    {'name': 'Margao Village', 'latitude': 15.2832, 'longitude': 73.9862, 'state_name': 'Goa', 'soil_type_name': 'Loam'},
    # Gujarat
    {'name': 'Ahmedabad Village', 'latitude': 23.0225, 'longitude': 72.5714, 'state_name': 'Gujarat', 'soil_type_name': 'Loam'},
    {'name': 'Surat Village', 'latitude': 21.1702, 'longitude': 72.8311, 'state_name': 'Gujarat', 'soil_type_name': 'Clay'},
    {'name': 'Vadodara Village', 'latitude': 22.3072, 'longitude': 73.1812, 'state_name': 'Gujarat', 'soil_type_name': 'Sandy'},
    # Haryana
    {'name': 'Chandigarh Village', 'latitude': 30.7333, 'longitude': 76.7794, 'state_name': 'Haryana', 'soil_type_name': 'Sandy'},
    {'name': 'Faridabad Village', 'latitude': 28.4089, 'longitude': 77.3178, 'state_name': 'Haryana', 'soil_type_name': 'Loam'},
    # Himachal Pradesh
    {'name': 'Shimla Village', 'latitude': 31.1048, 'longitude': 77.1734, 'state_name': 'Himachal Pradesh', 'soil_type_name': 'Loam'},
    {'name': 'Manali Village', 'latitude': 32.2432, 'longitude': 77.1892, 'state_name': 'Himachal Pradesh', 'soil_type_name': 'Clay'},
    # Jharkhand
    {'name': 'Ranchi Village', 'latitude': 23.3441, 'longitude': 85.3096, 'state_name': 'Jharkhand', 'soil_type_name': 'Clay'},
    {'name': 'Jamshedpur Village', 'latitude': 22.8046, 'longitude': 86.2029, 'state_name': 'Jharkhand', 'soil_type_name': 'Sandy'},
    # Karnataka
    {'name': 'Bangalore Village', 'latitude': 12.9716, 'longitude': 77.5946, 'state_name': 'Karnataka', 'soil_type_name': 'Sandy'},
    {'name': 'Mysore Village', 'latitude': 12.2958, 'longitude': 76.6394, 'state_name': 'Karnataka', 'soil_type_name': 'Loam'},
    {'name': 'Mangalore Village', 'latitude': 12.9141, 'longitude': 74.8560, 'state_name': 'Karnataka', 'soil_type_name': 'Clay'},
    # Kerala
    {'name': 'Thiruvananthapuram Village', 'latitude': 8.5241, 'longitude': 76.9366, 'state_name': 'Kerala', 'soil_type_name': 'Clay'},
    {'name': 'Kochi Village', 'latitude': 9.9312, 'longitude': 76.2673, 'state_name': 'Kerala', 'soil_type_name': 'Sandy'},
    {'name': 'Kozhikode Village', 'latitude': 11.2588, 'longitude': 75.7804, 'state_name': 'Kerala', 'soil_type_name': 'Loam'},
    # Madhya Pradesh
    {'name': 'Bhopal Village', 'latitude': 23.2599, 'longitude': 77.4126, 'state_name': 'Madhya Pradesh', 'soil_type_name': 'Loam'},
    {'name': 'Indore Village', 'latitude': 22.7196, 'longitude': 75.8577, 'state_name': 'Madhya Pradesh', 'soil_type_name': 'Clay'},
    {'name': 'Jabalpur Village', 'latitude': 23.1815, 'longitude': 79.9864, 'state_name': 'Madhya Pradesh', 'soil_type_name': 'Sandy'},
    # Maharashtra
    {'name': 'Mumbai Village', 'latitude': 19.0760, 'longitude': 72.8777, 'state_name': 'Maharashtra', 'soil_type_name': 'Clay'},
    {'name': 'Pune Village', 'latitude': 18.5204, 'longitude': 73.8567, 'state_name': 'Maharashtra', 'soil_type_name': 'Sandy'},
    {'name': 'Nagpur Village', 'latitude': 21.1458, 'longitude': 79.0882, 'state_name': 'Maharashtra', 'soil_type_name': 'Loam'},
    # Manipur
    {'name': 'Imphal Village', 'latitude': 24.8170, 'longitude': 93.9368, 'state_name': 'Manipur', 'soil_type_name': 'Loam'},
    {'name': 'Thoubal Village', 'latitude': 24.6389, 'longitude': 94.0167, 'state_name': 'Manipur', 'soil_type_name': 'Clay'},
    # Meghalaya
    {'name': 'Shillong Village', 'latitude': 25.5788, 'longitude': 91.8933, 'state_name': 'Meghalaya', 'soil_type_name': 'Clay'},
    {'name': 'Tura Village', 'latitude': 25.5128, 'longitude': 90.2200, 'state_name': 'Meghalaya', 'soil_type_name': 'Sandy'},
    # Mizoram
    {'name': 'Aizawl Village', 'latitude': 23.7271, 'longitude': 92.7176, 'state_name': 'Mizoram', 'soil_type_name': 'Sandy'},
    {'name': 'Lunglei Village', 'latitude': 22.8667, 'longitude': 92.7500, 'state_name': 'Mizoram', 'soil_type_name': 'Loam'},
    # Nagaland
    {'name': 'Kohima Village', 'latitude': 25.6747, 'longitude': 94.1100, 'state_name': 'Nagaland', 'soil_type_name': 'Loam'},
    {'name': 'Dimapur Village', 'latitude': 25.9094, 'longitude': 93.7267, 'state_name': 'Nagaland', 'soil_type_name': 'Clay'},
    # Odisha
    {'name': 'Bhubaneswar Village', 'latitude': 20.2961, 'longitude': 85.8245, 'state_name': 'Odisha', 'soil_type_name': 'Clay'},
    {'name': 'Cuttack Village', 'latitude': 20.4625, 'longitude': 85.8830, 'state_name': 'Odisha', 'soil_type_name': 'Sandy'},
    {'name': 'Rourkela Village', 'latitude': 22.2604, 'longitude': 84.8536, 'state_name': 'Odisha', 'soil_type_name': 'Loam'},
    # Punjab
    {'name': 'Amritsar Village', 'latitude': 31.6340, 'longitude': 74.8723, 'state_name': 'Punjab', 'soil_type_name': 'Loam'},
    {'name': 'Ludhiana Village', 'latitude': 30.9000, 'longitude': 75.8573, 'state_name': 'Punjab', 'soil_type_name': 'Clay'},
    # Rajasthan
    {'name': 'Jaipur Village', 'latitude': 26.9124, 'longitude': 75.7873, 'state_name': 'Rajasthan', 'soil_type_name': 'Sandy'},
    {'name': 'Jodhpur Village', 'latitude': 26.2389, 'longitude': 73.0243, 'state_name': 'Rajasthan', 'soil_type_name': 'Clay'},
    {'name': 'Udaipur Village', 'latitude': 24.5854, 'longitude': 73.7125, 'state_name': 'Rajasthan', 'soil_type_name': 'Loam'},
    # Sikkim
    {'name': 'Gangtok Village', 'latitude': 27.3389, 'longitude': 88.6065, 'state_name': 'Sikkim', 'soil_type_name': 'Loam'},
    {'name': 'Namchi Village', 'latitude': 27.1650, 'longitude': 88.3650, 'state_name': 'Sikkim', 'soil_type_name': 'Clay'},
    # Tamil Nadu
    {'name': 'Chennai Village', 'latitude': 13.0827, 'longitude': 80.2707, 'state_name': 'Tamil Nadu', 'soil_type_name': 'Sandy'},
    {'name': 'Madurai Village', 'latitude': 9.9252, 'longitude': 78.1198, 'state_name': 'Tamil Nadu', 'soil_type_name': 'Clay'},
    {'name': 'Coimbatore Village', 'latitude': 11.0168, 'longitude': 76.9558, 'state_name': 'Tamil Nadu', 'soil_type_name': 'Loam'},
    # Telangana
    {'name': 'Hyderabad Village', 'latitude': 17.3850, 'longitude': 78.4867, 'state_name': 'Telangana', 'soil_type_name': 'Loam'},
    {'name': 'Warangal Village', 'latitude': 17.9689, 'longitude': 79.5941, 'state_name': 'Telangana', 'soil_type_name': 'Clay'},
    # Tripura
    {'name': 'Agartala Village', 'latitude': 23.8315, 'longitude': 91.2868, 'state_name': 'Tripura', 'soil_type_name': 'Sandy'},
    {'name': 'Udaipur Village', 'latitude': 23.5333, 'longitude': 91.4833, 'state_name': 'Tripura', 'soil_type_name': 'Loam'},
    # Uttar Pradesh
    {'name': 'Lucknow Village', 'latitude': 26.8467, 'longitude': 80.9462, 'state_name': 'Uttar Pradesh', 'soil_type_name': 'Clay'},
    {'name': 'Kanpur Village', 'latitude': 26.4499, 'longitude': 80.3319, 'state_name': 'Uttar Pradesh', 'soil_type_name': 'Loam'},
    {'name': 'Agra Village', 'latitude': 27.1767, 'longitude': 78.0081, 'state_name': 'Uttar Pradesh', 'soil_type_name': 'Sandy'},
    # Uttarakhand
    {'name': 'Dehradun Village', 'latitude': 30.3165, 'longitude': 78.0322, 'state_name': 'Uttarakhand', 'soil_type_name': 'Sandy'},
    {'name': 'Haridwar Village', 'latitude': 29.9457, 'longitude': 78.1642, 'state_name': 'Uttarakhand', 'soil_type_name': 'Loam'},
    # West Bengal
    {'name': 'Kolkata Village', 'latitude': 22.5726, 'longitude': 88.3639, 'state_name': 'West Bengal', 'soil_type_name': 'Clay'},
    {'name': 'Darjeeling Village', 'latitude': 27.0410, 'longitude': 88.2663, 'state_name': 'West Bengal', 'soil_type_name': 'Loam'},
    {'name': 'Howrah Village', 'latitude': 22.5958, 'longitude': 88.2636, 'state_name': 'West Bengal', 'soil_type_name': 'Sandy'},
]

# Add crops
for crop in crops_data:
    session.add(Crop(**crop))

# Add soil types
for soil in soil_data:
    session.add(SoilType(**soil))

# Add states
for state_name in states_data:
    session.add(State(name=state_name))

session.commit()

# Add locations with state and soil type relationships
for loc in locations_data:
    state = session.query(State).filter_by(name=loc['state_name']).first()
    soil = session.query(SoilType).filter_by(name=loc['soil_type_name']).first()
    location = Location(name=loc['name'], latitude=loc['latitude'], longitude=loc['longitude'], state=state, soil_type=soil)
    session.add(location)

session.commit()

# Sample weather data
locations = session.query(Location).all()
for loc in locations:
    for _ in range(10):  # 10 random weather entries per location
        weather = WeatherData(
            location=loc,
            temperature=random.uniform(15, 35),
            humidity=random.uniform(40, 80),
            rainfall=random.uniform(0, 100)
        )
        session.add(weather)

session.commit()

print("Sample data populated successfully!")