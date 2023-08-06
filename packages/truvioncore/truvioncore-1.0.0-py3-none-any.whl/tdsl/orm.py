# print(f". loading {__name__}")
import os
import sys
import re
import time
import traceback
import inspect as inspect_
import isodate
import arrow
from enum import Enum
import random
import string
import datetime
import decimal
import json
import logging
import pprint
from collections import *
import uuid
import importlib
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.types import *
# from sqlalchemy.dialects.postgresql import *
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import *
from sqlalchemy.sql.ddl import DDL
from sqlalchemy import event
from sqlalchemy.exc import *
from sqlalchemy.ext.mutable import MutableDict

from mako.template import Template

from tdsl import *
from tdsl import dinj
from tdsl.dinj import *
from tdsl.codify import *
from tdsl.express import *
from tdsl import sql as pyaella_sql

from logging.handlers import RotatingFileHandler

log = logging.getLogger(f'{__name__+str(uuid.uuid4())}')
log.setLevel(logging.DEBUG)
os.makedirs('log', exist_ok=True)
# fh = logging.FileHandler(__name__+'.log')
fh = RotatingFileHandler(os.path.join('log', __name__ + '.log'), mode='a', maxBytes=1024 * 5, backupCount=0)
fh.setLevel(logging.DEBUG)
frmttr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmttr)
log.addHandler(fh)


try:
	runtime = dinj.Runtime()
except:
	# allow docs
	pass


__all__ = [
	'Base',
	'ReflBase',
	'create_default_tablename',
	'gen_date_for_partition',
	'gen_date_with_limits_for_partition',
	'gen_prev_frmt_date_from_iso',
	'to_column_name',
	'lut_fctry',
	'retrieve_lut_values',
	'LutValues',
	'DaysOfTheWeek',
	'PyaellaDataModelMetaclass',
	'PyaellaReflectiveModelMetaclass',
	'PyaellaDataModel',
	'PyaellaSQLAlchemyBase',
	'QueryPlan',
	'entify',
	'iter_entities',
	'collect_entities',
	'model_from_repr_str',
	'make_xrossable_dict',
	'FieldDef',
	'make_f',
	'EmpytPyaellaBase',
	'SQLAlchemySessionFactory',
	'ModelSqlAdditions',
	'SqlAdditions'
]

SIMPLE_TYPES = (int, int, float, bool, dict, str)

class DaysOfTheWeek(Enum):

	# ISO
	MONDAY = 0
	TUESDAY = 1
	WEDNESDAY = 2
	THURSDAY = 3
	FRIDAY = 4
	SATURDAY = 5
	SUNDAY = 6


# def import_decl_base_from_models(models_module):
# 	global DECL_BASE
# 	DECL_BASE = __import__(models_module, fromlist=['Base'])
# 	print(f'. import_models Imported models {models_module}')
# 	return DECL_BASE


def to_column_name(col):
	return str(col).lower().strip().replace(' ', '_').replace('#', 'num')\
		.replace('/', '_').replace('(', '').replace(')', '').replace("&", "")


@memoize
def lut_fctry(model, session=None):
	# print(f'. lut_fctry called, {model}')
	return LutValues(model=model, session=session)


def gen_date_for_partition(now=None):
	"""
	TODO: Deprecate
	Generate a date, formated for partition ranges. Uses padded
	month for correct range limits ie. 05 intead of 5
	"""

	now = datetime.datetime.now() if not now else now
	limit_from = f'{now.year}-{"%02d" % now.month}-01'
	limit_to = f'{now.year}-{"%02d" % (now.month+1)}-01'
	partition_key = f'{now.year}-{"%02d" % now.month}'
	# print(str(f'{now.year}-{"%02d" % now.month}-{now.day}'))
	return str(f'{now.year}-{"%02d" % now.month}-{now.day}')


def gen_date_with_limits_for_partition(now=None):
	"""
	Generate limits and dates, formated for partition ranges. Uses padded
	month for correct range limits ie. 05 intead of 5
	"""
	now = datetime.datetime.now() if not now else now
	return dict(
		limit_from = f'{now.year}-{"%02d" % now.month}-01',
		limit_to = f'{now.year}-{"%02d" % (now.month+1)}-01',
		partition_key = f'{now.year}-{"%02d" % now.month}',
		date_str = str(f'{now.year}-{"%02d" % now.month}-{now.day}')
	)


def gen_prev_frmt_date_from_iso(shift_week_amount, shift_weekday_enum, now=None):
	""" returns formatted shifted date, ie... 2021-08-01 """
	now = arrow.now() if not now else now
	# TODO: create arrow from naive
	then = now
	# shift to next monday, increase by 1 if shift_week_amount is neg
	if shift_week_amount < 0:
		then = then.shift(weekday=0).shift(weeks=shift_week_amount-1, weekday=shift_weekday_enum)
	else:
		then = then.shift(weeks=shift_week_amount, weekday=shift_weekday_enum)
	# today_wkday = now_iso.weekday
	# print(f'. today_wkday {today_wkday}')
	# shift_days = now_iso.weekday - shift_weekday_enum
	# print(f'. shift_days {shift_days}')
	# then = then.shift(days=+shift_days)
	# print(f'. then {then}')
	# then = then.shift(weeks=+shift_week_amount).naive
	# print(f'. then {then}')
	return f'{then.year}-{"%02d" % then.month}-{"%02d" % then.day}'


class MockAnnotations(object):

	id_: int
	string_: str
	date_: datetime

	def __init(self, id_: int, string_: str, date_: datetime):

		self.id_ = id_
		self.string_ = string_
		self.date_ = date_


column_types_map = {
    "String": str,
    "Integer": int,
    "BigInteger": int,
    "Numeric": float,
    "Decimal": float,
}


def get_column_attribute_type(column_string):

	column_string = column_string.rstrip().lstrip()
	s = ""
	cnt = column_string.count(",")
	match cnt:
		case 0:
			s = column_string[column_string.index("(") + 1 : column_string.find(")")]
		case _ if cnt >= 1:
			s = column_string[column_string.index("(") + 1 : column_string.find(",")]
		case _:
			print(cnt)
			raise Exception("Column definition not recognized")

	if "(" in s:
		s = s[: s.index("(") :]

	return column_types_map[s] if s in column_types_map else str


