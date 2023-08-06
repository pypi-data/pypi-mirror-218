__author__ = 'mat mathews'
__version__ = '0.1.0'

import sys as _sys
import time
import math
import types
import random
import string
import urllib.request, urllib.parse, urllib.error
import http.client
import inspect
import datetime
import traceback
import functools
import threading
import unicodedata
from itertools import *
from textwrap import dedent
from keyword import iskeyword
from hashlib import sha224, sha256
from operator import itemgetter as _itemgetter
from keyword import iskeyword as _iskeyword
from collections.abc import Mapping as _Mapping
from six import exec_, string_types

# print(f'module {__file__} loaded')

__all__ = [
	'RSRVD_CLS_METH_NAMES',
	'RSRVD_OBJ_METH_NAMES',
	'RSRVD_PYAELLA_NAMES',
	'Configures',
	'Configurable',
	'Affector',
	'Affectable',
	'ExpressibleException',
	'PyaellaException',
	'CausalException',
	'CausalSpaceException',
	'CausalProgrammingErr',
	'CausalExpressorException',
	'CausalCallbackErr',
	'Mix',
	'Mixable',
	'Container',
	'SynchronisedContainer',
	'_GelMethod',
	'register_decorator',
	'memoize',
	'memoize_exp',
	'argument_bind_params',
	'ExpFilter',
	'flt_', 'ret_',
	'accepts_expfilter',
	'simple_timestamp',
	'url_exists',
	'Commander',
	'CommanderDelegate',
	'CommanderDelegateWithMixIns',
	'recordtype',
	'grouper',
	'dict_to_slices',
	'seeked_batch',
	'op',
	'MsgChannelNames',
	'SyncChannelState'
]

RSRVD_CLS_METH_NAMES = [
	'__init__', '__new__', '__doc__', '__module__', '__main__', '__slots__',
	'__metaclass__',
]

RSRVD_OBJ_METH_NAMES = [
	'__abs__', '__add__', '__and__', '__call__', '__cmp__', '__coerce__',
	'__contains__', '__delitem__', '__delslice__', '__div__', '__divmod__',
	'__eq__', '__float__', '__floordiv__', '__ge__', '__getitem__',
	'__getslice__', '__gt__', '__hash__', '__hex__', '__iadd__', '__iand__',
	'__idiv__', '__idivmod__', '__ifloordiv__', '__ilshift__', '__imod__',
	'__imul__', '__int__', '__invert__', '__ior__', '__ipow__', '__irshift__',
	'__isub__', '__iter__', '__itruediv__', '__ixor__', '__le__', '__len__',
	'__long__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__',
	'__neg__', '__oct__', '__or__', '__pos__', '__pow__', '__radd__',
	'__rand__', '__rdiv__', '__rdivmod__', '__reduce__', '__reduce_ex__',
	'__repr__', '__reversed__', '__rfloorfiv__', '__rlshift__', '__rmod__',
	'__rmul__', '__ror__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__',
	'__rtruediv__', '__rxor__', '__setitem__', '__setslice__', '__sub__',
	'__truediv__', '__xor__', 'next',
]

RSRVD_PYAELLA_NAMES = [
	'__schema__', '__cls_proxy__', '__tablename__',
]


class ExpressibleException(Exception):
	pass


class TooManyRequests(Exception):
	pass


class Configures:
	""" marking type """


class Configurable:
	""" marking type """


class Affector:
	""" class that supports context
		manager, planner
	"""

	def __lshift__(self, planner=None, **kws):
		return self

	def __mod__(self, other):
		raise NotImplemented


class Affectable:
	""" marking type """


def reformat_named_fields_str(llc):
	""" """
	llc = llc.replace('\t', ' ').replace('\n', ' ').strip(' ')
	llc = llc.replace('-', '_')
	llc = llc.replace('(', '_')
	llc = llc.replace(')', '_')
	return llc


def grouper(iterable, n, fillvalue=None):
	args = [iter(iterable)] * n
	return zip_longest(*args, fillvalue=fillvalue)


def dict_to_slices(dict_, size=10000):
	it = iter(dict_)
	for i in range(0, len(dict_), size):
		yield {k:dict_[k] for k in islice(it, size)}


