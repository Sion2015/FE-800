from django.shortcuts import render
from django.utils.safestring import mark_safe
import urllib.request
import codecs
import pandas as pd
from pandas.io.json import json_normalize
import json
import datetime




class Typeform(object):
    def __init__(self, myEmail, url='https://api.typeform.com/v1/form/L3dqRV?key=86b376b41e8ff574b2fd8a87cbbf7fd374998eac'):
        self.myEmail = myEmail
        data = urllib.request.urlopen(url)
        reader = codecs.getreader("utf-8")
        obj = json.load(reader(data))
        df = json_normalize(obj)
        responses = df["responses"]
        responses = list(responses)
        responses = json_normalize(responses[0])
        self.responses = responses[
            ['token', 'answers.email_47631123', 'answers.number_47635826', 'answers.opinionscale_47631274',
            'metadata.date_land']].dropna()
        self.findMyResponse = False
        self.amount = 0
        self.risk_tolerance = 0
        self.find_my_response()

    def find_my_response(self):
        for i in range(len(self.responses)):
            self.responses.iloc[i]["metadata.date_land"] = datetime.datetime.strptime(
                self.responses.iloc[i]["metadata.date_land"],
                '%Y-%m-%d %H:%M:%S')
        if (pd.Series(list(self.responses['answers.email_47631123'] == self.myEmail)).any() == False):
            self.findMyResponse = False
        else:
            self.findMyResponse = True
            MyResponse = self.responses.loc[self.responses['answers.email_47631123'] == self.myEmail]
            MyResponse = MyResponse.sort_values('metadata.date_land', axis=0, ascending=False)
            MyLatestResponse = MyResponse.iloc[0]
            self.amount = int(MyLatestResponse['answers.number_47635826'])
            self.risk_tolerance = int(MyLatestResponse['answers.opinionscale_47631274'])

