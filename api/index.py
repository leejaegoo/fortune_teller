import os
import sys

# Vercel Serverless Function Entry Point
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from fortune_app import app

# Vercel needs 'app' to be exposed
