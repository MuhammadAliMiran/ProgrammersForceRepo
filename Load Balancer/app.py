from flask import Flask, render_template, request
import traceback

app = Flask(__name__)

class ML:
    def __init__(self):
        self.available_models = {
            "face_detection": "Face Detection Model",
            "car_detection": "Car Detection Model",
            "shoe_detection": "Shoe Detection Model",
            "cloth_detection": "Cloth Detection Model",
            "signal_detection": "Signal Detection Model",
            "water_level_detection": "Water Level Detection Model",
            "missile_detection": "Missile Detection Model"
        }
        self.loaded_models_limit = 2
        self.loaded_models = {
            model: self.load_weights(model)
            for model in list(self.available_models)[:self.loaded_models_limit]
        }

        # The request_counts dictionary keeps track of the number of requests processed by each model.
        self.request_counts = {model: 0 for model in self.loaded_models}

    def load_weights(self, model):
        return self.available_models.get(model, None)

    def load_balancer(self, new_model):
        if new_model:
            if new_model not in self.loaded_models:
                # If new_model is not already loaded, add it to the loaded models
                if len(self.loaded_models) >= self.loaded_models_limit:
                    # If we have reached the limit of loaded models, replace the least used model
                    least_used_model = min(self.request_counts, key=self.request_counts.get)
                    self.loaded_models.pop(least_used_model)
                    self.request_counts.pop(least_used_model)

                self.loaded_models[new_model] = self.load_weights(new_model)
                self.request_counts[new_model] = 0

            # Update the request count of the new model
            self.request_counts[new_model] += 1

        # Update the loaded models count
        loaded_models_count = len(self.loaded_models)

        # Return the loaded models and their request counts
        return list(self.loaded_models), self.request_counts, loaded_models_count
    
ml = ML()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_loaded_models', methods=['GET'])
def get_loaded_models():
    loaded_models, request_counts, loaded_models_count = ml.load_balancer(None)

    return render_template('loaded_models.html', models=loaded_models, counts=request_counts, count=loaded_models_count)


@app.route('/process_request', methods=['POST'])
def process_request():
    try:
        model = request.form["model"]
        ml.load_balancer(model)
        return "Processed by " + model
    except:
        return str(traceback.format_exc())

if __name__ == "__main__":
    app.run(debug=True)
