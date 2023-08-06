import os
import sys
import threading
import datetime
from tdsl import *
from tdsl.dinj import __borg_cls__, __borg_lex__, Lexicon
from tdsl.server.api import *
from tdsl import orm
from tdsl import codify


class StateCheck(threading.Thread):

	"""
	thread to continue examining a filepath
	until it is 'ripe' and ready for processing.
	when ripe, the callback method is called,
	passing the filepath to the next process
	"""

	def __init__(self, callbk_f, *args, **kwds):
		tmstmp = simple_timestamp(datetime.datetime.now())
		threading.Thread.__init__(self, name='RipeCheck_%s'%tmstmp)


class ApplicationRuntimeBorg:

	__monostate = None

	def __init__(self, opts=None):

		print(f'. ApplicationRuntimeBorg.__init__() opts {opts}')
		if not ApplicationRuntimeBorg.__monostate:

			if opts is None:
				raise Exception("Runtime options can not be None if ARB is not initialized")

			ApplicationRuntimeBorg.__monostate = self.__dict__

			self.__opts = opts
			self.__config = Lexicon(parsable=self.__opts.CONFIG)

			app_kseq = codify.get_app_kseq(
				int(self.__config.App.AppId), codify.get_master_kseq())
			d = dict(self.__config.App.items())
			d['AppKeySeq'] = app_kseq
			d['FullConfigPath'] = os.path.abspath(self.__opts.CONFIG)
			self.__app_config = __borg_cls__('AppConfig')(**d)

			self.__model_schema_config = __borg_lex__('ModelConfig')(parsable=self.__config.Resources.Schema)

			# print(f'. calling import_config_for_xsqlalchemy()')
			# xsqlalchemy.import_config_for_xsqlalchemy()
			self.__models = import_models(self.__config.Resources.Models)

			print(f'. instantiating SQLAlchemySessionFactory in ARB')
			model_list = [v for k, v in self.__models.__dict__.items() if k in self.__models.__all__]
			orm.SQLAlchemySessionFactory(
				base=self.__models.Base if 'Base' in self.__models.__dict__ else None,
				reflbase=self.__models.ReflBase if 'ReflBase' in self.__models.__dict__ else None,
				create_all=self.__config.Resources.Database.CreateTables,
				reflect=True,
				models=model_list,
				models_module=self.__models,
				max_overflow=self.__config.Resources.ORM.MaxOverflow,
				pool_size=self.__config.Resources.ORM.PoolSize,
				echo=self.__config.Resources.ORM.Echo,
				convert_unicode=self.__config.Resources.ORM.ConvertUnicode,
				user=self.__config.Resources.Database.User,
				psswd=self.__config.Resources.Database.Password,
				host=self.__config.Resources.Database.Host,
				port=self.__config.Resources.Database.Port,
				db=self.__config.Resources.Database.Schema)

			if self.__config.Resources.Database.CreateTables:
				orm.ModelSqlAdditions(self.__model_schema_config, self.__models).execute()
				orm.SqlAdditions(self.__model_schema_config, self.__models).execute()

		else:
			self.__dict__ = ApplicationRuntimeBorg.__monostate

	@memoize_exp(expiration=30)
	def get_app_config(self):
		return self.__app_config

	@memoize_exp(expiration=30)
	def get_dinj_config(self):
		return Lexicon(parsable=self.__app_config.FullConfigPath)

	def get_models(self):
		print(f'. ApplicationRuntimeBorg.get_models called')
		return self.__models

	def get_session(self):
		return orm.SQLAlchemySessionFactory().Session

	def get_authenticated_db_user(self, email_address):

		U = ~(self.__models.User)
		session = orm.SQLAlchemySessionFactory().Session
		user = session.query(U).filter(U.email_address==email_address).first()
		print(f'. get_authenticated_db_user user {user}')

		if user:
			utl_lut = self.lut_fctry(model=self.__models.UserTypeLookup, session=session)
			utl_names = [utl_lut.get_name(ut.user_type_id) for ut in user.user_types]
			print(f'. utl_names user {utl_names}')
			print(f'. ugs {user.user_groups}')

			# TODO: use this function to handle rbac of groups and types granularity
			# user, user_type_names, user_type_lookup = (
			# 	get_current_rbac_user(email_address,
			# 		accept_user_type_names=[
			# 			'super_user',
			# 			'user'
			# 		],
			# 		session=session
			# 	)
			# )
			# print(f'. rbac user {user}')

		session.close()
		return self.__models.User(entity=user) if user else None


	@memoize_exp(expiration=5)
	def lut_fctry(self, model, session=None):
		return orm.LutValues(model=model, session=session)









