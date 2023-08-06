import os
import sys
import csv
import argparse
from subprocess import call
import traceback
from tdsl.express import twk_hammer
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import JSONP
from pyramid.response import Response
import mako
from mako.template import Template

from tdsl import *
from tdsl import dinj


print(f'dbinstall.py module loaded!!! WHY?')
def parse_args(args=None):

    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--host", dest="HOST", default="localhost",
        help="HOST")

    parser.add_argument(
        "--port", dest="PORT", default=5432,
        help="PORT")

    parser.add_argument(
        "--db", dest="DATABASE",
        help="Database")

    parser.add_argument(
        "-U", dest="USER",
        help="User")

    parser.add_argument(
        "-O", dest="OWNER", default=None,
        help="Owner")

    parser.add_argument(
        "--password", dest="PASSWORD",
        help="Password")

    parser.add_argument(
        "--no-postgis", dest="NOPOSTGIS",
        action='store_true', default=False,
        help="Install PostGIS")

    parser.add_argument(
        "--only-postgis", dest="ONLYPOSTGIS",
        action='store_true', default=False,
        help="Only Install PostGIS")

    parser.add_argument(
        "--no-dsl", dest="NOPYAELLA",
        action='store_true', default=False,
        help="Install PYAELLA")

    parser.add_argument(
        "--contrib-dir", dest="CONTRIBDIR",
        help="Contrib Dir")

    parser.add_argument(
        "--appcfg", dest="CONFIG",
        help="Absolute path to App configuration file")

    # /opt/local/lib/postgresql13/bin/
    parser.add_argument(
        "--pg-bin", dest="PGBIN",
        help="Path to the postgres install bin directory")

    parser.add_argument(
        "--sslmode", dest="SSLMODE", default="notrequired",
        help="SSL mode")

    args = parser.parse_args()

    print(f'. parse_args options: {args}')
    return args


OPTS = parse_args()
print(f'. loaded OPTS {OPTS}')
runtime = dinj.Runtime(opts=OPTS)


from tdsl.server.api import *
from tdsl.server.adminviews import *
from tdsl.xsqlalchemy import *
from tdsl.auth import *
from tdsl.dinj import Lexicon, BorgLexicon, __borg_lex__, __borg_cls__
from tdsl.codify import *


CONFIG = None
APP_CONFIG = None
MODEL_SCHEMA_CONFIG = None
MODELS_MODULE_NAME = None
DATABASE_URL = None

# dsl dinj'd models module
models = None


def dinj_imports():
    print('. dinj_imports import_config_for_xsqlalchemy()')
    # import_config_for_xsqlalchemy()
    global CONFIG
    global models
    print(f'. dbinstall importing models....')
    models = import_models(CONFIG.Resources.Models)


def get_session():
    return SQLAlchemySessionFactory().Session


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
    APP_CONFIG = AppConfig(**d)

    global MODEL_SCHEMA_CONFIG
    MODEL_SCHEMA_CONFIG = __borg_lex__('ModelConfig')(
                parsable=dinj_config.Resources.Schema)

    global MODELS_MODULE_NAME
    MODELS_MODULE_NAME = dinj_config.Resources.Models

    # print(f'. load_config called MODEL_SCHEMA_CONFIG: {type(MODEL_SCHEMA_CONFIG)} {MODEL_SCHEMA_CONFIG.__dict__}')
    # for k in runtime.SCHEMA._lex.items():
    #     print(f'MODEL_SCHEMA_CONFIG K: {k}')


