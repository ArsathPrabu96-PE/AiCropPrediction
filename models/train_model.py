import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
from models import Crop, SoilType, Location, WeatherData, engine
from sqlalchemy.orm import sessionmaker
import random

Session = sessionmaker(bind=engine)
session = Session()

# Generate synthetic training data
def generate_training_data():
    crops = session.query(Crop).all()
    soil_types = session.query(SoilType).all()
    locations = session.query(Location).all()

    data = []
    for _ in range(1000):  # Generate 1000 samples
        crop = random.choice(crops)
        soil = random.choice(soil_types)
        location = random.choice(locations)
        weather = session.query(WeatherData).filter_by(location_id=location.id).first()
        if not weather:
            continue

        # Features
        features = {
            'ph': soil.ph_level + np.random.normal(0, 0.5),
            'nitrogen': soil.nitrogen_content + np.random.normal(0, 0.02),
            'phosphorus': soil.phosphorus_content + np.random.normal(0, 0.01),
            'potassium': soil.potassium_content + np.random.normal(0, 0.02),
            'temperature': weather.temperature + np.random.normal(0, 2),
            'rainfall': weather.rainfall + np.random.normal(0, 20),
            'season': random.randint(1, 4),  # 1: winter, 2: spring, 3: summer, 4: autumn
            'crop_id': crop.id
        }

        # Calculate yield based on how well conditions match optimal
        ph_match = 1 if crop.optimal_ph_min <= features['ph'] <= crop.optimal_ph_max else 0.5
        temp_match = 1 if crop.optimal_temperature_min <= features['temperature'] <= crop.optimal_temperature_max else 0.5
        rain_match = 1 if crop.optimal_rainfall_min <= features['rainfall'] <= crop.optimal_rainfall_max else 0.5

        base_yield = crop.average_yield_per_hectare
        yield_factor = (ph_match + temp_match + rain_match) / 3
        predicted_yield = base_yield * yield_factor * np.random.uniform(0.8, 1.2)

        features['yield'] = predicted_yield
        data.append(features)

    return pd.DataFrame(data)

# Train model for each crop
def train_models():
    df = generate_training_data()
    crops = session.query(Crop).all()
    models = {}

    for crop in crops:
        crop_data = df[df['crop_id'] == crop.id]
        if len(crop_data) < 10:
            continue

        X = crop_data[['ph', 'nitrogen', 'phosphorus', 'potassium', 'temperature', 'rainfall', 'season']]
        y = crop_data['yield']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Model for {crop.name}: MSE = {mse}")

        models[crop.id] = model
        joblib.dump(model, f'models/crop_{crop.id}_model.pkl')

    return models

if __name__ == "__main__":
    import random
    models = train_models()
    print("Models trained and saved!")