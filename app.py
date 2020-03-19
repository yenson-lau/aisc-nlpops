from flask import Flask, request, jsonify, flash, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import mlflow.pyfunc
import pandas as pd
import json


class RequestForm(FlaskForm):
  rss_url = StringField('URL to RSS feed', validators=[DataRequired()])
  html_tgts = StringField('Target elements', validators=[DataRequired()])
  submit = SubmitField('Summarize')

# Name of the apps module package
app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

# Load in the model at app startup
# model = mlflow.pyfunc.load_model('./model')

# Load in our meta_data
f = open("./model/code/meta_data.txt", "r")
load_meta_data = json.loads(f.read())

# Meta data endpoint
@app.route('/', methods=['GET', 'POST'])
def meta_data():
  return jsonify(load_meta_data)

def get_rss_summary(rss_url, html_tgts):
  out = [rss_url, html_tgts]
  return '<br/>'.join(out)

@app.route('/rss', methods=['GET', 'POST'])
def req_rss_sum():
  form = RequestForm()

  if form.validate_on_submit():
    flash(f'Summary requested for URL {form.rss_url.data}...')
    return get_rss_summary(form.rss_url.data, form.html_tgts.data)

  return render_template('rss-summarize.html',
                         title='Summarize', form=form)

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
  req = request.get_json()

  # Log the request
  print({'request': req})

  # Format the request data in a DataFrame
  inf_df = pd.DataFrame(req['data'])

  # Get model prediction - convert from np to list
  pred = model.predict(inf_df).tolist()

  # Log the prediction
  print({'response': pred})

  # Return prediction as reponse
  return jsonify(pred)

app.run(host='0.0.0.0', port=5000, debug=True)
