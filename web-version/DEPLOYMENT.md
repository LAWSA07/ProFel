# Deployment Guide

This document outlines the steps to deploy the Profel application to both development and production environments.

## Environment Setup

### Frontend (.env files)

The frontend uses environment variables to configure API endpoints and other settings:

1. Development (`.env`):
   - Uses localhost API endpoint
   - Development mode enabled

2. Production (`.env.production`):
   - Points to the production API endpoint
   - Disables source maps for smaller bundles

### Backend (Environment Variables)

The backend requires the following environment variables:
- `PORT`: The port on which the API server runs (default: 5000)
- `FLASK_DEBUG`: Set to "true" for development, "false" for production
- `GROQ_API_KEY`: Your Groq API key for AI services

## Deployment Options

### Render (Recommended)

1. **Using render.yaml**:
   - Push the code to a GitHub repository
   - Connect your Render account to GitHub
   - Create a new "Blueprint" in Render and select the repository
   - Render will automatically deploy both frontend and backend services
   - Set the `GROQ_API_KEY` in the Render dashboard

### Heroku Alternative

1. **Backend**:
   - A `Procfile` is included for Heroku deployment
   - Create a new Heroku app for the backend
   - Push the backend directory to Heroku
   - Set the necessary environment variables in Heroku

2. **Frontend**:
   - Create a new Heroku app for the frontend
   - Build the frontend locally (`npm run build`)
   - Deploy the `build` directory to Heroku
   - Set the `REACT_APP_API_URL` to point to your backend

## Manual Deployment

### Backend
```bash
cd web-version/backend
pip install -r requirements.txt
gunicorn app:app
```

### Frontend
```bash
cd web-version/frontend
npm install
npm run build
npx serve -s build
```

## Environment Variables Reference

### Frontend
- `PORT`: The port on which the frontend server runs (default: 3000)
- `REACT_APP_API_URL`: The URL of the backend API
- `REACT_APP_ENV`: The environment (development/production)
- `GENERATE_SOURCEMAP`: Whether to generate source maps

### Backend
- `PORT`: The port on which the API server runs (default: 5000)
- `FLASK_DEBUG`: Whether to run Flask in debug mode
- `GROQ_API_KEY`: Your Groq API key