def load_session_factory():
    global models
    global CONFIG
    global MODEL_SCHEMA_CONFIG
    model_list = [v for k,v in models.__dict__.items() if k in models.__all__]
    print('. Creating SQLAlchemySessionFactory {models}')
    SQLAlchemySessionFactory(
        base=models.Base if 'Base' in models.__dict__ else None, 
        reflbase=models.ReflBase if 'ReflBase' in models.__dict__ else None,
        create_all=True,
        reflect=True,
        models=model_list,
        models_module=models,
        max_overflow=CONFIG.Resources.ORM.MaxOverflow,
        pool_size=CONFIG.Resources.ORM.PoolSize,
        echo=CONFIG.Resources.ORM.Echo,
        convert_unicode=CONFIG.Resources.ORM.ConvertUnicode,
        user=CONFIG.Resources.Database.User, 
        psswd=CONFIG.Resources.Database.Password, 
        host=CONFIG.Resources.Database.Host,
        port=CONFIG.Resources.Database.Port,
        db=CONFIG.Resources.Database.Schema,
        create_all_override=True)

    print(f'load_session_factory, calling ModelSqlAdditions {MODEL_SCHEMA_CONFIG} {models}')

    ModelSqlAdditions(
        MODEL_SCHEMA_CONFIG, models).execute(create_all_override=True)

    print('load_session_factory, calling ModelSqlAdditions')

    SqlAdditions(
        MODEL_SCHEMA_CONFIG, models).execute(create_all_override=True)


def examine_custom_SQL_model_cfg():
    global MODEL_SCHEMA_CONFIG
    global models
    try:
        models_dcgf = \
            dict([(k,v,) for k,v in MODEL_SCHEMA_CONFIG.items() 
                                    if k not in ['LEXC', 'REFLECTIVE', 'AFTER_CREATE_SQL']])
        for n, m in models_dcgf.items():
            if 'SQL' in m:
                print(m.SQL)
            if 'Options' in m:
                print(m.Options)
            if n.endswith('Lookup') and 'Values' in m:
                ins_d = {}
                model = models.__dict__[n]()
                i = 0
                for fld_name, val_lst in m.Values.items():
                    for val in val_lst:
                        ins_d[i] = {}
                        i += 1
                    break #
                for fld_name, val_lst in m.Values.items():
                    i = 0
                    for val in val_lst:
                        ins_d[i][fld_name] = val
                        i += 1
                ins_lst = [v for k,v in ins_d.items()]

                print('examine_custom_SQL_model_cfg ins_lst ->', ins_lst)

                ins = model.Table.insert()

                print('examine_custom_SQL_model_cfg supposedly inserted', ins)

                print(ins)
                print(ins_lst)

                print('examine_custom_SQL_model_cfg done')

    except:
        print(traceback.format_exc())


