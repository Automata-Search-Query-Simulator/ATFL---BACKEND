"""Vercel serverless function entry point."""
import sys
from pathlib import Path

# Add BACKEND directory to Python path so we can import our modules
backend_dir = Path(__file__).resolve().parent.parent / "BACKEND"
sys.path.insert(0, str(backend_dir))

from app import app

# Vercel will use this 'app' object
# The 'app' variable is automatically detected by Vercel's Python runtime

