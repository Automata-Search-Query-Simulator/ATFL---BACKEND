"""Vercel serverless function entry point."""
import sys
import os
from pathlib import Path
import traceback

# Add BACKEND directory to Python path so we can import our modules
backend_dir = Path(__file__).resolve().parent.parent / "BACKEND"
sys.path.insert(0, str(backend_dir))

# Disable file logging in serverless environment
os.environ["VERCEL"] = "1"

try:
    from app import app
    
    # Add a debug route to verify everything is working
    @app.route("/debug")
    def debug():
        return {
            "status": "ok",
            "backend_dir": str(backend_dir),
            "sys_path": sys.path[:3],
            "environ_vercel": os.environ.get("VERCEL"),
            "python_version": sys.version
        }
        
except Exception as e:
    # If import fails, create a simple Flask app to show the error
    import traceback
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path=''):
        return jsonify({
            "error": "Import failed in api/index.py",
            "message": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc(),
            "backend_dir": str(backend_dir),
            "sys_path": sys.path[:3]
        }), 500

# Vercel will use this 'app' object
# The 'app' variable is automatically detected by Vercel's Python runtime

