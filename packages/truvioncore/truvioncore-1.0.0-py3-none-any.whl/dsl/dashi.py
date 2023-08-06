__author__ = "mat mathews"
__version__ = "0.1.0"

import csv
import os, sys
import io
from optparse import OptionParser
import psutil
import uuid
import datetime, time
import random
import string
from mako.template import Template
import collections
import decimal
import gzip
import zipfile
import itertools
import traceback
import multiprocessing
import logging
import json
import mako
import sqlalchemy
from sqlalchemy.sql import expression as sa_exp
from sqlalchemy.schema import CreateTable
import sqlparse
from dsl import dinj
from dsl import sql as pyaella_sql
from dsl.express import STATES_ABV
from dsl import codify


def parse_args(args=None):
    """
    Example: -c "config.yaml" < --test >
    """
    usage = "usage: %prog [options] arg"
    parser = OptionParser()

    parser.add_option(
        "-c", dest="CONFIG", help="Absolute path to main dependency injection file"
    )

    parser.add_option(
        "-r",
        dest="RUNINLINE",
        action="store_true",
        default=False,
        help="Run code before interactive",
    )

    parser.add_option(
        "--create-all",
        action="store_true",
        default=False,
        dest="CREATEALL",
        help="Create tables",
    )

    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error("incorrect number of arguments.")
        sys.exit(0)
    return options


OPTS = parse_args()
runtime = dinj.Runtime(opts=OPTS)

import dsl
from dsl import *
from dsl.codify import *
from dsl.processes import *

# print(f'. dashi Runtime {runtime}: {dir(runtime)}')

from dsl.orm import *
from dsl.server.api import *


# can safely import models after runtime
from Kasayama import domain as models
from Kasayama import mixes
from Kasayama.recordtypes.quantarium import *
from Kasayama.feeds import *
from Kasayama.feeds.input.quantarium_ftp import QuantariumFTP


print(f". loaded models {models}")


@memoize_exp(expiration=5)
def lut_fctry(model, session=None):
    return LutValues(model=model, session=session)


def get_session():
    return SQLAlchemySessionFactory().Session


def load_session_factory():
    # global models
    model_list = [v for k, v in models.__dict__.items() if k in models.__all__]
    SQLAlchemySessionFactory(
        base=models.Base if "Base" in models.__dict__ else None,
        reflbase=models.ReflBase if "ReflBase" in models.__dict__ else None,
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
        db=runtime.CONFIG.Resources.Database.Schema,
    )


def examine_create_statement(dao, engine):
    create_stmt = CreateTable(dao.__table__).compile(engine)
    print(create_stmt)


def repr_model(modelclz):

    session = get_session()

    res = session.query(~modelclz).first()

    j = modelclz(entity=res).to_json()

    session.close()

    return json.dumps(j)


def examine_custom_SQL_model_cfg(only_model_name=None, engine=None):
    try:

        for n, m in runtime.SCHEMA.__dict__.items():

            if not only_model_name or n == only_model_name:

                print(f"\n******** {n} ********")

                if "SQL" in m:
                    print(f". {n} SQL {m.SQL}")
                if "Options" in m:
                    print(f". {n} Options {m.Options}")
                if n.endswith("Lookup") and "Values" in m:
                    ins_d = {}
                    model = models.__dict__[n]()
                    i = 0
                    for fld_name, val_lst in m.Values.items():
                        for val in val_lst:
                            ins_d[i] = {}
                            i += 1
                        break
                    for fld_name, val_lst in m.Values.items():
                        i = 0
                        for val in val_lst:
                            # ins_d[i]['id'] = 1
                            # ins_d[i]['initial_entry_date'] = datetime.datetime.now()
                            ins_d[i][fld_name] = val
                            i += 1

                    ins_list = [v for k, v in ins_d.items()]
                    ins = model.Table.insert()

                    # print(f'. ins_list {ins_list}')
                    # print(f'. model {model}')
                    # print(f'. ins_d	 {ins_d}')
                    # print(f'. {n} Insert Def\n{ins}')
                    # print(f'. {n} Insert Def\n{sqlparse.format(str(ins), reindent=True, keyword_case="upper")}')
                    # print(f'. {n} Insert Items\n{ins_list}')

                    # self._conn.execute(sql_stamement)

                    dir_ = os.path.dirname(pyaella_sql.__file__)

                    tmpl_filepath = os.path.join(dir_, "insert_lookup_table.sql.mako")
                    tmpl = mako.template.Template(filename=tmpl_filepath)
                    sql_stamement = tmpl.render(
                        table_name=model.TableName, ins_list=ins_list
                    )
                    print(sql_stamement)

    except:
        print(traceback.format_exc())


