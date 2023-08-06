import unittest
import os
import time
import json
import traceback
import isodate
import datetime
import logging

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.schema import *
from sqlalchemy.orm import *
from sqlalchemy.sql.expression import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.exc import *

from tdsl import *
from tdsl import dinj
from tdsl.orm import *


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
fh = logging.FileHandler(__name__ + '.log')
fh.setLevel(logging.DEBUG)
frmttr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmttr)
log.addHandler(fh)


# happens first for ALL dependency injection
__schema_file__ = os.path.join(os.path.dirname(__file__), "lex.yaml")
MODEL_SCHEMA_CONFIG = dinj.__borg_lex__('ModelConfig')(parsable=__schema_file__)
print(f'METACLASSES TEST. MODEL_SCHEMA_CONFIG ModelConfig {dinj.ModelConfig()} MSC: {MODEL_SCHEMA_CONFIG.__dict__.items()}')


# A custom dictionary
class MemberTable(dict):

	def __init__(self):
		print(f'MemberTable.__init__ called')
		self.member_names = []

	def __setitem__(self, key, value):
		# if the key is not already defined, add to the
		# list of keys.
		if key not in self:
			self.member_names.append(key)

		# Call superclass
		dict.__setitem__(self, key, value)


# # The metaclass
# class OrderedClass(type):
#
# 	# The prepare function
# 	@classmethod
# 	def __prepare__(metacls, name, bases): # No keywords in this case
# 		print(f'OrderedClass.__prepare__ called')
# 		return MemberTable()
#
# 	# The metaclass invocation
# 	def __new__(cls, name, bases, classdict):
# 		# Note that we replace the classdict with a regular
# 		# dict before passing it to the superclass, so that we
# 		# don't continue to record member names after the class
# 		# has been created.
# 		print(f'OrderedClass.__new__ called')
# 		result = type.__new__(cls, name, bases, dict(classdict))
# 		result.member_names = classdict.member_names
# 		return result
#
#
# class MyClass(metaclass=OrderedClass):
# 	# method1 goes in array element 0
# 	def method1(self):
# 		pass
#
# 	# method2 goes in array element 1
# 	def method2(self):
# 		pass
#


Base = declarative_base(cls=PyaellaSQLAlchemyBase)
ReflBase = declarative_base(cls=DeferredReflection)


class MockDataModelMetaclass(type):

	# # The prepare function
	# @classmethod
	# def __prepare__(metacls, name, bases): # No keywords in this case
	# 	print(f'TestDataModelMetaclass.__prepare__ called')

	def __new__(meta, classname, bases, classDict):
		""" """

		print(f'MockDataModelMetaclass.__new__ called {classname} {classDict}')

		schemafp = os.path.abspath('lex.yaml')
		sch = dinj.get_lexical_tokens('lex.yaml') \
			if os.path.exists('lex.yaml') \
			else None
		if not sch:
			# using a shared state config
			# will only work if its been initialised
			# before this point in execution
			sch = dinj.ModelConfig()

		table_name_plural, table_name_standard = create_default_tablename(classname)

		classDict['__domain__'] = sch
		classDict['__tablename__'] = table_name_plural
		classDict['__pkname__'] = '%s_id' % table_name_standard
		classDict['__relationships__'] = {}

		# TODO: refactor a bit prettier
		classDict['__pyaella_args__'] = {}

		if sch and classname in sch:
			classDict['__schema__'] = sch[classname]
			sch_lex = classDict['__schema__']
			members = {}
			if 'Fields' in sch_lex:
				if type(sch_lex['Fields']) == list:
					# use fields as slots
					classDict['__slots__'] = \
						tuple(sch_lex['Fields'])
				else:
					# load fields from schema definition
					if (type(sch_lex['Fields']) == dict or
							isinstance(sch_lex, dinj.LexicalToken)):

						members = dict([
							(k, eval(str(v)),)

							for k, v in sch_lex['Fields'].items()

							if k not in RSRVD_CLS_METH_NAMES and
							   k not in RSRVD_OBJ_METH_NAMES and
							   k not in RSRVD_PYAELLA_NAMES
						])

						# deprecated GeoAlchemy 0.6 support
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
							except:
								print('WARNING. Mix module threw exception on __import__', traceback.format_exc())
							mix_cls = mod.__dict__[clsn]
							classDict['__pyaella_args__'] \
								.setdefault('entity_mixes', []).append(mix_cls)

			if 'Relations' in sch_lex:
				if (type(sch_lex['Relations']) == dict or
						isinstance(sch_lex, dinj.LexicalToken)):
					for attr, attrval in \
							sch_lex['Relations'].items():

						if attrval.startswith('relationship'):
							classDict['__relationships__'][attr] = attrval
							members[attr] = declared_attr(make_f(attr, attrval))

						else:
							members[attr] = declared_attr(
								make_f(attr, attrval))

			if 'Rules' in sch_lex:
				if 'Unique' in sch_lex.Rules:
					classDict['__unique_fields__'] = \
						sch_lex.Rules.Unique

			# TODO: more inheritence support someday?
			proxy_base = (object,)

			print(f'.... 1 setting __clz_proxy {classname} {proxy_base} {members}')
			classDict['__clz_proxy__'] = type(classname + 'Proxy', proxy_base, members)

		return type.__new__(
			meta,
			classname,
			# (bases[-1],) if bases else (), # only use last base
			bases,
			classDict
		)

	def __invert__(self):
		print(f'. __invert__ called')
		return self.__decl_class__

	def __pow__(self, data):
		print(f'. __pow__ called')
		return self.unserialise(data)

	def __xor__(self, other):
		print(f'. __xor__ called {other}')