class LutValues(object):
	def __init__(self, model=None, data=None, session=None):
		# print(f'. instantiating LutValues {model}, {session}')
		self._model = model
		self._data = data if data else retrieve_lut_values(model, session=session)

	@memoize
	def get_name(self, id_):
		return self._data[id_][0]

	@memoize
	def get_display_name(self, id_=None, name=None):
		x = None
		try:
			if id_:
				x = self._data[id_][1]
			else:
				x = self._data[self._data['id_for_name'][name]][1]
		except:
			pass
		return x if x not in ('Not Set', None) else None

	@memoize
	def get_description(self, id_=None, name=None):
		if id_:
			return self._data[id_][2]
		elif name:
			return self._data[self._data['id_for_name'][name]][2]

	@memoize
	def get_id(self, name):
		if self._data:
			return self._data['id_for_name'][name] if name in self._data['id_for_name'] else None
		# print(f'. get_id None _data {self._data} for {name} model {self._model}')
		return None

	@memoize
	def get_id_for_display_name(self, display_name):
		display_name = display_name.strip()
		return self._data['id_for_display_name'][display_name]      \
			if display_name in self._data['id_for_display_name']    \
			else None

	@memoize
	def get_all_ids(self):
		for k in self._data:
			if k not in ['id_order', 'name_order', 'id_for_name', 'id_for_display_name']:
				yield k

	@memoize
	def get_all_names(self):
		return self._data['id_for_name'].keys()

	def get_all_display_names(self):
		for k in self._data:
			if k not in ['id_order', 'name_order', 'id_for_name', 'id_for_display_name']:
				yield self._data[k][1]

	def get_id_display_name_pairs(self):
		for k in self._data:
			if k not in ['id_order', 'name_order', 'id_for_name', 'id_for_display_name']:
				yield self.get_id(self._data[k][0]), self._data[k][1]

	def to_dict(self):
		d = []
		for id_ in self._data['id_order']:
			row = [id_]
			row.extend(list(self._data[id_]))
			d.append(tuple(row))
		return d

	def __call__(self, val):
		# print(f'. LutValues __call__ {val} {caller_name()}')
		""" if val is int, return name and vs vrs"""
		if type(val)==int:
			return self.get_name(val)
		elif type(val) in [str]:
			return self.get_id(val)
		raise TypeError(str(val))

	def __pos__(self):
		return self.to_dict()

	def __getattr__(self, item):
		# print(f'. __getattr__ {self}, {item} {caller_name()}')
		return self._data['id_for_name'][item.lower()]


@memoize_exp(expiration=60*5)
def retrieve_lut_values(lut_model, session):
	# print(f'. retrieve_lut_values called {lut_model}')
	# print(dir(inspect_))
	# curframe = inspect_.currentframe()
	# calframe = inspect_.getouterframes(curframe, 2)
	# print('caller name:', calframe[1][3])
	# for frameinfo in calframe:
	# 	print(f'. ---- {frameinfo}')

	try:
		# session = get_session() if not session else session
		q = session.query(~lut_model)
		rp = q.all()
		result = {'id_order':[], 'id_for_name':OrderedDict(), 'id_for_display_name':OrderedDict()}
		pk = 'id'
		if not hasattr(rp[0], 'id'):
			ent = lut_model(entity=rp[0])
			pk = ent.PrimaryKeyName
		for row in rp:
			pkval = getattr(row, pk)
			result[pkval] = (row.name, row.display_name, row.description,)
			result['id_order'].append(pkval)
			result['id_for_name'][row.name] = row.id
			result['id_for_display_name'][row.display_name] = row.id
		result['id_order'].sort()
		result['name_order'] = [result[id_] for id_ in result['id_order']]
		# print(f'. retrieve_lut_values returning {result}')
		return result
	except:
		print(traceback.format_exc())
		log.debug(traceback.format_exc())
	finally:
		try:
			pass
			#print(f'. should close? session in retrieve_lut_values')
			# session.close()
		except:
			pass