def seeked_batch(n=100, b=10):
	bsp = []
	end = None
	for i in range(0, int(n / b)):
		start = b * i
		end = start + b
		bsp.append((start,end,))
	if n % b > 0:
		bsp.append((end,None))
	return bsp


def simple_timestamp(datetime_=None, now=False):
	if now:
		datetime_ = datetime.datetime.now()
	return str(datetime_).replace('-', '').replace(':', '') \
		.replace('.', '_').replace(' ', '_')


def url_exists(site, path):
	try:
		conn = http.client.HTTPConnection(site)
		conn.request('HEAD', path)
		response = conn.getresponse()
		conn.close()
		return response.status == 200
	except:
		print(traceback.format_exc())
		return False


class Mergeable:
	"""
	Allows the merging of two objects' values
	"""

	def define_attribute(self, attribute_name, direction, nullable):
		if hasattr(self, '_mergeable_fields'):
			self._mergeable_fields[attribute_name] = direction, nullable,
		else:
			self._mergeable_fields = {
				attribute_name: (direction, nullable,)
			}

	def merge_value(self, attribute, value):
		#
		def n_(v, nullable):
			return True \
				if v in [
				None, '', ' ', 'None', 'NULL', 'Null'
			] and nullable \
				else False  #

		direction = 'RIGHT'  # default, allow write
		nullable = True
		if hasattr(self, '_mergeable_fields'):
			if attribute in self._mergeable_fields:
				direction, nullable = self._mergeable_fields[attribute]
				try:
					v = getattr(self, attribute)
					if v:
						return v \
							if direction == 'LEFT' and \
							   not (nullable or not value and n_(v, nullable)) \
							else value if nullable else v  #
				except:
					pass
		return value


class PyaellaException(Exception):
	pass


class op(object):
	"""deprecated"""

	json = 'op.json'
	jsonp = 'op.jsonp'
	id_json = 'op.id_json'
	raw = 'op.raw'
	k_v = 'op.k_v'


class Cast(object):
	""" example
		jsonData = Cast.json **task
	"""
	json = 'Cast.json'
	jsonp = 'Cast.jsonp'
	id_json = 'Cast.id_json'
	raw = 'Cast.raw'
	k_v = 'Cast.k_v'


class MsgChannelNames(object):

	TaskEvents = 'task_events_channel'
	TaskProcessIn = 'task_process_in'
	TaskProcessOut = 'task_process_out'
	NotificationIn = 'notification_in'
	NotificationOut = 'notification_out'
	BusinessProcessIn = 'business_process_in'
	BusinessProcessOut = 'business_process_out'
	ReportProcessIn = 'report_process_in'
	ReportProcessOut = 'report_process_out'
	AssetProcessIn = 'asset_process_in'
	AssetProcessOut = 'asset_process_out'
	SynchronisedTasks = 'synchronised_tasks_channel'


class SyncChannelState(object):

	AQUIRE = 'SYNC:CHANNEL:STATE:LOCK:AQUIRE'
	WARM = 'SYNC:CHANNEL:STATE:LOCK:WARM'
	PROCESS = 'SYNC:CHANNEL:STATE:LOCK:PROCESS'
	STANDBY = 'SYNC:CHANNEL:STATE:LOCK:STANDBY'
	RELEASE = 'SYNC:CHANNEL:STATE:LOCK:RELEASE'

	@classmethod
	def format(cls, state, key):
		if hasattr(cls, state.split(':')[-1]):
			return f'{state}:{key.upper()}'
		raise Exception(f'Invalid SyncChannelState {state}')




class CausalException(Exception):

	def __init__(self, s, errno=1, **kw):
		Exception.__init__(self, s)
		for k, v in list(kw.items()):
			setattr(self, k, v)
		self.errno = errno

	def __gt__(self, other):
		return self.errno > other

	def __ge__(self, other):
		return self.errno >= other


class CausalSpaceException(CausalException):
	pass


class CausalExpressorException(CausalException):
	pass


class CausalProgrammingErr(Exception):
	pass


class CausalCallbackErr(Exception):
	pass


class Mix(object):
	""" marker interface to Mix in Mixables """

	def __init__(self):
		pass

	def mixit(self):
		pass

	def gel(self):
		pass


class _GelMethod(object):
	"""
		call all methods that
		are gelled into the Mixable
		returning a tuple of results
	"""

	def __init__(self, gels):
		self.__gs = gels

	def __call__(self, *args, **kwds):
		r = []
		for f in self.__gs:
			r.append(f(*args, **kwds))
		return tuple(r)