class DataModelSuperclass(object, metaclass=MockDataModelMetaclass):
	"""
	ssf = SQLAlchemySessionFactory(
		DeclBase, user='matmathew', psswd='12345678',
		host='localhost', db='geodk'
	)

	sssn = ssf.Session

	res = sssn.query(~Droplet).filter('id=1').all()

	u = User(
		user_name = 'mateyuzo',
		email_address = 'mat@miga.me'
	)

	sssn.add(~u)
	sssn.commit()

	res = sssn.query(~User).filter("user_name='mateyuzo'").all()
	for row in res:
		print row.__class__
		print row.email_address
		u = User(row)
		print type(u)

	"""

	__slots__ = ()
	__decl_class__ = None

	def __init__(self, entity=None, base=None, **kw):
		""" """
		print(f'DataModelSuperclass.__init__ called {entity} {base}, {kw}')
		self.get_table_args()
		if entity:
			print(f'Entity is _dao')
			self._dao = entity
		else:
			print(f'__slots__ {self.__slots__}')
			if len(self.__slots__) == 0:
				if base:
					print(f'has base {base}')
					self.__decl_base = base

					print(f'base._decl class registry {base._decl_class_registry}')
					self._dao = \
						base._decl_class_registry[self.__class__.__name__]() \
							if self.__class__.__name__ in base._decl_class_registry \
							else type(
								self.__class__.__name__,
								(self.__clz_proxy__, base,),
								self.get_table_args() or {}
							)()  # instantiate

					print(f'self._dao new {self._dao}')
				else:
					print(f'no base, creating dao')
					self._dao = type(
						self.__class__.__name__,
						(self.__clz_proxy__, (object,),),
						self.get_table_args() or {}
					)()  # instantiate
				self.__class__.__decl_class__ = self._dao.__class__
			else:
				print(f'__slots__ werent 0')
				for s in self.__slots__:
					print(f'slot member {s}')

		for k, v in kw.items():
			setattr(self, k, v)

		if hasattr(self, 'mixin'):
			if 'entity_mixes' in self.__pyaella_args__:
				for em in self.__pyaella_args__['entity_mixes']:
					self.mixin(em)

	# TODO: Create interface for Geometry
	# @memoize
	# def has_geo(self):
	#     return len(list(self.get_fields_by_sql_type(Geometry))) > 0

	@classmethod
	def get_table_args(cls):
		try:
			if '__table_args__' in cls.__dict__:
				return cls.__dict__['__table_args__']
			if '__unique_fields__' in cls.__dict__:
				return {
					'__table_args__': (UniqueConstraint(*cls.__dict__['__unique_fields__']),)
				}
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
		""" default is JSON"""
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
		if session:
			try:
				# TODO: decide on whether keys
				# are worth the 2-phase creation
				session.add(~self)
				session.commit()
				self._gen_entity_key()
				session.add(~self)
				session.commit()
				try:
					(~self).id
				except:
					pass
				return self

			except IntegrityError as ie:
				log.debug('IntegrityError: ' + str(ie))
				try:
					session.rollback()
				except:
					log.debug('Rollback error: ' + traceback.format_exc())
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
				log.debug('Rollback hell error: ' + traceback.format_exc())
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
		return self._dao.__mapper__.columns._data[field_name].type

	def get_fields_by_sql_type(self, field_type):
		for field in self.Fields:
			if type(self.field_sql_type(field)) == field_type:
				yield field

	@memoize
	def field_def(self, field_name):
		# TODO: must update to use SQLAlchemy introspection
		c = self._dao.__mapper__.columns._data[field_name]
		formtype_dsp = {
			str: 'text',

			# TODO: check for old unicode?
			#unicode: 'text',

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

		if hasattr(c.type, 'length'):
			length = c.type.length
		if hasattr(c, 'unique'):
			unique = c.unique

		opt_text = ''
		if not c.nullable or c.foreign_keys:
			opt_text = 'required'

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
		return self.__json__(None)

	def __json__(self, request):
		d = self.to_dict()
		for f in self.get_fields_by_sql_type(Date):
			d[f] = d[f].isoformat() if (f in d and d[f]) else None
		for f in self.get_fields_by_sql_type(DateTime):
			d[f] = d[f].isoformat() if (f in d and d[f]) else None
		for f in self.get_fields_by_sql_type(TIMESTAMP):
			d[f] = d[f].isoformat() if (f in d and d[f]) else None
		for f in self.get_fields_by_sql_type(NUMERIC):
			d[f] = float(d[f]) if (f in d and d[f]) else None
		for f in self.get_fields_by_sql_type(DECIMAL):
			d[f] = float(d[f]) if (f in d and d[f]) else None
		return d

	def __getattr__(self, name):
		""" """
		try:
			print(f'__getattr__ called {name} : {self.__dict__}')
			return getattr(object.__getattribute__(self, '_dao'), name)
		except:
			print(f'no __clz_proxy__ return {name}')
			return object.__getattribute__(self, name)

	def __delattr__(self, name):
		try:
			delattr(object.__getattribute__(self, '_dao'), name)
		except:
			obj.__delattr__(self, name)

	def __setattr__(self, name, value):
		try:
			setattr(object.__getattribute__(self, '_dao'), name, value)
		except:
			object.__setattr__(self, name, value)

	def __invert__(self):
		print(f'. invert called')
		return self._dao

	def __xor__(self, other):
		print(f'. __xor__ called {other}')


class ApplicationDomain(DataModelSuperclass):

	def __init__(self, base=Base, metaclass=PyaellaDataModelMetaclass, **kw):
		print(f'ApplicationDomain __init__ called')
		DataModelSuperclass.__init__(self, base=base, **kw)


# class TestMetaClasses(unittest.TestCase):
# 	def test_ordered_class(self):
#
# 		oc = MyClass()
#
# 		# OrderedClass.__prepare__
# 		# called
# 		# MemberTable.__init__
# 		# called
# 		# OrderedClass.__new__
# 		# called
#
# 		self.assertEqual(True, True)
#


class TestMockDatamodel(unittest.TestCase):

	def test_mock_data(self):
		ad = ApplicationDomain(this='That')
		print(f'ApplicationDomain Obj {ad}')
		print(f'~ApplicationDomain Obj {~ad}')
		fd = ad.field_def('name')
		print(f'ApplicationDomain.field_def {fd}')
		print(repr(fd))

if __name__ == '__main__':
	unittest.main()
