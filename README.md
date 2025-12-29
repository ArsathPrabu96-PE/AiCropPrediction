# AI-Based Crop Recommendation System

This is a web application that helps farmers choose the best crop to grow based on soil type, season, weather conditions, and local market price.

## Features

- Input soil information and location
- Get crop recommendations with expected yield and profit
- Web-based interface
- REST API backend

## Installation

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the backend: `python backend/app.py`
6. Open `frontend/index.html` in a web browser

## API Endpoints

- `GET /locations`: Get list of available locations
- `POST /recommend`: Get crop recommendations
  - Body: `{"location": "Delhi", "ph": 6.5, "season": 1}`

## Technologies Used

- Backend: Flask, Python
- Frontend: HTML, JavaScript
- AI: Rule-based recommendation system

## Future Improvements

- Add machine learning models
- Integrate real weather APIs
- Expand to more locations and crops
- Add user authentication