class Mixable(object):
	""" """

	def mixin(self, mixingClass, antecedent=False):
		if (issubclass(mixingClass, Mix) == False):
			raise Exception(
				'To mix classes in Mixables ' +
				'the mixing class must be an Mix subclass, %s' % str(mixingClass))
		if antecedent:
			if mixingClass not in self.__class__.__bases__:
				self.__class__.__bases__ = \
					(mixingClass,) + self.__class__.__bases__
		else:
			# baseClasses = list(mixingClass.__bases__)
			# baseClasses.reverse()
			# for baseClass in baseClasses:
			#   Mix(self.__class__, baseClass)
			# Install the mix-in methods into the class
			for n in dir(mixingClass):
				if not n.startswith('__'):
					# no privates
					member = getattr(mixingClass, n)
					if type(member) is types.MethodType:
						member = member.__func__
						if n.startswith('gel'):
							# TODO: metaclasses? I don't like instantiating
							# this object just to get the name of the instance
							mc = mixingClass()
							n += ('_' + str(mc.__class__.__name__))
					setattr(self.__class__, n, member)
		# mix in the mix's required members
		self.mixit()

	def __getattribute__(self, name):
		if name == 'gel':
			gels = []
			for m in inspect.getmembers(self):
				if inspect.ismethod(m[1]) and m[0].startswith('gel_'):
					gels.append(m[1])
			if len(gels) > 0:
				return _GelMethod(gels)
		return object.__getattribute__(self, name)


class Container(object):
	""" an object that dynamically collects and sets attribute
		from a class definition and keywords on __init__.

		future: supporting exclusion of attributes passed based on name
	"""

	def __init__(self, klass, **kwds):
		# print(f'. Container.__init__ called klass: {klass}')
		klz = self.__class__.__bases__[0] \
			if klass == None \
			else klass
		self._index = {}
		self._set_inners(klz, **kwds)
		self.collect()

	def collect(self, excludes=None):
		self._index = \
			[k for k in list(self.__dict__.keys())
			 if k not in excludes and not k.startswith('_')] \
				if excludes != None \
				else [k for k in list(self.__dict__.keys()) if not k.startswith('_')]

	def __getitem__(self, key):
		if type(key) == int:
			if key in self._index:
				return self._index[key], self.__dict__[self._index[key]]
		if key in self.__dict__:
			return self.__dict__[key]

	def __setitem__(self, key, value):
		self.__dict__[key] = value

	def __delitem__(self, key):
		if key in self.__dict__:
			del self.__dict__[key]

	def __contains__(self, key):
		return key in self.__dict__

	def _set_inners(self, klass, **kwds):
		try:
			for k, v in list(kwds.items()):
				if type(v) == dict:
					setattr(self, k, klass(**v))
				else:
					setattr(self, k, v)
		except:
			print(traceback.format_exc())


class SynchronisedContainer(object):
	""" """

	def __init__(self):
		self._lock = threading.Lock()
		self._d = {}

	def pop(self, key):
		with self._lock:
			return self._d.pop(key)

	def has_key(self, key):
		return self.__contains__(key)

	def __getitem__(self, key):
		with self._lock:
			return self._d[key]

	def __setitem__(self, key, value):
		with self._lock:
			self._d[key] = value

	def __delitem__(self, key):
		with self._lock:
			del self._d[key]

	def __contains__(self, key):
		with self._lock:
			return key in self._d

	def __len__(self):
		return len(list(self._d.keys()))

	def __repr__(self):
		return self._d.__repr__()

	def __str__(self):
		return self._d.__str__()


class StrictList(list):
	""" list with a limit, pops on capacity """

	def __init__(self, limit=11):
		""" limit default = 11 """

		super(list, self).__init__()
		self._limit = limit

	def append(self, item):
		if (len(self) == self._limit):
			self.pop(0)
		list.append(self, item)


def register_decorator(decorator):
	""" """

	def wrapping_deco(func):
		r = decorator(func)
		r.decorator = wrapping_deco
		r.original = func
		return r

	wrapping_deco.__name__ = decorator.__name__
	wrapping_deco.__doc__ = decorator.__doc__

	return wrapping_deco


