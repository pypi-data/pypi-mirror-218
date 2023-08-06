import sys
import traceback
from optparse import OptionParser
import tdsl
from tdsl.server import ApplicationRuntimeBorg


def parse_args(args=None):

	usage = "usage: %prog [options] arg"
	parser = OptionParser()

	parser.add_option(
		"-c", dest="CONFIG",
		help="Absolute path to main dependency injection file")

	parser.add_option(
		"--create-all", action='store_true',
		default=False, dest="CREATEALL", help="Create tables")

	(options, args) = parser.parse_args()
	if len(args) > 1:
		parser.error("incorrect number of arguments.")
		sys.exit(0)
	return options


if __name__ == '__main__':

	arb = ApplicationRuntimeBorg(parse_args())

	session = arb.get_session()

	print(f'SqlAlchemySession {session}')

	session.close()

	print('done')