def load_partitions(
    load_property_loans=False,
    load_property_loan_masters=False,
    load_qnt_open_liens=False,
    load_leads=False,
    load_dmcm=False,
):

    if load_qnt_open_liens:
        session = get_session()
        # pre-emptive creation of QntOpenLien partitions
        for pkey_for_state in ALL_VALID_MARKETS:
            print(f". pkey_for_state {pkey_for_state}")
            partition = models.QntOpenLien.create_partition(
                key=str(pkey_for_state), engine=SQLAlchemySessionFactory().Engine
            )
            session.commit()
            session.flush()
        session.close()

        session = get_session()
        # pre-emptive creation of QntOpenLienTmp partitions
        for pkey_for_state in ALL_VALID_MARKETS:
            print(f". pkey_for_state QntOpenLienTmp: {pkey_for_state}")
            partition = models.QntOpenLienTmp.create_partition(
                key=str(pkey_for_state), engine=SQLAlchemySessionFactory().Engine
            )
            session.commit()
            session.flush()
        session.close()

    if load_property_loans:
        session = get_session()
        # pre-emptive creation of PropertyLoan partitions
        for year in range(2021, 2023):
            for month in range(1, 13):
                limit_from = f'{year}-{"%02d" % month}-01'
                limit_to = f'{year}-{"%02d" % (month+1)}-01'
                partition_key = f'{year}-{"%02d" % month}'
                print(f"{partition_key} : {limit_from} to {limit_to}")
                partition = models.PropertyLoan.create_partition(
                    key=partition_key,
                    limit_from=limit_from,
                    limit_to=limit_to,
                    engine=SQLAlchemySessionFactory().Engine,
                )
                session.commit()
                session.flush
        session.close()

    if load_property_loan_masters:
        session = get_session()
        # pre-emptive creation of PropertyLoanMaster partitions
        for pkey_for_state in ALL_VALID_MARKETS:
            print(f". pkey_for_state {pkey_for_state}")
            partition = models.PropertyLoanMaster.create_partition(
                key=str(pkey_for_state), engine=SQLAlchemySessionFactory().Engine
            )
            session.commit()
            session.flush()
        session.close()

    if load_leads:
        session = get_session()
        for year in range(2018, 2023):
            for month in range(1, 13):
                limit_from = f'{year}-{"%02d" % month}-01'
                limit_to = f'{year}-{"%02d" % (month+1)}-01'
                partition_key = f'{year}-{"%02d" % month}'

                # print(f'{partition_key} : {limit_from} to {limit_to}')

                partition = models.Lead.create_partition(
                    key=partition_key,
                    limit_from=limit_from,
                    limit_to=limit_to,
                    engine=SQLAlchemySessionFactory().Engine,
                )
                session.commit()
                session.flush

                partition_key_for_table = partition_key.replace("-", "_")
                stmt = f"""
				CREATE TRIGGER tr_leads_{partition_key_for_table.lower()}
					BEFORE INSERT OR UPDATE 
					ON public.leads_{partition_key_for_table.lower()}
					FOR EACH ROW
					EXECUTE FUNCTION public.tr_standard_mod(); 
				"""

                # print(stmt)

                conn = SQLAlchemySessionFactory().Engine.connect()
                conn.execute(stmt)
                conn.close()

        session.close()

    if load_dmcm:
        session = get_session()
        # pre-emptive creation of QntOpenLien partitions
        for pkey_for_state in ALL_VALID_MARKETS:

            try:

                print(f". pkey_for_state {pkey_for_state}")
                partition = models.DirectMailCampaignMember.create_partition(
                    key=str(pkey_for_state), engine=SQLAlchemySessionFactory().Engine
                )

                session.commit()
                session.flush()

            except:
                print(f". caught exception {traceback.format_exc()}. Continuing....")

            stmt = f"""
			CREATE TRIGGER tr_direct_mail_campaign_members_{pkey_for_state.lower()}
				BEFORE INSERT OR UPDATE 
				ON public.direct_mail_campaign_members_{pkey_for_state.lower()}
				FOR EACH ROW
				EXECUTE FUNCTION public.tr_standard_mod(); 
			"""

            conn = SQLAlchemySessionFactory().Engine.connect()
            try:
                conn.execute(stmt)
            except:
                print(f". caught exception {traceback.format_exc()}. Continuing....")
            conn.close()

        session.close()


