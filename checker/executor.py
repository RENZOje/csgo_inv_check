import json
from collections import Counter
import humanize
from datetime import datetime
from requests_html import HTMLSession

from checker.async_scraper_float import call_float
from checker.async_scraper_price import call_price



session = HTMLSession()




# json_data = json.load(open(r'C:\Project(python)\csgo_inv_check\checker\file.txt','r'))

# steam_id64 = '76561198245579318'





def inspect_url(steam_id64,rg_inv_keys,rg_descr_keys, json_data):
    global rd_inspect_url
    _dict_for_inspect = dict()

    for i in rg_inv_keys:
        if json_data['rgInventory'][i]['classid'] not in _dict_for_inspect.values():
            _dict_for_inspect[i] = json_data['rgInventory'][i]['classid']

    rd_inspect_url = []
    for _ in zip(rg_descr_keys,_dict_for_inspect.keys()):
        try:
            rd_inspect_url.append((json_data['rgDescriptions'][_[0]]['actions'][0]['link']).replace('%owner_steamid%',steam_id64).replace('%assetid%',_[1]))
        except KeyError:
            rd_inspect_url.append(None)
            pass
    return rd_inspect_url

def inspect_quality_exterior_data(rg_descr_keys, json_data):
    global rd_inspect_quality_exterior #['Covert', 'eb4b4b', 'Factory New']
    rd_inspect_quality_exterior = []
    for _ in rg_descr_keys:
        try:
            rd_inspect_quality_exterior.append([json_data['rgDescriptions'][_]['tags'][4]['name'],json_data['rgDescriptions'][_]['tags'][4]['color'],json_data['rgDescriptions'][_]['tags'][5]['name']])
        except (KeyError, IndexError):
            try:
                rd_inspect_quality_exterior.append([json_data['rgDescriptions'][_]['tags'][3]['name'],
                                                    json_data['rgDescriptions'][_]['tags'][3]['color'],
                                                    json_data['rgDescriptions'][_]['tags'][4]['name']])

            except (KeyError, IndexError):
                rd_inspect_quality_exterior.append([None,None,None])
                pass
    return rd_inspect_quality_exterior


def expiration_data(rg_descr_keys, json_data):
    # trade lock
    global rd_expiration
    rd_expiration = []
    for _ in rg_descr_keys:
        try:
            time = json_data['rgDescriptions'][_]['cache_expiration']
            try:
                rd_expiration.append(humanize.naturaldelta(datetime.fromisoformat(time.replace('Z', ''))))
            except (TypeError, AttributeError):
                rd_expiration.append(None)
        except (KeyError,AttributeError):
            rd_expiration.append(None)
            pass
    return rd_expiration

def executor(steam_id64):
    json_data = json.loads(session.get(f'https://steamcommunity.com/profiles/{steam_id64}/inventory/json/730/2').text)
    rg_inv_keys = json_data['rgInventory'].keys()
    rg_descr_keys = json_data['rgDescriptions'].keys()
    ri_classid_amount = list(dict(Counter((json_data['rgInventory'][_]['classid'] for _ in rg_inv_keys))).values())
    rd_full_name = [json_data['rgDescriptions'][_]['market_hash_name'] for _ in rg_descr_keys]
    rd_icon_url = [f'https://steamcommunity-a.akamaihd.net/economy/image/{json_data["rgDescriptions"][_]["icon_url"]}/330x192' for _ in rg_descr_keys]
    rd_inspect_url = inspect_url(steam_id64,rg_inv_keys,rg_descr_keys, json_data)
    rd_inspect_quality_exterior = inspect_quality_exterior_data(rg_descr_keys, json_data)
    rd_expiration = expiration_data(rg_descr_keys, json_data)
    prices_items = call_price(rd_full_name=rd_full_name)
    floats_items = call_float(rd_inspect_url=rd_inspect_url)

    items = {'rd_full_name':rd_full_name,
             'rd_icon_url':rd_icon_url,
             'rd_inspect_url':rd_inspect_url,
             'float':floats_items,
             'amount':ri_classid_amount,
             'class_item':[i[:][0] for i in rd_inspect_quality_exterior],
             'condition':[i[:][2] for i in rd_inspect_quality_exterior],
             'color':[i[:][1] for i in rd_inspect_quality_exterior],
             'expiration':rd_expiration,
             'price':prices_items,
             
             }
    items_min = min([len(x) for x in items.values()])

    items = {'rd_full_name': rd_full_name[0:items_min],
             'rd_icon_url': rd_icon_url[0:items_min],
             'rd_inspect_url': rd_inspect_url[0:items_min],
             'float': floats_items[0:items_min],
             'amount': ri_classid_amount[0:items_min],
             'class_item': [i[:][0] for i in rd_inspect_quality_exterior][0:items_min],
             'condition': [i[:][2] for i in rd_inspect_quality_exterior][0:items_min],
             'color': [i[:][1] for i in rd_inspect_quality_exterior][0:items_min],
             'expiration': rd_expiration[0:items_min],
             'price': prices_items[0:items_min],

             }
    return items

# executor('76561197980865567')
