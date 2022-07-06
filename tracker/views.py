from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# from django.http import HttpResponse
# Create your views here.


def home(request):
    data_request = requests.get('https://api.covid19india.org/data.json')
    data = data_request.json()
    context = {
        'confirmed': data['statewise'][0]['confirmed'],
        'active': data['statewise'][0]['active'],
        'recovered': data['statewise'][0]['recovered'],
        'deceased': data['statewise'][0]['deaths'],
        'deltaconfirmed': data['cases_time_series'][-1]['dailyconfirmed'],
        'deltaactive': int(data['cases_time_series'][-1]['dailyconfirmed'])-(int(data['cases_time_series'][-1]['dailyrecovered'])+int(data['cases_time_series'][-1]['dailydeceased'])),
        'deltarecovered': data['cases_time_series'][-1]['dailyrecovered'],
        'deltadeaths': data['cases_time_series'][-1]['dailydeceased']
    }
    # print(context)
    series_length = len(data['cases_time_series']) - 31
    series_date = []
    series_confirmed = []
    series_recovered = []
    series_deceased = []
    for i in range(series_length, len(data['cases_time_series'])):
        series_confirmed.append(data['cases_time_series'][i]['dailyconfirmed'])
        series_recovered.append(data['cases_time_series'][i]['dailyrecovered'])
        series_deceased.append(data['cases_time_series'][i]['dailydeceased'])
        series_date.append(data['cases_time_series'][i]['date'])
    # series = [series_date, series_confirmed, series_recovered, series_deceased]
    return render(request, 'tracker/home.html', {'context': context})


def country(request):
    # url = 'https://www.worldometers.info/coronavirus/'
    # html_content = requests.get(url).text
    # soup = BeautifulSoup(html_content, 'lxml')
    # data = soup.find_all('div', class_='maincounter-number')
    # d = []
    # for dx in data:
    #     d.append(dx.text.replace('\n', ' ').strip())
    # context = {'confirmed': d[0], 'active': d[0], 'recovered': d[1], 'deceased': d[2]}
    return render(request, 'tracker/country.html')
    # data_request = requests.get('https://covidapi.info/api/v1/global')
    # data = data_request.json()
    # context = {
    #     'confirmed': data['result']['confirmed'],
    #     'recovered': data['result']['recovered'],
    #     'deceased': data['result']['deaths'],
    #     # 'active': (data['result']['confirmed']-(data['result']['recovered']+data['result']['deaths']))
    # }
    # # print(context)
    # return render(request, 'tracker/home.html', {'context': context})

def news(request):

    # url = 'https://www.indiatoday.in/coronavirus-covid-19-outbreak'
    # html_content = requests.get(url).text
    # soup = BeautifulSoup(html_content, 'lxml')
    # article = soup.find_all('div', class_='catagory-listing')
    # news = []
    # for data in article:
    #     pic = data.find('img')['src']
    #     heading = data.find('div', class_='detail').h2
    #     link = heading.a['href']
    #     content = data.find('div', class_='detail').p.text
    #     s = {'pic': pic, 'heading': heading.text.replace('\n', ' ').strip(), 'link': link, 'content': content.replace('\n', ' ').strip()}
    #     news.append(s)
    url = "http://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=38f476a7b8fe450eb9ee0482ae30c808"
    data = requests.get(url)
    news_data = data.json()
    news = news_data['articles']
    latest_news = []
    for d in news:
        di = {'source': d['source']['name'], 'pic': d['urlToImage'], 'heading': d['title'],
              'content': d['description'], 'link': d['url']}
        latest_news.append(di)
    return render(request, 'tracker/news.html', {'context': latest_news})


def statedata(request):
    data_request = requests.get('https://api.covid19india.org/data.json')
    update_data = requests.get('https://api.covid19india.org/states_daily.json')
    update = update_data.json()
    data = data_request.json()
    deceased = update['states_daily'][-1]
    recovered = update['states_daily'][-2]
    confirmed = update['states_daily'][-3]
    # print(data['statewise'][1])
    table_data = []
    for i in range(1, len(data['statewise'])):
        state_data = data['statewise'][i]
        da = {'state': state_data['state'], 'confirmed': state_data['confirmed'], 'active': state_data['active'],
              'deaths': state_data['deaths'], 'recovered': state_data['recovered'],
              'latest_confirm': confirmed[state_data['statecode'].lower()],
              'latest_recovered': recovered[state_data['statecode'].lower()], 'latest_deaths': deceased[state_data['statecode'].lower()]}
        table_data.append(da)
    return render(request, 'tracker/statewise.html', {'context': table_data})