from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import os
from dotenv import load_dotenv
from locations import locations

load_dotenv()

app = Flask(__name__)
CORS(app)

# Hardcoded data for MVP
crops = [
    {'id': 1, 'name': 'Wheat', 'category': 'Cereal', 'optimal_ph_min': 6.0, 'optimal_ph_max': 7.5, 'optimal_temperature_min': 15, 'optimal_temperature_max': 25, 'optimal_rainfall_min': 300, 'optimal_rainfall_max': 600, 'average_yield_per_hectare': 3000, 'market_price_per_kg': 21},
    {'id': 2, 'name': 'Rice', 'category': 'Cereal', 'optimal_ph_min': 5.5, 'optimal_ph_max': 6.5, 'optimal_temperature_min': 20, 'optimal_temperature_max': 30, 'optimal_rainfall_min': 1000, 'optimal_rainfall_max': 2000, 'average_yield_per_hectare': 4000, 'market_price_per_kg': 25},
    {'id': 3, 'name': 'Maize', 'category': 'Cereal', 'optimal_ph_min': 5.8, 'optimal_ph_max': 7.0, 'optimal_temperature_min': 18, 'optimal_temperature_max': 27, 'optimal_rainfall_min': 500, 'optimal_rainfall_max': 800, 'average_yield_per_hectare': 3500, 'market_price_per_kg': 17},
    {'id': 4, 'name': 'Tomato', 'category': 'Vegetable', 'optimal_ph_min': 6.0, 'optimal_ph_max': 6.8, 'optimal_temperature_min': 15, 'optimal_temperature_max': 25, 'optimal_rainfall_min': 500, 'optimal_rainfall_max': 700, 'average_yield_per_hectare': 20000, 'market_price_per_kg': 42},
    {'id': 5, 'name': 'Potato', 'category': 'Vegetable', 'optimal_ph_min': 5.0, 'optimal_ph_max': 6.5, 'optimal_temperature_min': 15, 'optimal_temperature_max': 20, 'optimal_rainfall_min': 500, 'optimal_rainfall_max': 700, 'average_yield_per_hectare': 25000, 'market_price_per_kg': 25},
]


@app.route('/recommend', methods=['POST'])
def recommend_crop():
    data = request.json
    location_name = data.get('location')
    soil_ph = data.get('ph')
    nitrogen = data.get('nitrogen')
    phosphorus = data.get('phosphorus')
    potassium = data.get('potassium')
    season = data.get('season', 1)  # default to 1

    # Get location
    location = next((loc for loc in locations if loc['name'] == location_name), None)
    if not location:
        return jsonify({'error': 'Location not found'}), 404

    # Get soil data
    if soil_ph is None:
        soil_ph = location['soil_ph']
        nitrogen = location['nitrogen']
        phosphorus = location['phosphorus']
        potassium = location['potassium']

    temperature = location['temperature']
    rainfall = location['rainfall']

    recommendations = []

    for crop in crops:
        # Calculate match scores for each factor
        ph_score = 1.0 if crop['optimal_ph_min'] <= soil_ph <= crop['optimal_ph_max'] else max(0, 1 - abs(soil_ph - (crop['optimal_ph_min'] + crop['optimal_ph_max'])/2) / 2)
        temp_score = 1.0 if crop['optimal_temperature_min'] <= temperature <= crop['optimal_temperature_max'] else max(0, 1 - abs(temperature - (crop['optimal_temperature_min'] + crop['optimal_temperature_max'])/2) / 10)
        rain_score = 1.0 if crop['optimal_rainfall_min'] <= rainfall <= crop['optimal_rainfall_max'] else max(0, 1 - abs(rainfall - (crop['optimal_rainfall_min'] + crop['optimal_rainfall_max'])/2) / 200)

        # Average score
        overall_score = (ph_score + temp_score + rain_score) / 3

        predicted_yield = crop['average_yield_per_hectare'] * overall_score

        # Calculate profit (simplified: yield * price - costs)
        # Assume cost per hectare is 20% of revenue
        revenue = predicted_yield * crop['market_price_per_kg']
        cost = revenue * 0.2
        profit = revenue - cost

        recommendations.append({
            'crop': crop['name'],
            'yield': round(predicted_yield, 2),
            'profit': round(profit, 2),
            'category': crop['category']
        })

    # Sort by profit descending
    recommendations.sort(key=lambda x: x['profit'], reverse=True)

    return jsonify({'recommendations': recommendations[:5]})  # Top 5

@app.route('/districts', methods=['GET'])
def get_districts():
    state = request.args.get('state')
    if state:
        districts = list(set(loc['district'] for loc in locations if loc['state'] == state))
        return jsonify(districts)
    return jsonify([])

@app.route('/villages', methods=['GET'])
def get_villages():
    state = request.args.get('state')
    district = request.args.get('district')
    if state and district:
        villages = [loc['village'] for loc in locations if loc['state'] == state and loc['district'] == district and loc['village']]
        return jsonify(villages)
    return jsonify([])

@app.route('/locations', methods=['GET'])
def get_locations():
    state = request.args.get('state')
    district = request.args.get('district')
    village = request.args.get('village')
    if village:
        loc = next((loc for loc in locations if loc['state'] == state and loc['district'] == district and loc['village'] == village), None)
        if loc:
            return jsonify([{'name': loc['name'], 'latitude': loc['latitude'], 'longitude': loc['longitude']}])
    elif district:
        filtered = [loc for loc in locations if loc['state'] == state and loc['district'] == district and not loc['village']]
        result = [{'name': loc['name'], 'latitude': loc['latitude'], 'longitude': loc['longitude']} for loc in filtered]
        return jsonify(result)
    elif state:
        districts = list(set(loc['district'] for loc in locations if loc['state'] == state))
        return jsonify(districts)
    else:
        states = list(set(loc['state'] for loc in locations))
        return jsonify(states)
    return jsonify([])

@app.route('/states', methods=['GET'])
def get_states():
    states = list(set(loc['state'] for loc in locations))
    return jsonify(states)

@app.route('/')
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'frontend'), 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)