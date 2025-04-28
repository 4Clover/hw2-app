from flask import Flask, jsonify, send_from_directory
import os
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app) # This is the function to allow for different front and backend IP's when developing


@app.route("/api/key")
def get_key():
    # return jsonify({"apiKey": os.getenv("NYT_API_KEY")})
    # https://www.w3schools.com/python/python_strings_format.asp
    api_key = os.getenv("NYT_API_KEY")
    return jsonify({"searchURL": f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key={api_key}"})


@app.route("/")
@app.route("/<path:path>")
def serve_frontend(path=""):
    if path != "" and os.path.exists(f"static/{path}"):
        return send_from_directory("static", path)
    return send_from_directory("templates", "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))