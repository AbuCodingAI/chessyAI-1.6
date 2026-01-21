"""
Test script to verify all packages are installed correctly
Run this BEFORE starting the server
"""

print("🔍 Testing Python package installation...\n")

# Test Flask
try:
    import flask
    print(f"✅ Flask {flask.__version__} - OK")
except ImportError as e:
    print(f"❌ Flask - FAILED: {e}")
    print("   Install with: pip install flask")

# Test Flask-CORS
try:
    import flask_cors
    print(f"✅ Flask-CORS - OK")
except ImportError as e:
    print(f"❌ Flask-CORS - FAILED: {e}")
    print("   Install with: pip install flask-cors")

# Test TensorFlow
try:
    import tensorflow as tf
    print(f"✅ TensorFlow {tf.__version__} - OK")
except ImportError as e:
    print(f"❌ TensorFlow - FAILED: {e}")
    print("   Install with: pip install tensorflow")

# Test NumPy
try:
    import numpy as np
    print(f"✅ NumPy {np.__version__} - OK")
except ImportError as e:
    print(f"❌ NumPy - FAILED: {e}")
    print("   Install with: pip install numpy")

# Test python-chess
try:
    import chess
    print(f"✅ python-chess {chess.__version__} - OK")
    
    # Test chess.engine module (part of python-chess)
    try:
        import chess.engine
        print(f"✅ chess.engine module - OK")
    except ImportError:
        print(f"⚠️  chess.engine module - Not available (optional)")
        
except ImportError as e:
    print(f"❌ python-chess - FAILED: {e}")
    print("   Install with: pip install python-chess")

print("\n" + "="*50)

# Check if all required packages are installed
try:
    import flask, flask_cors, tensorflow, numpy, chess
    print("🎉 All required packages installed!")
    print("✅ You can now run: python chess_ai_server.py")
except ImportError:
    print("❌ Some packages are missing!")
    print("📦 Run: pip install flask flask-cors tensorflow numpy python-chess")

print("="*50)
