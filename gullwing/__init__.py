# -*- coding: utf-8 -*-
from datetime import date
from datetime import datetime
from datetime import timedelta
from logging import getLogger
from MySQLdb import connect
from os import makedirs
from os import putenv
from os.path import exists
from os.path import join
from os.path import realpath
from settings import CHARTS_PATH
from settings import DAYS_TO_FETCH
from settings import ENGINE_PATH
from settings import EXTERN_PATH
from settings import R_DB_CONFIG_PATH
from settings import R_PATH
from settings import R_LIBS_USER
from subprocess import Popen
from subprocess import PIPE

logger = getLogger('gullwing')


def generate_chart(symbol, date):
  chart_path = join(CHARTS_PATH, symbol)
  if not exists(chart_path):
    makedirs(chart_path)
  chart_filename = realpath(join(chart_path, date.strftime('%Y-%m-%d') + '.png'))

  putenv('R_LIBS_USER', R_LIBS_USER)
  proc = Popen([
      R_PATH,
      EXTERN_PATH,
      date.strftime('%Y-%m-%d'),
      symbol,
      chart_filename,
      R_DB_CONFIG_PATH], stdout=PIPE, stderr=PIPE)
  (out, err) = proc.communicate()
  logger.info('%s\n%s', out, err)


def run_engine():
  logger.info('Running engine')
  now, start = _get_start_date()
  putenv('R_LIBS_USER', R_LIBS_USER)
  proc = Popen([
      R_PATH,
      ENGINE_PATH,
      start.strftime('%Y-%m-%d'),
      now.strftime('%Y-%m-%d'),
      'TRUE',
      'FALSE',
      R_DB_CONFIG_PATH], stdout=PIPE, stderr=PIPE)
  (out, err) = proc.communicate()
  logger.info('%s\n%s', out, err)


def db_connect(config):
  conn = connect(
      host=config['host'],
      user=config['user'],
      passwd=config['pass'],
      db=config['s_db'])
  cursor = conn.cursor()
  return (conn,cursor)


def _get_start_date():
  now = datetime.utcnow()
  return (now, (now - timedelta(days=DAYS_TO_FETCH)))
