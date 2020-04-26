import re

from indic_transliteration import sanscript
from indic_transliteration.sanscript import SCHEMES, SchemeMap, transliterate


def get_upper(upper):
    face = re.search(r'Property Face :\s*([^\n]+)', upper)
    face = face.group(1)
    year = re.search(r'Build Year :\s*([^\n]+)', upper)
    year = year.group(1)
    views = re.search(r'Views :\s*([^\n]+)', upper)
    views = views.group(1)
    return face, year, views


def get_lower(lower):
    area = re.search(r'Area Covered :\s*([^\n]+)', lower)
    area = area.group(1)
    road = re.search(r'Road Access :\s*([^\n]+)', lower)
    road = road.group(1)
    road_width, road_type = check_road(road)
    build_area = re.search(r'Build Up Area :\s*([^\n]+)', lower)
    build_area = build_area.group(1)
    posted = re.search(r'Posted :\s*([^\n]+)', lower)
    posted = posted.group(1)
    return area, road, road_width, road_type, build_area, posted


'''
def view_count(x):  #FAULTY
    if type(x) == float or type(x) == int:
        return x
    if 'K' or'k' in x:
        if len(x) > 1:
            return float(x.replace('K', '')) * 1000
        return 1000.0
    else:
        return x
'''


def get_price(data):
    eng = transliterate(data, sanscript.DEVANAGARI, sanscript.ITRANS)
    eng = re.sub(r"\D", "", eng)
    return(int(eng))


def check_road(s):
    if s.find('/') != -1:
        word_list = s.split('/')
        road_type = word_list[1]
        road_width = word_list[0]
    else:
        road_width = s
        road_type = 'NA'
    return road_width, road_type
