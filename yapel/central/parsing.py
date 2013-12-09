import datetime
import decimal
from xml import sax

class MarketstatParser(sax.ContentHandler):
    data_elems = ['volume', 'avg', 'max', 'min', 'stddev', 'median', 'percentile']
    order_elems = ['buy', 'sell', 'all']

    def __init__(self, *args, **kwargs):
        sax.ContentHandler.__init__(self)
        self.items = {}
        self.item, self.order = None, None
        self.chars = ''

    def startElement(self, name, attrs):
        self.chars = ''
        if name == 'type':
            self.item = attrs.getValue('id')
            self.items[self.item] = {}
        elif name in self.order_elems:
            self.order = name
            self.items[self.item][self.order] = {}

    def endElement(self, name):
        if name == 'type':
            self.item = None
        elif name in self.order_elems:
            self.order = None
        elif name in self.data_elems:
            self.items[self.item][self.order][name] = decimal.Decimal(self.chars)

    def characters(self, content):
        self.chars += content

    @classmethod
    def parse_response(cls, content):
        parser = cls()
        sax.parseString(content, parser)
        return parser.items

class QuicklookParser(sax.ContentHandler):
    data_elems = ['region', 'station', 'security', 'range', 'price', 'vol_remain', 'min_volume', 'expires', 'reported_time']
    order_elems = ['sell_orders', 'buy_orders']
    query_meta = ['item', 'hours', 'minqty']

    def __init__(self, *args, **kwargs):
        sax.ContentHandler.__init__(self)
        self.orders = {'meta': {}}
        self.order_type, self.order= None, None
        self.chars = ''

    def _convert_value(self, name, value):
        if name in ['price', 'security']:
            value = decimal.Decimal(value)
        elif name in ['min_volume', 'vol_remain']:
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
            self.order = attrs.getValue('id')
            self.orders[self.order_type][self.order] = {}
        elif name in self.data_elems:
            self.meta = name
        elif name in self.query_meta:
            self.orders['meta'][name] = None

    def endElement(self, name):
        if name == 'region' and not self.order_type:
            return
        if name in self.order_elems:
            self.order_type = None
        elif name in self.data_elems:
            value = self._convert_value(name, self.chars)
            self.orders[self.order_type][self.order][name] = value
        elif name == 'order':
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
