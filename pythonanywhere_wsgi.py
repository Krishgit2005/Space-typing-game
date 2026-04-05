# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.

import sys
import os

# 1. Update this path to where your Flask app is located on PythonAnywhere
# By default, PythonAnywhere creates a directory called 'mysite'
path = '/home/yourusername/mysite'
if path not in sys.path:
    sys.path.append(path)

# 2. Set the environment variables if needed
# os.environ['FLASK_ENV'] = 'production'

# 3. Import your Flask app
# Since our main script is named 'ship.py', we import 'app' from 'ship'
from ship import app as application
