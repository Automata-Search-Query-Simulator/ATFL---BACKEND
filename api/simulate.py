"""Simulate endpoint - connects to BACKEND automata simulator."""
import sys
from pathlib import Path
from flask import Flask, jsonify, request

app = Flask(__name__)

# Add BACKEND to path
backend_dir = Path(__file__).resolve().parent.parent / "BACKEND"
sys.path.insert(0, str(backend_dir))

try:
    # Import the actual Flask app from BACKEND
    from app import simulate as backend_simulate
    
    @app.route('/', methods=["GET"])
    @app.route('/api/simulate', methods=["GET"])
    def simulate():
        # Call the actual simulate function from BACKEND
        return backend_simulate()
        
except Exception as e:
    import traceback
    
    @app.route('/', methods=["GET"])
    @app.route('/api/simulate', methods=["GET"])
    def simulate():
        return jsonify({
            "error": "Failed to import BACKEND",
            "message": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }), 500
