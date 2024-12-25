from flask import Flask
from routes import all_routes

app = Flask(__name__)

# Register all routes
all_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
