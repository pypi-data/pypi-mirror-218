import csv
import sys, os, stat
import datetime
import pdb
import shutil
import inspect
import traceback
import gzip
import itertools
import time
from collections import namedtuple
from optparse import OptionParser
import multiprocessing
from multiprocessing import Process, Pool
from multiprocessing.queues import Queue
from multiprocessing.queues import Empty as QueueEmpty
# from multiprocessing.queues import Pipe

import sqlalchemy
from sqlalchemy.sql import expression as sa_exp

import pyaella3
from pyaella3 import *
from pyaella3 import dinj
from pyaella3.codify import *
from pyaella3.processes import *
from pyaella3.orm import *
from pyaella3.server.api import *
from Kasayama.recordtypes.quantarium import *

def parse_args(args=None):
    """
    python ./pyaella3/processes.py -c ./pyaella3/tests/app_test_localhost.yaml

    """

    usage = "usage: %prog [options] arg"
    parser = OptionParser()

    parser.add_option(
        "-c", dest="CONFIG",
        help="Absolute path to main dependency injection file")

    parser.add_option(
        "-i", dest="INPUTFILE",
        help="CSV File")

    parser.add_option(
        "-o", dest="OUTPUTFILE",
        help="Output TSV File")

    parser.add_option(
        "-n", dest="NUMOFRECS",
        help="Number of Records to gen in TSV File")

    parser.add_option(
        "-l", dest="LIMIT",
        help="Limit Number of Records")

    parser.add_option(
        "--test-from-select", dest="TESTFROMSELECT",
        help="Do Test From Select")

    (options, args) = parser.parse_args()

    print(f'options {options} args {args}')
    if len(args) > 1:
        parser.error("incorrect number of arguments.")
        sys.exit(0)
    return options


OPTS = None
runtime = None
models = None


__all__ = [
    'MapKey',
    'new_msgPipe',
    'MsgPipe',
    'Distributor',
    'CollectingParser',
    'QuantariumParserFormatter'
]


MsgPipe = namedtuple('MsgPipe', 'ParentConn ChildConn')

MapKey = recordtype(
    'MapKey', 'Type InputFilepath RowNumber RowLine RowTuple')

def new_msgPipe():
    '''
        Creates new multiprocessing.Pipe
        @return: MsgPipe(ParentConn, ChildConn)
        @rtype: MsgPipe
    '''
    p,c = multiprocessing.Pipe()
    return MsgPipe(p,c)


# TODO: refactor out of this module
def create_qol_rec_mapping():

    keys = (list(map(to_column_name, OpenLienRecord._fields)))
    qol = models.QntOpenLien()
    keys_transformed = []

    for k in keys:

        col_name = to_column_name(k)

        # HACK (fixed)
        # if col_name in [
        #     'mtg01_est_monthly_pi', 
        #     'mtg02_est_monthly_pi', 
        #     'mtg03_est_monthly_pi', 
        #     'mtg04_est_monthly_pi']:
        #     col_name = col_name.replace('_pi', '_p&i').lower()

        if col_name not in qol.Fields:
            if col_name in qol.Relations:
                # is relation but not an ID?
                keys_transformed.append(col_name)

            elif col_name + '_id' in qol.Relations:
                # is relation with an ID to relation
                keys_transformed.append(col_name)

            else:
                raise Exception(f'. ERR Unknown col_name {col_name}')
        else:
            keys_transformed.append(col_name)

    return keys_transformed


class Distributor(multiprocessing.Process):
    
    def __init__(self, config, pipe, inqueue=None, outqueue=None):
        multiprocessing.Process.__init__(self)
        self.config = config
        self._pipe = pipe
        self._inqueue = inqueue
        self._outqueue = outqueue
        self._go = multiprocessing.Event()
        self._initd = False

    def setup(self):
        pass

    def shutdown(self):
        self._go.set()

    def run(self):
        self.setup()
        try:
            c = 0
            t = []
            print(f'. is {self.name} initialized in run? {self._initd}')
            while not self._go.is_set():
                # print(f'. {self.name} running')
                try:
                    mk = None
                    try:
                        mk = self._inqueue.get(timeout=.05)
                    except:
                        time.sleep(.001)
                    #if self._pipe.poll():
                        #mk = self._pipe.recv()
                    if mk:
                        self._outqueue.put_nowait(mk)
                        print(f'. {self.name} put mk')

                        # # print(f'. run {self.name} mk {mk}')
                        # if mk.Type in self._formatParserMap:
                        #     valid, mk = self._formatParserMap[mk.Type].parse(mk)
                        #     print(f'. formatted mk {mk}')
                        #     if valid:
                        #         self._outqueue.put_nowait(mk)
                        #     else:
                        #         # TODO: ERR heap queue
                        #         pass
                    else:
                        if not self._go.is_set():
                            time.sleep(.1)

                except EOFError as e:
                    print(traceback.format_exc())
                except Exception as hell:
                    print(traceback.format_exc())

        except Exception as e:
            print(traceback.format_exc())

        print(f'. {self.name} done')


