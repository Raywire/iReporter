"""Run docstring"""

from app import create_app

CONFIG_NAME = 'development'

APP = create_app(CONFIG_NAME)

if __name__ == "__main__":
    APP.run(debug=True)
    