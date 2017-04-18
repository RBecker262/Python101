



import json
import requests
import parsfunc

url = 'http://gd2.mlb.com/components/game/mlb/year_2017/month_04/day_02/gid_2017_04_02_chnmlb_slnmlb_1/boxscore.json'
urlresponse = requests.get(url)
dictdata = json.loads(urlresponse.text)

parsfunc.dictlevel(dictdata, 1)
