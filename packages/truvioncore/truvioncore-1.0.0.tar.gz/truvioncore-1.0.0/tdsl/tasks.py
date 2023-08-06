import os
import sys
import json
import datetime
import isodate
import threading
import uuid
from enum import IntEnum
from multiprocessing.managers import SyncManager
from collections import deque
from tdsl import *

__all__ = [
	'Task',
	'TaskList',
	'TaskListProctor',
	'TaskListProctorFactory',
	'DefaultTaskList',
	'TaskStatus'
]


class TaskStatus(IntEnum):
	CREATED = 0
	SUBMITTED = 1
	RECEIVED = 2
	RUNNING = 3
	SUCCEEDED = 4
	FAILED = 5


class TaskMeta(type):
	""" """

	def __new__(meta, classname, bases, classDict):
		return type.__new__(
			meta,
			classname,
			bases,
			classDict
		)

	def __pow__(self, data):
		"""
		t1 = Task ** srl_data
		"""
		return self.unserialise(data)


class Task(object, metaclass=TaskMeta):
	""" """

	def __init__(self, target, *args, **kwds):
		self._task_id = str(uuid.uuid4())
		self._target = target
		self._status = TaskStatus.CREATED
		self._args = args
		for k, v in kwds.items():
			k = 'id_' if k == 'id' else k
			setattr(self, k, v)
		self._date_created = datetime.datetime.now()

	@classmethod
	def unserialise(cls, serialised_data):
		d = json.loads(serialised_data)
		if d['cls'] != str(cls):
			raise Exception('Class mismatch')
		state = d['state']
		state['_date_created'] = isodate.parse_datetime(state['_date_created'])
		new_ = cls(state['_target'])
		for k, v in state.items():
			setattr(new_, k, v)
		return new_

	@property
	def id(self):
		""" deprecate this - don't shadow object.id"""
		return self._task_id

	@property
	def Id(self):
		return self._task_id
	
	@property
	def Target(self):
		return self._target

	@property
	def DateCreated(self):
		return self._date_created

	@property
	def TaskStatus(self):
		return self._status

	@TaskStatus.setter
	def TaskStatus(self, value):
		self._status = value
	
	def __str__(self):
		return '%s\t%s\t%s\t%s' % (
			self.Target, self.DateCreated, id(self), str(self.__dict__))

	def __json__(self, request):
		d = dict(self.__dict__)
		d['_date_created'] = d['_date_created'].isoformat()
		for k in d:
			if hasattr(d[k], '__json__'):
				d[k] = d[k].__json__(request)
		return dict(
			cls=str(self.__class__),
			state=d
		)

	def serialise(self, opr):
		return self.__json__(None)

	def __rpow__(self, opr):
		j = json.dumps(self.serialise(opr))
		return j


class TaskList(threading.Thread, Commander, Mixable):
	""" """

	def __init__(self, name='TaskList', mix_ins=None, *args, **kwds):
		threading.Thread.__init__(self, name=name)
		Commander.__init__(self, **kwds)
		self._new = deque()
		self._tasks = SynchronisedContainer()
		print(f'TaskList mixins {mix_ins}')
		if mix_ins and len(mix_ins) > 0:
			for mix in mix_ins:
				self.mixin(mix)

		# TODO: recursion problem
		# File
		# "/Users/mat/Documents/Pyaella3/dsl/__init__.py", line
		# 330, in __getattribute__
		# for m in inspect.getmembers(self):
		self.gel()


class TaskListProctor(SyncManager):
	""" """

	def __init__(self, name="TaskList", mix_ins=None, prefix='ask_', *args, **kwds):
		SyncManager.__init__(self)

		self._name = name
		self._mix_ins = mix_ins
		self._prefix = prefix
		self._args = args
		self._kwds = kwds

		x = []
		if mix_ins:
			for m in mix_ins:
				for attr in dir(m):
					if attr.startswith(prefix):
						x.append(attr)
		self.register(
			'TaskList',
			callable=TaskList,
			exposed=(x))


class TaskListProctorFactory(object):
	""" """
	__shared_state = {}

	def __init__(self, task_list=None, lock=None):
		self.__dict__ = self.__shared_state

		if task_list:
			self._task_list = task_list
			self._lock = lock

	@property
	def List(self):
		return self._task_list

	@property
	def Lock(self):
		return self._lock

	def __call__(self):
		return self.List, self.Lock,


class DefaultTaskList(Mix):

	def ask_add(self, task):
		id_ = id(task)
		self._new.append(id_)
		self._tasks[id_] = task
		with open('TaskList.txt', 'a') as f:
			f.write(str(task))
		return id_

	def ask_has(self, id_):
		return id_ in self._tasks

	def ask_get(self, id_=None):
		if id_:
			return self._tasks[id_]
		else:
			if self._new:
				id_ = self._new.pop()
				if id_ and id_ in self._tasks:
					return self._tasks[id_]

	def ask_close(self, task):
		id_ = id(task)
		if id_ in self._tasks:
			self._tasks.pop(id_)
