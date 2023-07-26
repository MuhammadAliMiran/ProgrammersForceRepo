from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/")
def home():
    return render_template('index.html')
@app.route("/predict", methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        data = int(request.form["data"])
        data = data*data
        return render_template("index.html", Squared_text=data)
if __name__ == "__main__":
    app.run(debug=True)