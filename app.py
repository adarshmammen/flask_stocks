from __future__ import print_function
from flask import Flask, render_template, request, redirect
import requests
import datetime
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

dates = []
now = datetime.datetime.now()
last_month =  int(str(now).split('-')[1])-1

close_prices_list = []

stock = 'GOOG'
api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json' % stock
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

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
 #create the graph
  x = list(range(0,  10+ 1))
  fig = figure(title="Polynomial")
  fig.line(x, [i ** 2 for i in x], color='Black', line_width=2)
  
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
  app.run(port=33507)
