import os
import sys
import time
import json
import socket
import select
import signal
import traceback
import threading
from optparse import OptionParser
from tdsl import *
from tdsl.server.api import *
from tdsl.orm import *
from tdsl import xsqlalchemy
from tdsl.xsqlalchemy import *
from tdsl.dinj import Lexicon, BorgLexicon, __borg_lex__, __borg_cls__
from tdsl.tasks import *
from tdsl.codify import *


OPTS = None
CONFIG = None
APP_CONFIG = None
MODEL_SCHEMA_CONFIG = None
MODEL_MODULE_NAMES = None


def load_config():
	"""Inject dependencies """

	global CONFIG
	dinj_config = Lexicon(parsable=OPTS.CONFIG)
	CONFIG = dinj_config

	global APP_CONFIG
	AppConfig = __borg_cls__('AppConfig')
	app_kseq = get_app_kseq(
		int(dinj_config.App.AppId), get_master_kseq())
	d = dict(dinj_config.App.items())
	d['AppKeySeq'] = app_kseq
	d['FullConfigPath'] = os.path.abspath(OPTS.CONFIG)
	APP_CONFIG = AppConfig(**d)

	global MODEL_SCHEMA_CONFIG
	MODEL_SCHEMA_CONFIG = __borg_lex__('ModelConfig')(
		parsable=dinj_config.Resources.Schema)


def dinj_imports():
	xsqlalchemy.import_config_for_xsqlalchemy()
	global CONFIG
	global models
	models = import_models(CONFIG.Resources.Models)


def parse_args(args=None):
	"""
	Example: -c "config.yaml" < --test >
	"""

	usage = "usage: %prog [options] arg"
	parser = OptionParser()

	parser.add_option(
		"-c", dest="CONFIG",
		help="Absolute path to main dependency injection file")

	(options, args) = parser.parse_args()
	if len(args) > 1:
		parser.error("incorrect number of arguments.")
		sys.exit(0)
	return options


if __name__ == '__main__':

	OPTS = parse_args()
	runtime = dinj.Runtime(opts=OPTS)

	another = dinj.Runtime()

	print(f'{runtime==another}')
	print(f'runtime {runtime.MODEL_MODULE_NAME}')
	print(f'runtime {another.MODEL_MODULE_NAME}')

	# for k, v in MODEL_SCHEMA_CONFIG._lex.items():
	# 	print(f'_lex {k}, {v}')

	for k,v in runtime.CONFIG._lex.items():
		print(f'CONFIG {k}, {v}')

	print(f'CONFIG.Resources {runtime.CONFIG.Resources.Models}')

	DOMAIN_BASE = __import__(runtime.CONFIG.Resources.Models, fromlist=['Base'])
	Base = DOMAIN_BASE.Base

	print(f'Base from DOMAIN_BASE {Base} {type(Base)}')



