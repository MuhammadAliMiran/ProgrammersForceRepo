from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/")
def home():
    return render_template('index.html')
@app.route("/predict", methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        data = int(request.form["data"])
        table = []
        for i in range(1,11):
            table.append(str(data) + " x "+ str(i) + " = " + str(data*i) )
        return render_template("index.html", table_text=table)
if __name__ == "__main__":
    app.run(debug=True)