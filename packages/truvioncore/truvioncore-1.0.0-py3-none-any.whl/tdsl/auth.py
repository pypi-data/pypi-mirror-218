__author__ = 'mat mathews'
__copyright__ = 'Copyright (c) 2021 Entrust Funding'
__version__ = '0.0.1'

import os
import sys
import traceback
import inspect
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktCookieHelper
from pyramid.csrf import CookieCSRFStoragePolicy
from pyramid.request import RequestLocalCache
from tdsl import *
from tdsl.orm import *
from tdsl import recordtype

ACL = None

_models = None

ucf = '''
user_name, email_address, password, user_types, groups
'''
UserCredentials = recordtype('UserCredentials', ucf)


def import_models_for_auth(models_module_name):
	return __import__(
		models_module_name,
		fromlist=[models_module_name])


def _get_acl():
	global ACL
	global _models
	if not ACL:
		ACL = ACLUserGroups()
		_models = import_models_for_auth(ACL.ModelsModuleName)
	return ACL


def get_user(email_address, force_refresh=False, session=None):
	acl = _get_acl()
	if force_refresh:
		return acl.force_refresh(email_address, session=session)
	if email_address in acl:
		return acl.get_user(email_address)


def forget_user(email_address, session=None):
	_get_acl().forget_user(email_address)


def user_group_finder(email_address, request):
	"""
	Returns the groups a user is a member of, to be paired with view permissions=
	"""
	print(f'user_group_finder called')
	# curframe = inspect.currentframe()
	# calframe = inspect.getouterframes(curframe, 2)
	# print(f'user_group_finder caller name: {calframe[1]}')

	# TODO: use a custom request factory to set a user
	if request and hasattr(request, 'user'):
		if request.user:
			return [group.name for group in request.user.groups]
	else:
		if request and hasattr(request, 'jwt_claims'):
			group = request.jwt_claims.get('group', [])
			print(f'user_group_finder group from jwt {group} for email_address {email_address}')
			return request.jwt_claims.get('group', [])

		print(f'no user or claims in request to authenticate')

	print(f'checking email for authenticatication {email_address}')
	acl = _get_acl()
	if email_address in acl:
		print(f'acl.get_groups returning {acl.get_groups(email_address)}')
		return acl.get_groups(email_address)


def user_type_finder(email_address, request):
	print(f'user_type_finder called')
	acl = _get_acl()
	if email_address in acl:
		return acl.get_user_types(email_address)


class ACLUserGroups(object):
	def __init__(self):
		self._users = {}
		self._sf = SQLAlchemySessionFactory()

	@property
	def ModelsModuleName(self):
		return self._sf.ModelsModuleName

	def _get_session(self):
		return self._sf.Session

	def __refresh(self, email_address, session=None):
		print('ACL refresh called', email_address)
		try:
			s = self._get_session() if not session else session
			U = ~_models.User
			G = ~_models.Group
			UxG = ~_models.UserXGroup
			UxUTL = ~_models.UserXUserTypeLookup
			UTL = ~_models.UserTypeLookup
			q = s.query(U, UTL, UxUTL, UxG, G) \
				.filter(U.id == UxG.user_id) \
				.filter(U.id == UxUTL.user_id) \
				.filter(UxUTL.user_type_id == UTL.id) \
				.filter(G.id == UxG.group_id) \
				.filter(U.email_address == email_address.lower())  #
			r = q.all()
			rec = UserCredentials('', '', '', set(), set())
			for t in r:
				u, utl, uxutl, uxg, g = t
				u = _models.User(entity=u)
				uxg = _models.UserXGroup(entity=uxg)
				utl = _models.UserTypeLookup(entity=utl)
				g = _models.Group(entity=g)
				# rec.email_address = u.email_address
				rec.email_address = u.email_address.lower()
				rec.password = u.password
				if utl.name:
					rec.user_types.add(utl.name)
				if g.name:
					rec.groups.add('group:%s' % g.name)
				print('ACL refresh user rec', str(rec))
			return rec
		except:
			print('Exception in ACL refresh', traceback.format_exc())
			return None
		finally:
			try:
				if not session:
					s.close()
			except:
				pass

	def force_refresh(self, email_address, session=None):
		try:
			uc = self.__refresh(email_address, session=session)
			if uc and uc.email_address:
				self._users[uc.email_address] = uc
			return uc
		except:
			print(traceback.format_exc())

	@memoize_exp(expiration=10)
	def _get_credentials(self, email_address):
		"""
		get a user, its group, and type
		using email_address as the userid
		"""
		return self.__refresh(email_address)

	def get_user(self, email_address):
		print('ACL get_user called for', email_address)
		if email_address in self:
			return self._users[email_address.lower()]

	def forget_user(self, email_address):
		try:
			self._users.pop(email_address.lower())
		except:
			pass

	def get_password(self, email_address):
		if email_address in self:
			return self._users[email_address.lower()].password

	def get_groups(self, email_address):
		"""method called by default auth toolkit"""
		if email_address in self:
			return list(self._users[email_address.lower()].groups)

	def get_user_types(self, email_address):
		if email_address in self:
			return list(self._users[email_address.lower()].user_types)

	@memoize_exp(expiration=1)
	def __contains__(self, email_address):
		try:
			if email_address.lower() not in self._users:
				print('ACL email not in users list', email_address)
				uc = self._get_credentials(email_address)
				if uc and uc.email_address:
					self._users[uc.email_address] = uc
			if email_address.lower() in self._users:
				return True

		except Exception as e:
			print(traceback.format_exc())


