import random

from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils.datastructures import MultiValueDictKeyError
import math


# Create your views here.

ALL_REGIONS = ["臺北市", "新北市", "基隆市", "桃園市", "新竹縣", "新竹市", "苗栗縣", "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義縣", "嘉義市", "臺南市", "高雄市", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣"]
MAX_DATA_PER_PAGE = 8

page = 1
r = '所有縣市'
k = ""
@csrf_exempt
def home_page(request, keyword, region):
    global page, r, k
    try:
        region = request.POST['region']
        keyword = request.POST['keyword']
        if r != region or k != keyword:
            page = 1
        r = region
        k = keyword
    except MultiValueDictKeyError:
        try:
            page += int(request.POST['next-page'])
            if page < 1:
                page = 1
        except:
            pass
    if r is not None:
        content = dict()
        print('r:', r)
        print('re:', region)
        if region == '所有縣市' or r == '所有縣市':
            hotel_list = Hotel.objects.filter(hotel_name__contains=k)
            attraction_list = Attraction.objects.filter(attraction_name__contains=k)
            food_list = Food.objects.filter(food_name__contains=k)
            # content = {'hotel': hotel_list[MAX_DATA_PER_PAGE*(page-1):MAX_DATA_PER_PAGE*(page-1)], 'attraction': attraction_list, 'food': food_list}
        else:
            hotel_list = Hotel.objects.filter(hotel_name__contains=k, hotel_region=r)
            attraction_list = Attraction.objects.filter(attraction_name__contains=k, attraction_region=r)
            food_list = Food.objects.filter(food_name__contains=k, food_region=r)

        if len(hotel_list) > MAX_DATA_PER_PAGE * page:
            content['hotel'] = hotel_list[MAX_DATA_PER_PAGE * (page - 1):MAX_DATA_PER_PAGE * page]
        else:
            content['hotel'] = hotel_list[MAX_DATA_PER_PAGE * (page - 1):MAX_DATA_PER_PAGE * page - len(hotel_list)]

        if len(attraction_list) > MAX_DATA_PER_PAGE * page:
            content['attraction'] = attraction_list[MAX_DATA_PER_PAGE * (page - 1):MAX_DATA_PER_PAGE * page]
        else:
            content['attraction'] = attraction_list[MAX_DATA_PER_PAGE * (page - 1):MAX_DATA_PER_PAGE * page - len(attraction_list)]

        if len(food_list) > MAX_DATA_PER_PAGE * page:
            content['food'] = food_list[MAX_DATA_PER_PAGE * (page - 1):MAX_DATA_PER_PAGE * page]
        else:
            content['food'] = food_list[MAX_DATA_PER_PAGE * (page - 1):MAX_DATA_PER_PAGE * page - len(food_list)]

        total_page = (len(hotel_list) + len(attraction_list) + len(food_list)) // 24 + 1
        content['page'] = str(f'{page}/{total_page}')

        return render(request, 'index.html', content)
    else:
        return render(request, 'index.html')


@csrf_exempt
def auto_schedule(request, region, days, schedule_per_day, radius):
    if request.POST:
        region = request.POST['region']
        days = int(request.POST['days'])
        schedule_per_day = int(request.POST['max-points-per-day'])
        radius = float(request.POST['range-of-activity'])

        if region == "隨機縣市":
            region = ALL_REGIONS[random.randrange(0, len(ALL_REGIONS))]

        def dis(x1, y1, x2, y2):
            return math.sqrt((abs(y1 - y2) * 110.9362) ** 2 + (abs(x1 - x2) * 101.77545) ** 2)

        from random import choice, sample
        hotel_list = Hotel.objects.filter(hotel_region=region)
        center_hotel = model_to_dict(choice(hotel_list))
        center_x, center_y = center_hotel['hotel_px'], center_hotel['hotel_py']

        attraction_list = Attraction.objects.filter(attraction_region=region)
        while True:
            try:
                choice_attraction_list = sample([model_to_dict(attraction_list[i]) for i in range(len(attraction_list)) if
                                                 dis(center_x, center_y, model_to_dict(attraction_list[i])['attraction_px'],
                                                     model_to_dict(attraction_list[i])['attraction_py']) <= radius]
                                                , schedule_per_day * days // 2)
                break
            except ValueError:
                radius += 1
            if radius >= 500:
                return render(request, 'schedule.html', {"error": True})

        food_list = Food.objects.filter(food_region=region)
        while True:
            try:
                choice_food_list = sample([model_to_dict(food_list[i]) for i in range(len(food_list)) if
                                           dis(center_x, center_y, model_to_dict(food_list[i])['food_px'],
                                               model_to_dict(food_list[i])['food_py']) <= radius],
                                          schedule_per_day * days // 2)
                break
            except ValueError:
                radius += 1
            if radius >= 500:
                return render(request, 'schedule.html', {"error": True})

        s = [center_hotel] + choice_food_list + choice_attraction_list
        ss = choice_food_list + choice_attraction_list
        sss = []
        random.shuffle(ss)
        step = int(len(ss) / days)
        for i in range(0, len(ss), step):
            sss.append(ss[i: i+step])
            print(len(ss[i: i+step]))
        print(sss)


        def to_url(d):
            r = []
            n = []
            for i in d:
                try:
                    r.append(i['attraction_region'])
                    n.append(i['attraction_name'])
                except KeyError:
                    pass
                try:
                    r.append(i['food_region'])
                    n.append(i['food_name'])
                except KeyError:
                    pass

            result = ""
            for i in range(len(r)):
                result += str(r[i])
                result += str(n[i])
                result += "%7C"

            return result
        urls = []
        for i in range(days):
            try:
                url = f"https://www.google.com/maps/dir/?api=1&origin={center_hotel['hotel_region']}{center_hotel['hotel_name']}" \
                      f"&waypoints={to_url(sss[i][:-1])}" \
                      f"&destination={s[-1]['attraction_region']}{sss[i][-1]['attraction_name']}"
                urls.append([url, i+1])
            except KeyError:
                pass
            except ValueError:
                pass
            try:
                url = f"https://www.google.com/maps/dir/?api=1&origin={center_hotel['hotel_region']}{center_hotel['hotel_name']}" \
                      f"&waypoints={to_url(sss[i][:-1])}" \
                      f"&destination={sss[i][-1]['food_region']}{sss[i][-1]['food_name']}"
                urls.append([url, i+1])
            except KeyError:
                pass
            except ValueError:
                pass
        return render(request, 'schedule.html', {'map': urls})

    return render(request, 'schedule.html')

@csrf_exempt
def about(request):
    return render(request, 'about.html')