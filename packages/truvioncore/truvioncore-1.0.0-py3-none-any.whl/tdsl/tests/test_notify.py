from optparse import OptionParser
import tdsl
from tdsl import *
from tdsl import dinj

def parse_args(args=None):
    '''
        Example: -c "config.yaml" < --test >
    '''
    usage = "usage: %prog [options] arg"
    parser = OptionParser()

    parser.add_option(
        "--test", dest="TEST",
        action='store_true',
        default=False, help="Tests")

    parser.add_option(
        "-c", dest="CONFIG",
        help="Absolute path to main dependency injection file")

    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error("incorrect number of arguments.")
        sys.exit(0)
    return options


OPTS = parse_args()
runtime = dinj.Runtime(opts=OPTS)


from tdsl.server import notify


res = notify.send_simple_message(
	'etfdata',
	'mbrown@entrustfunding.com',
	'Test Subject',
	'Test Message'
	)
 
print(res.text)

res = notify.send_smtp_message(
	'etfdata',
	'mbrown@entrustfunding.com',
	'Test Subject',
	'Test Message'
	)
 
print(res)
