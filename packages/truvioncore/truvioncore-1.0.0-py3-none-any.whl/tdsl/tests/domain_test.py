import os
import sys
import re
import datetime
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.schema import *
from sqlalchemy.orm import *
from sqlalchemy.sql.expression import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import *
from pyramid.security import Allow, Everyone

from tdsl import *
from tdsl import dinj
from tdsl.orm import *
from tdsl import Mixable, Mix
from tdsl.xsqlalchemy import PyaellaSQLAlchemyBase, SQLAlchemySessionFactory
from tdsl.dinj import LexicalToken, BorgLexicon, __borg_lex__

Base = declarative_base(cls=PyaellaSQLAlchemyBase)
ReflBase = declarative_base(cls=DeferredReflection)

__autogen_date__ = "2021-02-11 08:17:08.799283"

__schema_file__ = os.path.join(os.path.dirname(__file__), "lex.yaml")

MODEL_SCHEMA_CONFIG = __borg_lex__('ModelConfig')(parsable=__schema_file__)

__all__ = [
	# "ApplicationDomain",
	# "Application",
	# "Group",
	# "ApplicationGroupTypeLookup",
	# "UserXGroup",
	# "UserTypeLookup",
	# "UserXUserTypeLookup",
	# "User",
	# "UserAccountFilter",
	# "UserAccount",
	# "DefaultServiceProviderFilter",
	# "ActionFunctionTypeLookup",
	# "FilterableFieldsTypeLookup",
	# "FilterFunctionTypeLookup",
	# "GlobalFilter",
	# "ServiceProvider",
]


class ApplicationDomain(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):
	"""
	An ApplicationDomain defines an arbitrary boundry or demarcation based
	on business application and/or notions respective to corporate or conglomerate
	entities. This does not specifically mean a 'domain name' but a unique identifier
	like a domain name is perfectly acceptable.

	An ApplicationDomain could span multiple servers, `clouds`, or any related topography.

	Basic premise:

	    Segment a database or a cluster for companies, domains.
	    An ApplicationDomain has to be unique within each instatianated realm.
	"""

	def __init__(self, base=Base, **kw):
		print(f'ApplicationDomain __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class Application(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):
	"""
	An Application is an application or web-app associated
	to an ApplicationDomain.
	"""

	def __init__(self, base=Base, **kw):
		print(f'Application __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class Group(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):
	"""
	The Group model defines names of Role Based Access Control, at a 'higher'
	level than a User Type as defined by UserTypeLookup. A Group is considered
	System or Database lever RBAC, such as 'SuperUser', 'Editor', 'Viewer', and
	can be applied to C.R.U.D in a UI of an application.
	"""

	def __init__(self, base=Base, **kw):
		print(f'Group __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class ApplicationGroupTypeLookup(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):
	"""
	An ApplicationGroupTypeLookup model is a LookupTable that defines
	types of application groups, a high-level segmentation of users
	"""

	def __init__(self, base=Base, **kw):
		print(f'ApplicationGroupTypeLookup __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class UserXGroup(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):
	"""
	An Association model for User and Group... ie. Which User is
	a member of which Group. These are not RDBMS users / roles
	"""

	def __init__(self, base=Base, **kw):
		print(f'UserXGroup __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class UserTypeLookup(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):

	def __init__(self, base=Base, **kw):
		print(f'UserTypeLookup __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class UserXUserTypeLookup(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):

	def __init__(self, base=Base, **kw):
		print(f'UserXUserTypeLookup __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class User(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):

	def __init__(self, base=Base, **kw):
		print(f'User __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class UserAccountFilter(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):

	def __init__(self, base=Base, **kw):
		print(f'UserAccountFilter __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class UserAccount(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):

	def __init__(self, base=Base, **kw):
		print(f'UserAccount __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class DefaultServiceProviderFilter(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):

	def __init__(self, base=Base, **kw):
		print(f'DefaultServiceProviderFilter __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class ActionFunctionTypeLookup(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):

	def __init__(self, base=Base, **kw):
		print(f'ActionFunctionTypeLookup __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class FilterableFieldsTypeLookup(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):

	def __init__(self, base=Base, **kw):
		print(f'FilterableFieldsTypeLookup __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class FilterFunctionTypeLookup(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):

	def __init__(self, base=Base, **kw):
		print(f'FilterFunctionTypeLookup __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class GlobalFilter(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):

	def __init__(self, base=Base, **kw):
		print(f'GlobalFilter __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


class ServiceProvider(PyaellaDataModel, metaclass=PyaellaDataModelMetaclass):

	def __init__(self, base=Base, **kw):
		print(f'ServiceProvider __init__ called')
		PyaellaDataModel.__init__(self, base=base, **kw)


# print(f'....calling eval {__all__}')
_ = [eval("%s()" % c) for c in __all__]
_ = None

if __name__ == "__main__":

	import sqlalchemy
	from sqlalchemy.orm import relationship, backref
	from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint
	from sqlalchemy.schema import CheckConstraint, Sequence
	from sqlalchemy import Integer, String, DateTime
	from sqlalchemy import Unicode, Text, Boolean, REAL
	from sqlalchemy.dialects import postgresql


	def dump(sql, *multiparams, **params):
		if type(sql) == str:
			print(sql)
		else:
			# add line delimiter
			s = str(sql.compile(dialect=postgresql.dialect()))
			print(f'{s.rstrip()};\n')


	__here__ = os.path.abspath(__file__)

	schp = os.path.join(os.path.dirname(__here__), 'lex.yaml')
	if not os.path.exists(schp):
		schp = os.path.join(os.path.dirname(__here__), 'schema.yaml')

	config_lex = BorgLexicon(parsable=schp)

	# print(f'....calling eval for objs {__all__}')

	objs = [eval("%s()" % c) for c in __all__]

	print('\n')
	print('Dir of objects -----------------------------------------------------')
	print('\n')
	for o in objs:
		print(str(o))
		print(dir(o))
		if hasattr(o, '_dao'):
			print(dir(o._dao))
		print('---------------------------------------------------------------#')
		print('\n')

	print('\n\n')

	print('Data model objects -------------------------------------------------')
	print('\n')
	print(objs)

	print('\n\n')

	print('SQL text -----------------------------------------------------------')

	engine = create_engine('postgresql://', strategy='mock', executor=dump)
	Base.metadata.create_all(engine, checkfirst=False)
	print('\n')
	print('-------------------------------------------------------------------#')
