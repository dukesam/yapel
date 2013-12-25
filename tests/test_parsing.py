import decimal
import unittest

from . import parsing_helpers as helpers

from yapel.central import parsing


def _build_market_stat_xml(item_id=None, **kwargs):
    format_dict = {'item_id': item_id or 1}
    for order_type in helpers.MARKET_STAT_ORDERS:
        for node_name in helpers.MARKET_STAT_NODES:
            format_dict['{0}_{1}'.format(order_type, node_name)] = -1

    format_dict.update(kwargs)
    return helpers.MARKET_STAT_TMPL.format(**format_dict)


def _build_quick_look_xml(item_id=None, **kwargs):
    format_dict = {}
    for order_type in ['buy', 'sell']:
        for node_name in helpers.QUICK_LOOK_NODES:
            format_dict['{0}_{1}'.format(order_type, node_name)] = -1

    format_dict.update({
        'item_id': item_id or 1,
        'sell_expires': '2000-1-1',
        'buy_expires': '2000-1-1',
        'hours': 24,
        'min_quant': 1,
    })
    format_dict.update(**kwargs)
    return helpers.QUICK_LOOK_TMPL.format(**format_dict)

class TestMarketStatParsing(unittest.TestCase):
    item_id = 1

    def _get_items(self, item_id=None, **kwargs):
        item_id = item_id or self.item_id
        xml_string = _build_market_stat_xml(item_id, **kwargs)
        items = parsing.MarketstatParser.parse_response(xml_string)
        return items

    def test_simple_parsing(self):
        """Simple smoke test"""
        items = self._get_items()[self.item_id]
        for order_type in helpers.MARKET_STAT_ORDERS:
            for node_name in helpers.MARKET_STAT_NODES:
                self.assertEqual(items[order_type][node_name], -1)

    def test_format_handling(self):
        """Spaces/tabs/newlines should not cause problems with parsing values"""
        items = self._get_items(sell_volume='\n\t 100 \t\n')
        self.assertEqual(items[self.item_id]['sell']['volume'], 100)

    def test_decimal_pasing(self):
        """Deciaml values should make it out unscathed"""
        dec_string = '10.1'
        items = self._get_items(sell_avg=dec_string)
        self.assertEqual(
            items[self.item_id]['sell']['avg'], decimal.Decimal(dec_string)
        )

class TestQuickLookParsing(unittest.TestCase):
    def test_simple_parsing(self):
        xml_string = _build_quick_look_xml()
        orders = parsing.QuicklookParser.parse_response(xml_string)