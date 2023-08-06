

class LittleMeta(type):
	def __new__(cls, clsname, superclasses, attributedict):
		print("clsname: ", clsname)
		print("superclasses: ", superclasses)
		print("attributedict: ", attributedict)
		return type.__new__(cls, clsname, superclasses, attributedict)


class S:
	pass


class A(S, metaclass=LittleMeta):
	pass


class MetaclassTest(type):
	def __new__(cls, clsname, bases, attrs, *, keyword_here):

		print("clsname: ", clsname)
		print("bases: ", bases)
		print("attrs: ", attrs)

		@classmethod
		def get_partition_name(cls_, key):

			return 'get_partition_name called'

		attrs.update(
			{
				'__table_args__': 'this would be a __table_arg__',
				'partitions': {},
				'keyword_added': keyword_here,
				'get_partition_name': get_partition_name,
			}
		)

		return super().__new__(cls, clsname, bases, attrs)


class Mixin:
	mixin_int = -999


class Foo(Mixin, metaclass=MetaclassTest, keyword_here='I_ADD_A_KEYWORD'):
	pass


if __name__ == '__main__':

	f = Foo()
	print(f'{f} dict: {f.__dict__}')

	print(dir(f))

	print(f.mixin_int)
	print(f.partitions)
	print(f.keyword_added)
	print(f.__table_args__)
	print(f.get_partition_name('passing_key'))

	# from SQAlalchemy docs on __table_args__
	# class MyClass(Base):
	# 	__tablename__ = 'sometable'
	# 	__table_args__ = (
	# 		ForeignKeyConstraint(['id'], ['remote_table.id']),
	# 		UniqueConstraint('foo'),
	# 		{'autoload': True}
	# 	)

	# __table_args__ = (ForeignKeyConstraint(['id'], ['remote_table.id']), UniqueConstraint('foo'), {'autoload': True})

	# adding to attrs dict
	attrs = ('A','B',)
	partition_by = 'key_for_partition'
	# sqlalchemp tables args are a tuple or dict, for example
	newd = attrs.get('__table_args__', ()) + ( dict(postgresql_partition_by=f'RANGE({partition_by})' ), ),
	print(newd)
	import pprint
	pprint.pprint(newd)



# metaclasses changed
#
# https://www.python.org/dev/peps/pep-3115/
#
# >>> class MetaTable(type):
# ...     def __getattr__(cls, key):
# ...         temp = key.split("__")
# ...         name = temp[0]
# ...         alias = None
# ...         if len(temp) > 1:
# ...             alias = temp[1]
# ...         return cls(name, alias)
# ...
# >>> class Table(object, metaclass=MetaTable):
# ...     def __init__(self, name, alias=None):
# ...         self._name = name
# ...         self._alias = alias
# ...
# >>> d = Table
# >>> d.student__s
# <__main__.Table object at 0x10d7b56a0>