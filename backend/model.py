import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import io
import os


class Plant_Disease_Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = models.resnet34(weights=models.ResNet34_Weights.IMAGENET1K_V1)
        num_ftrs = self.network.fc.in_features
        self.network.fc = nn.Linear(num_ftrs, 38)

    def forward(self, xb):
        return self.network(xb)


# Image transformation pipeline
transform = transforms.Compose(
    [
        transforms.Resize((128, 128)),  # Ensure correct tuple format
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        ),  # Normalization for ResNet
    ]
)

# Define class labels
num_classes = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

# Load model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
device = "cuda" if torch.cuda.is_available() else "cpu"
model = Plant_Disease_Model().to(device)
model_path = os.path.join(BASE_DIR, "Models", "plantDisease-resnet34.pth")
model.load_state_dict(torch.load(model_path, map_location=device))
# model = torch.compile(model)  # 🔥 Speeds up inference
model.eval()
torch.cuda.empty_cache()


def predict_image(img):
    """Predicts the disease of a plant leaf image."""
    img_pil = Image.open(io.BytesIO(img)).convert(
        "RGB"
    )  # Convert to RGB to handle grayscale images
    # tensor = transform(img_pil).unsqueeze(0)  # Add batch dimension
    tensor = transform(img_pil).unsqueeze(0).to(device)  # Move to GPU

    with torch.no_grad():  # Disable gradients for inference
        yb = model(tensor)
        _, preds = torch.max(yb, dim=1)

    return num_classes[preds[0].item()]


# import torch
# import torch.nn as nn
# import torchvision.models as models
# import torchvision.transforms as transforms
# from PIL import Image
# import io


# class Plant_Disease_Model(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.network = models.resnet34(pretrained=True)
#         num_ftrs = self.network.fc.in_features
#         self.network.fc = nn.Linear(num_ftrs, 38)

#     def forward(self, xb):
#         out = self.network(xb)
#         return out


# transform = transforms.Compose([transforms.Resize(size=128), transforms.ToTensor()])

# num_classes = [
#     "Apple___Apple_scab",
#     "Apple___Black_rot",
#     "Apple___Cedar_apple_rust",
#     "Apple___healthy",
#     "Blueberry___healthy",
#     "Cherry_(including_sour)___Powdery_mildew",
#     "Cherry_(including_sour)___healthy",
#     "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
#     "Corn_(maize)___Common_rust_",
#     "Corn_(maize)___Northern_Leaf_Blight",
#     "Corn_(maize)___healthy",
#     "Grape___Black_rot",
#     "Grape___Esca_(Black_Measles)",
#     "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
#     "Grape___healthy",
#     "Orange___Haunglongbing_(Citrus_greening)",
#     "Peach___Bacterial_spot",
#     "Peach___healthy",
#     "Pepper,_bell___Bacterial_spot",
#     "Pepper,_bell___healthy",
#     "Potato___Early_blight",
#     "Potato___Late_blight",
#     "Potato___healthy",
#     "Raspberry___healthy",
#     "Soybean___healthy",
#     "Squash___Powdery_mildew",
#     "Strawberry___Leaf_scorch",
#     "Strawberry___healthy",
#     "Tomato___Bacterial_spot",
#     "Tomato___Early_blight",
#     "Tomato___Late_blight",
#     "Tomato___Leaf_Mold",
#     "Tomato___Septoria_leaf_spot",
#     "Tomato___Spider_mites Two-spotted_spider_mite",
#     "Tomato___Target_Spot",
#     "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
#     "Tomato___Tomato_mosaic_virus",
#     "Tomato___healthy",
# ]


# import os
# model = Plant_Disease_Model()
# # model.load_state_dict(
# #     torch.load("./Models/plantDisease-resnet34.pth", map_location=torch.device("cpu"))
# # )
# model_path = os.path.join(os.path.dirname(__file__), "backend/Models/plantDisease-resnet34.pth")
# model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
# model.eval()


# def predict_image(img):
#     img_pil = Image.open(io.BytesIO(img))
#     tensor = transform(img_pil)
#     xb = tensor.unsqueeze(0)
#     yb = model(xb)
#     print("Image model ...")
#     _, preds = torch.max(yb, dim=1)
#     return num_classes[preds[0].item()]
