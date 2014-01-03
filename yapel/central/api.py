import requests
from requests import exceptions as requests_exceptions

from yapel import exceptions as yapel_exceptions
from yapel.central import parsing


EVE_CENTRAL_HOST = 'http://api.eve-central.com'
URL_ROOT = EVE_CENTRAL_HOST + '/api'


def _api_get(url, params):
    try:
        req = requests.get(url, params=params)
    except requests_exceptions.RequestException as e:
        raise yapel_exceptions.YapelApiError(e)
    else:
        return req.text

def market_stat(item_ids, system=None, regions=None, min_quant=None, hours=None):
    item_param = 'typeid=' + '&typeid='.join([str(x) for x in item_ids])

    url = URL_ROOT + '/marketstat?'
    url += item_param

    if regions:
        regions = [str(x) for x in regions]
        region_param = 'regionlimit=' + '&regionlimit'.join(regions)
        url += '&{region_param}'.format(region_param=region_param)

    params = {}
    if system:
        params['usesystem'] = system
    if min_quant:
        params['minQ'] = min_quant
    if hours:
        params['hours'] = hours

    raw_xml = _api_get(url, params)
    items = parsing.MarketstatParser.parse_response(raw_xml)
    return items

def quick_look(item_id, system=None, regions=None, min_quant=None, hours=None):
    url = URL_ROOT + '/quicklook'

    if regions:
        regions = [str(x) for x in regions]
        region_param = 'regionlimit=' + '&regionlimit'.join(regions)
        url += '?{region_param}'.format(region_param=region_param)

    params = {'typeid': item_id}
    if system:
        params['usesystem'] = system
    if min_quant:
        params['setminQ'] = min_quant
    if hours:
        params['sethours'] = hours

    raw_xml = _api_get(url, params)
    orders = parsing.QuicklookParser.parse_response(raw_xml)
    return orders
