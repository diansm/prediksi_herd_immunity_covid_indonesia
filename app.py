from flask import Flask, request, render_template
import pickle
from datetime import datetime
import cgi

def exp_func(x, a, b, c):
    return (a+b*c**x)

app = Flask(__name__)

model_file = open('dts_model.pkl', 'rb')
model = pickle.load(model_file, encoding='bytes')

@app.route('/')
def index():
    return render_template('index.html', prediksi=0)

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Predict based on user inputs and render the result to the html page
    '''

    form = cgi.FieldStorage()
    date =  request.form['Tanggal']
    
    initial_date = datetime.strptime('2021-01-13', '%Y-%m-%d').date()
    input_date = datetime.strptime(date, '%Y-%m-%d').date()
    delta_date = (input_date - initial_date).days
    data = delta_date/225

    prediction = model.eval_components(x=data) 
    output = int(33357347*prediction.get('exp_func'))
    
    percent = round((output/208265720)*80, 3)

    return render_template('index.html', prediksi=output, tanggal=input_date, persen=percent)


if __name__ == '__main__':
    app.run(debug=True)