from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import asyncio

from utils.api_wrapper import APIWrapper
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS with more specific settings
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3001", "http://localhost:3000", "http://localhost:3007", "http://localhost:3008"],
                               "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                               "allow_headers": ["Content-Type", "Authorization"]}},
     supports_credentials=True)

# Initialize API wrapper
api_wrapper = APIWrapper()

# Handle OPTIONS requests explicitly for preflight
@app.route('/api/match/calculate', methods=['OPTIONS'])
def handle_options_match_calculate():
    response = jsonify({'status': 'ok'})
    response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# General OPTIONS handler for all /api routes
@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    response = jsonify({'status': 'ok'})
    response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Helper to run async functions from Flask routes
def run_async(func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(func)
    loop.close()
    return result

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "API is running"})

@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    """Get supported platforms"""
    result = api_wrapper.get_supported_platforms()
    return jsonify(result)

@app.route('/api/profile/<platform>/<username>', methods=['GET'])
def get_profile(platform, username):
    """Get profile data for a specific platform and username"""
    session_id = request.args.get('session_id', '')

    # Run the async function in a synchronous context
    result = run_async(api_wrapper.fetch_profile(platform, username, session_id))
    return jsonify(result)

@app.route('/api/profile/validate', methods=['POST'])
def validate_profile():
    """Validate if a profile exists"""
    data = request.json
    platform = data.get('platform', '')
    username = data.get('username', '')

    if not platform or not username:
        return jsonify({
            "status": "error",
            "message": "Platform and username are required"
        })

    result = run_async(api_wrapper.validate_profile(platform, username))
    return jsonify(result)

@app.route('/api/profile/multi', methods=['POST'])
def get_multi_platform_profile():
    """Get profile data from multiple platforms"""
    data = request.json
    platform_usernames = data.get('platforms', {})
    session_id = data.get('session_id', '')

    if not platform_usernames:
        return jsonify({
            "status": "error",
            "message": "Platform usernames are required"
        })

    result = run_async(api_wrapper.fetch_multi_platform_profile(platform_usernames, session_id))
    return jsonify(result)

@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new job listing"""
    job_data = request.json

    if not job_data.get('title') or not job_data.get('company') or not job_data.get('description'):
        return jsonify({
            "status": "error",
            "message": "Title, company, and description are required"
        })

    result = api_wrapper.create_job(job_data)
    return jsonify(result)

@app.route('/api/match', methods=['POST'])
def match_profile_to_jobs():
    """Match a profile against jobs"""
    data = request.json
    platform = data.get('platform', '')
    username = data.get('username', '')
    job_ids = data.get('job_ids', None)

    if not platform or not username:
        return jsonify({
            "status": "error",
            "message": "Platform and username are required"
        })

    result = api_wrapper.match_profile_to_jobs(platform, username, job_ids)
    return jsonify(result)

@app.route('/api/match/calculate', methods=['POST'])
def calculate_match():
    """Calculate match score between profile and job"""
    try:
        data = request.json
        profile = data.get('profile')
        job = data.get('job')

        if not profile:
            return jsonify({"error": "Missing profile data"}), 400
        if not job:
            return jsonify({"error": "Missing job data"}), 400

        result = api_wrapper.calculate_match_score(profile, job)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error in match calculation: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/match/calculate-combined', methods=['POST'])
def calculate_combined_match():
    """Calculate match score using multiple profiles combined"""
    try:
        data = request.json
        profiles = data.get('profiles', [])
        job = data.get('job')

        if not profiles or len(profiles) == 0:
            return jsonify({"error": "Missing profiles data"}), 400
        if not job:
            return jsonify({"error": "Missing job data"}), 400

        result = api_wrapper.calculate_combined_match(profiles, job)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error in combined match calculation: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/profile/combine', methods=['POST'])
def combine_profiles():
    """Combine multiple profiles from different platforms"""
    try:
        data = request.json
        profiles = data.get('profiles', [])

        if not profiles or len(profiles) == 0:
            return jsonify({"error": "Missing profiles data"}), 400

        result = api_wrapper.combine_profiles(profiles)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error combining profiles: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    logger.info(f"Starting API server on port {port}, debug={debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)