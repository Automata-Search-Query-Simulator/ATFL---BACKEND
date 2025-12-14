"""Simulate endpoint - step by step debugging."""
from flask import Flask, jsonify, request
import sys
import os
from pathlib import Path
import traceback

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
@app.route('/api/simulate', methods=["GET", "POST"])
def simulate():
    try:
        # Step 1: Add BACKEND to path
        backend_dir = Path(__file__).resolve().parent.parent / "BACKEND"
        sys.path.insert(0, str(backend_dir))
        os.environ["VERCEL"] = "1"
        
        # Step 2: Try importing modules one by one
        import_results = {}
        
        try:
            from config import AUTOMATA_SIM_PATH, BackendConfigError, ensure_binary_available
            import_results["config"] = "✅ Success"
        except Exception as e:
            import_results["config"] = f"❌ {str(e)}"
            
        try:
            from logger import get_logger
            import_results["logger"] = "✅ Success"
        except Exception as e:
            import_results["logger"] = f"❌ {str(e)}"
            
        try:
            from parser import parse_stdout
            import_results["parser"] = "✅ Success"
        except Exception as e:
            import_results["parser"] = f"❌ {str(e)}"
            
        try:
            from utils import build_command, write_sequences_to_tempfile
            import_results["utils"] = "✅ Success"
        except Exception as e:
            import_results["utils"] = f"❌ {str(e)}"
        
        return jsonify({
            "status": "debugging",
            "backend_dir": str(backend_dir),
            "sys_path": sys.path[:3],
            "imports": import_results,
            "request_args": dict(request.args)
        })
        
    except Exception as e:
        return jsonify({
            "error": "Exception in simulate",
            "message": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }), 500