class PyaellaDataModelMetaclass(type):
	""" """

	def __new__(meta, classname, bases, classDict, *, partition_by=None):
		"""
		postgres partitions: https://alexey-soshin.medium.com/dealing-with-partitions-in-postgres-11-fa9cc5ecf466
		"""

		#. PyaellaDataModelMetaclass.__init__ classname BackgroundEventStatusHistory bases (<class 'dsl.orm.PyaellaDataModel'>,) classDict {'__module__': 'Kasayama.domain', '__qualname__': 'BackgroundEventStatusHistory', '__doc__': '\n\tAn BackgroundEvent tracks the state of an background event.\n\t', '__init__': <function BackgroundEventStatusHistory.__init__ at 0x10711a5e0>}

		#print(f'. PyaellaDataModelMetaclass.__init__ classname {classname} bases {bases} classDict {classDict} ')


		# Support dynamic partitioning
		@classmethod
		def get_partition_name(cls_, key):
			# 'measures' -> 'measures_2020' (customise as needed)
			print(f'. get_partition_name {key}')
			return f'{cls_.__tablename__}_{key.replace("-", "_").lower()}'

		@classmethod
		def create_partition(cls_, key=None, limit_from=None, limit_to=None, engine=None):
			"""
			"""

			print (f'. create_partition() key {key}, limit_to {limit_to}, limit_from {limit_from}, {cls_.partitions}')

			if key not in cls_.partitions:

				Partition = type(
					f'{classname}{key.replace("-", "_")}',  # Class name, only used internally
					(~cls_).__bases__,
					{'__tablename__': cls_.get_partition_name(key)}
				)

				Partition.__table__.add_is_dependent_on((~cls_).__table__)

				if limit_from != None and limit_to != None:
					ddl_clause = f"""
							ALTER TABLE {(~cls_).__tablename__}
							ATTACH PARTITION {Partition.__tablename__}
							FOR VALUES FROM ('{limit_from}') TO ('{limit_to}');
							"""
				else:
					ddl_clause = f"""
							ALTER TABLE {(~cls_).__tablename__}
							ATTACH PARTITION {Partition.__tablename__}
							FOR VALUES IN ('{key}');
							"""

				# print(f'. DDL Clause {ddl_clause} for Partition.__table__ {Partition.__table__} {Partition.__tablename__}')

				event.listen(
					Partition.__table__,
					'after_create',
					DDL(
						# TODO: More non-year ranges, modify the FROM and TO below, etc...
						ddl_clause
						# f"""
						# ALTER TABLE {(~cls_).__tablename__}
						# ATTACH PARTITION {Partition.__tablename__}
						# FOR VALUES FROM ('{limit_from}') TO ('{limit_to}');
						# """
					)
				)

				# Example
				# Partition = Measure.create_partition(2020)
				# if not engine.dialect.has_table(Partition.__table__.name):
				# 	Partition.__table__.create(bind=engine)
				# print(f'. Checking to see if Table is already defined {Partition.__table__.name}')

				try:
					if not engine.dialect.has_table(engine.connect(), Partition.__tablename__):
						Partition.__table__.create(bind=engine)
						print(f'. created Partition {Partition.__tablename__}')
					cls_.partitions[key] = Partition
				except Exception as hell:
					print(f'. Caught exception checking || creating table {hell}')
					raise hell

			return cls_.partitions[key]

		schemafp = os.path.abspath('lex.yaml')
		sch = get_lexical_tokens('lex.yaml') \
			if os.path.exists('lex.yaml') \
			else None
		if not sch:
			# using a shared state config
			# will only work if its been initialised
			# before this point in execution
			sch = dinj.ModelConfig()

		table_name_plural, table_name_standard = \
			create_default_tablename(classname)

		classDict['__domain__'] = sch
		classDict['__tablename__'] = table_name_plural
		classDict['__pkname__'] = '%s_id' % table_name_standard
		classDict['__relationships__'] = {}
		classDict['__annotations__'] = {}

		# TODO: refactor a bit prettier
		classDict['__pyaella_args__'] = dict(
			module_name=classDict['__module__'],
			class_name=classDict['__qualname__']
			)

		partition_rule_by_clause = None

		if sch and classname in sch:
			classDict['__schema__'] = sch[classname]
			sch_lex = classDict['__schema__']
			members = {}
			annotations = {}
			if 'Fields' in sch_lex:
				if type(sch_lex['Fields']) == list:
					# use fields as slots
					classDict['__slots__'] = \
						tuple(sch_lex['Fields'])
				else:
					# load fields from schema definition
					if (type(sch_lex['Fields']) == dict or
							isinstance(sch_lex, LexicalToken)):

						# print(f'sch_lex fields: {sch_lex["Fields"].items()}')

						members = dict([
							(k, eval(str(v)),)

							for k, v in sch_lex['Fields'].items()

							if k not in RSRVD_CLS_METH_NAMES and
								k not in RSRVD_OBJ_METH_NAMES and
								k not in RSRVD_PYAELLA_NAMES
						])

						annotations = dict([
							(k, get_column_attribute_type(v),)

							for k, v in sch_lex['Fields'].items()

							if k not in RSRVD_CLS_METH_NAMES and
								k not in RSRVD_OBJ_METH_NAMES and
								k not in RSRVD_PYAELLA_NAMES
						])


						# pprint.pprint(f'. member fields {members}')
						# pprint.pprint(members)

						# TODO: GeoAlchemy support
						for k, v in sch_lex['Fields'].items():
							if 'GeometryColumn' in v:
								classDict['__geocolumns__'] = True
								members[k] = declared_attr(
									make_f(k, v))

			if 'EntityMixes' in sch_lex:
				em = sch_lex['EntityMixes']
				if type(em) == list:
					for s in em:
						rindx, lindx = s.rindex('.'), s.index('.')
						if rindx != lindx:
							mn, clsn = s[:rindx], s[rindx + 1:]
							mod = None
							try:
								mod = __import__(mn, fromlist=[mn])

								# print(f'. getting mix {clsn} from mod {mod} {mod.__dict__.keys()}')
								mix_cls = mod.__dict__[clsn]
								# print(f'. setting EntityMix {mix_cls} in {classname}')
								classDict['__pyaella_args__'] \
									.setdefault('entity_mixes', []).append(mix_cls)
										
							except:
								print('WARNING. Mix module threw exception on __import__', traceback.format_exc())


			if 'Relations' in sch_lex:
				# print(f'. Processing Relations. Metadata - ')
				if (type(sch_lex['Relations']) == dict or
						isinstance(sch_lex, LexicalToken)):
					for attr, attrval in \
							sch_lex['Relations'].items():
						# print(f'. Relations attr: {attr} for attrval: {attrval}')
						if attrval.startswith('relationship'):
							# print(f'. starts with relationship')
							classDict['__relationships__'][attr] = attrval
							members[attr] = declared_attr(make_f(attr, attrval))
						else:
							# print(f'. DECL ATTR {attr} {attrval}')
							# TODO: support DECL BASE from config injection
							members[attr] = declared_attr(
								make_f(attr, attrval))
							# if attr == 'property_loan_id_seq':
							# 	print(f'. NON RELATION SHIP: {attrval} {type(members[attr])}')

			if 'Rules' in sch_lex:
				if 'Unique' in sch_lex.Rules:
					classDict['__unique_fields__'] = sch_lex.Rules.Unique
				if 'Partition' in sch_lex.Rules:
					# print(f'. Partition Rule Found: {sch_lex.Rules.Partition.Field} by: {sch_lex.Rules.Partition.By}, with partition_by kwd {partition_by}')
					classDict['__partition_by__'] = sch_lex.Rules.Partition.Field
					if partition_by is not None and partition_by != sch_lex.Rules.Partition:
						raise Exception(f'Partition By {partition_by} does not match Lex {sch_lex.Rules.Partition}')
					partition_by = sch_lex.Rules.Partition.Field
					partition_rule_by_clause = sch_lex.Rules.Partition.By

			# TODO: more inheritence support someday?
			proxy_base = (object,)

			classDict['__annotations__'] = annotations

			pprint.pprint(classDict['__annotations__'])

			# print(f'.... 1 setting __clz_proxy {classname} {proxy_base} {members}')
			classDict['__clz_proxy__'] = type(classname + 'Proxy', proxy_base, members)

		classDict.update(
			{
				'partitions': {},
				'partitioned_by': partition_by,
				'get_partition_name': get_partition_name,
				'create_partition': create_partition
			}
		)
		if partition_by is not None:

			# TODO: More non-RANGE partition support, modifying the `postgresql_partition_by` key below
			ppb = f'RANGE({partition_by})'
			if partition_rule_by_clause == 'LIST':
				ppb = f'LIST({partition_by})'

			classDict.update(
				{
					'__table_args__': {
						**classDict.get('__table_args__', {}),
						**dict(postgresql_partition_by=ppb)
					},
				}
			)

		# print(f'. Returning new type from: {meta} named: {classname} with: {bases} members: {classDict}')
		return type.__new__(
			meta,
			classname,
			# (bases[-1],) if bases else (), # only use last base
			bases,
			classDict
		)

	def __invert__(self):
		# print(f'. PyaellaDataModelMetaclass __invert__ called {self.__decl_class__}')
		return self.__decl_class__

	def __pow__(self, data):
		return self.unserialise(data)

	def __xor__(self, other):
		pass
		# print(f'. __xor__ called {other}')


class PyaellaReflectiveModelMetaclass(type):
	""" """

	def __new__(meta, classname, bases, classDict):
		""" """

		print(f'PyaellaReflectiveModelMetaclass.__new__ called {classname} {classDict}')

		schemafp = os.path.abspath('lex.yaml')
		sch = get_lexical_tokens('lex.yaml') \
			if os.path.exists('lex.yaml') \
			else None
		if not sch:
			sch = dinj.ModelConfig()

		table_name_plural, table_name_standard = \
			create_default_tablename(classname)

		print(f'. PyaellaReflectiveModelMetaclass table names {table_name_plural} {table_name_standard}')

		classDict['__domain__'] = sch
		classDict['__schema__'] = None
		classDict['__tablename__'] = table_name_plural
		classDict['__pkname__'] = '%s_id' % table_name_standard

		members = {
			'__tablename__': table_name_plural
		}

		print(f'.... 1 setting __clz_proxy {classname} {members}')
		classDict['__clz_proxy__'] = type(classname + 'Proxy', (object,), members)

		return type.__new__(
			meta,
			classname,
			(bases[0],),
			classDict
		)

	def __invert__(self):
		# print('. PyaellaReflectiveModelMetaclass invert called')
		return self.__decl_class__


