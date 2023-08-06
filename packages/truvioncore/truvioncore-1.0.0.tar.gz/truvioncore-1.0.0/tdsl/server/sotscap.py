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

import sqlalchemy
from sqlalchemy.sql import expression as sa_exp

import tdsl
from tdsl import *
from tdsl import dinj
from tdsl.codify import *

OPTS = parse_args()
runtime = dinj.Runtime(opts=OPTS)

from tdsl.orm import *
from tdsl.server.api import *

# can safely import models after runtime
from Kasayama import domain as models
from Kasayama.recordtypes.quantarium import *

BG = []


@memoize_exp(expiration=5)
def lut_fctry(model):
    return LutValues(model=model)


def get_session():
    return SQLAlchemySessionFactory().Session


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


def signal_handler(signal, frame):
	global BG
	if BG:
		for bg in BG:
			try:
				bg.shutdown()
			except:
				print(traceback.format_exc())
	sys.exit()


def parse_args(args=None):
	'''
		Example: -c "config.yaml" < --test >
	'''
	usage = "usage: %prog [options] arg"
	parser = OptionParser()

	parser.add_option(
		"-c", dest="CONFIG",
		help="Absolute path to main dependency injection file")

	parser.add_option(
		"--create-all", action='store_true',
		default=False, dest="CREATEALL", help="Create tables")

	(options, args) = parser.parse_args()
	if len(args) > 1:
		parser.error("incorrect number of arguments.")
		sys.exit(0)
	return options


if __name__ == '__main__':

	load_session_factory()

	task_list, task_list_lock = None, None


	if runtime.APP_CONFIG.AsyncFamily == "Threading":
		# use threads and no processes, locally

		task_list = TaskList(mix_ins=[DefaultTaskList])
		task_list_lock = threading.RLock()

		task_list_proctor_factory = \
			TaskListProctorFactory(
				task_list=task_list, lock=task_list_lock)


	bg_clz = []
	if('BackgroundModules' in runtime.APP_CONFIG.__dict__ and runtime.APP_CONFIG.BackgroundModules):

		for m_name in runtime.APP_CONFIG.BackgroundModules:
			m = __import__(m_name, fromlist=[m_name])
			bg_clz.extend(
				[   cls
				    for _, cls in m.__dict__.items()
				    if _ in m.__procs__
				    and (
						    hasattr(cls, 'AsyncFamily')
						    and
						    cls.AsyncFamily == runtime.APP_CONFIG.AsyncFamily
				    )
				    ]
			)

	if bg_clz:
		for bg_cls in bg_clz:
			bg_inst = bg_cls()
			bg_inst.start()
			BG.append(bg_inst)

	signal.signal(signal.SIGINT, signal_handler)
	signal.pause()

	while 1:
		time.sleep(5)
