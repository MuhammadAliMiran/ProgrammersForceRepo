import os
import hashlib
from flask import Flask, request,render_template

UPLOAD_FOLDER = (r"C:\Users\DELL\Documents\Evaluation Task 2\static\UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/predict", methods=['GET','POST'])
def predict():
    file = request.files['image_file']

    # If the user does not select a file, the browser sends an empty file without a filename.
    if file.filename == '':
        return "No selected file."

    # If the file is selected, save it to a temporary folder (optional)
    image_temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(image_temp_path)
    im_path = image_temp_path
    with open(im_path, "rb") as f:
        im_bytes = f.read()
    im_hash = str(hashlib.md5(im_bytes).hexdigest())
    return render_template("index.html", hash_text=im_hash)

if __name__ == "__main__":
    app.run(debug=True)