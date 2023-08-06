# import os
# import sys
# import re
# import datetime
# import traceback
#
# import sqlalchemy
# from sqlalchemy import *
# from sqlalchemy.orm import *
# from sqlalchemy.sql.expression import text
# from sqlalchemy.ext.declarative import *
#
# import mako
# from mako.template import Template
#
# from tdsl import *
# from tdsl import dinj
# from tdsl import sql as pyaella_sql
# from tdsl.codify import IdCoder, get_app_kseq, get_master_kseq
#
# CONFIG = None
#
# runtime = dinj.Runtime()
#
#
# def import_config_for_xsqlalchemy():
#     global CONFIG
#     CONFIG = dinj.AppConfig()
#
#
# def should_create_all():
#     """  """
#     if 'PYAELLA_CREATE_ALL' in os.environ:
#         val = os.environ['PYAELLA_CREATE_ALL']
#         print('PYAELLA_CREATE_ALL value', val, val.lower())
#         if val.lower() in ['false', 'no', '0']:
#             return False
#         return True
#     return False
#
#
# class EmpytPyaellaBase(object):
#     pass
#
#
# class PyaellaSQLAlchemyBase(object):
#     """ """
#
#     @declared_attr
#     def __tablename__(cls):
#         tn, _ = create_default_tablename(cls.__name__)
#         return tn
#
#     def _gen_entity_key(self, application_id=None):
#         print(f'PyaellaSQLAlchemyBase._gen_entity_key called {application_id}')
#         global CONFIG
#         if not self.id or int(self.id) < 0:
#             raise Exception(
#                 'Entity key gen reqs a pk id > 0')
#         idc_code_pos = 'X'
#         try:
#             tn0 = self.__tablename__[0].upper()
#             print(f'tn0 {tn0}')
#             if tn0 not in ['U', 'L', 'O', 'I']:
#                 idc_code_pos = self.__tablename__[0].upper()
#         except:
#             pass
#         use_kseq = CONFIG.AppKeySeq
#         if application_id:
#             use_kseq = get_app_kseq(application_id, get_master_kseq())
#
#         idc = IdCoder(kseq=use_kseq)
#         self.key = idc.encode(int(self.id), key=idc_code_pos)
#         print(f'returning key {self.key}')
#         return self.key
#
#     id = Column(Integer, primary_key=True)
#     key = Column(String)
#     initial_entry_by = Column(String)
#     initial_entry_date = Column(
#         DateTime(timezone=False),
#         default=datetime.datetime.now)
#     last_uid = Column(String)
#     last_opr = Column(String)
#     last_upd = Column(
#         DateTime(timezone=False),
#         default=datetime.datetime.now,
#         onupdate=datetime.datetime.now)
#
#
#
# class SQLAlchemySessionFactory(object):
#     """Shared state session factory. """
#     __shared_state = {}
#
#     def __init__(self, base=None, reflbase=None, create_all=False,
#                  reflect=True, models=None, models_module=None,
#                  max_overflow=0, pool_size=10, echo=True,
#                  convert_unicode=True, slave_id=None, **kwds):
#
#         print(f'. SQLAlchemySessionFactory.__init__() base: {base}')
#         self.__dict__ = self.__shared_state
#         if not models and not models_module:
#             return
#         if models_module:
#             self._models_module = models_module
#             self._models = \
#                 [v for k, v in models_module.__dict__.items()
#                  if k in models_module.__all__]
#         else:
#             self._models = models
#
#         self.__decl_base = base
#
#         if base or create_all or kwds:
#
#             # if create_all is False, no tables, funcs, etc..
#             # will be created, however, reflection will happen
#             create_all = should_create_all()
#
#             if 'create_all_override' in kwds:
#                 create_all = kwds['create_all_override']
#
#             echo = echo
#             if 'PYAELLA_DEBUG_ALL' in os.environ:
#                 if os.environ['PYAELLA_DEBUG_ALL']:
#                     val = os.environ['PYAELLA_DEBUG_ALL']
#                     if val in ['False', 'No', '0', 0]:
#                         echo = False
#                     elif val in ['True', 'Yes', '1', 1]:
#                         echo = True
#                     elif val in ['Verbose']:
#                         echo = 'debug'
#
#             if 'engine' not in kwds:
#
#                 connect_string = None
#
#                 if slave_id != None:
#                     # get connect string for slave
#                     envstr = 'DATABASE_URL_SLAVE_%s' % slave_id
#                     if envstr in os.environ:
#                         connect_string = os.environ[envstr]
#                     else:
#                         raise Exception('Database Slave conninfo environment var not set')
#
#                 else:
#                     if 'PYAELLA_DB_PASSWORD' in os.environ:
#                         kwds['psswd'] = os.environ['PYAELLA_DB_PASSWORD']
#
#                     # get master conninfo from env
#                     if 'DATABASE_URL' in os.environ:
#                         connect_string = os.environ['DATABASE_URL']
#                     else:
#                         if 'port' not in kwds:
#                             kwds['port'] = 5432
#                         connect_string = 'postgresql://' + \
#                                          '%(user)s:%(psswd)s@%(host)s:%(port)s/%(db)s' % kwds
#
#                 #print('xsqlalchemy Using conninfo', connect_string)
#
#                 # create new engine
#                 self._engine = create_engine(
#                     connect_string,
#                     max_overflow=max_overflow,
#                     pool_size=pool_size,
#                     echo=echo,
#                     convert_unicode=convert_unicode)
#
#             else:
#                 self._engine = kwds['engine']
#
#             if create_all:
#                 print(f'. SQLAlchemySessionFactory create_all True. base {base}')
#                 base.metadata.create_all(self._engine, checkfirst=True)
#
#             self._session_maker = sessionmaker(bind=self._engine)
#
#         if reflbase and reflect and self._engine:
#             # if there are reflected tables, must prepare engine
#             reflbase.prepare(self._engine)
#
#         self.__contextual_session = None
#
#     @property
#     def Session(self):
#         # create a Session
#         session = self._session_maker()
#         return session
#
#     @property
#     def Engine(self):
#         return self._engine
#
#     # TODO: Cleanup model accessors
#
#     @property
#     def Models(self):
#         if self._models:
#             return self._models
#
#     @property
#     def ModelsModuleName(self):
#         if self._models_module:
#             return self._models_module.__name__
#
#     @property
#     def ModelsModule(self):
#         if self._models_module:
#             return self._models_module
#
#     @property
#     def DeclBase(self):
#         return self.__decl_base
#
#     def __enter__(self):
#         self.__contextual_session = self.Session
#         return self.__contextual_session
#
#     def __exit__(self, type, value, traceback):
#         try:
#             pass
#             # self.__contextual_session.close()
#             # self.__contextual_session = None
#         except:
#             pass
#
#
# class ModelSqlAdditions(object):
#     """ """
#
#     def __init__(self, model_schema, models):
#         self._model_schema = model_schema
#         self._models = models
#         self._conn = self._open_conn()
#
#     def _open_conn(self):
#         return SQLAlchemySessionFactory().Engine.connect()
#
#     def __del__(self):
#         try:
#             self._conn.close()
#         except:
#             pass
#
#     def _gen_entity_keys(self, model_name, session):
#         """ """
#         try:
#             model = self._models.__dict__[model_name]
#             entity = model()
#             sess = session
#             result = sess.query(~model).filter((~model).key == None).all()
#             if result:
#                 to_save = []
#                 for orm_obj in result:
#                     orm_obj._gen_entity_key()
#                     to_save.append(orm_obj)
#                 if to_save:
#                     try:
#                         for orm_obj in to_save:
#                             sess.add(orm_obj)
#                         sess.commit()
#                     except:
#                         sess.rollback()
#         except:
#             print(traceback.format_exc())
#
#     def execute(self, create_all_override=False, suppress_exc=False):
#         print('ModelSqlAdditions.execute called', create_all_override, suppress_exc)
#         try:
#             if not create_all_override:
#                 if not should_create_all():
#                     print('ModelSqlAdditions.execute returning without processing')
#                     return
#
#             dir_ = os.path.dirname(pyaella_sql.__file__)
#
#             # TODO: check out why borg didn't have items() and had to change to __dict__.items()
#
#             print(f'self._model_schema {self._model_schema}')
#             models_dcgf = \
#                 dict([(k, v,) for k, v in self._model_schema.__dict__.items()
#                       if k not in ['LEXC', 'REFLECTIVE', 'AFTER_CREATE_SQL']])
#
#             print('ModelSqlAdditions.execute models_dcgf', str(models_dcgf))
#
#             session = SQLAlchemySessionFactory().Session
#
#             print('ModelSqlAdditions.execute session', str(session))
#
#             for n, m in models_dcgf.items():
#                 print(f'xsqlalchempy.ModelSqlAdditions.execute n {n}, {m} ')
#                 if 'Options' in m:
#
#                     allow_templated_sql = True
#                     print(f'. Checking for Rules {m}')
#                     if 'Rules' in m:
#                         print(f'. Checking for Partitions {m.Rules}')
#                         if 'Partition' in m.Rules:
#                             print(f'. Declarative Partition not supported for Table {n}')
#                             # templated sql not supported for declarative partitioned tables
#                             # TODO: templated sql should be added to the partitions individually
#                             allow_templated_sql = False
#
#                     if allow_templated_sql:
#                         model = self._models.__dict__[n]()
#                         for option in m.Options:
#                             print(f'. Processing option {option} for {n}')
#                             if option is not None and option.endswith('.sql.mako'):
#
#                                 print(f'templated option {option}')
#                                 # templated sql
#                                 tmpl_filepath = os.path.join(dir_, option)
#
#                                 tmpl = Template(filename=tmpl_filepath)
#
#                                 sql_stamement = \
#                                     tmpl.render(
#                                         **{
#                                             'tablename': model.__tablename__
#                                         }
#                                     )
#
#                                 print(sql_stamement)
#
#                                 if not suppress_exc:
#                                     self._conn.execute(sql_stamement)
#                                 else:
#                                     try:
#                                         self._conn.execute(sql_stamement)
#                                     except:
#                                         print(traceback.format_exc())
#
#                 if n.endswith('Lookup') and 'Values' in m:
#                     print('ModelSqlAdditions.execute processing Lookup table', n, str(m))
#                     ins_d = {}
#                     model = self._models.__dict__[n]
#                     entity = model()
#                     i = 0
#                     for fld_name, val_lst in m.Values.items():
#                         for val in val_lst:
#                             ins_d[i] = {}
#                             i += 1
#                         break  #
#                     for fld_name, val_lst in m.Values.items():
#                         i = 0
#                         for val in val_lst:
#                             ins_d[i][fld_name] = val
#                             i += 1
#                     ins_lst = [v for k, v in ins_d.items()]
#
#                     ins = entity.Table.insert()
#
#                     if not suppress_exc:
#                         self._conn.execute(ins, ins_lst)
#                     else:
#                         try:
#                             self._conn.execute(ins, ins_lst)
#                             print('Lookup Table insert executed with no suppression')
#                         except:
#                             print('Lookup Table insert exception', traceback.format_exc())
#
#                     print(f'Lookup calling _gen_entity_keys {n}')
#                     self._gen_entity_keys(n, session)
#
#                 if 'SQL' in m:
#                     if not suppress_exc:
#                         self._conn.execute(m.SQL)
#                     else:
#                         try:
#                             self._conn.execute(m.SQL)
#                         except:
#                             print(traceback.format_exc())
#
#                     print(f'SQL calling _gen_entity_keys {n}')
#                     self._gen_entity_keys(n, session)
#         except:
#             print(traceback.format_exc())
#             print(f'CURRENTLY LOADED MODELS {self._models.__dict__}')
#             try:
#                 session.close()
#             except:
#                 pass
#             sys.exit(-9999)
#
#         finally:
#             try:
#                 session.close()
#             except:
#                 pass
#             try:
#                 self._conn.close()
#             except:
#                 pass
#
#
# class SqlAdditions(object):
#     """ """
#
#     def __init__(self, model_schema, models):
#         self._model_schema = model_schema
#         self._models = models
#         self._conn = self._open_conn()
#
#     def _open_conn(self):
#         return SQLAlchemySessionFactory().Engine.connect()
#
#     def execute(self, create_all_override=False, suppress_exc=False):
#         try:
#             if not create_all_override:
#                 if not should_create_all():
#                     return
#
#             if 'AFTER_CREATE_SQL' in self._model_schema:
#                 if 'Literal' in self._model_schema.AFTER_CREATE_SQL:
#
#                     for statement in \
#                             self._model_schema.AFTER_CREATE_SQL.Literal.split(';'):
#
#                         statement = statement.strip()
#                         if len(statement):
#                             statement += ';'
#                             trans = None
#                             try:
#                                 trans = self._conn.begin()
#                                 self._conn.execute(statement)
#                                 trans.commit()
#                             except Exception as hell:
#                                 print(traceback.format_exc())
#                                 try:
#                                     if trans:
#                                         trans.rollback()
#                                         trans = None
#                                 except:
#                                     pass
#                                 raise hell
#
#         except:
#             print(traceback.format_exc())
#         finally:
#             try:
#                 self._conn.close()
#             except:
#                 pass
#
#     def __del__(self):
#         try:
#             self._conn.close()
#         except:
#             pass