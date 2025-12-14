"""Vercel serverless function entry point."""
import sys
import os
from pathlib import Path

# Add BACKEND directory to Python path so we can import our modules
backend_dir = Path(__file__).resolve().parent.parent / "BACKEND"
sys.path.insert(0, str(backend_dir))

# Disable file logging in serverless environment
os.environ["VERCEL"] = "1"

try:
    from app import app
except Exception as e:
    # If import fails, create a simple Flask app to show the error
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/<path:path>', defaults={'path': ''})
    @app.route('/')
    def catch_all(path=''):
        return jsonify({
            "error": "Import failed",
            "message": str(e),
            "type": type(e).__name__
        }), 500

# Vercel will use this 'app' object
# The 'app' variable is automatically detected by Vercel's Python runtime