class PyaellaDataModel(object):
	"""
	ssf = SQLAlchemySessionFactory(
		DeclBase, user='mat', psswd='DUdo15$%',
		host='localhost', db='kohigaku'
	)

	sssn = ssf.Session

	res = sssn.query(~PropertyLoan).filter('id=1').all()

	u = User(
		user_name = 'mat',
		email_address = 'mbrown@entrust-funding.com'
	)

	sssn.add(~u)
	sssn.commit()

	res = sssn.query(~User).filter("user_name='mat'").all()
	for row in res:
		print row.__class__
		print row.email_address
		u = User(row)
		print type(u)

	"""

	__slots__ = ()
	__decl_class__ = None

	def __init__(self, entity=None, base=None, **kw):
		"""
		self, entity=None, base=None, **kw
		"""

		# print(f'PyaellaDataModel.__init__ called {entity} {base}, {kw}')
		self.get_table_args()
		if entity:
			# print(f'Entity is _dao')
			self._dao = entity
		else:
			# print(f'__slots__ {self.__slots__}')
			if len(self.__slots__) == 0:
				if base:
					# print(f'has base {base} {self.__class__.__name__ in base._decl_class_registry}')
					self.__decl_base = base

					# debug_table_args = self.get_table_args()
					# print(f'. debug_table_args {debug_table_args}')
					# print(f'. debug base {base}')
					# print(f'. base._decl class registry {base._decl_class_registry}')
					# print(f'. creating dao class {self.__class__} base: {base}')

					# for k,v in base._decl_class_registry.items():
					# 	print(f'. {self.__class__.__name__} base._decl_class_registry value {k,v} {k in base._decl_class_registry} {k==self.__class__.__name__}')
					# print(f'. classname {self.__class__.__name__} {self.__class__.__name__ in base._decl_class_registry}')

					self._dao = \
						base._decl_class_registry[self.__class__.__name__]() \
							if self.__class__.__name__ in base._decl_class_registry \
							else type(
									self.__class__.__name__,
									(self.__clz_proxy__, base,),
									self.get_table_args(pyaella_args=self.__pyaella_args__) or {}
								)()  # instantiate

					#print(f'self._dao new {self._dao} {type(self._dao)}')

				else:
					#print(f'no base, creating dao {self.__class__.__name__}')
					self._dao = type(
						self.__class__.__name__,
						(self.__clz_proxy__, (object,),),
						self.get_table_args(pyaella_args=self.__pyaella_args__) or {}
					)()  # instantiate

				self.__class__.__decl_class__ = self._dao.__class__

			else:
				# print(f'__slots__ werent 0')
				for s in self.__slots__:
					# print(f'slot member {s}')
					pass

		for k, v in kw.items():
			setattr(self, k, v)

		if hasattr(self, 'mixin'):
			if 'entity_mixes' in self.__pyaella_args__:
				for em in self.__pyaella_args__['entity_mixes']:
					self.mixin(em)


	@classmethod
	def get_table_args(cls, pyaella_args=None):


		# print(f'. get_table_args {cls.__dict__.keys()}')

		try:
			# TODO: check to see if __table_args__ is
			# ever created first, and masking __table_args__ for uniques
			if '__table_args__' in cls.__dict__:
				# print(f"get_table_args __table_args__ in cls: {cls.__dict__['__table_args__']}")
				return dict(
					__pyaella_args__=pyaella_args,
					__table_args__=cls.__dict__['__table_args__']
				)

			if '__unique_fields__' in cls.__dict__:
				# print(f"get_table_args __table_args__ for unique in cls: {cls.__dict__['__unique_fields__']}")
				# d = dict(__table_args__=(UniqueConstraint(*cls.__dict__['__unique_fields__']),))
				# print(f'd: {d}')
				return dict (
					__pyaella_args__=pyaella_args,
					__table_args__=(UniqueConstraint(*cls.__dict__['__unique_fields__']),)
				)

		except Exception as hell:
			print('Exception in get_table_args', hell)
			raise hell

	@classmethod
	def load(cls, ident, session=None, eager=False):
		ident_attr = 'id' if type(ident) in [int, int] else 'key'
		if session:
			entity = cls()
			q = session.query(~cls).filter(getattr(~cls, ident_attr) == ident)
			if eager:
				rels = [x for x in entity.Relations if x]
				if rels:
					for rel in rels:
						# TODO: required xcross table not null?
						# q = q.join(getattr(~cls, rel))
						# q = q.options(contains_eager(getattr(~cls, rel)))
						q = q.options(joinedload(rel))

			## TODO: AttributeError: 'NoneType' object has no attribute 'twophase'
			try:
				res = q.all()
			except:
				print(traceback.format_exc())
				print('Trying to execute query.. waiting')
				time.sleep(.5)
				res = q.all()
			if res:
				return cls(entity=res[0]) if type(res) == list else cls(entity=res)
		else:
			raise Exception('Causal session not implemented')

	@classmethod
	def find(cls, **kwds):
		if 'session' in kwds:
			session = kwds.pop('session')
			entity = cls()
			q = session.query(~cls)
			for attr, val in kwds.items():
				q = q.filter(getattr(~cls, attr) == val)
			return [cls(entity=x) for x in q.all()]
		else:
			raise Exception('Causal session not implemented')

	@classmethod
	def unserialise(cls, serialised_data):
		d = json.loads(serialised_data)
		if d['cls'] != str(cls):
			raise Exception('Class mismatch')
		state = d['state']
		if 'last_upd' in state:
			state['last_upd'] = isodate.parse_datetime(state['last_upd'])
		new_ = cls()
		for k, v in state.items():
			setattr(new_, k, v)
		return new_

	def serialise(self, srl_tmpl=None):
		""" default is JSON """
		d = self.__json__(None)
		if hasattr(self, 'last_opr'):
			d['last_opr'] = self.last_opr
		if hasattr(self, 'last_upd'):
			d['last_upd'] = self.last_upd.isoformat()
		if hasattr(self, 'last_uid'):
			d['last_uid'] = self.last_uid

		if srl_tmpl:
			# TODO: use a template to structure the output
			pass

		d = dict(
			cls=str(self.__class__),
			state=d
		)
		return json.dumps(d)

	def __rpow__(self, opr):
		srl = self.serialise(opr)
		if opr == op.id_json:
			return int(self.id), srl,

		return self.serialise(opr)

	def save(self, session=None, upsert=False):
		# print(f'. save called {upsert}')
		if session:
			try:
				# TODO: decide on whether keys
				# are worth the 2-phase creation
				session.add(~self)
				session.commit()
				dirty, key = self._gen_entity_key()
				if dirty:
					session.add(~self)
					session.commit()
					try:
						(~self).id
					except:
						pass
				return self

			except IntegrityError as ie:
				# log.debug('IntegrityError: ' + str(ie))
				try:
					session.rollback()
				except:
					# log.debug('Rollback error: ' + traceback.format_exc())
					print(traceback.format_exc())
				if upsert and self.id and int(self.id):
					m = self.load(int(self.id), session)
					if m:
						for k in self.Fields:
							val = getattr(self, k)
							if val:
								setattr(m, k, val)
					m.save(session)
					self = m
					return self
				else:
					raise ie
			except Exception as hell:
				# log.debug('Rollback hell error: ' + traceback.format_exc())
				# try:
				#     session.rollback()
				# except:
				#     print traceback.format_exc()
				raise hell
		else:
			raise Exception('Causal session not implemented')

	@property
	def AllowsPublicIdent(self):
		if hasattr(self, '_private_ident'):
			return self._private_ident
		return True

	@property
	def EntityKey(self):
		return self.key if self.key else self._dao._gen_entity_key()

	@property
	def Fields(self):
		if self.__slots__:
			return self.__slots__
		elif self.__schema__ and 'Fields' in self.__schema__:
			x = [k for k, v in self.__schema__.Fields.items()]
			x.sort()
			if self.AllowsPublicIdent:
				x.insert(0, 'key')
				if 'id' not in x:
					x.insert(0, 'id')
			return x
		else:
			if self._dao:
				# TODO: use SQLAlchemy introspection tools
				# if this is a refl model, dao will not
				# have a mapper until DeferredBase prepare()
				return self._dao.__mapper__.columns._data.keys()
		return []

	@property
	def Relations(self):
		if self.__schema__ and 'Relations' in self.__schema__:
			x = [k for k, v in self.__schema__.Relations.items()]
			x.sort()
			return x
		return []

	@property
	def Name(self):
		return self.__class__.__name__

	@property
	def Table(self):
		return self._dao.__table__

	@property
	def TableName(self):
		return self._dao.__tablename__

	@property
	def PrimaryKeyName(self):
		if self.__schema__:
			return self.__class__.__dict__['__pkname__']
		else:
			for fld in self.Fields:
				if self.field_def(fld).primary_key:
					return fld

	@memoize
	def get_rule(self, rule_name):
		if self.__schema__ and 'Rules' in self.__schema__:
			if rule_name in self.__schema__.Rules:
				return getattr(self.__schema__.Rules, rule_name)

	def field_py_type(self, field_name):
		""" """
		try:
			# TODO: must update to use SQLAlchemy introspection
			return \
				self._dao.__mapper__.columns \
					._data[field_name] \
					.type \
					.python_type
		except:
			t = self._dao.__mapper__.columns._data[field_name].type
			if type(t).__name__.startswith('ARRAY'):
				return list
			if type(t).__name__.startswith('Geometry'):
				return str

	def array_field_item_py_type(self, field_name):
		""" """
		# TODO: must update to use SQLAlchemy introspection
		return \
			self._dao.__mapper__.columns \
				._data[field_name] \
				.type \
				.item_type \
				.python_type

	def geometry_field_item_type(self, field_name):
		""" """
		# TODO: must update to use SQLAlchemy introspection
		return \
			self._dao.__mapper__.columns \
				._data[field_name] \
				.type \
				.geometry_type

	def field_sql_type(self, field_name):
		# TODO: must update to use SQLAlchemy introspection
		# print(f'. field_sql_type {self._dao.__mapper__.columns._data[field_name].type}')
		return self._dao.__mapper__.columns._data[field_name].type

	def get_fields_by_sql_type(self, field_type):
		for field in self.Fields:
			if type(self.field_sql_type(field)) == field_type:
				yield field

	@memoize
	def field_def(self, field_name):

		# TODO: must update to use SQLAlchemy introspection
		if field_name in self._dao.__mapper__.columns._data:
			c = self._dao.__mapper__.columns._data[field_name]

		# TODO: support relationships one/many, many/many, in field_def
		elif self._dao.__mapper__.relationships._data:
			raise NotImplementedError('TODO: support relationships one/many, many/many, in field_def')
		# 	c = self._dao.__mapper__.relationships._data[field_name]
		# 	print(f'. got it {c}')
		# 	print(f'{dir(c)}')

		formtype_dsp = {
			str: 'text',

			# TODO: check for old unicode?
			# unicode: 'text',

			int: 'number',
			int: 'number',
			list: 'text',
			dict: 'text',
			datetime.datetime: 'datetime',
			datetime.date: 'date',
			bool: 'checkbox'
		}
		pytype = None
		coltype = None
		formtype = None
		length = 0
		unique = None
		transform_f = None

		try:
			pytype = c.type.python_type
			coltype = c.type
			# print(f'. pytype: {pytype}, coltype{coltype}')

		except Exception as e:
			# TODO: must update to use SQLAlchemy introspection
			t = self._dao.__mapper__.columns._data[field_name].type
			if type(t).__name__.startswith('ARRAY'):
				pytype = list
				coltype = c.type.item_type.python_type

		# if type(t).__name__.startswith('Geometry'):
		#     pytype = str
		#     coltype = self.field_sql_type(field_name)
		#     transform_f = transform_wkb_to_form_text

		if field_name in ['password', 'psswd', 'passphrase']:
			formtype = 'password'
		else:
			if pytype in formtype_dsp:
				formtype = formtype_dsp[pytype]
			else:
				formtype = 'text'
			# print(f'. formtype: {formtype}')

		if hasattr(c.type, 'length'):
			length = c.type.length
		if hasattr(c, 'unique'):
			unique = c.unique

		opt_text = ''
		if not c.nullable or c.foreign_keys:
			opt_text = 'required'

		# print(f'. setting pytype: {pytype}')
		return FieldDef(
			name=field_name,
			pytype=pytype,
			coltype=coltype,
			formtype=formtype,
			opt_text=opt_text,
			unique=unique,
			length=length,
			nullable=c.nullable,
			primary_key=c.primary_key,
			foreign_keys=c.foreign_keys,
			transform_f=transform_f
		)

	@memoize
	def _has_valid_attr(self, obj, name):
		res = hasattr(obj, name) and getattr(obj, name) != None
		return res

	def to_dict(self, ignore_fields=None):
		""" """

		def get_(k):
			try:
				x = getattr(self, k)
				if type(x) == sqlalchemy.orm.attributes.InstrumentedAttribute:
					return None
				if type(x) == sqlalchemy.orm.collections.InstrumentedList:
					return None
				fd = self.field_def(k)
				if fd.transform_f:
					x = fd.transform_f(x)
				return x
			except:
				# attribute not available, such as a relationship()
				# not loaded
				return None

		if self.__slots__:
			return dict([(k, getattr(self, k),) for k in self.__slots__])
		else:
			d = {}
			if not ignore_fields:
				ignore_fields = []
			if self.__schema__:
				if (self._has_valid_attr(self, 'Fields')
						and self._has_valid_attr(self.__schema__, 'Fields')):
					d.update(dict([(k, get_(k),)
								   for k, v in self.__schema__.Fields.items()
								   if k not in ignore_fields]))
				if (self._has_valid_attr(self, 'Relations')
						and self._has_valid_attr(self.__schema__, 'Relations')):
					d.update(dict([(k, get_(k),)
								   for k, v in self.__schema__.Relations.items()
								   if k not in ignore_fields]))
				if self.AllowsPublicIdent:
					if self._has_valid_attr(self, 'key'):
						d['key'] = self.EntityKey \
							if 'key' not in ignore_fields \
							else 'NA'
					if self._has_valid_attr(self, 'id'):
						d['id'] = int(self.id) if 'id' not in ignore_fields else 'NA'
			# return d
			else:
				# no schema, is reflected model
				d.update(dict([(k, get_(k),)
							   for k in self.Fields if k not in ignore_fields]))
			return d

	def to_json(self):
		# print(f'. to_json called')
		return self.__json__(None)

	def __json__(self, request):
		d = self.to_dict()
		for f in self.get_fields_by_sql_type(Date):
			d[f] = d[f].isoformat() if (f in d and d[f]) else None
		for f in self.get_fields_by_sql_type(DateTime):
			d[f] = d[f].isoformat() if (f in d and d[f]) else None
		for f in self.get_fields_by_sql_type(TIMESTAMP):
			d[f] = d[f].isoformat() if (f in d and d[f]) else None
		
		for f in self.get_fields_by_sql_type(sqlalchemy.sql.sqltypes.Numeric):
			d[f] = float(d[f]) if (f in d and d[f]) else None

		# stick with 'aggregated' numeric types
		for f in self.get_fields_by_sql_type(decimal.Decimal):
			d[f] = float(d[f]) if (f in d and d[f]) else None
		
		# for f in self.get_fields_by_sql_type(DECIMAL):
		# 	if d['curr_est_int_rate']:
		# 		print(f'. DECIMAL here {f} - {d[f]}')
		# 	d[f] = float(d[f]) if (f in d and d[f]) else None

		return d

	def __getattr__(self, name):
		""" """
		try:
			# print(f'__getattr__ called {name} : {self.__dict__}')
			return getattr(object.__getattribute__(self, '_dao'), name)
		except:
			# print(f'no __clz_proxy__ return {name}')
			return object.__getattribute__(self, name)

	def __delattr__(self, name):
		try:
			delattr(object.__getattribute__(self, '_dao'), name)
		except:
			object.__delattr__(self, name)

	def __setattr__(self, name, value):
		try:
			setattr(object.__getattribute__(self, '_dao'), name, value)
		except:
			object.__setattr__(self, name, value)

	def __invert__(self):
		# print(f'. invert {self._dao}')
		return self._dao

	def __xor__(self, other):
		if hasattr(self, "_cmp_guid_matrix"):
			return self._cmp_guid_matrix(other)
		raise Exception(f'GUID Matrix cmp not supported by {self}')


