from flask import Flask, render_template, request, redirect
import requests
import datetime

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
	if int(str(ele[0]).split('-')[1])< last_month:
		break

close_prices_list = close_prices_list[::-1]
print close_prices_list

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return str(close_prices_list)
  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=33507)
