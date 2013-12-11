MARKET_STAT_ORDERS = ['buy', 'sell', 'all']
MARKET_STAT_NODES = [
    'volume', 'avg', 'max', 'min', 'stddev', 'median', 'percentile'
]
QUICK_LOOK_NODES = [
    'region',
    'station',
    'security',
    'range',
    'price',
    'volume',
    'min_volume',
    'expires'
]


MARKET_STAT_TMPL = '''<evec_api version="2.0" method="marketstat_xml">
<marketstat>
<type id="{item_id}">
<buy>
<volume>{buy_volume}</volume>
<avg>{buy_avg}</avg>
<max>{buy_max}</max>
<min>{buy_min}</min>
<stddev>{buy_stddev}</stddev>
<median>{buy_median}</median>
<percentile>{buy_percentile}</percentile>
</buy>
<sell>
<volume>{sell_volume}</volume>
<avg>{sell_avg}</avg>
<max>{sell_max}</max>
<min>{sell_min}</min>
<stddev>{sell_stddev}</stddev>
<median>{sell_median}</median>
<percentile>{sell_percentile}</percentile>
</sell>
<all>
<volume>{all_volume}</volume>
<avg>{all_avg}</avg>
<max>{all_max}</max>
<min>{all_min}</min>
<stddev>{all_stddev}</stddev>
<median>{all_median}</median>
<percentile>{all_percentile}</percentile>
</all>
</type>
</marketstat>
</evec_api>'''

QUICK_LOOK_TMPL = '''<evec_api version="2.0" method="quicklook">
<quicklook>
<item>{item_id}</item>
<itemname>ITEM NAME</itemname>
<regions/>
<hours>{hours}</hours>
<minqty>{min_quant}</minqty>
<sell_orders>
<order id="1">
<region>{sell_region}</region>
<station>{sell_station}</station>
<station_name>STATION NAME</station_name>
<security>{sell_security}</security>
<range>{sell_range}</range>
<price>{sell_price}</price>
<vol_remain>{sell_volume}</vol_remain>
<min_volume>{sell_min_volume}</min_volume>
<expires>{sell_expires}</expires>
<reported_time>---</reported_time>
</order>
</sell_orders>
<buy_orders>
<order id="2">
<region>{buy_region}</region>
<station>{buy_station}</station>
<station_name>STATION NAME</station_name>
<security>{buy_security}</security>
<range>{buy_range}</range>
<price>{buy_price}</price>
<vol_remain>{buy_volume}</vol_remain>
<min_volume>{buy_min_volume}</min_volume>
<expires>{buy_expires}</expires>
<reported_time>---</reported_time>
</order>
</buy_orders>
</quicklook>
</evec_api>'''