class PyaellaSecurityPolicy:

	def __init__(self, secret):
		self.authtkt = AuthTktCookieHelper(secret)
		self.identity_cache = RequestLocalCache(self.load_identity)

	def load_identity(self, request):
		# identity = self.authtkt.identify(request)
		# if identity is None:
		# 	return None
		#
		# # an identity
		#
		# # identity['timestamp'] = timestamp
		# # identity['userid'] = userid
		# # identity['tokens'] = tokens
		# # identity['userdata'] = user_data
		# userid = identity['userid']

		return MockUser()

	def identity(self, request):
		# define our simple identity as None or a dict with userid and principals keys
		identity = self.helper.identify(request)
		if identity is None:
			return None
		userid = identity['userid']  # identical to the deprecated request.unauthenticated_userid

		# verify the userid, just like we did before with groupfinder
		principals = user_group_finder('mock@mock.moc', request)

		# assuming the userid is valid, return a map with userid and principals
		if principals is not None:
			return {
				'userid': userid,
				'principals': principals,
			}
		return self.identity_cache.get_or_create(request)

	def authenticated_userid(self, request):
		user = self.identity(request)
		if user is not None:
			return user.id

	def remember(self, request, userid, **kw):
		return self.authtkt.remember(request, userid, **kw)

	def forget(self, request, **kw):
		return self.authtkt.forget(request, **kw)


MOCK_AUTH = None


def add_role_principals(userid, request):
	print(f'---- request.jwt_claims.get() {request.jwt_claims.get("roles", [])}')
	return request.jwt_claims.get('roles', [])


def mock_get_user(email_address):
	global MOCK_AUTH
	if not MOCK_AUTH:
		MOCK_AUTH = MockACLUserGroups()
	if email_address in MOCK_AUTH:
		return MOCK_AUTH.get_user(email_address)


def mock_user_group_finder(email_address, request):
	global MOCK_AUTH
	if not MOCK_AUTH:
		MOCK_AUTH = MockACLUserGroups()
	if email_address in MOCK_AUTH:
		print('USING MOCK_AUTH', email_address, MOCK_AUTH.get_groups(email_address))
		return MOCK_AUTH.get_groups(email_address)


class MockUser:
	__tablename__ = 'users'
	id = 1111
	name = 'MockUser'
	role = 'Admin'
	password_hash = 'password'

	def set_password(self, pw):
		self.password_hash = pw

	def check_password(self, pw):
		return True


class MockACLUserGroups(object):
	def __init__(self):
		self._users = {}

	@property
	def ModelsModuleName(self):
		raise Exception('MockACLUserGroups does not have access to models')

	def _get_session(self):
		raise Exception('MockACLUserGroups does not have access to a database')

	@memoize_exp(expiration=5)
	def _get_credentials(self, email_address):
		"""
		get a user, its group, and type
		using email_address as the userid
		"""
		try:
			# ucf = ''' user_name, email_address, password, user_types, groups'''
			rec = UserCredentials(
				email_address, email_address, '12345678', set(), set())
			rec.user_types.add('Sys')
			rec.groups.add('group:su')
			return rec
		except Exception as e:
			print(traceback.format_exc())
			return None

	def get_user(self, email_address):
		if email_address in self:
			return self._users[email_address]

	def get_password(self, email_address):
		if email_address in self:
			return self._users[email_address].password

	def get_groups(self, email_address):
		"""method called by default auth toolkit"""
		if email_address in self:
			return list(self._users[email_address].groups)

	def get_user_types(self, email_address):
		if email_address in self:
			return list(self._users[email_address].user_types)

	@memoize_exp(expiration=10)
	def __contains__(self, email_address):
		try:
			if email_address not in self._users:
				uc = self._get_credentials(email_address)
				if uc and uc.email_address:
					print('Setting User in MockACLUserGroups', uc)
					self._users[uc.email_address] = uc
			if email_address in self._users:
				return True
		except Exception as e:
			print(traceback.format_exc())