def create_default_tablename(s, do_pluralize=True):
	"""
	Python class names usually follow PEP8 and titlecase without spaces.
	This is different than typical database table names, which
	are usually lower case and can include underscores and maybe plurarity.

	There are many different opinions on naming, plurarity, etc... The default
	ETFDsl format for classes and tables names are:

		ClassName for a class
		class_names for a table

	This module function creates the default ETFDsl table name, with an
	attempt to handle plurarity... which can be very complicated.

	ETFDsl does a bit of side-effective magic if a Python class name ends
	with `Lookup`. The table name ends with an appreviation `lu`, with no
	plurarity generated.

		TableLookup -> table_lu
	"""

	parts = re.findall('[A-Z][^A-Z]*', s)
	last = parts[len(parts) - 1]
	standard = '_'.join(parts).lower()
	if last == 'Lookup':
		parts[len(parts) - 1] = 'lu'
		standard = '_'.join(parts[:len(parts) - 1]).lower()
	elif do_pluralize and not last.endswith('s'):
		# print(f"do_pluralize")
		parts[len(parts) - 1] = pluralize(last)
	return '_'.join(parts).lower(), standard


def create_default_classname_from_tablename(s, do_singularize=True):
	""" do not use, just the beginnings of the work """

	# print(f'create_default_classname_from_tablename called {s}')
	parts = s.split('_')
	last = parts[len(parts) - 1]
	if last == 'lu':
		# lookup table
		last = 'Lookup'
		pass
	elif do_singularize:
		last = singularize(last)
	parts[len(parts) - 1] = last
	return ''.join(map(str.capitalize, parts))


