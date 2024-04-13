from flask import Blueprint, render_template, jsonify
from .performance3 import compare_strategies, get_pred_lists

# blueprint is a way of letting multiple files contain our view instructions
views = Blueprint('views', __name__)

# these are the instructions to present an HTML page based on the '/' route
@views.route('/')
def home():
    return render_template('home.html')

@views.route('/chart-data')
def chart_data():
    # get the data from performance2
    data = compare_strategies()
    
    # make it readable for chart.js
    chart_data = {
        'labels': data.index.tolist(),
        'data': {
            'column1': data['Top 10 Returns'].values.tolist(),
            'column2': data['Threshold Returns'].values.tolist(),
            'column3': data['Close'].values.tolist()
        }
    }
    
    # output JSON chart data
    return jsonify(chart_data)

@views.route('/portfolio-data')
def portfolio_data():
    # get the data from performance2
    data = get_pred_lists()
    
    serialized_data = []

    for df in data:
        serialized_df = df.to_dict(orient='records')
        serialized_data.append(serialized_df)

    # output JSON chart data
    return jsonify(serialized_data)

# render template for the information page
@views.route('/information')
def information():
    return render_template('information.html')

@views.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')