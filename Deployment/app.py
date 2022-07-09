from flask import Flask, request, jsonify
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from PIL import Image

app = Flask(__name__)

# initiate model & columns
LABEL = ['FIRE',"NO FIRE"]
datacol = ['images', 'label']

model_best = keras.models.load_model('model_best.hdf5')

@app.route("/")
def welcome():
    return "<h3>FIRE DETECTION</h3>"

@app.route("/predict", methods=['GET','POST'])
def predict_churn():
    if request.method == 'POST':
        content = request.json
        try:
            new_data = {'images': content['images']},
            res = model_best.predict(new_data) #gunakan model yang terbaik misal yg variable my_model untuk predict images
            print(res) 
            if res[0][0] == 1:
                print('NO FIRE')
            else:
                print('FIRE')

            return response, 200
        except Exception as e:
            response = jsonify(success=False,
                               message=str(e))
            return response, 400
            
    # return dari method get
    return "<p>Silahkan gunakan method POST untuk mode <em>inference model</em></p>"
    
app.run(debug=True)