def doit():

    DATABASE_URL = None

    if OPTS.DATABASE and OPTS.DATABASE != CONFIG.Resources.Database.Schema:
        raise Exception(
            f'Database argument and App config entry do not match. Failing {OPTS.DATABASE}!= {CONFIG.Resources.Database.Schema}')

    if OPTS.USER == None or not OPTS.USER:
        if 'DATABASE_URL' not in os.environ:
            raise Exception(
                'No database connection information supplied. Failing')
        DATABASE_URL = os.environ['DATABASE_URL']

    if not DATABASE_URL:
        print(f'dropdb no database_url {DATABASE_URL}')
        try:
            print('. dropping db')
            retcode = call(
                [os.path.join(OPTS.PGBIN, 'dropdb'),
                 '-U', OPTS.USER,
                 '--host', OPTS.HOST,
                 '--port', str(OPTS.PORT),
                 OPTS.DATABASE
                 ]
            )
            print('. DROPDBQ: {retcode}')
        except:
            print(traceback.format_exc())

    if not DATABASE_URL:
        print(f'createdb no database_url {DATABASE_URL}')
        s = os.path.join(OPTS.PGBIN, 'createdb') + ' -U ' + OPTS.USER + ' -O ' + OPTS.OWNER + ' --host ' + OPTS.HOST + ' --port ' + str(OPTS.PORT) + ' ' + str(OPTS.DATABASE)
        print(s)
        try:
            retcode = call(
                [os.path.join(OPTS.PGBIN, 'createdb'),
                 '-U', OPTS.USER,
                 '-O', OPTS.OWNER,
                 '--host', OPTS.HOST,
                 '--port', str(OPTS.PORT),
                 OPTS.DATABASE
                 ]
            )
            if retcode != 0:
                print(f'{traceback.format_exc()}')
                raise Exception(
                    'Error during install %s. Stopping' % retcode)
            else:
                print(f'. CREATEDB: {retcode}')

        except:
            print(traceback.format_exc())
            sys.exit(-1)

    contrib_dir = OPTS.CONTRIBDIR if OPTS.CONTRIBDIR else ''

    # if OPTS.ONLYPOSTGIS:
    #     # install PostGIS extention
    #     for postgisSQLfile in [
    #         'postgis.sql',
    #         'postgis_comments.sql',
    #         'spatial_ref_sys.sql',
    #         'rtpostgis.sql',
    #         'raster_comments.sql',
    #         'topology.sql',
    #         'topology_comments.sql'
    #     ]:
    #         retcode = call(['psql',
    #                         '--host', OPTS.HOST,
    #                         '--port', str(OPTS.PORT),
    #                         '-d', OPTS.DATABASE,
    #                         '-U', OPTS.USER,
    #                         '-f', os.path.join(contrib_dir, postgisSQLfile)])
    #         if retcode != 0:
    #             raise Exception('Error during install %s. Stopping' % retcode)
    #
    #     sys.exit(1)

    # if not OPTS.NOPOSTGIS and not DATABASE_URL:
    #     # install PostGIS extention
    #     for postgisSQLfile in [
    #         'postgis.sql',
    #         'postgis_comments.sql',
    #         'spatial_ref_sys.sql',
    #         'rtpostgis.sql',
    #         'raster_comments.sql',
    #         'topology.sql',
    #         'topology_comments.sql'
    #     ]:
    #         retcode = call(['psql',
    #                         '--host', OPTS.HOST,
    #                         '--port', str(OPTS.PORT),
    #                         '-d', OPTS.DATABASE,
    #                         '-U', OPTS.USER,
    #                         '-f', os.path.join(contrib_dir, postgisSQLfile)])
    #         if retcode != 0:
    #             raise Exception('Error during install %s. Stopping' % retcode)

    if not OPTS.NOPYAELLA:

        def do_templated_sql(filepath, **kwds):
            tmpl = mako.template.Template(
                filename=tmpl_filepath, default_filters=['decode.utf8'])

            sql_stamement = tmpl.render(**kwds)

            print(sql_stamement)

            ofp = os.path.join(
                dir_, 'tmp', os.path.basename(tmpl_filepath.strip('.mako')))
            if not os.path.exists(os.path.dirname(ofp)):
                try:
                    os.makedirs(os.path.dirname(ofp))
                except:
                    pass
            with open(ofp, 'w') as of:
                of.write(sql_stamement)

            if not DATABASE_URL:
                retcode = call(
                    [os.path.join(OPTS.PGBIN, 'psql'),
                     '--host', OPTS.HOST,
                     '--port', str(OPTS.PORT),
                     '-d', OPTS.DATABASE,
                     '-U', OPTS.USER,
                     '-f', ofp
                     ]
                )
                if retcode != 0:
                    raise Exception(
                        'Error during install %s. Stopping' % retcode)
            else:
                retcode = call([os.path.join(OPTS.PGBIN, 'psql'), DATABASE_URL, '-f', ofp])
                if retcode != 0:
                    raise Exception(
                        'Error during install %s. Stopping' % retcode)

        try:

            from tdsl import sql as pyaella_sql
            dir_ = os.path.dirname(pyaella_sql.__file__)

            print(f'dsl sql dir {dir_}')

            for trigger in [
                'tr_standard_mod.sql.mako',
                'tr_standard_lu_mod.sql.mako',
                'tr_standard_mod_no_del.sql.mako']:

                tmpl_filepath = os.path.join(dir_, trigger)

                try:

                    tmpl = mako.template.Template(filename=tmpl_filepath)

                except Exception as e:
                    print(e)
                    print(traceback.format_exc())
                    sys.exit()

                owner = OPTS.OWNER if DATABASE_URL == None else 'postgres'

                sql_stamement = \
                    tmpl.render(
                        **{
                            'owner': owner
                        }
                    )

                print(f'pyaella_sql templated SQL creation statement {sql_stamement}')
                print(sql_stamement)

                ofp = os.path.join(
                    dir_, 'tmp', os.path.basename(tmpl_filepath.strip('.mako')))
                if not os.path.exists(os.path.dirname(ofp)):
                    try:
                        os.makedirs(os.path.dirname(ofp))
                    except:
                        pass
                with open(ofp, 'w') as of:
                    of.write(sql_stamement)

                if not DATABASE_URL:
                    retcode = call(
                        [os.path.join(OPTS.PGBIN, 'psql'),
                         '--host', OPTS.HOST,
                         '--port', str(OPTS.PORT),
                         '-d', OPTS.DATABASE,
                         '-U', OPTS.USER,
                         '-f', ofp
                         ]
                    )
                    if retcode != 0:
                        print(str(traceback.format_exc()))
                        raise Exception(
                            'Error during install %s. Stopping' % retcode)
                else:
                    retcode = call([os.path.join(OPTS.PGBIN, 'psql'), DATABASE_URL, '-f', ofp])
                    if retcode != 0:
                        raise Exception(
                            'Error during install %s. Stopping' % retcode)

            tmpl_filepath = os.path.join(dir_, 'countries.sql.mako')
            csv_file = os.path.join(dir_, 'countries.csv')

            country_data = {}
            with open(csv_file, 'r') as csvf:
                reader = csv.reader(csvf, delimiter=",")
                for row in reader:
                    for i in range(0, len(row)):
                        if "'" in row[i]:
                            row[i] = row[i].replace("'", "")
                    country_data[row[0]] = \
                        twk_hammer(
                            str(row).replace('[', '(').replace(']', ')'))

            do_templated_sql(tmpl_filepath, data=country_data)

        except:
            print(traceback.format_exc())

    dinj_imports()
    load_session_factory()


