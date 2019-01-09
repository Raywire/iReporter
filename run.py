"""Module that creates app and runs the app"""

from app import create_app

APP = create_app()

if __name__ == "__main__":
    APP.run(debug=True)
