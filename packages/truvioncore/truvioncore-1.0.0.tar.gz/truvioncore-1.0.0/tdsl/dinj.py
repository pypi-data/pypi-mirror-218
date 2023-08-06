__author__ = 'mat mathews'
__copyright__ = 'Copyright (c) 2021 Entrust Funding'
__version__ = '0.0.1'

# print(f'. loading {__file__}')

import os
import sys
import yaml
import traceback
import inspect as inspect_
from textwrap import dedent
import unittest
from tdsl import *
from tdsl.codify import *

__here__ = os.path.abspath(os.path.dirname(__file__))


LogicalModelFlags = ['refl', 'expr', 'cntx', 'trck', 'dynamic', 'static',
					 'snippet', 'log', 'spoken', 'robotic', 'localize', 'record',
					 'statement', 'option', 'character', 'thread', 'scene']

ProtectedNodeNames = ['DOCUMENT']

EMBEDDED_TRIGGERS = ['GENERATE_REPORT_TRIGGER', 'ACTIVATE_TRANSFER_TRIGGER', 'TRANSFORM_TRIGGER', 'DATA_KEY_TRIGGER']

"""
Foo:
	This: 1
	Bar:
		ThisandThat: 2
FooB:
	attr_a: True
	InnerBar:
		InnerBar2:
			InnerBar3:
				Happy: True
				Sad:
					Maybe: False
FooC:
	InnerBar3:
		Different:
			InnerDifferent: [1,2,3,4,5]

>>>dinjL = Lexicon(parsable=test_path)
>>>for thing in dinjL.find_like('InnerBar3', only_lexical_tokens=True):
	print thing
>>>print dinjL.find_like('FooC')[0][1].items()
>>>dinjL = Lexicon(parsable=test_path)
>>>for thing in dinjL.find_like('InnerBar', only_lexical_tokens=True):
>>>    print thing
>>>print dinjL.find_like('FooC')[0][1].InnerBar3.Different.InnerDifferent

# Output
# ('FooC:InnerBar3', <dsl.dinj.FooC object at 0x10acf4310>)
#('FooB:InnerBar:InnerBar2:InnerBar3',<dsl.dinj.FooB object at 0x10acf43d0>)
#[('InnerBar3', <dsl.dinj.FooC object at 0x10acf4310>)]
#('FooC:InnerBar3', <dsl.dinj.FooC object at 0x10acede90>)
#('FooB:InnerBar', <dsl.dinj.FooB object at 0x10aceda50>)
#[1, 2, 3, 4, 5]

"""


print(f'module {__file__} loaded')


class Runtime(object):
	_instance = None

	def __new__(cls, opts=None, *args, **kwargs):
		"""
		Initialize configuration for global app settings and
		dependencies injections.
		"""

		# print(f'. Runtime __new__ called {opts}')
		# print(dir(inspect_))
		# curframe = inspect_.currentframe()
		# calframe = inspect_.getouterframes(curframe, 2)
		# print('caller name:', calframe[1][3])
		# for frameinfo in calframe:
		# 	print(f'. ---- {frameinfo}')
		
		if cls._instance is None:
			cls._instance = super(Runtime, cls).__new__(cls, *args, **kwargs)

			cls._opts = opts
			cls._config = Lexicon(parsable=cls._opts.CONFIG)
			_ = __borg_cls__('AppConfig')
			app_kseq = get_app_kseq(
				int(cls._config.App.AppId), get_master_kseq())
			d = dict(cls._config.App.items())
			d['AppKeySeq'] = app_kseq
			print(f'. loading config for app {cls._config.App.AppId} with key seq: {app_kseq}')
			cls._app_config = _(**d)

			cls._schema = __borg_lex__('ModelConfig')(parsable=cls._config.Resources.Schema)

		return cls._instance

	@property
	def OPTS(self):
		return self._opts

	@property
	def CONFIG(self):
		return self._config

	@property
	def APP_CONFIG(self):
		return self._app_config

	@property
	def SCHEMA(self):
		return self._schema

	@property
	def MODEL_MODULE_NAME(self):
		return self._config.Resources.Models


class DinjLoader(yaml.Loader):

	def __init__(self, stream):
		self._root = os.path.split(stream.name)[0]
		super(DinjLoader, self).__init__(stream)
		# print(f'DinjLoader.__init__ called')

	def include(self, node):
		filename = os.path.join(self._root, self.construct_scalar(node))
		with open(filename, 'r') as f:
			return yaml.load(f, DinjLoader)


DinjLoader.add_constructor('!include', DinjLoader.include)


