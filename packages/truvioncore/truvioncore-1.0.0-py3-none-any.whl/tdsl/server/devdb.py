import os
import sys
import csv
from optparse import OptionParser
from subprocess import call
import traceback
from mako.template import Template

from tdsl.express import twk_hammer


def parse_args(args=None):
    usage = "usage: %prog [options] arg"    
    parser = OptionParser()

    parser.add_option(
        "--host", dest="HOST", default="localhost",
        help="HOST")

    parser.add_option(
        "--port", dest="PORT", default=5432,
        help="PORT")

    parser.add_option(
        "--db", dest="DATABASE",  
        help="Database")

    parser.add_option(
        "-U", dest="USER",  
        help="User")

    parser.add_option(
        "-O", dest="OWNER",  
        help="Owner")

    parser.add_option(
        "--no-postgis", dest="NOPOSTGIS",
        action='store_true', default=False, 
        help="Install PostGIS")

    parser.add_option(
        "--no-dsl", dest="NOPYAELLA",
        action='store_true', default=False, 
        help="Install PYAELLA")

    parser.add_option(
        "--contrib-dir", dest="CONTRIBDIR",  
        help="Contrib Dir")

    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error("incorrect number of arguments.")
        sys.exit(0)
    return options

if __name__ == '__main__':
    """
    example usage - 

    cd /opt/local/share/postgresql92/contrib/postgis-2.0
    python /Users/mat/Documents/MigaCollabs/__src__/ETFDsl/dsl/server/dbcreate.py 
    -U postgres -O postgres --postgis --dsl --db mividio
    
    """

    if 'PYAELLA_DEV_TEST' not in os.environ:
        raise Exception('dbcreate can only be run under development mode')

    OPTS = parse_args()
    DATABASE_URL = None

    print('OPTS', OPTS)

    if OPTS.USER == None or not OPTS.USER:
        if 'DATABASE_URL' not in os.environ:
            raise Exception('No database connection information supplied. Failing')
        DATABASE_URL = os.environ['DATABASE_URL']

    if not DATABASE_URL:
        try:
            retcode = call(['dropdb', '-U', OPTS.USER, '--host', OPTS.HOST, '--port', OPTS.PORT, OPTS.DATABASE])
            print(retcode)
        except:
            print(traceback.format_exc())

    if not DATABASE_URL:
        try:
            retcode = call(['createdb', '-U', OPTS.USER, '-O', OPTS.OWNER, '--host', OPTS.HOST, '--port', OPTS.PORT, OPTS.DATABASE])
            print(retcode)
        except:
            print(traceback.format_exc())


    if not OPTS.NOPOSTGIS and not DATABASE_URL:
        # install PostGIS extention

        retcode = call(['psql', '--host', OPTS.HOST, '--port', OPTS.PORT, '-d', OPTS.DATABASE, '-U', OPTS.USER, '-f', 'postgis.sql'])
        print(retcode)

        retcode = call(['psql', '--host', OPTS.HOST, '--port', OPTS.PORT, '-d', OPTS.DATABASE,  '-U', OPTS.USER, '-f', 'postgis_comments.sql'])
        print(retcode)

        retcode = call(['psql', '--host', OPTS.HOST, '--port', OPTS.PORT, '-d', OPTS.DATABASE,  '-U', OPTS.USER, '-f', 'spatial_ref_sys.sql'])
        print(retcode)

        retcode = call(['psql', '--host', OPTS.HOST, '--port', OPTS.PORT, '-d', OPTS.DATABASE,  '-U', OPTS.USER, '-f', 'rtpostgis.sql'])
        print(retcode)

        retcode = call(['psql', '--host', OPTS.HOST, '--port', OPTS.PORT, '-d', OPTS.DATABASE,  '-U', OPTS.USER, '-f', 'raster_comments.sql'])
        print(retcode)

        retcode = call(['psql', '--host', OPTS.HOST, '--port', OPTS.PORT, '-d', OPTS.DATABASE,  '-U', OPTS.USER, '-f', 'topology.sql'])
        print(retcode)

        retcode = call(['psql', '--host', OPTS.HOST, '--port', OPTS.PORT, '-d', OPTS.DATABASE,  '-U', OPTS.USER, '-f', 'topology_comments.sql'])
        print(retcode)

    if not OPTS.NOPYAELLA:

        def do_templated_sql(filepath, **kwds):
            tmpl = Template(filename=tmpl_filepath, default_filters=['decode.utf8'])

            sql_stamement = tmpl.render(**kwds)

            print(sql_stamement)

            ofp = os.path.join(
                dir_, 'tmp', os.path.basename(tmpl_filepath.strip('.mako')))
            if not os.path.exists(os.path.dirname(ofp)):
                try:
                    os.makedirs(os.path.dirname(ofp))
                except:pass
            with open(ofp, 'w') as of:
                of.write(sql_stamement)

            if not DATABASE_URL:
                retcode = call(['psql', '--host', OPTS.HOST, '--port', OPTS.PORT, '-d', OPTS.DATABASE,  '-U', OPTS.USER, '-f', ofp])
                print(retcode)
            else:
                retcode = call(['psql', '-f', ofp, DATABASE_URL])
                print(retcode)

        try:

            from tdsl.orm import sql as pyaella_sql
            dir_ = os.path.dirname(pyaella_sql.__file__)

            for trigger in [
                'tr_standard_mod.sql.mako',
                'tr_standard_lu_mod.sql.mako']:

                tmpl_filepath = os.path.join(dir_, trigger)

                tmpl = Template(filename=tmpl_filepath)

                owner = OPTS.OWNER if not DATABASE_URL else 'postgres'

                sql_stamement = \
                    tmpl.render(
                        **{
                            'owner':owner
                        }
                    )

                print(sql_stamement)

                ofp = os.path.join(dir_, 'tmp', os.path.basename(tmpl_filepath.strip('.mako')))
                if not os.path.exists(os.path.dirname(ofp)):
                    try:
                        os.makedirs(os.path.dirname(ofp))
                    except:pass
                with open(ofp, 'w') as of:
                    of.write(sql_stamement)

                if not DATABASE_URL:
                    retcode = call(['psql', '--host', OPTS.HOST, '--port', OPTS.PORT, '-d', OPTS.DATABASE,  '-U', OPTS.USER, '-f', ofp])
                    print(retcode)
                else:
                    retcode = call(['psql', '-f', ofp, DATABASE_URL])
                    print(retcode)

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
                        twk_hammer(str(row).replace('[', '(').replace(']', ')'))

            do_templated_sql(tmpl_filepath, data=country_data)

        except:
            print(traceback.format_exc())


