import csv
import os, sys
from optparse import OptionParser
import psutil
import pandas
import uuid
import datetime

from tdsl import *
from tdsl import dinj
from tdsl.dinj import __borg_lex__, __borg_cls__, Lexicon


def parse_args(args=None):
	"""
	python ./tahoe/converters/create_application_rec_test.py -c ./dsl/tests/app_test.yaml
	"""

	usage = "usage: %prog [options] arg"
	parser = OptionParser()

	parser.add_option(
		"-c", dest="CONFIG",
		help="Absolute path to main dependency injection file")

	(options, args) = parser.parse_args()

	print(f'options {options} args {args}')
	if len(args) > 1:
		parser.error("incorrect number of arguments.")
		sys.exit(0)
	return options


OPTS = parse_args()
runtime = dinj.Runtime(opts=OPTS)

from tdsl.orm import *
from tdsl.codify import *
from tdsl.server.api import *
from Kasayama.domain import *

CONFIG = None
APP_CONFIG = None
MODEL_SCHEMA_CONFIG = None

# dependency injected models module
models = None


@memoize_exp(expiration=5)
def lut_fctry(model):
	return LutValues(model=model)


def dinj_imports():
	# xsqlalchemy.import_config_for_xsqlalchemy()
	global CONFIG
	global models
	# models = import_models(CONFIG.Resources.Models)
	models = import_models(runtime.MODEL_MODULE_NAME)


def get_session():
	return SQLAlchemySessionFactory().Session


def load_config():
	"""Inject dependencies """

	global CONFIG
	dinj_config = Lexicon(parsable=OPTS.CONFIG)
	CONFIG = dinj_config

	# MODEL_SCHEMA_CONFIG = __borg_lex__('ModelConfig')(parsable=runtime.CONFIG.Resources.Schema)


def load_session_factory():
	global models
	model_list = [v for k, v in models.__dict__.items() if k in models.__all__]
	SQLAlchemySessionFactory(
		base=models.Base if 'Base' in models.__dict__ else None,
		reflbase=models.ReflBase if 'ReflBase' in models.__dict__ else None,
		create_all=False,
		reflect=True,
		models=model_list,
		models_module=models,
		max_overflow=runtime.CONFIG.Resources.ORM.MaxOverflow,
		pool_size=runtime.CONFIG.Resources.ORM.PoolSize,
		echo=runtime.CONFIG.Resources.ORM.Echo,
		convert_unicode=runtime.CONFIG.Resources.ORM.ConvertUnicode,
		user=runtime.CONFIG.Resources.Database.User,
		psswd=runtime.CONFIG.Resources.Database.Password,
		host=runtime.CONFIG.Resources.Database.Host,
		port=runtime.CONFIG.Resources.Database.Port,
		db=runtime.CONFIG.Resources.Database.Schema)


def do_it():

	# # will create a KEY, with an UPDATE

	session = get_session()
	bes_lu = LutValues(model=BackgroundEventStatusLookup)

	print(f'BES {bes_lu}')

	print(bes_lu.get_all_names())

	print(bes_lu.REQUESTED)
	print(bes_lu.CANCELED)
	print(bes_lu.STARTED)
	print(bes_lu.FAILED)
	print(bes_lu.RESTARTED)



if __name__ == '__main__':

	load_config()
	dinj_imports()
	load_session_factory()

	do_it()

	print('done.')