def get_lexical_tokens(parsable=None, fromStr=None):
	""" """
	# d = yaml.load(fromStr if fromStr else open(parsable))
	# print(f"get_lexical_tokens called. parsable: {parsable}")
	if fromStr:
		d = yaml.load(fromStr)
	else:
		with open(parsable) as f:
			d = yaml.load(f, DinjLoader)

	objs = {}
	d2 = {}
	for k, v in d.items():
		if k.startswith('('):
			k, flags = parse_lgcl_mdl_rl_name(k)
			if flags:
				v['__rl_flags__'] = flags
		d2[k] = v
	for k, v in d2.items():
		oClz = type('%s' % k, (LexicalToken,), {})
		obj = oClz(parsable, **d2[k])
		objs[oClz.__name__] = obj
		# print(f'get_lexical_tokens objs[oClz.__name__] {oClz.__name__}')
	# print(f'returning new LexicalToken')
	return LexicalToken(parsable, **objs)


def parse_lgcl_mdl_rl_name(s):
	def clean_flag(flag):
		return (flag.strip()
				.replace(',', '')
				.replace(';', '')
				.replace(':', ''))

	if not s.replace(' ', '').endswith(')'):
		raise SyntaxError('This is not a Rule, expecting "):" ending. %s' % s)

	s = s.strip()[1:-1].strip()
	elems = [e.strip() for e in s.split(' ') if e]
	if len(elems) >= 1:
		flags = [clean_flag(flag) for flag in elems[1:]]
		flags = [flag for flag in flags if flag in LogicalModelFlags]
		return elems[0], tuple(flags)
	else:
		return elems[0], None


class LexicalToken(Container):
	"""
	"""

	def __init__(self, parsable=None, **kwds):
		# print(f'. LexicalToken.__init__ called parsable: {parsable}')
		Container.__init__(self, self.__class__, **kwds)
		self.__parsable = parsable

	def items(self, lxtn=None):
		"""
			returns .items()
		"""
		lxtn = self if lxtn == None else lxtn
		return \
			dict(
				[(k, v,) for k, v in lxtn.__dict__.items() if k in self._index]
			).items()

	def find(self, key, lxtn=None, only_lexical_tokens=True):
		raise NotImplementedError

	def find_like(self, key,
				  found=None, lxtn=None,
				  only_lexical_tokens=True,
				  eval_obj_name='startswith'):
		raise NotImplementedError

	def load(self, **kwds):
		"""
		"""
		self.__load()
		for k, v in kwds.items():
			setattr(self, k, v)

	def __load(self):

		if self.__parsable:
			self._lex = get_lexical_tokens(self.__parsable)
			for k, v in self._lex.__dict__.items():
				if type(k) == str and not k.startswith('_'):
					setattr(self, k, v)

	def __getstate__(self):
		"""
			remove refecences to dinj anonymous classes
			returns dict of parsable: self.parsable

		"""
		return {'__parsable': self.__parsable}

	def __setstate__(self, dict):
		"""
			reloads inner dinj anonymous classes
		"""
		self.__dict__['__parsable'] = dict['__parsable']
		if self.__dict__['__parsable'] != None:
			self.load()


class Lexicon(Container, Configures):
	""" """

	def __init__(self, parsable=None, **kwds):
		# print(f'. Lexicon.__init__ called parsable: {parsable}')
		Container.__init__(self, self.__class__, **kwds)
		if parsable:
			self._lex = get_lexical_tokens(parsable)
			for k, v in self._lex.__dict__.items():
				if type(k) == str and not k.startswith('_'):
					setattr(self, k, v)
			setattr(self, '__parsable', parsable)

	def find(self, key, lxtn=None, only_lexical_tokens=True):
		"""
			finds requested element
		"""
		r = None
		lxtn = self if lxtn == None else lxtn
		for k, v in lxtn.__dict__.items():
			if k == key:
				if not only_lexical_tokens or \
						(only_lexical_tokens and isinstance(v, LexicalToken)):
					return v
			elif isinstance(v, LexicalToken):
				r = self.find(key, lxtn=v)
				if r != None: return r
		return r

	def find_like(self,
				  key, found=None, lxtn=None,
				  only_lexical_tokens=False, eval_obj_name='startswith', previous=''):
		"""
			find desired LexicalTokens
		"""
		if found == None: found = []
		try:
			r = None
			lxtn = self._lex if not lxtn else lxtn
			cn = None
			for k, v in lxtn.__dict__.items():
				is_inst = isinstance(v, LexicalToken)
				if is_inst:
					if cn == None:
						cn = v.__class__.__name__
					elif cn != v.__class__.__name__:
						cn = v.__class__.__name__
						previous = ''
						cn = v.__class__.__name__
				previous += ':%s' % k if is_inst else ''
				if (eval_obj_name == 'contains'):
					if(key in k):
						if not only_lexical_tokens or \
								(only_lexical_tokens and isinstance(v, LexicalToken)):
							found.append(v)
					elif isinstance(v, LexicalToken):
						found = self.find_like(
							key, found, lxtn=v,
							only_lexical_tokens=only_lexical_tokens,
							eval_obj_name=eval_obj_name, previous=previous)
				else:
					if eval('k.%s("%s")' % (eval_obj_name, key)):
						if not only_lexical_tokens or \
								(only_lexical_tokens and is_inst):
							if is_inst:
								found.append((previous[1:], v,))
							else:
								found.append(v)
					elif isinstance(v, LexicalToken):
						found = self.find_like(
							key, found, lxtn=v,
							only_lexical_tokens=only_lexical_tokens,
							eval_obj_name=eval_obj_name, previous=previous)
			return found
		except Exception as e:
			print(traceback.format_exc())
			raise e