def gen_entity_keys(model_name, session):
    """ """
    try:
        model = models.__dict__[model_name]
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


def gen_property_loan_guids():

    for b in range(0, 100):
        print(f". batch {b} creating guids")
        session = get_session()
        i = 0
        cache = []
        PL = ~models.PropertyLoan
        pL_data = (
            session.query(
                PL.id,
                PL.year_month,
                PL.last_name,
                PL.own_cass_address_1,
                PL.own_cass_city,
                PL.own_cass_state,
                PL.own_cass_zipcode,
            )
            .filter(PL.guid_matrix == None)
            .all()
        )
        print(f". pL_data len {len(pL_data)}")
        start_time = time.time()
        for p in pL_data:
            i += 1
            zipcode = p.own_cass_zipcode
            if zipcode:
                if "-" in zipcode:
                    z_5, z_4 = zipcode.split("-")
                else:
                    z_5 = zipcode
                    z_4 = ""

                guid = mixes.PropertyLoanMix.gen_guid(
                    z_5,
                    p.own_cass_state,
                    p.own_cass_city,
                    p.own_cass_address_1,
                    p.last_name,
                )

                cache.append(
                    dict(
                        id=p.id,
                        year_month=p.year_month,
                        guid_matrix=guid,
                        own_cass_zipcode=z_5,
                        own_cass_zipcode_plus4=z_4,
                    )
                )

            if len(cache) > 5000:
                print("cache full, updating db.")
                break

        print(f". generated 5000 guids {time.time() - start_time}")
        if cache:
            print("updating ...")
            start_time = time.time()
            try:
                stmt = (
                    PL.__table__.update()
                    .where(PL.__table__.c.id == sa_exp.bindparam("id"))
                    .values(
                        {
                            "id": sa_exp.bindparam("id"),
                            "own_cass_zipcode": sa_exp.bindparam("own_cass_zipcode"),
                            "guid_matrix": sa_exp.bindparam("guid_matrix"),
                            "own_cass_zipcode_plus4": sa_exp.bindparam(
                                "own_cass_zipcode_plus4"
                            ),
                        }
                    )
                )
                with SQLAlchemySessionFactory().Engine.connect() as conn:
                    conn.execute(stmt, cache)
                print(f". updated 5000 guids {time.time() - start_time}")
            except:
                print(traceback.format_exc())
                try:
                    session.rollback()
                except:
                    print_log_msg(traceback.format_exc())

        session.close()


# def load_partitions():
# 	session = get_session()
# 	# pre-emptive creation of PropertyLoan partitions
# 	for year in range(2021, 2023):
# 		for month in range(1,13):
# 			limit_from = f'{year}-{"%02d" % month}-01'
# 			limit_to = f'{year}-{"%02d" % (month+1)}-01'
# 			partition_key = f'{year}-{"%02d" % month}'
# 			print(f'{partition_key} : {limit_from} to {limit_to}')
# 			partition = models.PropertyLoan.create_partition(
# 				key=partition_key,
# 				limit_from=limit_from,
# 				limit_to=limit_to,
# 				engine=SQLAlchemySessionFactory().Engine)
# 			session.commit()
# 			session.flush
# 	session.close()


def create_qol_rec_mapping():

    keys = list(map(to_column_name, OpenLienRecord._fields))
    qol = models.QntOpenLien()
    keys_transformed = []
    lookup_table_keys = []

    for k in keys:
        col_name = to_column_name(k)
        if col_name not in qol.Fields:
            if col_name in qol.Relations:
                # is relation but not an ID?
                keys_transformed.append(col_name)

            elif col_name + "_id" in qol.Relations:
                # is relation with an ID to relation
                col_name = col_name + "_id"
                keys_transformed.append(col_name)
                lookup_table_keys.append(col_name)

            else:
                raise Exception(f". ERR Unknown col_name {col_name}")
        else:
            keys_transformed.append(col_name)

    return keys_transformed, lookup_table_keys