def memoize(func):
	""" """

	cache = {}

	@functools.wraps(func)
	def wrapper(*args, **kw):
		key = (args, frozenset(list(kw.items())))
		if key in cache: return cache[key]
		result = func(*args, **kw)
		cache[key] = result
		return result

	return wrapper


def memoize_exp(expiration=None):
	""" Memoize with an expiration time (in seconds) """

	cache = {}

	def wrap(func):
		def wrapper(*args, **kw):
			key = (args, frozenset(list(kw.items())))
			if key in cache:
				age = cache[key][1]
				if (time.time() - age) < expiration:
					return cache[key][0]
			result = func(*args, **kw)
			cache[key] = (result, time.time())
			return result

		return wrapper

	return wrap


def argument_bind_params(func):
	"""
	@argument_bind_params

	"""

	@functools.wraps(func)
	def wrapper(*args, **kw):
		doc_args, _, _, _ = inspect.getargspec(func)
		bp = dict(list(zip(doc_args, args)))
		kw['bind_params'] = bp
		try:
			kw['bind_params'].pop('self')
		except:
			pass
		result = func(*args, **kw)
		return result

	return wrapper


class ExpFilter(object):
	"""
		Example ExpFilter
		
		class Foo(ExpFilter):
			pass
		class Bar(ExpFilter):
			def __init__(self, who, what, where, when, why):
				ExpFilter.__init__(self, who, what, where, when, why)
		class TestExpressible(object):
			@accepts_expfilter
			def __mod__(self, other, **kwds):
				def foo_func(*args):
					print 'Foo Func called',
						dir(args[0]), args[0]._kwds, args[0]._args
				def sad_func(*args):
					print 'Bar Func called', dir(args[0]),
						args[0]._kwds, args[0]._args
				dispatch = {
					'Foo':foo_func,
					'Bar':bar_func
				}
				try:
					dispatch[kwds.keys()[0]](kwds[kwds.keys()[0]])
				except KeyError:
					raise

		TestExpressible() % Bar(1,2,3,4,5)
	"""

	def __init__(self, *args, **kwds):
		""" """
		self._args = args
		self._kwds = kwds
		argspec, _, _, _ = inspect.getargspec(self.__init__)
		bp = list(zip(argspec[1:], args))
		self._kwds['bound_args'] = bp

	@property
	def ReturnType(self):
		return self._kwds['rtype_'] if 'rtype_' in self._kwds else None


def flt_(*args, **kwds):
	type_ = ExpFilter if 'type_' not in kwds else kwds['type_']
	return type_(args, kwds)


def ret_(rtype_, amb_=None, *args, **kwds):
	return rtype_(amb_=amb_, *args, **kwds)


def accepts_expfilter(func):
	@functools.wraps(func)
	def wrapper(*args, **kwds):
		obj = args[1] if len(args) > 1 else args[0]
		if type(obj) == type and (type(obj) == ExpFilter or \
								  issubclass(obj, ExpFilter)):
			kwds[obj.__name__] = obj
		elif isinstance(obj, ExpFilter):
			kwds[obj.__class__.__name__] = obj
		else:
			raise ExpressibleException('ExpFilter required')
		result = func(*args, **kwds)
		return result

	return wrapper


