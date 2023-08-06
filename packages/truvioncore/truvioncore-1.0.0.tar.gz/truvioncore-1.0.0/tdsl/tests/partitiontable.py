import unittest

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.sql.ddl import DDL
from sqlalchemy import event


# this is the example of DeclarativeMeta impl
# class DeclarativeMeta(type):
#     def __init__(cls, classname, bases, dict_, **kw):
#         if "_decl_class_registry" not in cls.__dict__:
#             _as_declarative(cls, classname, cls.__dict__)
#         type.__init__(cls, classname, bases, dict_)
#
#     def __setattr__(cls, key, value):
#         _add_attribute(cls, key, value)
#
#     def __delattr__(cls, key):
#         _del_attribute(cls, key)


class PartitionByYearMeta(DeclarativeMeta):
	def __new__(cls, clsname, bases, attrs, *, partition_by):

		@classmethod
		def get_partition_name(cls_, key):
			# 'measures' -> 'measures_2020' (customise as needed)
			return f'{cls_.__tablename__}_{key}'

		@classmethod
		def create_partition(cls_, key):
			if key not in cls_.partitions:
				Partition = type(
					f'{clsname}{key}',  # Class name, only used internally
					bases,
					{'__tablename__': cls_.get_partition_name(key)}
				)

				Partition.__table__.add_is_dependent_on(cls_.__table__)

				event.listen(
					Partition.__table__,
					'after_create',
					DDL(
						# For non-year ranges, modify the FROM and TO below
						f"""
                        ALTER TABLE {cls_.__tablename__}
                        ATTACH PARTITION {Partition.__tablename__}
                        FOR VALUES FROM ('{key}-01-01') TO ('{key + 1}-01-01');
                        """
					)
				)

				cls_.partitions[key] = Partition

			return cls_.partitions[key]

		# from SQAlalchemy docs on __table_args__
		# class MyClass(Base):
		# 	__tablename__ = 'sometable'
		# 	__table_args__ = (
		# 		ForeignKeyConstraint(['id'], ['remote_table.id']),
		# 		UniqueConstraint('foo'),
		# 		{'autoload': True}
		# 	)


		attrs.update(
			{
				# For non-RANGE partitions, modify the `postgresql_partition_by` key below
				'__table_args__': attrs.get('__table_args__', ()) + (dict(postgresql_partition_by=f'RANGE({partition_by})'),),
				'partitions': {},
				'partitioned_by': partition_by,
				'get_partition_name': get_partition_name,
				'create_partition': create_partition
			}
		)

		return super().__new__(cls, clsname, bases, attrs)


class MeasureMixin:
	# The columns need to be pulled out into this mixin
	# Note: any foreign key columns will need to be wrapped like this:

	@declared_attr
	def city_id(self):
		return Column(ForeignKey('cities.id'), not_null=True)

	log_date = Column(Date, not_null=True)
	peaktemp = Column(Integer)
	unitsales = Column(Integer)


class Measure(MeasureMixin, Base, metaclass=PartitionByYearMeta, partition_by='logdate'):
	__tablename__ = 'measures'


# Creating a new partition on the fly works like this:
# Make sure you commit any session that is currently open, even for select queries:
session.commit()

Partition = Measure.create_partition(2020)

if not engine.dialect.has_table(Partition.__table__.name):
	Partition.__table__.create(bind=engine)


class MyTestCase(unittest.TestCase):
	def test_something(self):
		self.assertEqual(True, False)


if __name__ == '__main__':
	unittest.main()