class BorgLexicon(Lexicon, Configures):
	__shared_state = {}
	"""
	"""

	def __init__(self, parsable=None, **kwds):
		self.__dict__ = self.__shared_state
		Lexicon.__init__(self, parsable=parsable, **kwds)


class Injectable(object):
	"""
	"""

	__here__ = os.path.abspath(__file__)
	__module_config__ = None
	__class_config = None

	@classmethod
	def load_di_config(cls):
		print(f"Injectable.load_di_config: __here__ {__here__}")
		fp = os.path.join(os.path.dirname(cls.__here__), '__config__.yaml')
		if os.path.exists(fp):
			cls.__module_config__ = Lexicon(parsable=fp)


# INSUFFERABLE MAGIC
def __borg_lex__(classname):
	"""
	:param classname: Name of the new class to generate and add to the __named__'d module
	:return: void
	"""
	cdef = dedent(
		'''
		class %(classname)s(Lexicon):
			__shared_state = {}
			def __init__(self, parsable=None, **kwds):
				self.__dict__ = self.__shared_state
				#print(f"generated class code {parsable} {kwds}")
				Lexicon.__init__(self, parsable=parsable, **kwds)
		''' % locals()
	)

	exec(cdef)
	# print(f'exec cdef {classname}')
	mobj = sys.modules[globals()['__name__']]
	# print(f'__borg_lex__ mojb {mobj}')
	setattr(mobj, classname, locals()[classname])

	mc = mobj.ModelConfig()
	# print(f'ModelConfig {mc} {mc.__dict__.items()}')

	return locals()[classname]


def __borg_cls__(classname):
	"""
	Creates a new borg class and adds to the dinj module
	"""
	cdef = dedent(
		'''
		class %(classname)s(object):
			__shared_state = {}
			def __init__(self, **kwds):
				self.__dict__ = self.__shared_state
				if kwds:
					for k,v in kwds.items():
						setattr(self, k, v)
		''' % locals()
	)
	exec(cdef)
	mobj = sys.modules[globals()['__name__']]
	setattr(mobj, classname, locals()[classname])
	return locals()[classname]

#
# class TestSetup(unittest.TestCase):
#
#
#     # def test_setup(self):
#     #     print("starting unittests, checking setup...")
#     #     self.assertEqual(True, True)
#
#     def test_injectable(self):
#
#         class Mock(Injectable):
#             pass
#
#         m = Mock()
#         Mock.load_di_config()
#
#         sl = m.__module_config__.find_like('This', only_lexical_tokens=False)
#         print(f"some_list result A: {sl} len {len(sl)}")
#         self.assertEqual(sl[0], 1)
#         self.assertEqual(sl[1], '2_Val')
#
#         sl = m.__module_config__.find_like('This', only_lexical_tokens=False, eval_obj_name = 'contains')
#         print(f"some_list result B: {sl} len {len(sl)}")
#         self.assertEqual(sl[2], '3_Val')
#
#         sl = m.__module_config__.find_like('Second', only_lexical_tokens=True, eval_obj_name = 'contains')
#         print(f"some_list result C: {sl} len {len(sl)}")
#
#         print(sl[0].__dict__)
#         print(type(sl[0]))
#         self.assertTrue(issubclass(sl[0].__class__, LexicalToken))
#
#         # sl = sl[0].find('ThatAndThis', only_lexical_tokens=False)
#         # print(f"some_list result D: {sl}")
#
#         # sl = sl[0].__module_config__.find_like('ThatAndThis', only_lexical_tokens=False)
#         # print(f"some_list result E: {sl}")
#
#         # sl = m.__module_config__.find_like('happy', only_lexical_tokens=True)
#         # print(f"some_list result: {sl}")
#         #
#         # # sl = m.__module_config__.find_like('SecondLevel',only_lexical_tokens=True)
#         # print(f"some_list result: {sl}")
#         #
#         # sl = m.__module_config__.find_like('InnerBar2')
#         #
#         # print(f"some_list result: {sl}")
#
#         sl = m.__module_config__.find_like('LastDifferent', only_lexical_tokens=False)
#         print(f"some_list result for LastDifferent: {sl} len {len(sl[0])}")
#
#         'done'