def set_enable_autovacuum_for_tables(table_names, enabled):

    """
    ALTER TABLE wl_disk_data SET (autovacuum_vacuum_scale_factor = 0.0);
    ALTER TABLE wl_disk_data SET (autovacuum_vacuum_threshold = 1000);
    ALTER TABLE wl_disk_data SET (autovacuum_analyze_scale_factor = 0.0);
    ALTER TABLE wl_disk_data SET (autovacuum_analyze_threshold = 1000);
    """

    try:
        engine = SQLAlchemySessionFactory().Engine
        with engine.connect() as conn:
            for table_name in table_names:
                print(f". setting {table_name} autovacuum to {enabled}")
                stmt = f"""ALTER TABLE {table_name} SET (autovacuum_enabled = {enabled});"""
            res = conn.execute(stmt)
            print(res)
    except:
        print(traceback.format_exc())
    finally:
        try:
            engine.dispose()
        except:
            pass


def set_enable_autovacuum_for_state_partitions(enabled):

    table_names = []
    for state_abv in STATES_ABV:
        table_names.append(f"qnt_open_liens_{state_abv.lower()}")

    set_enable_autovacuum_for_tables(table_names, enabled)


def reset_storage_opts_for_tables(table_names, enabled):

    try:
        engine = SQLAlchemySessionFactory().Engine
        with engine.connect() as conn:
            for table_name in table_names:
                stmt = """ALTER TABLE {table_name} reset 
					(autovacuum_enabled, autovacuum_analyze_scale_factor, autovacuum_analyze_threshold);"""
            res = conn.execute(stmt)
            print(res)
    except:
        print(traceback.format_exc())
    finally:
        try:
            engine.dispose()
        except:
            pass


rec_str, QOL_Lut_Keys = create_qol_rec_mapping()
QOL_Tmp_Rec = recordtype("QOL_Tmp_Rec", ", ".join(rec_str).replace("&", ""))


def gen_user_api_key(email_address):

    session = SQLAlchemySessionFactory().Session

    U = ~models.User

    user = session.query(U).filter(U.email_address == email_address).first()
    if user:

        if user.is_active:

            app_conf = runtime.APP_CONFIG
            adc = codify.AppDomainCoder(app_conf.AppId, app_conf.DomainId)
            # TODO: allow versioning of API key
            return adc.get_api_key(user.id, user.access_token_cnt)

        else:
            raise ("Err. User inactive")

    else:
        raise ("Err. User not found")


def verify_user_api_key(api_token, email_address):

    session = SQLAlchemySessionFactory().Session

    U = ~models.User

    user = session.query(U).filter(U.email_address == email_address).first()
    if user:

        app_conf = runtime.APP_CONFIG
        adc = codify.AppDomainCoder(app_conf.AppId, app_conf.DomainId)
        user_id, cnt = adc.get_user_data_from_api_key(api_token)
        return user_id == user.id

    else:
        raise ("Err. User not found")

    # adc.get_user_id_from_api_key(k[:4])