def make_f(f_name, to_eval):
	""" """

	def new_f(cls):
		try:
			return eval(to_eval)
		except Exception as e:
			print(traceback.format_exc())
			raise e

	new_f.__name__ = f_name
	return new_f


@memoize
def model_from_repr_str(s, model_module):
	""" """
	cls_name = s[s.rindex('.') + 1:s.rindex("'")]
	return model_module.__dict__[cls_name]


def iter_entities(result_proxy, model):
	""" """
	if result_proxy:
		for r in result_proxy:
			yield model(entity=r)



def collect_entities(result_proxy, model, map_f=None):
	""" """
	if map_f:
		return [map_f(e) for e in iter_entities(result_proxy, model)]
	return [e for e in iter_entities(result_proxy, model)]


def get_column_type(column_string):

	column_string = column_string.rstrip().lstrip()
	s = ''
	cnt = column_string.count(',')
	match cnt:
		case 0:
			s = column_string[column_string.index('(') + 1:column_string.find(')')]
		case _ if cnt > 1:
			s = column_string[column_string.index('(') + 1:column_string.find(',')]
		case _:
			raise Exception('Column definition not recognized')

	if '(' in s:
		s = s[:s.index('('):]

	return s


# TODO: move into required module
# @memoize
# def transform_wkb_to_form_text(data):
#     if data is not None and data is not '':
#         return load_wkb(str(data).decode('hex')).to_wkt()
#     return ''


def make_xrossable_dict(xmodel_name, *xrossables):
	""" """
	x = {}
	x[xmodel_name] = {}
	for entity in xrossables:
		x[xmodel_name][entity.Name] = entity.__json__(None)
	return x


def unpack(result_proxy, *models):
	""" """
	if result_proxy:
		for r in result_proxy:
			row = []
			for i in range(0, len(models)):
				row.append(models[i](entity=r[i]))
			yield row


def collect(result_proxy, *models):
	""" """
	return [row for row in unpack(result_proxy, *models)]


def entify(query_plan=None, result_proxy=None):
	if query_plan != None:
		result = collect(query_plan.ResultProxy, *query_plan.Models)
		return result


class QueryPlan(object):
	""" QueryPlan, to organize models and queries.
		WORK IN PROGRESS. DO NOT USE.
	"""

	def __init__(self, *models, **kwds):
		""" if lgcl kwds suppiled models argument is ignored
			but models keyword is required

			example:
			qp = QueryPlan(
				logicals=[models.User, models.User],
				models=['_', aliased(~models.User, name='User2')]
			)
		"""
		if 'logicals' in kwds:
			self._mdls = kwds['logicals']
			self._daos = []
			for i in range(0, len(kwds['models'])):
				self._daos.append(
					~kwds['logicals'][i]
					if kwds['models'][i] == '_' else kwds['models'][i])
		else:
			self._mdls = models
			self._daos = [~m for m in models]  # model objects must be dsl logical models

		self._sssn = kwds['session'] if 'session' in kwds else None
		self._qry = (self._sssn.query(*self._daos)) if self._sssn else None
		self._rp = None

	@property
	def Models(self):
		return self._mdls

	@property
	def ColumnKeys(self):
		if self.Width > 1:
			return self._rp[0].keys()

	@property
	def ResultProxy(self):
		if self._rp == None:
			self._rp = self.all()
		return self._rp

	@property
	def Width(self):
		if self._rp:
			return len(self._rp[0])
		return 0

	def __getattr__(self, name):
		if name in ['filter', 'first', 'all']:
			return getattr(self._qry, name)
		return object.__getattribute__(self, name)


class ModelDef(object):
	""" """

	def __init__(self, meta_base=None, db_profile=None, **kwds):
		self._meta_base = meta_base
		self._db_profile = db_profile
		for k, v in kwds.items():
			setattr(self, k, v)

	@property
	def MetaBase(self):
		return self._meta_base

	@property
	def DbProfile(self):
		return self._db_profile