class CollectingParser(multiprocessing.Process):
    
    def __init__(self, config, pipe, inqueue=None, outqueue=None):
        multiprocessing.Process.__init__(self)
        self.config = config
        self._pipe = pipe
        self._inqueue = inqueue
        self._outqueue = outqueue
        self._go = True
        self._num_of_saves = 0
        self._session = None

        self._formatParserMap = {
            'QNT':QuantariumParserFormatter(self.config),
        }

        self._go = multiprocessing.Event()

    def setup(self):

        self.QOL_Tmp_Rec = recordtype('QOL_Tmp_Rec', ', '.join(create_qol_rec_mapping()).replace('&', ''))

        # new process, must create a new instance of factory
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

        self._session = SQLAlchemySessionFactory().Session

    def shutdown(self):
        self._go.set()

    def run(self):
        self.setup()
        try:
            c = 0
            t = []
            print(f'. preparing to run {self.name}, with session: {self._session}')
            while not self._go.is_set():
                try:
                    mk = None
                    try:
                        mk = self._inqueue.get(timeout=.05)
                        print(f'. run {self.name} inqueue mk {mk}')
                    except:
                        time.sleep(.001)
                    #if self._pipe.poll():
                        #mk = self._pipe.recv()
                    if mk:
                        print(f'. run {self.name} mk {mk}')
                        if mk.Type in self._formatParserMap:
                            valid, mk = self._formatParserMap[mk.Type].parse(mk, self.QOL_Tmp_Rec)
                            print(f'. run {self.name} {valid} mk {mk}')
                            if valid:
                                print(f'. valid {mk.RowTuple}')
                                # self._outqueue.put_nowait(mk)
                                self._do_insert(mk.RowTuple)
                            else:
                                # TODO: ERR heap queue
                                pass
                    else:
                        if not self._go.is_set():
                            time.sleep(.1)

                except EOFError as e:
                    print(traceback.format_exc())
                except Exception as hell:
                    print(traceback.format_exc())

        except Exception as e:
            print(traceback.format_exc())

        print(f'. {self.name} done.')

    def _do_insert(self, rec):
        print(f'. do_insert called {rec}')

        start_time = datetime.datetime.now()

        d = rec._asdict()
        qol = models.QntOpenLien(**d)
        print(f'. _do_insert() {qol}')
        # save to database
        try:
            # qol.save(session=session)
            self._num_of_saves += 1
        except Exception as e:
            print(traceback.format_exc())
            print(f'. ERR row {row}, qnt id: {qol.quantarium_internal_pid}')

        print(f'. worker end time: {datetime.datetime.now() - start_time}, num_of_saves: {self._num_of_saves} -------- /')


class QuantariumParserFormatter(object):
    """

    """
    def __init__(self, config, connection=None):
        self.config = config
        self._sqlPreloadResults = {}

        if connection:
            # pre load sql data for compare, transform
            sql = []
            for sqlStr in sql:
                s = connection.execute(sqlStr).fetchall()
                for x in s:
                    self._sqlPreloadResults[x._row[1]] = x._row[0]
        
        # TODO: cache
        # if the tmp db exists, load from cache
        # self._sqlPreloadResults = json.load(
        #     open(os.path.join(os.getcwd(), 'db', 'SQLPreloadResults.json'))) \
        #     if not self._sqlPreloadResults else self._sqlPreloadResults

    def parse(self, mk, line_tuple_record_frmt):
        try:
            mk.RowLine = self._pre_row_line_transform(mk.RowLine)
            if not self._filter_out(mk.RowLine):
                if self._filter_in(mk.RowLine):

                    mk.RowTuple = line_tuple_record_frmt(*mk.RowLine)
                    mk.RowTuple = self._post_row_tuple_transform(mk.RowTuple)
                    return True, mk

            return False, mk

        except:
            print(traceback.format_exc())
    
    def _filter_in(self, row_line):
        return True

    def _filter_out(self, row_line):
        return False

    def _pre_row_line_transform(self, row_line):

        # null out missing values
        row_line = [v if v != '' else None for v in row_line]

        return row_line

    def _post_row_tuple_transform(self, row_tuple):
        return row_tuple


def doit():

    distributer_inqueue = multiprocessing.Queue()
    distributor_outqueue = multiprocessing.Queue()

    msgPipe = new_msgPipe()
    distributors = []
    collectors = []
    
    for i in range(0, 1):  
        distributors.append(Distributor(
            None, None, inqueue=distributer_inqueue, outqueue=distributor_outqueue))
    for i in range(0, 1):
        collectors.append(CollectingParser(
            None, None, inqueue=distributor_outqueue))
    for d in distributors:
        d.start()
    for c in collectors:
        c.start()

    # distributer_inqueue.put('testval')

    if OPTS.INPUTFILE:
        with open(OPTS.INPUTFILE, 'r') as tsv_file:
            reader = csv.reader(tsv_file, delimiter='\t')
            i = 1
            for row in itertools.islice(reader, 1, 2):
                # 'MapKey', 'Type InputFilepath RowNumber RowLine RowTuple')
                mk = MapKey('QNT', OPTS.INPUTFILE, i, row, None)
                distributer_inqueue.put(mk)

    print('. running....')
    time.sleep(10)
    print('. stopping....')

    for d in distributors:
        try:
            d.shutdown()
            d.join()
        except Exception as e:
            print(e)
    for c in collectors:
        try:
            c.shutdown()
            c.join()
        except Exception as e:
            print(e)


if __name__ == '__main__':

    OPTS = parse_args()
    runtime = dinj.Runtime(opts=OPTS)
    # can safely import models after runtime
    from Kasayama import domain as models

    doit()
    print('done.')