class ThrottledCondition(threading.Condition):
	'''
		Condition object to notify a requesting process
		whether or not a new Thread can be created once
		the Condition has been acquired.

		# if condition has too many
		# tracked threads, exception is
		# thrown
		with condition:
			if condition.increase(target, *args):
				new tracked thread started
			else:
				thread was not started
				second check on limit
				TODO:
				will be adding check on waiters
	'''

	def __init__(self, limit=10, pass_cards=None, lock=None, verbose=None):
		# TODO: check for vebose
		# threading.Condition.__init__(self, lock=lock, verbose=None)
		threading.Condition.__init__(self, lock=lock)
		self.__requesters = []
		self.__limit = limit
		self.__pass_cards = pass_cards if pass_cards else []
		self.__denied = set()
		self._tcLock = threading.Lock()

	def set_pass_cards(self, thread_name):
		self.__pass_cards.append(thread_name)

	@property
	def pass_cards(self):
		return self.__pass_cards

	def can_increase(self):
		return len(self.__requesters) < self.__limit

	def increase(self, target, callable_fctry=None, *args):
		if len(self.__requesters) < self.__limit:
			if callable_fctry:
				# TODO
				#
				# t = callable_fctry(target, *args)
				pass
			if (type(target) == threading.Timer or
					type(target) == threading.Thread):
				t = target
			elif callable(target):
				t = threading.Thread(
					name=sha224(
						'%s%s' % (random.randint(0, 65536), str(target))) \
						.hexdigest(),
					target=target, *args)
			else:
				raise Exception('Target must be callable or a Thread')
			t.start()
			self.__requesters.append(t.name)
			return True
		return False

	def close(self, name=None):
		name = threading.currentThread().name if name == None else name
		if name in self.__requesters:
			self.__requesters.remove(name)
			if name in self.__denied:
				self.__denied.remove(name)

	def len_requestors(self):
		return len(self.__requesters)

	# def len_waiters(self):
	#     return len(self._Condition__waiters)

	def __enter__(self):
		with self._tcLock:
			owner = threading.currentThread()
			if owner.name not in self.__pass_cards:
				if (owner.name not in self.__requesters and
						len(self.__requesters) >= self.__limit):
					# print 'can not acquire requests', \
					#   len(self.__requestors),\
					#   str(self.__limit), \
					#   (owner.name in self.__requestors), \
					#   owner.name, str(self.__requestors), \
					#   str(self.__pass_cards)
					self.__denied.add(owner.name)
					raise TooManyRequests(
						'Can not acquire, too many requests %s %s %s %s',
						len(self.__requesters),
						str(self.__limit),
						owner.name, (owner.name in self.__requesters))
			return self._Condition__lock.__enter__()

	def __exit__(self, *args):
		return self._Condition__lock.__exit__(*args)


class Commander(object):
	""" """

	def __init__(self, prefix='ask_', **kwds):
		self._prefix = prefix
		self._commanderId = random.Random()
		for k, v in kwds.items():
			setattr(self, k, v)

	@property
	def Prefix(self):
		return self._prefix

	@property
	def Commands(self):
		return self.__dict__.items()

	def ask_identify(self, *args, **kwds):
		stack = inspect.stack()[0]
		print('Commander_%s with_exposed(%s, %s) id %s and id %s' % (
			stack, str(args), str(kwds), str(self),
			str(self._commanderId)))


class _DelegatedMethod(object):
	"""
		idea of this class was lifted from Pyro.core.
		might put a async process here in __call__
	"""

	def __init__(self, f, name):
		self.__f = f
		self.__name = name

	def __call__(self, *args, **kwds):
		return self.__f(*args, **kwds)


class CommanderDelegate(object):
	""" """

	def __init__(self, commander, *args, **kwds):
		self._dispatchMap = {}
		if type(commander) == object:
			self._commander = commander
		else:
			self._commander = commander(*args, **kwds)
		for m in inspect.getmembers(self._commander):
			if (inspect.ismethod(m[1]) and
					m[0].startswith(self._commander.Prefix)):
				self._dispatchMap[m[0]] = m[1]

	def __getattribute__(self, name):
		d = object.__getattribute__(self, '_dispatchMap')
		if d.has_key(name):
			return _DelegatedMethod(d[name], name)
		return object.__getattribute__(self, name)


class CommanderDelegateWithMixIns(CommanderDelegate):
	""" """

	def __init__(self, commander, mix_ins, *args, **kwds):
		self._dispatchMap = {}
		self._commander = commander(mix_ins=mix_ins, *args, **kwds)
		for m in inspect.getmembers(self._commander):
			if (inspect.ismethod(m[1]) and
					m[0].startswith(self._commander.Prefix)):
				self._dispatchMap[m[0]] = m[1]

	def __getattribute__(self, name):
		d = object.__getattribute__(self, '_dispatchMap')
		if d.has_key(name):
			return _DelegatedMethod(d[name], name)
		return object.__getattribute__(self, name)


NO_DEFAULT = object()


# Keep track of fields, both with and without defaults.
class _Fields(object):
	def __init__(self, default):
		self.default = default
		self.with_defaults = []  # List of (field_name, default).
		self.without_defaults = []  # List of field_name.

	def add_with_default(self, field_name, default):
		if default is NO_DEFAULT:
			self.add_without_default(field_name)
		else:
			self.with_defaults.append((field_name, default))

	def add_without_default(self, field_name):
		if self.default is NO_DEFAULT:
			# No default. There can't be any defaults already specified.
			if self.with_defaults:
				raise ValueError(
					"field {0} without a default follows fields "
					"with defaults".format(field_name)
				)
			self.without_defaults.append(field_name)
		else:
			self.add_with_default(field_name, self.default)