class FieldDef(object):
	def __init__(self, **kwds):
		for k, v in kwds.items():
			setattr(self, k, v)

	def get_html_presentable(self):
		d = dict()
		for k, v in self.__dict__.items():
			v = str(v).replace('<', '').replace('>', '').replace('class', '').replace("'", '')
			d[k] = v

		return FieldDef(**d)

	def __str__(self):
		return '%s' % self.__class__

	def __repr__(self):
		return \
			"Column(%(coltype)s, nullable=%(nullable)s, unique=%(unique)s, primary_key=%(primary_key)s)" % \
			{
				'coltype': self.coltype if hasattr(self, 'coltype') else None,
				'primary_key': self.primary_key \
					if hasattr(self, 'primary_key') else False,
				'nullable': self.nullable \
					if hasattr(self, 'nullable') else True,
				'unique': self.unique \
					if (hasattr(self, 'unique')) \
					else True \
					if (hasattr(self, 'primary_key') \
						and self.primary_key) \
					else False
			}


# class JsonableModel:
#     """ deprecated """
#
#     def jsonable_dict(self):
#         output = {}
#
#         # TODO: magic happening here?
#         o_dict = db.to_dict(self)
#
#         for k, v in o_dict.items():
#             if not v or isinstance(
#                     v, (int, int, float, bool, dict, str,)):
#                 output[k] = v
#             elif isinstance(v, datetime.datetime):
#                 output[k] = str(isodate.datetime_isoformat(v))
#             elif isinstance(v, datetime.date):
#                 output[k] = str(isodate.date_isoformat(v))
#             elif isinstance(v, db.GeoPt):
#                 output[k] = {'lat': v.lat, 'lon': v.lon}
#             elif isinstance(v, list):
#                 # This will need better logic but for now addresses lists of Keys
#                 output[k] = [item if type(item) == str else str(item)
#                              for item in v]
#             elif isinstance(v, JsonableModel):
#                 output[k] = v.jsonable_dict()
#                 output[k]['key'] = str(v.key())
#             else:
#                 raise ValueError('cannot encode ' + repr(k))
#         return output


class PyaellaSQLAlchemyBase(object):
	""" """

	@declared_attr
	def __tablename__(cls):
		tn, _ = create_default_tablename(cls.__name__)
		return tn

	def _gen_entity_key(self, application_id=None):
		#  print(f'PyaellaSQLAlchemyBase._gen_entity_key called {application_id}')
		if not self.id or int(self.id) < 0:
			raise Exception(
				'Entity key gen reqs a pk id > 0')

		dirty = False

		if not self.key:
			idc_code_pos = 'X'
			try:
				tn0 = self.__tablename__[0].upper()
				# print(f'tn0 {tn0}')
				if tn0 not in ['U', 'L', 'O', 'I']:
					idc_code_pos = self.__tablename__[0].upper()
			except:
				pass
			use_kseq = runtime.APP_CONFIG.AppKeySeq
			if application_id:
				use_kseq = get_app_kseq(application_id, get_master_kseq())

			idc = IdCoder(kseq=use_kseq)
			self.key = idc.encode(int(self.id), key=idc_code_pos)
			dirty = True

		# create a comparable guid matrix
		# don't override if already set.
		if (hasattr(self, 'guid_matrix') 
			and hasattr(self, 'gen_guid_matrix')
			and self.guid_matrix == None):
			
			self.guid_matrix = self.gen_guid_matrix()
			dirty = True

		return dirty, self.key,

	id = Column(Integer, primary_key=True)
	key = Column(String)
	initial_entry_by = Column(String)
	initial_entry_date = Column(
		DateTime(timezone=False),
		default=datetime.datetime.now)
	last_uid = Column(String)
	last_opr = Column(String)
	last_upd = Column(
		DateTime(timezone=False),
		default=datetime.datetime.now,
		onupdate=datetime.datetime.now)

	def __invert__(self):
		
		#print(f'. base invert called dict: {self.__dict__} type: {type(self)} dir: {dir(self)} {self.__pyaella_args__}')
		
		if self.__pyaella_args__:

			module = __import__(self.__pyaella_args__['module_name'], fromlist=[None])
			class_ = getattr(module, self.__pyaella_args__['class_name'])
			return class_(entity=self)


class EmpytPyaellaBase(object):
	pass


class SQLAlchemySessionFactory(object):
	"""Shared state session factory. """
	__shared_state = {}

	def __init__(self, base=None, reflbase=None, create_all=False,
				 reflect=True, models=None, models_module=None,
				 max_overflow=0, pool_size=10, echo=True,
				 convert_unicode=True, slave_id=None, **kwds):

		# print(f'. SQLAlchemySessionFactory.__init__() base: {base}')
		self.__dict__ = self.__shared_state
		if not models and not models_module:
			return
		if models_module:
			self._models_module = models_module
			self._models = \
				[v for k, v in models_module.__dict__.items()
				 if k in models_module.__all__]
		else:
			self._models = models

		self.__decl_base = base

		self.__connect_string = None

		if base or create_all or kwds:

			# if create_all is False, no tables, funcs, etc..
			# will be created, however, reflection will happen
			create_all = should_create_all()

			if 'create_all_override' in kwds:
				create_all = kwds['create_all_override']

			echo = echo
			if 'PYAELLA_DEBUG_ALL' in os.environ:
				if os.environ['PYAELLA_DEBUG_ALL']:
					val = os.environ['PYAELLA_DEBUG_ALL']
					if val in ['False', 'No', '0', 0]:
						echo = False
					elif val in ['True', 'Yes', '1', 1]:
						echo = True
					elif val in ['Verbose']:
						echo = 'debug'

			if 'engine' not in kwds:

				connect_string = None

				if slave_id != None:
					# get connect string for slave
					envstr = 'DATABASE_URL_SLAVE_%s' % slave_id
					if envstr in os.environ:
						connect_string = os.environ[envstr]
					else:
						raise Exception('Database Slave conninfo environment var not set')

				else:
					if 'PYAELLA_DB_PASSWORD' in os.environ:
						kwds['psswd'] = os.environ['PYAELLA_DB_PASSWORD']

					# get master conninfo from env
					if 'DATABASE_URL' in os.environ:
						connect_string = os.environ['DATABASE_URL']
					else:
						if 'port' not in kwds:
							kwds['port'] = 5432
						connect_string = 'postgresql://' + \
										 '%(user)s:%(psswd)s@%(host)s:%(port)s/%(db)s' % kwds

						self.__connect_string = connect_string

				#print('xsqlalchemy Using conninfo', connect_string)

				# create new engine
				self._engine = create_engine(
					connect_string,
					max_overflow=max_overflow,
					pool_size=pool_size,
					echo=echo,
					convert_unicode=convert_unicode)

				self._mock_engine = create_engine(
					self.__connect_string,
					max_overflow=max_overflow,
					pool_size=pool_size,
					echo=echo,
					convert_unicode=convert_unicode,
					strategy='mock',
					executor=self.dump)

			else:
				self._engine = kwds['engine']

			if create_all:
				print(f'. SQLAlchemySessionFactory create_all True. base {base}')
				base.metadata.create_all(self._engine, checkfirst=True)

			self._session_maker = sessionmaker(bind=self._engine)

		if reflbase and reflect and self._engine:
			# if there are reflected tables, must prepare engine
			reflbase.prepare(self._engine)

		self.__contextual_session = None

	@property
	def Session(self):
		
		# create a Session
		session = self._session_maker()
		# print(f'. type of session {session, type(session)}')
		return session
		
	@property
	def Engine(self):
		return self._engine

	@property
	def MockEngine(self):
		return self._mock_engine

	def dump(self, sql, *multiparams, **params):
		# print(f'. dump called {sql} {multiparams}, {params}')
		compiled = sql.compile(self._mock_engine, 
			compile_kwargs={"literal_binds": True, "render_postcompile": True})
		print(str(compiled) % compiled.params)
	

	# TODO: Cleanup model accessors

	@property
	def Models(self):
		if self._models:
			return self._models

	@property
	def ModelsModuleName(self):
		if self._models_module:
			return self._models_module.__name__

	@property
	def ModelsModule(self):
		if self._models_module:
			return self._models_module

	@property
	def DeclBase(self):
		return self.__decl_base

	def __enter__(self):
		self.__contextual_session = self.Session
		return self.__contextual_session

	def __exit__(self, type, value, traceback):
		try:
			pass
			# self.__contextual_session.close()
			# self.__contextual_session = None
		except:
			pass


