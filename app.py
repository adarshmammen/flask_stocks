from __future__ import print_function
from flask import Flask, render_template, request, redirect
import requests
import datetime
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
'''
dates = []
now = datetime.datetime.now()
last_month =  int(str(now).split('-')[1])-1

close_prices_list = []

stock = 'GOOG'
api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json?api_key=XPJ-bHXLTF3CvTThXtzL' % stock
session = requests.Session()
session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
raw_data = session.get(api_url)

for i,ele in enumerate(raw_data.json()["dataset"]['data']):
	if int(str(ele[0]).split('-')[1]) == last_month:
		close_prices_list.append(ele[4]) # field for closing price
		dates.append(str(ele[0]))
	if int(str(ele[0]).split('-')[1])< last_month:
		break
dates = dates[::-1]
close_prices_list = close_prices_list[::-1]
pd_dates = pd.to_datetime(dates)

df = pd.DataFrame(close_prices_list, index = pd_dates)
'''
app = Flask(__name__)
app.vars = {}

@app.route('/')
def landing():
  if request.method == 'GET':
    return render_template('landing.html')
@app.route('/index',methods=['POST'])
def index():
  app.vars['name'] = request.form['name_lulu']
  dates = []
  now = datetime.datetime.now()
  last_month =  int(str(now).split('-')[1])-1

  close_prices_list = []
  stock = app.vars['name']
  api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json?api_key=XPJ-bHXLTF3CvTThXtzL' % stock
  session = requests.Session()
  session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
  raw_data = session.get(api_url)

  for i,ele in enumerate(raw_data.json()["dataset"]['data']):
    if int(str(ele[0]).split('-')[1]) == last_month:
                close_prices_list.append(ele[4]) # field for closing price
                dates.append(str(ele[0]))
    if int(str(ele[0]).split('-')[1])< last_month:
                break
  dates = dates[::-1]
  close_prices_list = close_prices_list[::-1]
  pd_dates = pd.to_datetime(dates)

  df = pd.DataFrame(close_prices_list, index = pd_dates) 

#create the graph
  x = list(range(0,  10+ 1))
  fig = figure(title="Stock value last month",x_axis_label='date',y_axis_label='Price in $')
  fig.line(range(len(close_prices_list)),close_prices_list, color='Black', line_width=2)
  
  #config resources for BokehJS
  js_resources = INLINE.render_js()
  css_resources = INLINE.render_css()
  
  #embedd html components
  script, div = components(fig,INLINE)
  html= render_template('embed.html', plot_script=script, plot_div=div,js_resources=js_resources,css_resources=css_resources)
  return encode_utf8(html)
  return str(df)
  return render_template('index.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=33507)
