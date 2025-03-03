from flask import Flask, render_template, jsonify, request
from markupsafe import Markup

import sys
import os

# Add the parent directory to Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.model import predict_image  # Now it should work
import backend.utils as utils


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        file = request.files.get("file")
        if not file:
            return render_template("index.html", status=400, res="No file uploaded")

        img = file.read()
        prediction = predict_image(img)
        print(prediction, "...")

        if prediction in utils.disease_dic:
            res = Markup(utils.disease_dic[prediction])
            return render_template("display.html", status=200, result=res)
        else:
            return render_template("index.html", status=404, res="Prediction not found")
    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template("index.html", status=500, res="Internal Server Error")


if __name__ == "__main__":
    port = int(
        os.environ.get("PORT", 5000)
    )  # Get Render's assigned port or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)


# from flask import Flask, render_template, jsonify, request
# from markupsafe import Markup

# from backend.model import predict_image
# import backend.utils as utils

# app = Flask(__name__)


# @app.route("/", methods=["GET"])
# def home():
#     return render_template("index.html")


# @app.route("/predict", methods=["GET", "POST"])
# def predict():
#     if request.method == "POST":
#         try:
#             file = request.files["file"]
#             img = file.read()
#             prediction = predict_image(img)
#             print(prediction, "...")
#             res = Markup(utils.disease_dic[prediction])
#             return render_template("display.html", status=200, result=res)
#         except:
#             print("erro happen somthing ")
#     return render_template("index.html", status=500, res="Internal Server Error")


# if __name__ == "__main__":
#     app.run(debug=True)