class ModelSqlAdditions(object):
	""" """

	def __init__(self, model_schema, models):
		self._model_schema = model_schema
		self._models = models
		self._conn = self._open_conn()

	def _open_conn(self):
		return SQLAlchemySessionFactory().Engine.connect()

	def __del__(self):
		try:
			self._conn.close()
		except:
			pass

	def _gen_entity_keys(self, model_name, session):
		""" """
		try:
			model = self._models.__dict__[model_name]
			entity = model()
			sess = session
			result = sess.query(~model).filter((~model).key == None).all()
			if result:
				to_save = []
				for orm_obj in result:
					orm_obj._gen_entity_key()
					to_save.append(orm_obj)
				if to_save:
					try:
						for orm_obj in to_save:
							sess.add(orm_obj)
						sess.commit()
					except:
						sess.rollback()
		except:
			print(traceback.format_exc())

	def execute(self, create_all_override=False, suppress_exc=False):
		print('-- ModelSqlAdditions.execute called', create_all_override, suppress_exc)
		try:
			if not create_all_override:
				if not should_create_all():
					print('ModelSqlAdditions.execute returning without processing')
					return

			dir_ = os.path.dirname(pyaella_sql.__file__)

			# TODO: check out why borg didn't have items() and had to change to __dict__.items()

			# print(f'self._model_schema {self._model_schema}')
			models_dcgf = \
				dict([(k, v,) for k, v in self._model_schema.__dict__.items()
					  if k not in ['LEXC', 'REFLECTIVE', 'AFTER_CREATE_SQL']])

			# print('ModelSqlAdditions.execute models_dcgf', str(models_dcgf))

			session = SQLAlchemySessionFactory().Session

			# print('ModelSqlAdditions.execute session', str(session))

			for n, m in models_dcgf.items():
				print(f'-- orm ModelSqlAdditions.execute n {n}, {m} ')
				if 'Options' in m:

					allow_templated_sql = True
					# print(f'. Checking for Rules {m}')
					if 'Rules' in m:
						# print(f'. Checking for Partitions {m.Rules}')
						if 'Partition' in m.Rules:
							# print(f'. Declarative Partition not supported for Table {n} ?')
							
							# templated sql not supported for declarative partitioned tables?
							# TODO: templated sql should be added to the partitions individually
							# PostgreSQL 13 < supports BEFORE / FOR triggers on partitioned tables
							# but Azure does not.. So.. will have to wait
							allow_templated_sql = False

					if allow_templated_sql:
						model = self._models.__dict__[n]()
						for option in m.Options:
							# print(f'. Processing option {option} for {n}')
							if option is not None and option.endswith('.sql.mako'):

								# print(f'templated option {option}')
								# templated sql
								tmpl_filepath = os.path.join(dir_, option)

								tmpl = Template(filename=tmpl_filepath)

								sql_stamement = \
									tmpl.render(
										**{
											'tablename': model.__tablename__
										}
									)

								print(f'--------------> sql_stamement {sql_stamement}')

								if not suppress_exc:
									self._conn.execute(sql_stamement)
								else:
									try:
										self._conn.execute(sql_stamement)
									except:
										print(traceback.format_exc())

				if n.endswith('Lookup') and 'Values' in m:
					# print('ModelSqlAdditions.execute processing Lookup table', n, str(m))
					ins_d = {}
					model = self._models.__dict__[n]
					entity = model()
					i = 0
					for fld_name, val_lst in m.Values.items():
						for val in val_lst:
							ins_d[i] = {}
							i += 1
						break  #
					for fld_name, val_lst in m.Values.items():
						i = 0
						for val in val_lst:
							ins_d[i][fld_name] = val
							i += 1
					ins_lst = [v for k, v in ins_d.items()]

					ins = entity.Table.insert()

					if not suppress_exc:
						self._conn.execute(ins, ins_lst)
					else:
						try:
							self._conn.execute(ins, ins_lst)
							# print('Lookup Table insert executed with no suppression')
						except:
							print('Lookup Table insert exception', traceback.format_exc())

					# print(f'Lookup calling _gen_entity_keys {n}')
					self._gen_entity_keys(n, session)

				if 'SQL' in m:
					if not suppress_exc:
						self._conn.execute(m.SQL)
					else:
						try:
							self._conn.execute(m.SQL)
						except:
							print(traceback.format_exc())

					# print(f'SQL calling _gen_entity_keys {n}')
					self._gen_entity_keys(n, session)
		except:
			print(traceback.format_exc())
			# print(f'CURRENTLY LOADED MODELS {self._models.__dict__}')
			try:
				session.close()
			except:
				pass
			sys.exit(-9999)

		finally:
			try:
				session.close()
			except:
				pass
			try:
				self._conn.close()
			except:
				pass


class SqlAdditions(object):
	""" Inject SQL after creation """

	def __init__(self, model_schema, models):
		""" 
		"""
		self._model_schema = model_schema
		self._models = models
		self._conn = self._open_conn()

	def _open_conn(self):
		return SQLAlchemySessionFactory().Engine.connect()

	def execute(self, create_all_override=False, suppress_exc=False):
		try:
			if not create_all_override:
				if not should_create_all():
					return

			if 'AFTER_CREATE_SQL' in self._model_schema:
				if 'Literal' in self._model_schema.AFTER_CREATE_SQL:

					for statement in \
							self._model_schema.AFTER_CREATE_SQL.Literal.split(';'):

						statement = statement.strip()
						if len(statement):
							statement += ';'
							trans = None
							try:
								trans = self._conn.begin()
								self._conn.execute(statement)
								trans.commit()
							except Exception as hell:
								print(traceback.format_exc())
								try:
									if trans:
										trans.rollback()
										trans = None
								except:
									pass
								raise hell

		except:
			print(traceback.format_exc())
		finally:
			try:
				self._conn.close()
			except:
				pass

	def __del__(self):
		try:
			self._conn.close()
		except:
			pass


def should_create_all():
	"""  """
	if 'PYAELLA_CREATE_ALL' in os.environ:
		val = os.environ['PYAELLA_CREATE_ALL']
		print('PYAELLA_CREATE_ALL value', val, val.lower())
		if val.lower() in ['false', 'no', '0']:
			return False
		return True
	return False


Base = declarative_base(cls=PyaellaSQLAlchemyBase)


ReflBase = declarative_base(cls=DeferredReflection)