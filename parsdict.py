



import json
import requests

url = 'http://gd2.mlb.com/components/game/mlb/year_2017/month_04/day_02/gid_2017_04_02_chnmlb_slnmlb_1/boxscore.json'
urlresponse = requests.get(url)
dictdata = json.loads(urlresponse.text)

keylist = list(dictdata.keys())

for dictkey in keylist:
    if type(dictdata[dictkey]) is dict:
        print('Subdictionary ' + dictkey)
    else:
        print('Subvalue ' + dictkey)