def parse_args(args=None):

    usage = "usage: %prog [options] arg"    
    parser = argparse.ArgumentParser()

    print(f'here a')

    parser.add_argument(
        "--host", dest="HOST", default="localhost",
        help="HOST")

    parser.add_argument(
        "--port", dest="PORT", default=5432,
        help="PORT")

    parser.add_argument(
        "--db", dest="DATABASE",
        help="Database")

    parser.add_argument(
        "-U", dest="USER",
        help="User")

    parser.add_argument(
        "-O", dest="OWNER", default=None,
        help="Owner")

    parser.add_argument(
        "--password", dest="PASSWORD",
        help="Password")

    parser.add_argument(
        "--no-postgis", dest="NOPOSTGIS",
        action='store_true', default=False,
        help="Install PostGIS")

    parser.add_argument(
        "--only-postgis", dest="ONLYPOSTGIS",
        action='store_true', default=False,
        help="Only Install PostGIS")

    parser.add_argument(
        "--no-dsl", dest="NOPYAELLA",
        action='store_true', default=False,
        help="Install PYAELLA")

    parser.add_argument(
        "--contrib-dir", dest="CONTRIBDIR",
        help="Contrib Dir")

    parser.add_argument(
        "--appcfg", dest="CONFIG",
        help="Absolute path to App configuration file")

    # /opt/local/lib/postgresql13/bin/
    parser.add_argument(
        "--pg-bin", dest="PGBIN",
        help="Path to the postgres install bin directory")

    parser.add_argument(
        "--sslmode", dest="SSLMODE", default="notrequired",
        help="SSL mode")

    args = parser.parse_args()

    print(f'ARGS HERE {args}')

    print(f'returning options {args}')
    return args


if __name__ == '__main__':

    print(f'dbinstall running....')

    """
    example usage - 

    python dbinstall.py 
        -U postgres -O postgres 
        --host localhost 
        --port 5432 
        --contrib-dir /opt/local/share/postgresql92/contrib/postgis-2.0/ 
        --appcfg ./tests/app_tests.yaml 
        --db pyaellatest
        
        -U postgres -O postgres --host localhost --port 5432 --appcfg ./dsl/tests/app_test.yaml --pg-bin /opt/local/lib/postgresql13/bin/ --db kohigaku
        -U ETFAdmin@etf-coolbeans -O ETFAdmin@etf-coolbeans --password=ETphoneh0me --host etf-coolbeans.postgres.database.azure.com --port 5432 --sslmode require --appcfg ./dsl/tests/app_test.yaml --pg-bin /opt/local/lib/postgresql13/bin/ --db kohigaku
    """

    load_config()

    print(f'Calling doit')

    doit()

    print('done.')