def extract_campaign_id_from_sequences():

    sequences = [
        "O3-2",
        "J987",
        "L5-2",
        "Z21T",
        "L12-",
        "P13-",
        "AVPG",
        "MQDH",
        "C127",
        "CBYF",
        "M0RS",
        "SCJV",
        "QSAC",
        "C149",
        "W7-3",
        "NKBY",
        "Y2-3",
        "3T49",
        "P-33",
        "F138",
        "KYFM",
        "Y6-2",
        "1498",
        "99VP",
        "C-15",
        "5QDH",
        "C9-5",
        "D8-2",
        "P5-1",
        "0ACJ",
        "60RS",
        "X6-1",
        "I14-",
        "E3-2",
        "8GWZ",
        "NCJV",
        "A11-",
        "QHNE",
        "M-41",
        "DRSA",
        "1XKB",
        "E876",
        "5M0R",
        "V5-5",
        "XJVP",
        "JJKB",
        "C143",
        "J13-",
        "U2-2",
        "ZRSA",
        "7FM0",
        "E10-",
        "YM0R",
        "M5-1",
        "E987",
        "F125",
        "M13-",
        "X876",
        "M14-",
        "A7-1",
        "K-60",
        "J8-4",
        "XVPG",
        "Z8-4",
        "S2-2",
        "X765",
        "9VPG",
        "QNEX",
        "WRSA",
        "O5-2",
        "C132",
        "GM0R",
        "K-29",
        "N4-2",
        "JYFM",
        "L1-2",
        "C13-",
        "FQDH",
        "B5QD",
        "K-44",
        "C142",
        "D21T",
        "G8-4",
        "BGWZ",
        "F142",
        "V8-6",
        "Z5-2",
        "YZ32",
        "I11-",
        "P11-",
        "31T4",
        "KVPG",
        "P-36",
        "C987",
        "F7-1",
        "9KBY",
        "W2-2",
        "C124",
        "U9-7",
        "K13-",
        "3NEX",
        "J8-3",
        "C139",
        "WH6-",
        "P65Q",
        "U11-",
        "S11-",
        "Q321",
        "K65Q",
        "R2-3",
        "W321",
        "HCJV",
        "CXKB",
        "R1T4",
        "K11-",
        "S1-2",
        "S1T4",
        "W11-",
        "WH5-",
        "7GWZ",
        "J6-3",
        "F139",
        "L5-1",
        "BPGW",
        "Y65Q",
        "EVPG",
        "V10-",
        "KK87",
        "B6-3",
        "K-65",
        "O12-",
        "K-72",
        "W6-4",
        "GZ32",
        "0RSA",
        "A12-",
        "R11-",
        "F143",
        "K1-2",
        "Z5-3",
        "HSAC",
        "B14-",
        "L10-",
        "V9-2",
        "S9-1",
        "VPGW",
        "Y11-",
        "G7-1",
        "L11-",
        "RT49",
        "N8-3",
        "L8-8",
        "T6-2",
        "G12-",
        "E498",
        "J876",
        "BYFM",
        "T5-2",
        "3HNE",
        "F124",
        "4876",
        "N6-3",
        "C133",
        "N3-1",
        "T4-2",
        "B6-2",
        "K-22",
        "N7-1",
        "XPGW",
        "W21T",
        "O11-",
        "SJVP",
        "Q9-4",
        "PM0R",
        "JKBY",
        "C876",
        "F3-1",
        "F8-4",
        "C129",
        "C136",
        "L13-",
        "9PGW",
        "K-70",
        "2498",
        "D6-1",
        "K-59",
        "77GW",
        "Y0RS",
        "U12-",
        "F122",
        "A14-",
        "C128",
        "ZDHN",
        "P2-2",
        "P-37",
        "N9-2",
        "KPGW",
        "K765",
        "S13-",
        "W5-3",
        "R10-",
        "Q12-",
        "U3-1",
        "F128",
        "YGWZ",
        "PPYF",
        "N14-",
        "PGWZ",
        "I9-9",
        "6Z32",
        "P-34",
        "O5-3",
        "U6-3",
        "B7-3",
        "C144",
        "8765",
        "3SAC",
        "B4-1",
        "FZ32",
        "VGWZ",
        "BWZ3",
        "EE49",
        "2T49",
        "F9-2",
        "4BYF",
        "3DHN",
        "C123",
        "TEXK",
        "W13-",
        "C125",
        "9765",
        "N12-",
        "MZ32",
        "DEXK",
        "I8-8",
        "Z3-1",
        "6WZ3",
        "D1T4",
        "V132",
        "Q8-3",
        "M10-",
        "M-40",
        "V6-5",
        "5RSA",
        "A7-2",
        "O14-",
        "M-44",
        "C6-7",
        "M-32",
        "M-49",
        "Z7-4",
        "X2-2",
        "WQDH",
        "Z1-1",
        "A9-4",
        "P-30",
        "Z0RS",
        "W10-",
        "MHNE",
        "P-35",
        "M4-2",
        "Q10-",
        "C7-4",
        "W0RS",
        "C147",
        "J6-2",
        "F5QD",
        "O10-",
        "P12-",
        "N987",
        "C140",
        "P8-3",
        "E9-7",
        "GFM0",
        "N8-4",
        "DACJ",
        "X2-1",
        "AJVP",
        "5321",
        "W8-2",
        "NACJ",
        "M12-",
        "C134",
        "WH10",
        "PYFM",
        "GQDH",
        "U9-6",
        "CCXK",
        "Z-20",
        "V7-2",
        "C135",
        "DSAC",
        "WM0R",
        "2ACJ",
        "Z10-",
        "3041",
        "H5-4",
        "W9-4",
        "F321",
        "M8-2",
        "F121",
        "R12-",
        "N498",
        "A8-7",
        "B765",
        "2HNE",
        "CKBY",
        "X13-",
        "F12-",
        "AT49",
        "4PGW",
        "F120",
        "D14-",
        "9GWZ",
        "I13-",
        "C138",
        "E14-",
        "BB76",
        "WH7-",
        "L9-3",
        "L14-",
        "XBYF",
        "J8-1",
        "V120",
        "FRSA",
        "75QD",
        "M3-1",
        "WDHN",
        "V13-",
        "B12-",
        "C131",
        "M321",
        "I7-3",
        "I5-2",
        "C498",
        "CVPG",
        "G4-2",
        "X10-",
        "V876",
        "U5-2",
        "M-42",
        "K-43",
        "4KBY",
        "865Q",
        "K8-8",
        "MDHN",
        "TCJV",
        "M-48",
        "Y10-",
        "S10-",
        "R7-4",
        "U9-8",
        "V765",
        "0HNE",
        "S8-5",
        "B9-4",
        "R8-2",
        "W5-2",
        "N5-4",
        "Y13-",
        "X7-2",
        "R9-2",
        "R13-",
        "C6-8",
        "H7-1",
        "B8-4",
        "1EXK",
        "7WZ3",
        "88PG",
        "VYFM",
        "V3-1",
        "01T4",
        "Y4-2",
        "Z3-2",
        "M-33",
        "G5QD",
        "N13-",
        "C7-5",
        "N10-",
        "I9-1",
        "C145",
        "S498",
        "E7-1",
        "I6-8",
        "U7-1",
        "HEXK",
        "FWZ3",
        "B65Q",
        "K-42",
        "N11-",
        "Q1-2",
        "B3-1",
        "Q-33",
        "H2-2",
        "H2-3",
        "T3-1",
        "Y12-",
        "QDHN",
        "Z13-",
        "F14-",
        "F6-3",
        "5DHN",
        "J5-1",
        "0DHN",
        "Y7-1",
        "VFM0",
        "ZQDH",
        "G2-1",
        "L7-1",
        "J10-",
        "S3-2",
        "2252",
        "WH2-",
        "765Q",
        "AXKB",
        "V12-",
        "K14-",
        "PFM0",
        "5HNE",
        "ECJV",
        "D7-4",
        "K2-2",
        "D4-1",
        "M-43",
        "44JV",
        "G65Q",
        "8PGW",
        "RACJ",
        "I8-7",
        "R21T",
        "O13-",
        "G14-",
        "K-45",
        "C5-2",
        "3RSA",
        "T7-1",
        "4VPG",
        "H14-",
        "W5QD",
        "L1-3",
        "QRSA",
        "1NEX",
        "X9-1",
        "S2-3",
        "Q13-",
        "T987",
        "H4-2",
        "A8-8",
        "EJVP",
        "H8-8",
        "S4-2",
        "L-25",
        "C130",
        "6DHN",
        "Q0RS",
        "VVBY",
        "T13-",
        "F145",
        "K-27",
        "Q7-4",
        "N5-3",
        "B11-",
        "A498",
        "Y5QD",
        "O6-5",
        "RNEX",
        "X5-2",
        "VBYF",
        "M-47",
        "TXKB",
        "Z1T4",
        "K876",
        "C121",
        "J11-",
        "Y5-7",
        "JBYF",
        "C146",
        "L3-2",
        "Z321",
        "T10-",
        "V1-1",
        "P6-4",
        "G1-2",
        "N1-2",
        "X987",
        "J8-2",
        "H9-3",
        "W2-1",
        "3040",
        "WH1-",
        "C126",
        "V5-6",
        "I6-7",
        "5Z32",
        "C122",
        "S12-",
        "WH8-",
        "9BYF",
        "M7-1",
        "D5-2",
        "TJVP",
        "2EXK",
        "G3-2",
        "H12-",
        "E5-3",
        "F10-",
        "M21T",
        "RCJV",
        "8BYF",
        "W7-4",
        "K9-3",
        "C3-1",
        "R6-2",
        "MSAC",
        "4JVP",
        "P-31",
        "V4-1",
        "C137",
        "I3-1",
        "G13-",
        "Y1-1",
        "C14-",
        "MRSA",
        "R4-2",
        "F144",
        "HXKB",
        "4XKB",
        "6M0R",
        "Z8-5",
        "Q5-4",
        "U8-5",
        "P-32",
        "F13-",
        "6FM0",
        "Y5-6",
        "M9-4",
        "NXKB",
        "T11-",
        "X8-2",
        "H13-",
        "W12-",
        "K6-1",
        "J7-4",
        "WH9-",
        "P765",
        "P10-",
        "U13-",
        "C120",
        "JPGW",
        "R1-1",
        "8WZ3",
        "50RS",
        "M-38",
        "YFM0",
        "X11-",
        "ZHNE",
        "XX98",
        "1987",
        "K7-4",
        "8YFM",
        "H6-2",
        "I12-",
        "7YFM",
        "G321",
        "TVPG",
        "EKBY",
        "Q-34",
        "DNEX",
        "J2-1",
        "M3-2",
        "Q1-1",
        "T876",
    ]

    C = ~models.Campaign

    for s in sequences:

        results = []

        if "-" not in s:
            cid, pos = mixes.decode_plxc_sequence_code(s + "-000001")

            session = SQLAlchemySessionFactory().Session

            campaign = models.Campaign.load(cid, session=session)

            if campaign:
                results.append(f"{s},{campaign.id},{campaign.name}")
                print(f". found {campaign.name}")

    print(results)


