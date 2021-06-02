from flask import Flask
import logging
from routes import app_routes

app = Flask(__name__)  # app creation
logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')
app_routes.create_routes(app)

if __name__ == '__main__':
    app.run()
