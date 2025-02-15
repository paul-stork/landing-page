from flask import Flask, Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField
import logging


projects = Blueprint('projects', __name__, template_folder='templates', static_folder='static')

logger = logging.getLogger('app.app')

class cryptoFilter(FlaskForm):
    startDate = DateField("Start Date:")
    endDate = DateField("End Date:")
    cryptoSelector = SelectField("Crypto Coin:", coerce=str)
    submitButton = SubmitField('Filter')

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

@projects.route('/cryptoproject', methods=['GET', 'POST'])
def cryptoProject():
    from ..extensions import db 
    from ..models import daily_crypto_prod
    import pandas as pd
    from datetime import datetime, timedelta
    from sqlalchemy import and_, exc
    from flask import request
    import plotly_express as px
    import plotly
    import json
    
    form = cryptoFilter()
    
    # Define the initial variables:
    endDate = datetime.strptime("2025-02-10T00:00:00", '%Y-%m-%dT%H:%M:%S')
    startDate = endDate - timedelta(days=1)
    cryptoCoin = 'All Coins'
    try:
        if request.method == 'POST':
            if request.form.get('startDate') != '':
                startDate = datetime.strptime(request.form.get('startDate') + "T00:00:00", '%Y-%m-%dT%H:%M:%S')
            if request.form.get('endDate') != '':
                endDate = datetime.strptime(request.form.get('endDate') + 'T00:00:00', '%Y-%m-%dT%H:%M:%S')
            cryptoCoin = request.form.get('cryptoSelector')
            
            if cryptoCoin !='All Coins':
                cryptoInfo = db.session.execute(db.select(daily_crypto_prod).order_by(daily_crypto_prod.time_period_end).filter(and_(
                    daily_crypto_prod.time_period_end.between(startDate, endDate)),
                    daily_crypto_prod.exchange_id==cryptoCoin)).scalars()
            else:
                cryptoInfo = db.session.execute(db.select(daily_crypto_prod).order_by(daily_crypto_prod.time_period_end).filter(
                daily_crypto_prod.time_period_end.between(startDate, endDate))).scalars()
                    
        else:
            cryptoInfo = db.session.execute(db.select(daily_crypto_prod).order_by(daily_crypto_prod.time_period_end).filter(
                daily_crypto_prod.time_period_end.between(startDate, endDate))).scalars()
    except exc.SQLAlchemyError as e:
        logger.error(e)
    tempList = []
    
    for x in cryptoInfo:
        logger.info(f"x: {x}")
        tempVar = x.__dict__
        tempDict = dict(tempVar)
        tempDict.pop('_sa_instance_state', None)
        logger.info(f'tempDict: {tempDict}')
        tempList.append(tempDict)
    logger.info(f"tempList: {tempList}")    
    cryptoDF = pd.DataFrame(tempList)
    
    
    coinInfo = db.session.execute(db.select(daily_crypto_prod.exchange_id.distinct())).scalars().all()
    
    coinList = []
    for x in coinInfo:
        coinList.append(x)
    
    coinList = sorted(coinList)
    
    coinList.insert(0,'All Coins')

    form.cryptoSelector.choices = coinList

    
    title = f"{cryptoCoin} value in USD between {startDate.strftime('%Y-%m-%d')} and {endDate.strftime('%Y-%m-%d')}"
    crypto_line = px.line(data_frame=cryptoDF, \
                          x='time_period_end',\
                          y='rate_close',\
                          color='exchange_id',\
                          title = title,\
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
    
@projects.route('/dataengineering', methods=['GET'])
def dataengineeringprojects():
    return render_template('cryptoapipull.html')

@projects.route('/animatedplot', methods=['GET'])
def animatedplot():
    return render_template('animatedplot.html')