# Used for both the type name and field names. If is_type_name is
#  False, seen_names must be provided. Raise ValueError if the name is
#  bad.
def _check_name(name, is_type_name=False, seen_names=None):
	if len(name) == 0:
		raise ValueError(
			"Type names and field names cannot be zero " "length: {0!r}".format(name)
		)
	if not all(c.isalnum() or c == "_" for c in name):
		raise ValueError(
			"Type names and field names can only contain "
			"alphanumeric characters and underscores: "
			"{0!r}".format(name)
		)
	if _iskeyword(name):
		raise ValueError(
			"Type names and field names cannot be a keyword: " "{0!r}".format(name)
		)
	if name[0].isdigit():
		raise ValueError(
			"Type names and field names cannot start with a "
			"number: {0!r}".format(name)
		)

	if not is_type_name:
		# these tests don't apply for the typename, just the fieldnames
		if name in seen_names:
			raise ValueError("Encountered duplicate field name: " "{0!r}".format(name))

		if name.startswith("_"):
			raise ValueError(
				"Field names cannot start with an underscore: " "{0!r}".format(name)
			)


# Validate a field name. If it's a bad name, and if rename is True,
#  then return a 'sanitized' name. Raise ValueError if the name is bad.
def _check_field_name(name, seen_names, rename, idx):
	try:
		_check_name(name, seen_names=seen_names)
	except ValueError as ex:
		if rename:
			return "_" + str(idx)
		else:
			raise

	seen_names.add(name)
	return name


def _default_name(field_name):
	# Can't just use _{0}_default, because then a field name '_0'
	#  would give a default name of '__0_default'. Since it begins
	#  with 2 underscores, the name gets mangled.
	return "_x_{0}_default".format(field_name)


