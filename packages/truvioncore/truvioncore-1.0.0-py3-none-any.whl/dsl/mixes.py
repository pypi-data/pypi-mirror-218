__author__ = 'mat mathews'
__version__ = '0.1.0'

import os
import sys
import redis
import base64
import logging
import traceback
from hashlib import sha1, sha512
from urllib.parse import urlparse
from logging.handlers import RotatingFileHandler

from dsl import *
from dsl import dinj
from dsl.dinj import *
from dsl.codify import *
from dsl.express import *


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
os.makedirs('log', exist_ok=True)
fh = RotatingFileHandler(os.path.join('log', __name__ + '.log'), mode='a', maxBytes=1024 * 5, backupCount=0)
fh.setLevel(logging.DEBUG)
frmttr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmttr)
log.addHandler(fh)


_models = None
_redis = None


@memoize
def _get_model(name):
	global _models
	if not _models:
		_models = SQLAlchemySessionFactory().ModelsModule
	return _models.__dict__[name]


# TODO: memoize
def get_app_config():
	return dinj.AppConfig()


def get_dinj_config(app_config):
	return dinj.Lexicon(parsable=app_config.FullConfigPath)


def _get_redis_server(dinj_config):
	global _redis
	if not _redis:
		if ('RedisServer' in dinj_config.Resources or 'REDISCLOUD_URL' in os.environ):
			if 'REDISCLOUD_URL' in os.environ:
				url = urlparse(os.environ.get('REDISCLOUD_URL'))
				_redis = redis.Redis(
					host=url.hostname, port=url.port, password=url.password)
			elif dinj_config.Resources.RedisServer not in [None, '']:
				_redis = redis.Redis(dinj_config.Resources.RedisServer)
			else:
				raise Exception('No Redis server specified in ENV or Config')
	return _redis


class GlobalFilterMix(Mix):

	def post_pre_hook(self, **kwds):
		pass

	def post_final_hook(self, session, **kwds):
		try:

			ac = get_app_config()

			dconfig = get_dinj_config(ac)

			# task = Task(
			# 	target='KasayamaUpdateGlobalFilter',
			# )
			#
			# r_srv = _get_redis_server(dconfig)
			#
			# if r_srv:
			# 	data = op.json ** task
			# 	rpush_res = r_srv.rpush(
			# 		KASAYAMA_INPUT_CHANNEL, data)

		except:
			traceback.format_exc()

	def put_pre_hook(self, session, **kwds):
		try:

			ac = get_app_config()

			dconfig = get_dinj_config(ac)

			# task = Task(
			# 	target='KasayamaUpdateGlobalFilter',
			# )
			#
			# r_srv = _get_redis_server(dconfig)
			#
			# if r_srv:
			# 	data = op.json ** task
			# 	rpush_res = r_srv.rpush(
			# 		KASAYAMA_INPUT_CHANNEL, data)

		except:
			traceback.format_exc()

		return self, kwds

	def pre_delete(self, session, **kwds):
		try:

			ac = get_app_config()

			dconfig = get_dinj_config(ac)

			# task = Task(
			# 	target='KasayamaUpdateGlobalFilter',
			# )
			#
			# r_srv = _get_redis_server(dconfig)
			#
			# if r_srv:
			# 	data = op.json ** task
			# 	rpush_res = r_srv.rpush(
			# 		KASAYAMA_INPUT_CHANNEL, data)

		except:
			traceback.format_exc()

		return self, kwds













