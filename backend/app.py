from flask import Flask, jsonify, send_from_directory
import os
from flask_cors import CORS
import requests
import requests

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app) # This is the function to allow for different front and backend IP's when developing

NYT_SAC_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=sacramento&begin_date=20250404&end_date=20250428&timestags.location.includes=california&api-key="
NYT_DAVIS_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=%22Davis,%20California%22&begin_date=20210301&api-key="


@app.get('/api/searchArticles')
def get_Key_and_Articles():
    # help from CourseAssist (see aiUsage.txt) and 
    # https://www.w3schools.com/python/module_requests.asp
    apiKey =  os.getenv('NYT_API_KEY')
    full_url = NYT_SAC_URL + apiKey
    response = requests.get(full_url)
    if response.status_code != 200:
        return jsonify({"message": "Error!"})
    else:
        return jsonify(response.json())

@app.route("/api/getKey")
def getKey():
    # Note: This function is only for testing! Do not test unless you want to reveal your key
    # unless you want the searchArticles route to not work!
    return jsonify({"message": os.getenv('NYT_API_KEY')})

@app.route("/")
@app.route("/<path:path>")
def serve_frontend(path=""):
    if path != "" and os.path.exists(f"static/{path}"):
        return send_from_directory("static", path)
    return send_from_directory("templates", "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))