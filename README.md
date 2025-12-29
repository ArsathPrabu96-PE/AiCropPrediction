# AI-Based Crop Recommendation System

This is a web application that helps farmers choose the best crop to grow based on soil type, season, weather conditions, and local market price.

## Features

- Input soil information and location
- Get crop recommendations with expected yield and profit
- Web-based interface
- REST API backend

## Installation (Local Development)

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `python app.py`
6. Open http://localhost:5000 in a web browser

## Deployment on Render

1. Sign up for a free account at https://render.com
2. Connect your GitHub repository
3. Create a new Web Service
4. Select Python as the runtime
5. Set the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
6. Add environment variable: `PORT` (Render sets this automatically)
7. Deploy

## Deployment on PythonAnywhere

1. Sign up for a free account at https://pythonanywhere.com
2. Go to the "Files" tab and upload your project files, or clone from GitHub
3. Go to "Web" tab and create a new web app
4. Select "Flask" and Python 3.10 (or latest available)
5. Set the source code path to `/home/yourusername/yourproject`
6. Set the application file to `app.py`
7. In the "Virtualenv" section, create a virtual environment and install requirements: `pip install -r requirements.txt`
8. Reload the web app
9. Your app will be available at `yourusername.pythonanywhere.com`

Note: For production, build the frontend first:
- `cd frontend && npm install && npm run build`
- Update app.py to change 'frontend' to 'frontend/build' in send_from_directory calls
- Commit and push the changes

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