def recordtype(typename, field_names, default=NO_DEFAULT, rename=False, use_slots=True):
	# field_names must be a string or an iterable, consisting of fieldname
	#  strings or 2-tuples. Each 2-tuple is of the form (fieldname,
	#  default).

	fields = _Fields(default)

	_check_name(typename, is_type_name=True)

	if isinstance(field_names, string_types):
		# No per-field defaults. So it's like a namedtuple, but with
		#  a possible default value.
		field_names = field_names.replace(",", " ").split()

	# If field_names is a Mapping, change it to return the
	#  (field_name, default) pairs, as if it were a list
	if isinstance(field_names, _Mapping):
		field_names = field_names.items()

	# Parse and validate the field names.  Validation serves two
	#  purposes: generating informative error messages and preventing
	#  template injection attacks.

	# field_names is now an iterable. Walk through it,
	# sanitizing as needed, and add to fields.

	seen_names = set()
	for idx, field_name in enumerate(field_names):
		if isinstance(field_name, string_types):
			field_name = _check_field_name(field_name, seen_names, rename, idx)
			fields.add_without_default(field_name)
		else:
			try:
				if len(field_name) != 2:
					raise ValueError(
						"field_name must be a 2-tuple: " "{0!r}".format(field_name)
					)
			except TypeError:
				# field_name doesn't have a __len__.
				raise ValueError(
					"field_name must be a 2-tuple: " "{0!r}".format(field_name)
				)
			default = field_name[1]
			field_name = _check_field_name(field_name[0], seen_names, rename, idx)
			fields.add_with_default(field_name, default)

	all_field_names = fields.without_defaults + [
		name for name, default in fields.with_defaults
	]

	# Create and fill-in the class template.
	argtxt = ", ".join(all_field_names)
	quoted_argtxt = ", ".join(repr(name) for name in all_field_names)
	if len(all_field_names) == 1:
		# special case for a tuple of 1
		quoted_argtxt += ","
	initargs = ", ".join(
		fields.without_defaults
		+ [
			"{0}={1}".format(name, _default_name(name))
			for name, default in fields.with_defaults
		]
	)
	reprtxt = ", ".join("{0}={{{0}!r}}".format(f) for f in all_field_names)
	dicttxt = ", ".join("{0!r}:self.{0}".format(f) for f in all_field_names)

	# These values change depending on whether or not we have any fields.
	if all_field_names:
		inittxt = "; ".join("self.{0}={0}".format(f) for f in all_field_names)
		eqtxt = "and " + " and ".join(
			"self.{0}==other.{0}".format(f) for f in all_field_names
		)
		itertxt = "; ".join("yield self.{0}".format(f) for f in all_field_names)
		tupletxt = "(" + ", ".join("self.{0}".format(f) for f in all_field_names) + ")"
		getstate = "return " + tupletxt
		setstate = tupletxt + " = state"
	else:
		# No fields at all in this recordtype.
		inittxt = "pass"
		eqtxt = ""
		itertxt = "return iter([])"
		getstate = "return ()"
		setstate = "pass"

	if use_slots:
		slotstxt = "__slots__ = _fields"
	else:
		slotstxt = ""

	template = """class {typename}(object):
		"{typename}({argtxt})"

		_fields = ({quoted_argtxt})
		{slotstxt}

		def __init__(self, {initargs}):
			{inittxt}

		def __len__(self):
			return {num_fields}

		def __iter__(self):
			{itertxt}

		def _asdict(self):
			return {{{dicttxt}}}

		def __repr__(self):
			return "{typename}(" + "{reprtxt}".format(**self._asdict()) + ")"

		def __eq__(self, other):
			return isinstance(other, self.__class__) {eqtxt}

		def __ne__(self, other):
			return not self==other

		def __getstate__(self):
			{getstate}

		def __setstate__(self, state):
			{setstate}\n""".format(
		typename=typename,
		argtxt=argtxt,
		quoted_argtxt=quoted_argtxt,
		initargs=initargs,
		inittxt=inittxt,
		dicttxt=dicttxt,
		reprtxt=reprtxt,
		eqtxt=eqtxt,
		num_fields=len(all_field_names),
		itertxt=itertxt,
		getstate=getstate,
		setstate=setstate,
		slotstxt=slotstxt,
	)

	# Execute the template string in a temporary namespace.
	namespace = {}
	# Add the default values into the namespace.
	for name, default in fields.with_defaults:
		namespace[_default_name(name)] = default

	try:
		exec_(template, namespace, namespace)
	except SyntaxError as e:
		raise SyntaxError(e.message + ":\n" + template)

	# Find the class we created, set its _source attribute to the
	#   template used to create it.
	cls = namespace[typename]
	cls._source = template

	# For pickling to work, the __module__ variable needs to be set to
	#  the frame where the named tuple is created.  Bypass this step in
	#  enviroments where sys._getframe is not defined (Jython for
	#  example).
	if hasattr(_sys, "_getframe") and _sys.platform != "cli":
		cls.__module__ = _sys._getframe(1).f_globals.get("__name__", "__main__")

	return cls


