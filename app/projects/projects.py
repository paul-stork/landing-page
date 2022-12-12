from flask import Flask, Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import DateField, SelectField


projects = Blueprint('projects', __name__, template_folder='templates', static_folder='static')

class cryptoFilter(FlaskForm):
    startDate = DateField("Start Date:")
    endDate = DateField("End Date:")
    cryptoSelector = SelectField("Crypto Coin:")

@projects.route('/projects')
def projectsHome():
    
    return render_template('projects.html')

""" 
    First project for plotting crypto closing values between two user defined dates.
    Initially, the date will be between todays date and today - 7 days, until we get more 
    data in the crypto database. Once the project has loaded, the user will be able to filter
    based on start date (startDate), end date (endDate), and specific crypto coin or all (cryptoCoin).
    Here goes nothing!
"""

@projects.route('/cryptoprojects', methods=['GET', 'POST'])
def cryptoProjects():
    from ..extensions import db 
    from ..models import daily_crypto_data
    import pandas as pd
    from datetime import datetime, timedelta
    from sqlalchemy import and_
    from flask import request
    import plotly_express as px
    import plotly
    import json
    
    form = cryptoFilter()
    
    # Define the initial variables:
    endDate = datetime.now()
    startDate = endDate - timedelta(days=7)
    cryptoCoin = 'All Coins'
    
    if request.method == 'POST':
        if request.form.get('startDate') != '':
            startDate = datetime.strptime(request.form.get('startDate') + "T00:00:00", '%Y-%m-%dT%H:%M:%S')
        if request.form.get('endDate') != '':
            endDate = datetime.strptime(request.form.get('endDate') + 'T00:00:00', '%Y-%m-%dT%H:%M:%S')
        cryptoCoin = request.form.get('cryptoSelector')
        
        print(startDate)
        print(endDate)
        print(cryptoCoin)
        
        if cryptoCoin !='All Coins':
            cryptoInfo = db.session.execute(db.select(daily_crypto_data).order_by(daily_crypto_data.time_period_end).filter(and_(
                daily_crypto_data.time_period_end.between(startDate, endDate)),
                daily_crypto_data.exchange_id==cryptoCoin)).scalars()
        else:
            cryptoInfo = db.session.execute(db.select(daily_crypto_data).order_by(daily_crypto_data.time_period_end).filter(
            daily_crypto_data.time_period_end.between(startDate, endDate))).scalars()
                
    else:
        cryptoInfo = db.session.execute(db.select(daily_crypto_data).order_by(daily_crypto_data.time_period_end)).scalars()
    
    tempList = []
    
    for x in cryptoInfo:
        tempVar = x.__dict__
        tempDict = dict(tempVar)
        tempDict.pop('_sa_instance_state', None)
        tempList.append(tempDict)
        
    cryptoDF = pd.DataFrame(tempList)
    
    
    coinInfo = db.session.execute(db.select(daily_crypto_data.exchange_id.distinct())).scalars().all()
    
    coinList = []
    for x in coinInfo:
        coinList.append(x)
    
    coinList.insert(0,'All Coins')
    print(coinList)
    
    title = f"{cryptoCoin} value between {startDate} and {endDate}"
    
   
    crypto_line = px.line(cryptoDF, x='time_period_end',
                          y='rate_close',
                          color='exchange_id',
                          title = title,
                          labels={
                              'time_period_end':'Date and Time',
                              'rate_close':'Price ($)',
                              'exchange_id':'Crypto Coin'
                          })
    
    crypto_line_json = json.dumps(crypto_line, cls=plotly.utils.PlotlyJSONEncoder)
     
    return render_template('cryptoProjects.html', 
                           crypto_line_json = crypto_line_json,
                           form=form,
                           coinList = coinList)