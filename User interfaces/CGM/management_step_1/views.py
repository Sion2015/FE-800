from django.shortcuts import render
from django.utils.safestring import mark_safe
from pymongo import MongoClient

from django import forms
from .database.collection_ETF import *
# --Connect to MongoDB to get all stock tickers
# host = '155.246.104.19:27017'
host = 'localhost:27017'
client = MongoClient(host=[host])
db = client.RoboAdvisor
tickers = [x['_id'] for x in list(db.ETF.find({}, {"_id": 1}))]
asset_type = get_asset_class(host, tickers)
tickers_choices = ['(\"'+ e + '\", ' + '\"'+ e + ', ' + asset_type[e] + '\"),'  for e in tickers]
tickers_choices = ' '.join(tickers_choices)
tickers_choices = (
    eval(tickers_choices)
)


posts = db.Parameters
df = list(posts.find({'_id': "unique"}, {'_id': 0}))
df = json_normalize(df)
my_tickers = df["my_tickers"][0]

class TickerForm(forms.Form):
    ETFs = forms.MultipleChoiceField(
        label='Your ETFs',
        widget=forms.CheckboxSelectMultiple(attrs={'class': "hide-checkbox"}), # 'checked': False
        choices=tickers_choices,
        initial=my_tickers,
        # help_text="Select your ETFs for portfolio construction",



        )


def management(request, tickers=tickers):



    # --Convert stocks list into a string. Then the html will parse the string into json object.
    tickers = '\", \"'.join(tickers)
    tickers = '[\"' + tickers + '\"]'

    result = "Changing the views will update the portfolio data in MongoBD"

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TickerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TickerForm()


    context = {
        'tickers': mark_safe(tickers),
        'result': result,
        'form': form,
    }

    return render(request, 'management/step_1.html', context)