'''
	#
	def run(self):
		try:
			self.__st_chk = StateCheck(self, self._exec_f)
			self.__st_chk.start()
			if self.__mx_current in [None, -1, 0]:
				self.__mx_current = 2
			self.__snk = \
				Sink(self.__mx_current,
						self.__snk_sphn_f, prc_name=self._attrs.Name)   
			if self.__snk_srt_k:    
				self.__snk.set_sortkey(self.__snk_srt_k)
			dq_lmt = int(self._di.DequeLimit)
			self._copySpawnQ = deque()

			sb = self.__findSubLock()
			if isinstance(sb, ThrottledCondition):
				sb.set_pass_card(threading.currentThread().name)
				sb.set_pass_card(self.__st_chk.name)
				sb.set_pass_card(self.__snk._dst.name)

			self._started = True

			#
			while(not self._go.is_set()):
				sleepFlags = []
				try:
					# poll for callbx events, close tasks requests
					try:
						for i in range(0, dq_lmt):
							if self._childConn.poll(): # was a 1 sec timeout
								msg = self._childConn.recv()
								if type(msg)==TaskStateMsg:
									# task should be closed
									# spawn off a thread to close this task
									ctt = None
									with self._taskRegLock:
										ctt = self._closeTaskThreadCls(
											msg,
											closeM=self._closeTaskThreadableM,
											parent=self)
									ctt.start()
								elif type(msg)==str:
									if msg=='STOP':
										# time to stop processing
										self._go.set()
										break
								else:
									try:
										# event for internal process
										self._exec_f(msg)
									except:
										pass #ignore    
					except Exception, msgPipeE:
						pass #ignore
					# pop copy processes from queue
					try:
						if (self._copySpawnQ and
							len(self._copySpawnQ) > 0):
							while(self._currentConcurrentTasks 
													< self.__mx_current):
								c = self._copySpawnQ.pop()
								c.start()
								self._callbkQCalled += 1
								self._currentConcurrentTasks += 1

						if len(self._copySpawnQ) > 0:
							sleepFlags.append(False)

					except Exception, scq:
						pass

					if self._currentConcurrentTasks > 1:
						time.sleep(random.randint(0, 
							self._currentConcurrentTasks \
								if self._currentConcurrentTasks \
								else 5)*.2)
					self._balance -= 1
					if self._should_get_next_task():
						# attempt a get next from TaskManager
						try:
							n = []
							eos = {}
							while len(n) < dq_lmt:
								tasksReceived = []
								with self._taskRegLock:
									for i in range(0, dq_lmt):
										for taskType in self._taskTypesHandled:
											task = self._taskReg.get_next_task(
													taskType, self.attrs.name)
											if task != None:
												tasksReceived.append(task)
											else:
												eos[taskType] = True
								# release the lock on registry
								if len(tasksReceived) > 0:
									sleepFlags.append(False)
									for task in tasksReceived:
										if self.handle_event:
											g = True
											try:
												if self.handle_event(task):
													n.append(task)
											except TooManyRequests, tmr:
												g = False
												time.sleep(.5)
												break
								else:
									break
							if len(n) > 0:
								with self._taskRegLock:
									for task in n:
										self._taskReg.confirm_request(
													task.Type, task.Id)
							if True in eos.values():
								for taskType in eos:
									self._taskReg.seek(taskType, 0) # reset
									time.sleep(.5)
						except Exception, tre:
							self._process_exc(tre, bunyan.ERROR)

					# poll for copy callbacks
					if(self._balance != 0):
						self._balance -= 1
						# not every RGzcProcess subclass
						if self._callbkQ != None:
							try:
								deqd = []
								while not self._go.is_set():
									try:
										for i in range(0,dq_lmt*5):
											d = self._callbkQ.get(timeout=1)
											if d:
												deqd.append(d)
										#while len(deqd) < dq_lmt*5:
										#   d = self._callbkQ.get(timeout=1)
										#   deqd.append(d)
										break
									except:
										break
								try:
									if len (deqd) > 0:
										callBkRes = self._copy_callbk(deqd)
										self.__snk.update(decr=len(deqd))
										#self._callbkQCalled += len(deqd)
										sleepFlags.append(False)
									else:
										pass
								except Exception, ce:
									print('Caught exception', ce)
							except Exception, qe:
								print('Caught exception', qe
						if self._pulsedFunc:
							# call main pulsed function from the child process
							self._pulsedFunc()
						self.background_poll()  
					#
					else:
						self._balance=self._execFListBalance
						try:
							for f in self._execFuncList:
								f()
						except Exception, ie:
							print('Caught exception', ie)
						#time.sleep(self._pulse)
				except TooManyRequests:pass     
				except Exception, e:
					print('Caught exception', e)
					self._Errors += 1
					if self._Errors >= 3:
						raise Exception(
							'CRITICAL! Too many errors. %s - Raising %s.%s()'%(
												self.__class__.__name__, '', e)
						)
				if False not in sleepFlags:
					self._sleep = (self._sleep + 1) \
						if(self._sleep 
							< 8 and self._currentConcurrentTasks == 0) else 1
					time.sleep(self._sleep)
				else:
					time.sleep(.003)
			else:
				# TODO: Add closing While loop logic.. shutdown cleanup, etc..
				self.__st_chk.shutdown()
				self.__st_chk.join()
				try:
					self.ripeQ.close()
				except Exception, e:
					pass
		except Exception, oe:
			self._process_exc(oe,
				bunyan.ERROR,
				'In Outer Except. Will Attempt to Fail Task...')
			m = 'Caught Exception %s from %s.%s() - Failing Task'%(
				oe, self.__class__.__name__, '')
			if task:
				self._fail_task(task, m)
			return False
'''