def set_all_campaign_sequences():

    session = SQLAlchemySessionFactory().Session

    C = ~models.Campaign

    cids = session.query(C).all()

    upsert_buffer = []

    for c in cids:
        c_seq_exmpl = mixes.gen_plxc_sequence_code(c.initial_entry_date, c.id, 0)
        sequence_prefix = c_seq_exmpl.split("-")[0]

        upsert_buffer.append(dict(id=c.id, sequence_prefix=sequence_prefix))

    print(len(upsert_buffer))

    stmt = (
        C.__table__.update()
        .where(C.__table__.c.id == sa_exp.bindparam("id"))
        .values(
            {
                "id": sa_exp.bindparam("id"),
                "sequence_prefix": sa_exp.bindparam("sequence_prefix"),
            }
        )
    )

    print(f". created stmt. executing....")
    print(stmt)
    with SQLAlchemySessionFactory().Engine.connect() as conn:
        with conn.begin():
            res = conn.execute(stmt, upsert_buffer)


if __name__ == "__main__":

    load_session_factory()
    print(f". session loaded.")

    print(f". func list:")
    for n in (
        "repr_model(modelclz)",
        "examine_create_statement(dao, engine)",
        "examine_custom_SQL_model_cfg (only_model_name=None, engine=None)",
        "load_partitions(load_property_loans=True, load_property_loan_masters=False, load_qnt_open_liens=True, load_leads=True)",
        "gen_property_loan_guids",
        "set_enable_autovacuum_for_tables",
        "reset_storage_opts_for_tables",
        "set_enable_autovacuum_for_state_partitions",
    ):
        print(f"-> {n}")

    engine = SQLAlchemySessionFactory().Engine

    print(f". engine loaded {engine}")

    if OPTS.RUNINLINE:
        pass

    print("ready....")


# GRANT SELECT, REFERENCES ON DATABASE iskaffi TO sammy;
# GRANT SELECT, REFERENCES, TRIGGER PRIVILEGES ON ALL TABLES IN SCHEMA public TO sammy;

# SELECT	Ability to perform SELECT statements on the table.
# INSERT	Ability to perform INSERT statements on the table.
# UPDATE	Ability to perform UPDATE statements on the table.
# DELETE	Ability to perform DELETE statements on the table.
# TRUNCATE	Ability to perform TRUNCATE statements on the table.
# REFERENCES	Ability to create foreign keys (requires privileges on both parent and child tables).
# TRIGGER	Ability to create triggers on the table.
# CREATE	Ability to perform CREATE TABLE statements.
# ALL	Grants all permissions.
