from website import create_app, socketio

if __name__ == "__main__":
    app = create_app()
    socketio.init_app(app)
    socketio.run(app, debug=True, host="0.0.0.0")