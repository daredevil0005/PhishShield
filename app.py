from flask import Flask, render_template, request, jsonify
from src.predictor import predict_url
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        url = request.form['url']
        result = predict_url(url)
    return render_template("index.html", result=result)

# 🔥 API for extension
@app.route('/api/check', methods=['POST'])
def check_url():
    data = request.get_json()
    url = data.get('url')

    result = predict_url(url)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)