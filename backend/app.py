from gradio_client import Client
from flask import Flask, render_template, request
from PIL import Image
from markupsafe import Markup
import requests
import os
import tempfile

app = Flask(__name__)

# Gradio API URL
# GRADIO_URL = "https://57c1afd144e623e52c.gradio.live/predict"
GRADIO_URL = "https://aa5f2b18cb316a6d0b.gradio.live"
client = Client(GRADIO_URL)


@app.route("/predict", methods=["POST"])
def predict():
    print("Predicting...")

    try:
        file = request.files.get("file")
        if not file:
            return render_template("index.html", status=400, res="No file uploaded")

        print("Uploading image for prediction...")

        # Convert FileStorage to PIL Image
        image = Image.open(file.stream)

        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            image.save(temp_file, format="JPEG")
            temp_file_path = temp_file.name  # Get the saved file path

        image = Image.open(file.stream)  # Convert Flask FileStorage to PIL image

        response = client.predict(image, api_name="/predict") 

        print(f"Raw Response: {response}")
        return render_template("display.html", status=200, result=response)

    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template("index.html", status=500, res="Internal Server Error")

    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template("index.html", status=500, res="Internal Server Error")


# @app.route("/predict", methods=["POST"])
# def predict():
#     print("Predicting...")
#     try:
#         file = request.files.get("file")
#         if not file:
#             return render_template("index.html", status=400, res="No file uploaded")
#         print("Predicting. up img")
#         # Send image to Gradio API
#         # Prepare file for Gradio API
#         files = {"data": ("image.jpg", file, file.content_type)}
#         print("file ",files)
#         # Send request to Gradio API
#         response = requests.post(GRADIO_URL, files=files,data={"fn_index": 0})
#         response_json = response.json() if response.text else {}
#         print(f"Raw Response: {response.status_code}, {response_json}")
#         print("Res: ", response.json())
#         if response.status_code == 200:
#             prediction = response.json()["data"][0]
#             print(prediction, "...")

#             return render_template(
#                 "display.html", status=200, result=Markup(prediction)
#             )
#         else:
#             return render_template("index.html", status=500, res="Prediction failed")

#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return render_template("index.html", status=500, res="Internal Server Error")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)


# from flask import Flask, render_template, jsonify, request
# from markupsafe import Markup

# import sys
# import os

# # Add the parent directory to Python's module search path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from backend.model import predict_image  # Now it should work
# import backend.utils as utils


# app = Flask(__name__)


# @app.route("/", methods=["GET"])
# def home():
#     return render_template("index.html")


# @app.route("/predict", methods=["POST"])
# def predict():
#     print("Predicting...")
#     try:
#         file = request.files.get("file")
#         if not file:
#             return render_template("index.html", status=400, res="No file uploaded")

#         img = file.read()
#         prediction = predict_image(img)
#         print(prediction, "...")

#         if prediction in utils.disease_dic:
#             res = Markup(utils.disease_dic[prediction])
#             return render_template("display.html", status=200, result=res)
#         else:
#             return render_template("index.html", status=404, res="Prediction not found")
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return render_template("index.html", status=500, res="Internal Server Error")


# if __name__ == "__main__":
#     port = int(
#         os.environ.get("PORT", 10000)
#     )  # Get Render's assigned port or default to 5000
#     app.run(host="0.0.0.0", port=port, debug=True)


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
