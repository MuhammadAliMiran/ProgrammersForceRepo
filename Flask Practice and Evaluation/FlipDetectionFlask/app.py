from flask import Flask, render_template, request
import os
import torch
import torchvision.transforms as transforms
import pickle
from model import FlipDetectionModel  # Import the model class from the module
import torch.nn as nn

app = Flask(__name__)
# Define the model class directly in app.py
class FlipDetectionModel(torch.nn.Module):
    def __init__(self):
        super(FlipDetectionModel, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc_layers = nn.Sequential(
            nn.Linear(32 * 32 * 32, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.fc_layers(x)
        return x
# Load the pickled model
with open('flipDetection.pkl', 'rb') as f:
    model = pickle.load(f)

def preprocess_image(image_path, target_shape=(128, 128, 3)):
    img = Image.open(image_path)
    img = img.resize(target_shape[:2])  # Resize the image to target_shape
    img = transforms.ToTensor()(img)  # Convert to a PyTorch tensor
    return img

@app.route('/')
def home():
    return render_template('upload_image.html')

@app.route('/predict_flipped', methods=['POST'])
def predict_flipped():
    if request.method == 'POST':
        # Check if the POST request has a file part
        if 'image_file' not in request.files:
            return "No image part in the request."
        
        file = request.files['image_file']

        # If the user does not select a file, the browser sends an empty file without a filename.
        if file.filename == '':
            return "No selected file."

        # If the file is selected, save it to a temporary folder (optional)
        image_temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_temp_path)

        # Preprocess the uploaded image
        img = preprocess_image(image_temp_path)

        # Convert the image tensor to a batch of size 1
        img_batch = img.unsqueeze(0)

        # Make a prediction using the loaded model
        model.eval()
        with torch.no_grad():
            output = model(img_batch)

        # Determine whether the image is flipped or not based on the prediction
        prediction = torch.round(output).item()
        if prediction == 0:
            result = "The uploaded image is NOT flipped."
        else:
            result = "The uploaded image is FLIPPED."

        # Remove the temporary image file
        os.remove(image_temp_path)

        return result

if __name__ == '__main__':
    app.run(debug=True)
