from flask import Flask, request, Response
import pandas as pd
import pickle, datetime, json

app = Flask(__name__)

model = pickle.load(open('model/bu02/model.pickle', 'rb'))

@app.route('/')
def home():
    return 'Hello World'

@app.route('/predictions')
def get_predictions():
    """
    """
    date_str = request.args.get('date')
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')

    list_YEAR=[]
    list_MONTH=[]
    list_DAY=[]
    list_HOUR=[]
    list_WOY=[]
    list_DOY=[]
    list_DOW=[]
    
    for i in range(24):
        list_YEAR.append(date_obj.year)
        list_MONTH.append(date_obj.month)
        list_DAY.append(date_obj.day)
        list_HOUR.append(i)
        list_WOY.append(date_obj.isocalendar()[1])
        list_DOY.append(date_obj.timetuple().tm_yday)
        list_DOW.append(date_obj.weekday())

    df = pd.DataFrame(list(zip(list_YEAR, list_MONTH, list_DAY, list_HOUR, list_WOY, list_DOY, list_DOW)),
                      columns=['YEAR', 'MONTH', 'DAY', 'HOUR', 'WOY', 'DOY', 'DOW'])

    df_predictions = pd.DataFrame(data=model.predict(df),
                                  columns=['PREDICT_CURRENT_VOLUME','PREDICT_DAILY_VOLUME'])

    df_all = pd.concat([df,df_predictions], axis=1, ignore_index=False)

    resp = Response(response=df_all.to_json(orient="records"), status=200, mimetype='application/json')

    return resp

app.run(port=5000)

