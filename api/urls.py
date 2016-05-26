# -*- coding: utf-8 -*-
from api.account import AccountHandler
from api.account import TransactionHandler
from api.alert import AlertHandler
from api.breakout import BreakoutHandler
from api.seeesvee import export
from api.seeesvee import progress
from api.seeesvee import upload
from api.opportunity import OpportunityHandler
from api.order import OrderHandler
from api.position import PositionHandler
from api.watched import WatchedHandler
from django.conf.urls.defaults import patterns
from piston.resource import Resource


account_resource = Resource(AccountHandler)
alert_resource = Resource(AlertHandler)
breakout_resource = Resource(BreakoutHandler)
opportunity_resource = Resource(OpportunityHandler)
order_resource = Resource(OrderHandler)
position_resource = Resource(PositionHandler)
transaction_resource = Resource(TransactionHandler)
watched_resource = Resource(WatchedHandler)


urlpatterns = patterns('',
  (r'^account$', account_resource))

urlpatterns += patterns('',
  (r'^alert/(?P<alert_id>\d+)$', alert_resource),
  (r'^alert$', alert_resource))

urlpatterns += patterns('',
  (r'^breakout/(?P<breakout_id>\d+)$', breakout_resource),
  (r'^breakout$', breakout_resource))

urlpatterns += patterns('',
  (r'^export$', export))

urlpatterns += patterns('',
  (r'^progress$', progress))

urlpatterns += patterns('',
  (r'^import$', upload))

urlpatterns += patterns('',
  (r'^opportunity$', opportunity_resource))

urlpatterns += patterns('',
  (r'^order/(?P<order_id>\d+)$', order_resource),
  (r'^order$', order_resource))

urlpatterns += patterns('',
  (r'^transaction/(?P<transaction_id>\d+)$', transaction_resource),
  (r'^transaction$', transaction_resource))

urlpatterns += patterns('',
  (r'^position/(?P<position_id>\d+)$', position_resource),
  (r'^position$', position_resource))

urlpatterns += patterns('',
  (r'^watched/(?P<watched_id>\d+)$', watched_resource),
  (r'^watched$', watched_resource))
