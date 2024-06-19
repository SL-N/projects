from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup

sURL = 'https://www.finam.ru/quotes/stocks/russia/?utm_source=google_adwords_POISK_dsa&utm_medium=cpc_dsa&utm_term=&utm_content=ad_433215312921%7Cps_%7Cmt_b%7Cdev_c&utm_campaign=trafik_finam&gclid=Cj0KCQjwse-DBhC7ARIsAI8YcWIZLDgzOnlrkNHM9NIvKS3a51_gSL3s6b9Ur0sJ9DhrTtI-AK3W5_4aAoQEEALw_wcB'
sHEADERS = { 'user_agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 'accept' : '*/*'}

bURL = 'https://www.sravni.ru/vklady/kazan/'  # Ссылка на сайт со вкладами  банков
bHEADERS = { 'user_agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 'accept' : '*/*'}

YEAR = 365

#парсер банков
def bsort_list(list):

    result = []
    sotred_list_of_value = []
    sorted_values = []

    for element in list:
        sotred_list_of_value.append(float(element['procent']))
    sotred_list_of_value.sort()
    sorted_values.append(sotred_list_of_value[0])
    sorted_values.append(sotred_list_of_value[len(sotred_list_of_value)//2])
    sorted_values.append(sotred_list_of_value[-1])


    for element in list:
        if element['procent'] in sorted_values:
            result.append(element)
        if len(result) == 3:
            break


    return result


def bget_html(url, params = None):
    r = requests.get(url, headers = bHEADERS, params = params)
    return r

def bget_content(html):
    offer = []
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all( 'div', class_ = 'sc-1n3h0ai-0 kWVwbK')
    for item in items:

        pars_proc = item.find('span', class_ = 'rnxgye-7 iIkkir t-bold').get_text().replace('до ', '')
        pars_proc =  pars_proc.replace('%', '')
        pars_proc = pars_proc.replace(',', '.')

        offer.append(
            { 'title' : item.find('img', class_ = 'sc-1mal9y-4 hiVUJJ').get('title'),
              'procent' : float(pars_proc)

            }
        )
    result = bsort_list(offer)
    return(result)


def bparse():

    html = bget_html(bURL)
    if html.status_code == 200:
        return bget_content(html.text)
    else:
        print('Smth went wrong')


#парсер акций

def ssort_list(list):

    result = []
    sotred_list_of_value = []
    sorted_values = []

    for element in list:
        sotred_list_of_value.append(element['potential'])
    sotred_list_of_value.sort()
    sorted_values.append(sotred_list_of_value[0])
    sorted_values.append(sotred_list_of_value[len(sotred_list_of_value)//2])
    sorted_values.append(sotred_list_of_value[-1])


    for element in list:
        if element['potential'] in sorted_values:
            result.append(element)
        if len(result) == 3:
            break



    return result



def sget_html(url, params = None):
    r = requests.get(url, headers = sHEADERS, params = params)
    return r

def sget_content(html):
    stonks = []
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr', class_ = 'QuoteTable__tableRow--1AA QuoteTable__withHover--1vT')



    for item in items:
        potential_of_stonks = item.find('a', class_ = 'Prognosis__root--10f')
        if potential_of_stonks:
            potential_of_stonks = potential_of_stonks.get_text().replace('Потенциал:', '')
            potential_of_stonks = potential_of_stonks.replace('%','' )
            if '+' in potential_of_stonks:
                potential_of_stonks = int(potential_of_stonks.replace('+', ''))
                if potential_of_stonks != 0:

                    stonks.append(
                        { 'title' : item.find('a', class_  = 'InstrumentLink__instrument--1PO').get_text(),
                          'potential': potential_of_stonks }
                    )

    result = ssort_list(stonks)
    return(result)

def sparse():

    html = sget_html(sURL)
    if html.status_code == 200:
        return sget_content(html.text)
    else:
        print('Smth went wrong')

#счетчик

def years_counter(rate, sum, years):
    for years_count in range(years):
        profit = sum
        profit *= rate
        sum += profit

    return sum

def days_counter(rate, sum, days):

    rate = (days / YEAR) * rate
    profit = rate * sum
    sum += profit
    return sum

def counter_normal(rate,sum, days):
    rate = rate / 100
    if days < YEAR :
        result = days_counter(rate,sum,days)
        return int(result)

    years = days // YEAR
    rest_days = days % YEAR

    result = years_counter(rate, sum, years)
    result = days_counter(rate,result,rest_days)
    return int(result)

def counter_without_time(rate, sum, goal_sum):
    rate = rate / 100
    current_sum = 0
    current_time_years = 0

    while current_sum < goal_sum:
        sum = sum + sum * rate
        current_time_years += 1
        current_sum = sum

    return current_time_years


def main(request):
    return render(request, 'main/main.html')

def count(request):
    if request.method == "POST":
        money = request.POST.get('money')
        time = request.POST.get('a')
        target = request.POST.get('b')
        chek2 = request.POST.get('c')
        print(type(chek2))

        if chek2 == 'b':
            parse = bparse()
            if time == '':

                time = counter_without_time(rate = float(parse[0]['procent']),sum = int(money), goal_sum = int(target))
                time1 = counter_without_time(rate = float(parse[1]['procent']),sum = int(money), goal_sum = int(target))
                time2 = counter_without_time(rate = float(parse[2]['procent']),sum = int(money), goal_sum = int(target))
                return render(request, 'main/data.html',{
                        'time': time, 'title' : parse[0]['title'], 'procent' : parse[0]['procent'], 'result' : target,
                        'time1': time1, 'title1' : parse[1]['title'], 'procent1' : parse[1]['procent'],'result1' : target,
                        'time2': time2, 'title2' : parse[2]['title'], 'procent2' : parse[2]['procent'],'result2' : target
                        })
            else:
                time = int(time)
                time *= 365
                result = counter_normal(rate = float(parse[0]['procent']),sum = int(money), days = time)
                result1 = counter_normal(rate = float(parse[1]['procent']),sum = int(money), days = time)
                result2 = counter_normal(rate = float(parse[2]['procent']),sum = int(money), days = time)
                time = time/365
                return render(request, 'main/data.html', {
                        'time': time, 'title' : parse[0]['title'], 'procent' : parse[0]['procent'], 'result' : result,
                        'time1': time, 'title1' : parse[1]['title'], 'procent1' : parse[1]['procent'], 'result1' : result1,
                        'time2': time, 'title2' : parse[2]['title'], 'procent2' : parse[2]['procent'], 'result2' : result2
                        })

        else:
            parse = sparse()
            if time == '':
                time = counter_without_time(rate = float(parse[0]['potential']),sum = int(money), goal_sum = int(target))
                time1 = counter_without_time(rate = float(parse[1]['potential']),sum = int(money), goal_sum = int(target))
                time2 = counter_without_time(rate = float(parse[2]['potential']),sum = int(money), goal_sum = int(target))
                return render(request, 'main/data2.html',{
                        'time': time, 'title' : parse[0]['title'], 'procent' : parse[0]['potential'], 'result' : target,
                        'time1': time1, 'title1' : parse[1]['title'], 'procent1' : parse[1]['potential'],'result1' : target,
                        'time2': time2, 'title2' : parse[2]['title'], 'procent2' : parse[2]['potential'],'result2' : target
                        })

            else:
                time = int(time)
                time *= 365
                result = counter_normal(rate = float(parse[0]['potential']),sum = int(money), days = time)
                result1 = counter_normal(rate = float(parse[1]['potential']),sum = int(money), days = time)
                result2 = counter_normal(rate = float(parse[2]['potential']),sum = int(money), days = time)
                time = time/365
                return render(request, 'main/data2.html', {
                        'time': time, 'title' : parse[0]['title'], 'procent' : parse[0]['potential'], 'result' : result,
                        'time1': time, 'title1' : parse[1]['title'], 'procent1' : parse[1]['potential'], 'result1' : result1,
                        'time2': time, 'title2' : parse[2]['title'], 'procent2' : parse[2]['potential'], 'result2' : result2
                        })


    return render(request, 'main/count.html')

def data(request):

    return render(request, 'main/data.html')
