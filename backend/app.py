from flask import Flask, jsonify, send_from_directory
import os
from flask_cors import CORS

# directory from which the assets created by the frontend build process are located.
BUILD_DIR = os.path.join(os.path.dirname(__file__), "build")

# flask app init, servers all static files from the build directory to the frontend
app = Flask(__name__, static_folder=os.path.join(BUILD_DIR), static_url_path='/')
CORS(app) # This is the function to allow for different front and backend IP's when developing



@app.route("/api/key")
def get_key():
    return jsonify({"apiKey": os.getenv("NYT_API_KEY")})


@app.route("/")
@app.route("/<path:path>")
def serve_frontend(path=""):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        # if existing static file, serve it
        return send_from_directory(app.static_folder, path)
    else:
        # for root or any other path, serve the SPA entry point
        return send_from_directory(BUILD_DIR, 'index.html')


# actual python script execution starts here
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("Flask server starting...")
    print(f"Serving frontend from: {BUILD_DIR}")
    print(f"Static folder set to: {app.static_folder}")
    print(f"Listening on http://0.0.0.0:{port}")
    # run the flask server on the host="0.0.0.0" which lets the server be seen externally
    # port is the determiner for where on the network it is accessible
    app.run(host="0.0.0.0", port=port)