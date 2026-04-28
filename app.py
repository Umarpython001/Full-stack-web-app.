from website import create_app, socketio
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    app = create_app()
    socketio.init_app(app)

    is_debug = os.getenv("FLASK_DEBUG", "0") == "1"

    socketio.run(app, debug=is_debug, host="0.0.0.0")