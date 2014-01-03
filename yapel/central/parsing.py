import collections
import datetime
from decimal import Decimal
from xml import sax

MARKET_STAT_ELEMENTS = [
    'volume',
    'avg',
    'max',
    'min',
    'stddev',
    'median',
    'percentile',
]
QUICK_LOOK_ELEMENTS = [
    'region',
    'station',
    'security',
    'range',
    'price',
    'vol_remain',
    'min_volume',
    'expires',
    'reported_time',
]
MARKET_STAT_RESULT = collections.namedtuple(
    'MarketStatData', MARKET_STAT_ELEMENTS)
QL_ORDER = collections.namedtuple(
    'QuickLookOrder', ['order_id'] + QUICK_LOOK_ELEMENTS
)

class MarketstatParser(sax.ContentHandler):
    order_elems = ['buy', 'sell', 'all']

    def __init__(self, *args, **kwargs):
        sax.ContentHandler.__init__(self)
        self.items = {}
        self.item, self.order = None, None
        self.chars = ''

    def startElement(self, name, attrs):
        self.chars = ''
        if name == 'type':
            self.item = int(attrs.getValue('id'))
            self.items[self.item] = {}
        elif name in self.order_elems:
            self.order = name
            self.items[self.item][self.order] = {}

    def endElement(self, name):
        if name == 'type':
            self.item = None
        elif name in self.order_elems:
            order_dict = self.items[self.item][self.order]
            self.items[self.item][self.order] = MARKET_STAT_RESULT(
                *[order_dict[key] for key in MARKET_STAT_ELEMENTS]
            )
            self.order = None
        elif name in MARKET_STAT_ELEMENTS:
            self.items[self.item][self.order][name] = Decimal(self.chars)

    def characters(self, content):
        self.chars += content

    @classmethod
    def parse_response(cls, content):
        parser = cls()
        sax.parseString(content, parser)
        return parser.items

class QuicklookParser(sax.ContentHandler):
    order_elems = ['sell_orders', 'buy_orders']
    query_meta = ['item', 'hours', 'minqty']

    def __init__(self, *args, **kwargs):
        sax.ContentHandler.__init__(self)
        self.orders = {'meta': {}}
        self.order_type, self.order= None, None
        self.chars = ''

    def _convert_value(self, name, value):
        if name in ['price', 'security']:
            value = Decimal(value)
        elif name in ['min_volume', 'vol_remain', 'station', 'region']:
            value = int(value)
        elif name == 'expires':
            value = datetime.date(*[int(x) for x in value.split('-')])

        return value

    def startElement(self, name, attrs):
        self.chars = ''
        if name in self.order_elems:
            self.orders[name] = {}
            self.order_type = name
        elif name == 'order':
            self.order = int(attrs.getValue('id'))
            self.orders[self.order_type][self.order] = {}
        elif name in QUICK_LOOK_ELEMENTS:
            self.meta = name
        elif name in self.query_meta:
            self.orders['meta'][name] = None

    def endElement(self, name):
        if name == 'region' and not self.order_type:
            return
        if name in self.order_elems:
            self.order_type = None
        elif name in QUICK_LOOK_ELEMENTS:
            value = self._convert_value(name, self.chars)
            self.orders[self.order_type][self.order][name] = value
        elif name == 'order':
            order_dict = self.orders[self.order_type][self.order]
            order_dict['order_id'] = self.order
            self.orders[self.order_type][self.order] = QL_ORDER(
                *[order_dict[key] for key in ['order_id'] + QUICK_LOOK_ELEMENTS]
            )
            self.order = None
        elif name in self.query_meta:
            self.orders['meta'][name] = self.chars

    def characters(self, content):
        self.chars += content

    @classmethod
    def parse_response(cls, content):
        parser = cls()
        sax.parseString(content, parser)
        return parser.orders
