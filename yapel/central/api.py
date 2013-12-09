import requests
from requests import exceptions as requests_exceptions

from yapel.central import parsing

def market_stat(item_ids, system=None, regions=None, min_quant=None, hours=None):
    item_param = 'typeid=' + '&typeid='.join([str(x) for x in item_ids])

    url = 'http://api.eve-central.com/api/marketstat?'
    url += item_param

    if regions:
        regions = [str(x) for x in regions]
        region_param = 'regionlimit=' + '&regionlimit'.join(regions)
        url += '&{region_param}'.format(region_param=region_param)

    data = {}
    if system:
        data['usesystem'] = system
    if min_quant:
        data['minQ'] = min_quant
    if hours:
        data['hours'] = hours

    try:
        req = requests.get(url, params=data)
    except requests_exceptions.RequestException:
        return {}

    items = parsing.MarketstatParser.parse_response(req.text)
    return items

def quick_look(item_id, system=None, regions=None, min_quant=None, hours=None):
    url = 'http://api.eve-central.com/api/quicklook'

    if regions:
        regions = [str(x) for x in regions]
        region_param = 'regionlimit=' + '&regionlimit'.join(regions)
        url += '?{region_param}'.format(region_param=region_param)

    data = {'typeid': item_id}
    if system:
        data['usesystem'] = system
    if min_quant:
        data['setminQ'] = min_quant
    if hours:
        data['sethours'] = hours

    try:
        req = requests.get(url, params=data)
    except requests_exceptions.RequestException:
        return {}

    print req.url

    orders = parsing.QuicklookParser.parse_response(req.text)
    return orders
