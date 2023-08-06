import sqlalchemy
from sqlalchemy import *
from sqlalchemy.schema import *
from sqlalchemy.orm import *
from sqlalchemy.sql.expression import *
from sqlalchemy.ext.declarative import declarative_base, declared_attr, DeferredReflection


Base = declarative_base()


class User(Base):

	__tablename__ = 'users'

	id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
	name = Column(String(50))
	fullname = Column(String(50))
	nickname = Column(String(50))

	def __repr__(self):
		return "<User(name='%s', fullname='%s', nickname='%s')>" % (
								self.name, self.fullname, self.nickname)


if __name__ == '__main__':

	print(f'version {sqlalchemy.__version__}')

	engine = create_engine('sqlite:///:memory:', echo=True)

	print(f'engine {engine}')

	print(f'User table {User.__table__}')

	Base.metadata.create_all(engine)

	# Session = sessionmaker()
	# Session.configure(bind=engine)  # once engine is available

	Session = sessionmaker(bind=engine)

	session = Session()

	ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')

	session.add(ed_user)

	# not just flushed, but.. still accessible

	our_user = session.query(User).filter_by(name='ed').first()

	session.add_all([
		User(name='wendy', fullname='Wendy Williams', nickname='windy'),
		User(name='mary', fullname='Mary Contrary', nickname='mary'),
		User(name='fred', fullname='Fred Flintstone', nickname='freddy')])
	ed_user.nickname = 'eddie'

	print(f'session.dirty {session.dirty}')

	session.commit()

	# session.rollback()

	# for row in session.query(User, User.name).all():
	# 	print(row.User, row.name)
	# 	< User(name='ed', fullname='Ed Jones', nickname='eddie') > ed
	# 	< User(name='wendy', fullname='Wendy Williams', nickname='windy') > wendy
	# 	< User(name='mary', fullname='Mary Contrary', nickname='mary') > mary
	# 	< User(name='fred', fullname='Fred Flintstone', nickname='freddy') > fred


	# aliased
	# from sqlalchemy.orm import aliased
	# user_alias = aliased(User, name='user_alias')
	# for row in session.query(user_alias, user_alias.name).all():
	# 	print(row.user_alias)
		# < User(name='ed', fullname='Ed Jones', nickname='eddie') >
		# < User(name='wendy', fullname='Wendy Williams', nickname='windy') >
		# < User(name='mary', fullname='Mary Contrary', nickname='mary') >
		# < User(name='fred', fullname='Fred Flintstone', nickname='freddy') >



	print('done')