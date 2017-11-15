import os
from flask import Flask
app = Flask(__name__)

database=dict(
    DATABASE=os.path.join(app.root_path, 'app.db'),
    SECRET_KEY='XXXXX',
    USERNAME='XXXXX',
    PASSWORD='XXXXX'
)
