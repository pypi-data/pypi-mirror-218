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
from sqlalchemy.exc import *
from pyramid.security import Allow, Everyone

from tdsl import *
from tdsl import dinj
from tdsl.orm import *
from tdsl import Mixable, Mix
from tdsl.dinj import LexicalToken, BorgLexicon, __borg_lex__

# Base = declarative_base(cls=PyaellaSQLAlchemyBase)
# ReflBase = declarative_base(cls=DeferredReflection)

__autogen_date__ = "2021-11-01 17:18:37.539030"

__schema_file__ = os.path.join(os.path.dirname(__file__), "lex.yaml")

MODEL_SCHEMA_CONFIG = __borg_lex__('ModelConfig')(parsable=__schema_file__)

__all__ = [
	"refltablea",
	"refltableb",
]




class refltablea(EmptyPyaellaBase, metaclass=PyaellaReflectiveModelMetaclass):
	def __init__(self, **kw):
		PyaellaDataModel.__init__(self, base=ReflBase, **kw)



class refltableb(EmptyPyaellaBase, metaclass=PyaellaReflectiveModelMetaclass):
	def __init__(self, **kw):
		PyaellaDataModel.__init__(self, base=ReflBase, **kw)






# print(f'....calling eval {__all__}')
_ = [eval("%s()"%c) for c in __all__]
_ = None

if __name__ == "__main__":

	import sqlalchemy
	from sqlalchemy.orm import relationship, backref
	from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint
	from sqlalchemy.schema import CheckConstraint, Sequence
	from sqlalchemy import Integer, String, DateTime
	from sqlalchemy import Unicode, Text, Boolean, REAL
	from sqlalchemy.dialects.postgresql import *

	def dump(sql, *multiparams, **params):
		if type(sql) == str:
			print(sql)
			print('\n\n')
		else:
			print (sql.compile(dialect=engine.dialect))

	__here__ = os.path.abspath(__file__)

	schp = os.path.join(os.path.dirname(__here__), 'lex.yaml')
	if not os.path.exists(schp):
		schp = os.path.join(os.path.dirname(__here__), 'schema.yaml')

	config_lex = BorgLexicon(parsable=schp)

	# print(f'....calling eval for objs {__all__}')

	objs = [eval("%s()"%c) for c in __all__]

	print('\n')
	print('Dir of objects -----------------------------------------------------')
	print('\n')
	for o in objs:
		print(str(o))
		print(dir(o))
		if hasattr(o, '_dao'):
			print(dir(o._dao))
		print ('---------------------------------------------------------------#')
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
