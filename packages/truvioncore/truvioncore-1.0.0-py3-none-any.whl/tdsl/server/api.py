import sys, os
import json
import copy
from urllib import parse
import datetime
import traceback
from hashlib import sha1
import uuid
import unicodedata
import isodate
import arrow
import decimal
import logging
from collections import OrderedDict
from isodate.isoerror import ISO8601Error
from sqlalchemy.exc import *
from sqlalchemy.sql import text
from pyramid.httpexceptions import *
from pyramid.security import Allow, Everyone

import tdsl
from tdsl import *
from tdsl.orm import *
from tdsl.codify import *
from tdsl.express import twk_hammer


from logging.handlers import RotatingFileHandler

log = logging.getLogger(f'{__name__+str(uuid.uuid4())}')
log.setLevel(logging.DEBUG)
# fh = logging.FileHandler(__name__+'.log')
fh = RotatingFileHandler(__name__ + '.log', mode='a', maxBytes=1024 * 5, backupCount=0)
fh.setLevel(logging.DEBUG)
frmttr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmttr)
log.addHandler(fh)


import inspect 

def info(msg):
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    print('[%s] %s' % (mod.__name__, msg))

def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method
    
       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.
       
       An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
      return f'. nope len stack {len(stack)}'
    parentframe = stack[start][0]    
    
    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)

    if 'self' in parentframe.f_locals:

        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)

    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append( codename ) # function or a method
    del parentframe
    print(f'. name here {name}')
    return ".".join(name)


__all__ = [
    'model_edit_get',
    'model_edit_put',
    'model_edit_post',
    'model_edit_delete',
    'model_search_get',
    'xmodel_upsert',
    'make_result_repr',
    'HttpMethodOverrideMiddleware',
    'load_entity_with_key',
    'retrieve_entity',
    'filter_model_attrs',
    'lookup_table_get_jsonp',
    #'retrieve_lut_values',
    #'LutValues',
    'get_current_user',
    'get_current_rbac_user',
    'is_user_type_allowed',
    'get_user_sbac',
    'WebRoot',
    'AdminContext',
    'ModelContext',
    'CompositeContext',
    'LookupTableContext',
    'XModelContext',
    'UploadContext',
    'EntityFound',
    'EntityNotFound',
    'EntityRestorable',
    'PyaellaHTTPException',
    'PyaellaHTTPPaymentRequired',
    'PyaellaHTTPUnprocessableEntity',
    'PyaellaHTTPPreconditionRequired',
    'PyaellaHTTPResourceNotFound',
    'MalformedRequest',
    'import_models',
    'get_injected_models',
    'model_cls_from_subpath',
    'ResultContainer',
    'create_user_app_license',
    '_process_subpath',
    '_process_args',
    '_process_xmodel_args'
]


MODELS = None


def import_models(models_module):
    print(f'. api.import_models called')
    global MODELS
    MODELS = __import__(models_module, fromlist=[models_module])
    print(f'. import_models Imported models {models_module} : {MODELS}')
    return MODELS


def get_injected_models():
    global MODELS
    return MODELS


def get_session():
    return SQLAlchemySessionFactory().Session


@memoize_exp(expiration=30)
def get_current_user(email_address, session=None):
    try:
        cont_session = False
        if email_address:
            if session:
                cont_session = True
            else:
                session = get_session()
            User = MODELS.__dict__['User']
            o = session.query(~User).filter((~User).email_address==email_address).first()
            if o:
                session.expunge(o)
                return User(entity=o)
    finally:
        try:
            if not cont_session:
                session.close()
        except:pass


def create_user_app_license(app_id, domain_id, user,
    app_license_type_name, session=None):
    try:
        cont_session = True if session else False
        session = session if session else get_session()

        now = datetime.datetime.now()

        adc = AppDomainCoder(int(app_id), int(domain_id))

        ALTLU = ~MODELS.__dict__['AppLicenseTypeLookup']
        ALBP = ~MODELS.__dict__['AppLicenseBillingPlan']
        UserAppLicense = MODELS.__dict__['UserAppLicense']

        alt_id, alb_id = (session.query(ALTLU.id, ALBP.id)
                    .filter(ALTLU.name==app_license_type_name)
                    .filter(ALBP.name==ALTLU.name)
                    .filter(ALBP.end_date==None)
                    ).first()

        lictxt, blocks, hash_ = adc.get_seat_lic(user.id, alt_id, now, now)

        ual = UserAppLicense(
            app_id=app_id,
            domain_id=domain_id,
            license_hash=hash_,
            user_id=user.id,
            start=now,
            expiry=now, # if same as start, no expiry
            app_license_type_id=alt_id,
            app_license_billing_plan_id=alb_id).save(session)

        return ual

    except:
        log.debug(traceback.format_exc())
    finally:
        try:
            if not cont_session and session:
                session.close()
        except:pass


def get_current_rbac_user(email_address, 
        accept_user_type_name=None,
        accept_user_type_names=None, 
        accept_user_type_ids=None,
        session=None):
    try:
        cont_session = True if session else False
        session = session if session else get_session()
        if email_address:
            User = MODELS.__dict__['User']
            user = session.query(~User).filter((~User).email_address==email_address).first()
            utl_lut = LutValues(model=MODELS.__dict__['UserTypeLookup'], session=session)
            g_lut = LutValues(model=MODELS.__dict__['Group'], session=session)
            utns = None
            if user:
                if accept_user_type_ids or accept_user_type_name or accept_user_type_names:
                    is_allowed, utns = is_user_type_allowed(
                                user, 
                                accept_user_type_name=accept_user_type_name,
                                accept_user_type_names=accept_user_type_names, 
                                accept_user_type_ids=accept_user_type_ids, 
                                session=session,
                                cont_session=cont_session)
                    if is_allowed:
                        try:
                            session.expunge(user)
                        except InvalidRequestError: pass
                        return user, utns, utl_lut
                    else:
                        raise HTTPUnauthorized('RBAC: User is not authorized')
                else:
                    utns = [utl_lut.get_name(ut.user_type_id) for ut in user.user_types]
                    session.expunge(user)
                    return user, utns, utl_lut
            else:
                return None, None, None
        else:
            raise Exception('No email to authenticated for RBAC')

    finally:
        if not cont_session and session:
            try:
                session.close()
            except:pass
 

def is_user_type_allowed(user, 
        accept_user_type_name=None,
        accept_user_type_names=None, 
        accept_user_type_ids=None, 
        session=None, 
        cont_session=True):
    try:
        if not session:
            cont_session = False
            session = get_session()
        
        user = session.merge(user)

        print(f'. is_user_type_allowed user {user}')

        utl_lut = LutValues(model=MODELS.__dict__['UserTypeLookup'], session=session)
        utl_names = [utl_lut.get_name(ut.user_type_id) for ut in user.user_types]
        print(f'. utl_names user {utl_names}')

        if accept_user_type_ids:
            if len(accept_user_type_ids & set([ut.user_type_id for ut in user.user_types])) > 0:
                return True, utl_names
            else:
                return False, []

        elif accept_user_type_name:
            allwd_utl_id_lvl = utl_lut.get_id(accept_user_type_name)
            user_types = [ut.user_type_id for ut in user.user_types]
            user_types.sort()
            return (user_types[0] <= allwd_utl_id_lvl, utl_names)

        elif accept_user_type_names:
            acceptable = set(accept_user_type_names)
            the_users_types = set(utl_names)
            intr_sct = set(accept_user_type_names) & set(utl_names)
            if len(intr_sct) > 0:
                return True, intr_sct
            else:
                return False, intr_sct

        raise Exception('Invalid arguments supplied to is_user_type_allowed')

    except:
        log.debug(traceback.format_exc())
        return False, []
    finally:
        try:
            if not cont_session and session:
                session.close()
        except:
            pass


sct = '''
user_name, email_address, password, user_types, groups
'''
SubscriptionControlRec = recordtype(
    'SubscriptionControlRec',
    'user, app_license_type_name, app_license_start, app_license_expiry, user_app_license, app_license_type_lu, app_license_billing_plan, license_text'
)

def get_user_sbac(app_id, domain_id, user, session=None):
    try:
        start = datetime.datetime.now()
        cont_session = True if session else False
        session = session if session else get_session()

        UAL = ~MODELS.__dict__['UserAppLicense']
        ALTLU = ~MODELS.__dict__['AppLicenseTypeLookup']
        ALBP = ~MODELS.__dict__['AppLicenseBillingPlan']

        adc = AppDomainCoder(app_id, domain_id)

        rp = (session.query(UAL, ALTLU, ALBP)
                .filter(UAL.user_id == user.id)
                .filter(UAL.app_id == app_id)
                .filter(UAL.domain_id == domain_id)
                .filter(ALTLU.id == UAL.app_license_type_id)
                .filter(ALBP.id == UAL.app_license_billing_plan_id)
                ).first()

        if rp:
            ual, altlu, albp = rp
            lictxt, blocks, hash_ = adc.get_seat_lic(
                user.id, ual.app_license_type_id, ual.start, ual.expiry)

            return SubscriptionControlRec(
                user, altlu.name, ual.start, ual.expiry, ual, altlu, albp, lictxt
                )

        return None

    except:
        log.debug(traceback.format_exc())
    finally:
        try:
            if not cont_session and session:
                session.close()
        except:
            pass
        print(datetime.datetime.now() - start)


# @memoize_exp(expiration=60*5)
# def retrieve_lut_values(lut_model, session=None):
#     # print(f'. retrieve_lut_values called {lut_model}')
#     try:
#         session = get_session() if not session else session
#         q = session.query(~lut_model)
#         rp = q.all()
#         result = {'id_order':[], 'id_for_name':OrderedDict(), 'id_for_display_name':OrderedDict()}
#         pk = 'id'
#         if not hasattr(rp[0], 'id'):
#             ent = lut_model(entity=rp[0])
#             pk = ent.PrimaryKeyName
#         for row in rp:
#             pkval = getattr(row, pk)
#             result[pkval] = (row.name, row.display_name, row.description,)
#             result['id_order'].append(pkval)
#             result['id_for_name'][row.name] = row.id
#             result['id_for_display_name'][row.display_name] = row.id
#         result['id_order'].sort()
#         result['name_order'] = [result[id_] for id_ in result['id_order']]
#         return result
#     except:
#         log.debug(traceback.format_exc())
#     finally:
#         try:
#             session.close()
#         except:
#             pass


# class LutValues(object):
#     def __init__(self, model=None, data=None, session=None):
#         self._model = model
#         self._data = data if data else retrieve_lut_values(model, session=session)

#     @memoize
#     def get_name(self, id_):
#         return self._data[id_][0]

#     @memoize
#     def get_display_name(self, id_):
#         return self._data[id_][1]

#     @memoize
#     def get_description(self, id_=None, name=None):
#         if id_:
#             return self._data[id_][2]
#         elif name:
#             return self._data[self._data['id_for_name'][name]][2]

#     @memoize
#     def get_id(self, name):
#         if self._data:
#             return self._data['id_for_name'][name] if name in self._data['id_for_name'] else None
#         print(f'. get_id None _data {self._data} for {name} model {self._model}')
#         return None

#     @memoize
#     def get_id_for_display_name(self, display_name):
#         return self._data['id_for_display_name'][display_name]      \
#             if display_name in self._data['id_for_display_name']    \
#             else None

#     @memoize
#     def get_all_ids(self):
#         for k in self._data:
#             if k not in ['id_order', 'name_order', 'id_for_name', 'id_for_display_name']:
#                 yield k

#     @memoize
#     def get_all_names(self):
#         return self._data['id_for_name'].keys()

#     def get_all_display_names(self):
#         for k in self._data:
#             if k not in ['id_order', 'name_order', 'id_for_name', 'id_for_display_name']:
#                 yield self._data[k][1]

#     def get_id_display_name_pairs(self):
#         for k in self._data:
#             if k not in ['id_order', 'name_order', 'id_for_name', 'id_for_display_name']:
#                 yield self.get_id(self._data[k][0]), self._data[k][1]

#     def to_dict(self):
#         d = []
#         for id_ in self._data['id_order']:
#             row = [id_]
#             row.extend(list(self._data[id_]))
#             d.append(tuple(row))
#         return d

#     def __call__(self, val):
#         # print(f'. LutValues __call__ {val} {caller_name()}')
#         """ if val is int, return name and vs vrs"""
#         if type(val)==int:
#             return self.get_name(val)
#         elif type(val) in [str]:
#             return self.get_id(val)
#         raise TypeError(str(val))

#     def __pos__(self):
#         return self.to_dict()

#     def __getattr__(self, item):
#         # print(f'. __getattr__ {self}, {item} {caller_name()}')
#         return self._data['id_for_name'][item.lower()]



class WebRoot(dict):
    """ default Root """
    __name__ = 'WebRoot'
    __parent__ = None
    def __init__(self, request):
        self.request = request
        self.__setitem__('_a', AdminContext(request))
        self.__setitem__('m', ModelContext(request))
        self.__setitem__('c', CompositeContext(request))
        self.__setitem__('lut', LookupTableContext(request))
        self.__setitem__('up', UploadContext(request))


class AdminContext(object):
    """
    Administration context

    /a/
    """
    __name__ = 'AdminContext'
    __parent__ = WebRoot
    def __init__(self, request):
        self.request = request


class ModelContext(dict):
    """
    Model context

    /m/
    """
    __name__ = 'ModelContext'
    __parent__ = WebRoot
    def __init__(self, request):
        self.request = request
        self.__setitem__('x', XModelContext(request))


class XModelContext(object):
    """
    Associated Models context

    /x/
    """
    __name__ = 'XModelContext'
    __parent__ = ModelContext
    def __init__(self, request):
        self.request = request


class CompositeContext(object):
    """
    Composite context

    /c/
    """
    __name__ = 'CompositeContext'
    __parent__ = WebRoot
    def __init__(self, request):
        self.request = request


class LookupTableContext(object):
    """
    Lookup Table context

    /lut/
    """
    __name__ = 'LookupTableContext'
    __parent__ = WebRoot
    def __init__(self, request):
        self.request = request


class UploadContext(object):
    """
    Upload context

    /up/
    """
    __name__ = 'UploadContext'
    __parent__ = WebRoot
    def __init__(self, request):
        self.request = request


class MalformedRequest(Exception):
    pass


class PyaellaHTTPException(HTTPException):
    pass


class PyaellaHTTPPaymentRequired(PyaellaHTTPException):
    code = 402
    title = 'Quota Reached or Payment Required'


class PyaellaHTTPResourceNotFound(PyaellaHTTPException):
    code = 404
    title = 'Resource Not Found'


class PyaellaHTTPUnprocessableEntity(PyaellaHTTPException):
    code = 422
    title = 'Unprocessable Entity'


class PyaellaHTTPPreconditionRequired(PyaellaHTTPException):
    code = 428
    title = 'Precondition Required'


class EntityFound(Exception):
    def __init__(self, resource_name, ident, **kwds):
        self._rn = resource_name
        self._id = ident
        self._kwds = kwds
    def __str__(self):
        return 'EntityFound: %s %s %s'%(self._rn, self._id, str(self._kwds))


class EntityNotFound(Exception):
    def __init__(self, resource_name, **kwds):
        self._rn = resource_name
        self._kwds = kwds
    def __str__(self):
        return 'EntityNotFound: %s %s'%(self._rn, str(self._kwds))


class EntityRestorable(Exception):
    def __init__(self, resource_name, ident):
        self._rn = resource_name
        self._id = ident
    def __str__(self):
        return 'EntityRestorable: %s %s'%(self._rn, self._id)


class HttpMethodOverrideMiddleware(object):
    '''
    WSGI middleware for overriding HTTP Request Method.

    Examines the POST body for the value of '_method' in a form-encoded POST or
    X-HTTP-Method-Override for an XML or JSON POST. 

    Middleware intercepts the POST and changes it to
    a GET,PUT, or DELETE before the Pyramid app receives it. So the HTTP
    request arrives as a POST to the server and gets around the URI length
    issue but is transformed into a request with the correct verb just 
    before it hits the app for processing.    
    '''

    
    def __init__(self, application):
        self.application = application
    
    def __call__(self, environ, start_response):
        if 'POST' == environ['REQUEST_METHOD']:         
            override_method = ''
            #if not override_method:
            override_method = \
                    environ.get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()
            if override_method in ('GET', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'):
                # Save the original HTTP method
                environ['http_method_override.original_method'] = \
                                            environ['REQUEST_METHOD']
                # Override HTTP method
                environ['REQUEST_METHOD'] = override_method
        return self.application(environ, start_response)


def model_cls_from_subpath(request, models=None):
    global MODELS
    args = list(request.subpath)
    model_class = MODELS.__dict__[args.pop(0)]  \
        if models == None                       \
        else models.__dict__[args.pop(0)]
    return model_class, args


def load_entity_with_key(model, key):
    session = get_session()
    entity = model.load(key, session=session)


def filter_model_attrs(model_class, allow_id_lookup=False, session=None, **kwds):
    entity = None
    opts = {}
    try:
        entity = model_class()
        try:
            if hasattr(entity, 'transform_kwds'):
                kwds = entity.transform_kwds(session, **kwds)
        except:
            log.debug(traceback.format_exc())

        for kw_ in kwds:
            if kwds[kw_] not in [None, '', u'', 'None']:
                try:
                    if kw_ in entity.Fields or kw_ in entity.Relations:
                        if entity.field_py_type(kw_) == list:
                            type_ = entity.array_field_item_py_type(kw_)
                            if kwds[kw_].endswith(';'):
                                kwds[kw_] = kwds[kw_].rstrip(';')

                            kwds[kw_] = [
                                        type_(item)
                                        for item in kwds[kw_].split(';')
                                        if item
                                    ]
                        else:

                            if kwds[kw_] not in [None, '', 'None', 'null']:

                                try:
                                    if entity.field_py_type(kw_) == bool:

                                        kwds[kw_] = (
                                                    True if kwds[kw_].lower() in dsl.express.TRUES else False
                                                    )

                                            # (True if kwds[kw_].upper()
                                            #     in ['TRUE', 'ON', 'YES', '1', 'CHECKED'] else False)
                                    else:
                                        kwds[kw_] = \
                                            entity.field_py_type(kw_)(kwds[kw_])
                                except:
                                    # needs transform

                                    # handle datetime
                                    if entity.field_py_type(kw_) == datetime:
                                        kwds[kw_].strip().replace(' ', 'T') 
                                        try:
                                            kwds[kw_] = \
                                                isodate.parse_datetime(kwds[kw_])
                                        except:
                                            kwds[kw_] = \
                                                isodate.parse_date(kwds[kw_])           

                                    elif entity.field_py_type(kw_) in [
                                            int, float, decimal.Decimal
                                        ]:
                                        try:
                                            # £, ¥, €
                                            # TODO: use re
                                            kwds[kw_] = entity.field_py_type(kw_)(
                                                kwds[kw_]               \
                                                .replace( ',', '')      \
                                                .replace( '.', '')      \
                                                .replace( '$', '')      \
                                                .replace(u'£', '')      \
                                                .replace(u'¥', '')      \
                                                .replace(u'€', '')      #
                                            )
                                        except:
                                            kwds[kw_] = None
                                            
                    elif kw_ == 'id' and allow_id_lookup:
                        kwds[kw_] = entity.field_py_type(kw_)(kwds[kw_])
                    else:
                        # optional parameters, i.e limit and offset
                        if kw_ not in ['id', 'key']:
                            opts[kw_] = kwds[kw_]

                except ISO8601Error:
                    pass
                except KeyError:
                    # For items that are fuctions and not attributes
                    if str(kw_) == 'key':
                        key = str(kwds[kw_])
                    else:
                        raise
            else:
                kwds[kw_] = None
        return model_class(**kwds), kwds, opts
    except:
        log.debug(traceback.format_exc())
        raise


def _process_subpath(subpath_args, formUrlEncodedParams=None, rawBodyData=None, useJSON=True):
    print(f'_process_subpath called subpath_args: {subpath_args}, formUrlEncodedParams: {formUrlEncodedParams}, rawBodyData: {rawBodyData}')
    kwds = {}
    if formUrlEncodedParams and '<NoVars' not in formUrlEncodedParams:
        print(f'. _process_subpath using formUrlEncodedParams')
        kwds = dict([(parse.unquote_plus(k), parse.unquote_plus(v),) for k,v in formUrlEncodedParams.items()])

    elif rawBodyData:
        print(f'. _process_subpath using rawBodyData {type(formUrlEncodedParams)} {formUrlEncodedParams.keys()}')

        kwds = {}
        # TODO. Use content type instead of function keywords
        #if '(Content-Type: application/json)' in formUrlEncodedParams:
        if useJSON:
            # attempt json load of rawBody
            try:
                print(f'. rawBodyData {rawBodyData}')
                kwds = json.loads(rawBodyData)
                print(f'. _process_subpath kwds from json {kwds}')
            except:
                print(traceback.format_exc())
        else:
            r = [i.split('=') for i in rawBodyData.split('&')]
            kwds = dict([(parse.unquote_plus(i[0]), parse.unquote_plus(i[1]),) for i in r])
    else:

        if len(subpath_args) > 0:

           if '=' in subpath_args[0]:

                # for debug
                # k, v = subpath_args[0].split('=')
                # print(f'_process_subpath.split k {k}: v {v}')
                # print(f'_process_subpath.parse.unquote_plus {parse.unquote_plus(v)}')
                # print(f'_process_subpath.parse.unquote_plus {parse.unquote_plus("id=1").split("=")}')

                kwds = dict( [parse.unquote_plus(i).split('=') for i in subpath_args] )

                for k, v in kwds.items():
                    yes, val = dsl.express.is_num(v)
                    if yes:
                        kwds[k] = val
                        print(f'cast as num {type(val)}')

    print(f'_process_subpath returning kwds {kwds}')
    return kwds


def _process_args(
        request,
        formUrlEncodedParams=None,
        rawBodyData=None,
        models=None,
        allow_id_lookup=False,
        allow_nulls=False,
        ignore_override_method=None
    ):
    """ """

    args = list(request.subpath)
    print(f'_process_args {args}')
    model_class = MODELS.__dict__[args.pop(0)]
    # if models == None
    # else models.__dict__[args.pop(0)]
    print(f'_process_args model_class {model_class}')

    kwds = _process_subpath(args,
                            formUrlEncodedParams=formUrlEncodedParams,
                            rawBodyData=rawBodyData)

    print(f'_process_args kwds {kwds}')

    if 'override_method' in kwds and ignore_override_method is not None:
        if ignore_override_method != 'PUT':
            if kwds['override_method'] == 'PUT':
                # shuttle this to PUT
                return None, None, None, kwds

    key = None
    model = None

    opts = {}

    if 'key' in kwds:
        key = kwds.pop('key')

    _, kwds, opts = filter_model_attrs(
        model_class, allow_id_lookup=True, **kwds)

    print(f'_process_args called filter_model_attrs {kwds} {opts}')

    if opts:
        for kw_ in opts:
            kwds.pop(kw_)

    if kwds:
        if allow_nulls:
            kwds = dict([(k,v,) for k,v in kwds.items()])
        else:
            kwds = dict([(k,v,) for k,v in kwds.items() if v not in[None, '']])

    print(f'_process_args returning {model_class}, {key}, {kwds}, {opts}')
    return model_class, key, kwds, opts


def _process_json_body(request, rawBodyData):
    if request.content_type in ['application/json']:
        jd = json.loads(rawBodyData)
        for xmodel_name, xrossable in jd.items():
            yield (
                xmodel_name, 
                [x for x in xrossable.keys() if not x.startswith('__')], 
                xrossable, 
                xrossable['__xmodel_kwds__'] if '__xmodel_kwds__' in xrossable else None
            )
    yield None, None, None, None


def _process_xmodel_args(
    request, formUrlEncodedParams=None, rawBodyData=None, 
                    models=None, allow_id_lookup=False):
    global MODELS
    subpath_args = list(request.subpath)
    req_model = subpath_args.pop(0)

    opts = {} \
        if not subpath_args \
        else dict([parse.unquote_plus(i).split('=') for i in subpath_args])

    for xmodel_name, xrossable_names, json_data, xmodel_kwds in \
            _process_json_body(request, rawBodyData=rawBodyData):

        opts['xmodel_kwds'] = xmodel_kwds

        if xmodel_name and xrossable_names and json_data:
            #print xmodel_name, xrossable_names, json_data

            xmodel_class = MODELS.__dict__[xmodel_name]     \
                if models == None                           \
                else models.__dict__[xmodel_name]

            for model_name in xrossable_names:

                model_class = MODELS.__dict__[model_name]       \
                    if models == None                           \
                    else models.__dict__[model_name]

                entity, kwds, xopts = \
                    filter_model_attrs(model_class, **json_data[model_name]) 
                opts.update(xopts)
                yield xmodel_class, entity, kwds, opts


def retrieve_entity(request):
    """ requires id or key
        relies _process_args
    """
    try:
        entity = None
        model, key, kwds, opts = \
            _process_args(request, formUrlEncodedParams=request.POST,
                                            rawBodyData=request.body,
                                            allow_id_lookup=True)
        session = get_session()
        if key or 'id' in kwds:
            entity = model.load(key or int(kwds['id']), session=session)
        return model, key, kwds, entity
    except:
        log.debug(traceback.format_exc())
        return None, None, None, None,


def ResultContainer(object):
    def __init__(self, **kwds):
        for k,v in kwds.items():
            setattr(self, k,v)
    def to_dict(self):
        return self.__dict__


def make_result_repr(model, results, msg='', force_json=False, **kwds):
    """
    .. code-block:: python

        {model_name, entity_field_names, length, results, messages}


    """
    def serialize(entity):
        if hasattr(entity, '__json__'):
            # print(f'. doing __json__ {force_json}')
            if force_json:
                return entity.__json__(None)
            return entity
        elif hasattr(entity, 'to_dict'):
            # print(f'. doing to_dict')
            return entity.to_dict()
        else:
            return {str(entity):'JSON Repr Not Available'}
    if results:
        # print(f'. got some results {results}')
        r = {   'model':str(model),
                'entity_field_names': results[0].Fields if hasattr(results[0], 'Fields') else [],
                'length':len(results),
                'results':[serialize(e) for e in results],
                'message':msg}
    else:
        r = {'status':'OK', 'results':None, 'length':0, 'messages':'No Results'}

    # print('make_result_repr ', r)
    r.update(kwds)
    return r


def model_edit_post(request):
    """
    Post (create) a new Entity for a Model.

    HTTP action: POST

    /m/edit/ModelName

    Form-encoded data must not include `key` or `id`. All required fields 
    for the model must be included and be the correct data type.

    If `override_method` is included in the data and the value is `PUT`,
    the Put action will be called, however, an `id` or `key` must be included.
    This override is implemented to help clients that can't support HTTP PUTs.

    If `override_method` is included in the data and the value is `DELETE`,
    the Delete action will be called, and entity `key` is required.

    If the model has POST hooks implemented in a Mixin, the hooks will be called.

    Returns `result_repr` structured JSON of the new entity.

    """
    try:
        session = get_session()
        entity = None
        model, key, kwds, opts = \
            _process_args(request, formUrlEncodedParams=request.POST,
                                            rawBodyData=request.body)
                
        if 'override_method' in opts:

            if opts['override_method'] == 'PUT':
                # from a standard HTML form
                request.method = 'PUT'
                request.headers['pyaella_flag'] = 'FROM_POST'
                put_result = model_edit_put(request)
                return put_result
            if opts['override_method'] == 'DELETE':
                # from a standard HTML form
                request.method = 'DELETE'
                request.headers['pyaella_flag'] = 'FROM_POST'
                del_result = model_edit_delete(request)
                return del_result

        if key:
            raise MalformedRequest('Key not permitted for POST')
                
        entity = model(**kwds)
        
        d = None
        if hasattr(entity, 'post_pre_hook'):
            d = dict(kwds)
            d.update(opts)
            try:
                entity.post_pre_hook(session=session, **d)
            except EntityFound as ef:
                return {
                    'type':'PyaellaException',
                    'name':'EntityFound',
                    'resource_name':ef._rn,
                    'ident':ef._id
                }
            # TODO!!! FIXME
            except EntityRestorable as e:
                return {
                    'type':'PyaellaException',
                    'name':'EntityRestorable',
                    'resource_name':e._rn,
                    'ident':e._id,
                    # 'restore_url':'/dev/properties/restore/property_id=%s/'%e._id
                    'restore_url':""
                }

        
        entity.save(session)
        key = entity.EntityKey
        entity.save(session)

        if hasattr(entity, 'post_final_hook'):
            if not d:
                d = dict(kwds)
                d.update(opts)
            entity.post_final_hook(session=session, **d)

        result = make_result_repr(model, [entity])
        
        if 'redirect_loc' in opts:
            raise HTTPFound(location=opts['redirect_loc'])

        return result

    except HTTPFound: raise
    except IntegrityError:
        log.debug(traceback.format_exc())
        raise exception_response(409)
    except MalformedRequest:
        log.debug(traceback.format_exc())
        raise exception_response(400)
    except Exception as hell:
        print('Raising hell', hell)
        log.debug(traceback.format_exc())
        raise exception_response(500)
    finally:
        try:
            session.close()
        except:pass

        
def model_edit_get(request):
    """
    Get (read) an Entity for a Model.

    HTTP action GET

    /m/edit/ModelName

    Returns `result_repr` structured JSON of the entity.
    """

    log.info('model_edit_get() %s'%(str(request)))

    try:
        model, key, kwds, entity = \
            retrieve_entity(request)

        log.info('model_edit_get ---- %s %s %s %s'%(str(model), str(key), str(kwds), str(entity)))

        if entity:
            return make_result_repr(model, [entity])

    except IntegrityError:
        log.debug(traceback.format_exc())
        raise exception_response(409)
    except MalformedRequest:
        log.debug(traceback.format_exc())
        raise exception_response(400)
    except:
        log.debug(traceback.format_exc())
        raise exception_response(500)
    finally:
        try:
            session.close()
        except:pass


def model_edit_put(request):
    """ 
    Put (update) Entity for a Model.

    HTTP action PUT

    /m/edit/ModelName

    Any matching field in the supplied form-encoded data will update
    the corresponding field of the entity. The data must include 
    either the entity's key or id.

    Returns `result_repr` structured JSON of the updated entity.
    """

    try:
        force_json = False
        if 'pyaella_flag' in request.headers:
            if request.headers['pyaella_flag'] == 'FROM_POST':
                force_json = True

        entity = None
        model, key, kwds, opts = \
            _process_args(request, formUrlEncodedParams=request.POST,
                                            rawBodyData=request.body,
                                            allow_id_lookup=True,
                                            allow_nulls=True,
                                            ignore_override_method='PUT')
            
        session = get_session()
        if key or 'id' in kwds:
            entity = model.load(key or int(kwds['id']), session=session)
            if hasattr(entity, 'put_pre_hook'):
                self, kwds = entity.put_pre_hook(session, **kwds)
            for k in kwds:
                setattr(entity, k, kwds[k])
            entity.save(session)

            if hasattr(entity, 'put_finalize'):
                try:
                    entity.put_finalize(session, **kwds)
                except:
                    pass

            if 'redirect_loc' in opts:
                # WARNING: Redirecting from PUT?
                raise HTTPFound(location=opts['redirect_loc'])

            return make_result_repr(model, [entity], force_json=True)
        else:
            log.debug(traceback.format_exc())
            raise MalformedRequest(417)

    except HTTPFound: raise
    except IntegrityError:
        log.debug(traceback.format_exc())
        raise exception_response(409)
    except MalformedRequest as mr:
        log.debug(traceback.format_exc())
        raise mr
    except:
        log.debug(traceback.format_exc())
        raise exception_response(500)
    finally:
        try:
            session.close()
        except:pass


def model_edit_delete(request):
    """ 
    Delete the Entity for the Model.

    HTTP action: DELETE

    /m/edit/ModelName

    Delete the entity. The form-encoded data must include the  entity's `key`

    Returns JSON {'status':'OK', 'action':'DELETE', 'entity_id':[int]}
    """
    try:    
        model, key, kwds, opts = \
            _process_args(request, formUrlEncodedParams=request.POST,
                                            rawBodyData=request.body)
        force_json = False
        if 'pyaella_flag' in request.headers:
            if request.headers['pyaella_flag'] == 'FROM_POST':
                force_json = True

        session = get_session()
        if key:
            entity = model.load(key, session=session)
            if entity:
                if hasattr(entity, 'pre_delete'):
                    entity.pre_delete(session, **kwds)

                session.delete(~entity)
                session.commit()
            return {
                'status': 'Ok',
                'action': 'DELETE',
                'entity_id': entity.id if entity else None
            }

        else:
            raise MalformedRequest()

    except IntegrityError:
        log.debug(traceback.format_exc())
        raise exception_response(409)
    except MalformedRequest:
        log.debug(traceback.format_exc())
        raise exception_response(400)
    except:
        log.debug(traceback.format_exc())
        raise exception_response(500)
    finally:
        try:
            session.close()
        except:pass


def model_search_form(request):
    return {}


def model_search_get(request):
    """
    Search for an Entity for a Model

    HTTP action: GET

    /m/search/ModelName/filter_params_1=val/filter_params_2=val

    /m/search/ModelName/starts_with=[filter_params_1=val]

    Returns collected `result_repr` structured JSON of the matching entities.
    """

    if request.POST:
        if 'search_query' in request.body and 'search_query' in request.POST:
            # use search query builder
            sqb = SearchQueryBuilder(request.body)
            model = MODELS.__dict__[sqb.ModelName]
            session = get_session()
            query = session.query(~model)
            for param, arg in sqb.get_eq_param_args():
                query = sqb.build_eq_filter(query, model, param, arg)
            r = query.all()
            ents = collect_entities(r, model)
            result = make_result_repr(model, ents, force_json=True)
            return result

    #else

    model, key, kwds, opts = \
        _process_args(request, formUrlEncodedParams=request.POST,
                                        rawBodyData=request.body)

    try:
        session = get_session()
        q = session.query(~model)
        # searching by id or key not permitted
        if 'id' in kwds or 'key' in kwds:
            raise MalformedRequest()

        print(f'. kwds: {kwds}')

        do_search = False
        if kwds:
            for k,v in kwds.items():
                fltr = "%s=%s"%(k, "'%s'"%v if type(v) != int else v)
                q = q.filter(text(fltr))
                do_search = True

        # BUGZ: where is starts_with_terms?
        if 'starts_with' in opts:
            for term in starts_with_terms:
                term, val = term.split(':')
                q = q.filter(getattr(~model, term).like(val+'%'))
                do_search = True


        if 'limit' in opts:
            q = q.limit(int(opts['limit']))
        else:
            # default a limit to 10
            q = q.limit(10)

        if 'offset' in opts:
            q = q.offset(int(opts['offset']))

        ents = []
        if do_search:
            r = q.all()
            ents = collect_entities(r, model)

        return make_result_repr(model, ents, force_json=True)

    except IntegrityError:
        log.debug(traceback.format_exc())
        raise exception_response(409)
    except MalformedRequest:
        log.debug(traceback.format_exc())
        raise exception_response(400)
    except:
        log.debug(traceback.format_exc())
        raise exception_response(500)
    finally:
        try:
            session.close()
        except:pass


def model_search_ajax_autocomplete(request):
    """
    Search for Entities for Model for Autocomplete

    /m/jxauto/ModelName/starts_with=true/term=val

    Returns JSONP {'callback':callback, 'model_name':model_name, 'entities':[entities]}
    """

    try:
        kwds = dict(request.GET)
        model_name = kwds['model']
        callback = kwds['callback']
        model_class = MODELS.__dict__[model_name]
        entities = []
        if 'starts_with' in kwds and bool(kwds['starts_with']):

            with SQLAlchemySessionFactory() as session:
                entities = (session.query(~model_class)
                                .filter((~model_class).name.like(kwds['term']+'%'))
                                ).all()
                entities = [model_class(entity=e) for e in entities]

        return {
            'callback':kwds['callback'],
            'model_name':str(model_class),
            'entities':entities
        }
    except IntegrityError:
        log.debug(traceback.format_exc())
        raise exception_response(409)
    except MalformedRequest:
        log.debug(traceback.format_exc())
        raise exception_response(400)
    except:
        log.debug(traceback.format_exc())
        raise exception_response(500)
    finally:
        try:
            session.close()
        except:pass


def xmodel_delete(request):
    """
    Delete associated Entities

    HTTP action: POST

    Raw request body data is JSON

    {"UserXUserTeam": {"User": {"id": 1011011012}, "UserTeam": {"id": 1}}}

    Parsed data:

        {
            <class 'fusilli.models.UserXUserTeam'>: {
                <fusilli.models.UserTeam object at 0x10c670290>: {
                    'fk': 'user_team_id', 'kwds': {u'id': 1}
                }, 
                <fusilli.models.User object at 0x10c6701d0>: {
                    'fk': 'user_id', 'kwds': {u'id': 1011011012}}}, 'opts': {
                }
            }
        }

    
    Returns `result_repr` structured JSON of the deteled entities.
    """

    try:
        deletes = {}
        xmodel_class, entity, kwds, opts = None, None, None, None
        
        # yield xmodel_name, entity, kwds, opts
        for xmodel_class, entity, kwds, opts in \
            _process_xmodel_args(
                request, 
                formUrlEncodedParams=request.POST, 
                rawBodyData=request.body
            ):

            deletes.setdefault(xmodel_class, {})[entity] = {
                'kwds': kwds,
                'fk': entity.PrimaryKeyName
            }

        deletes['opts'] = opts
        
        fks = {}
        xmodel_class = None

        for k,v in deletes.items():
            if k not in opts:
                xmodel_class = k
                for entity, data in v.items():

                    # this is rather explicit
                    # and done for understandability
                    if 'id' in data['kwds']:
                        entity.id = int(data['kwds']['id'])

                    fks[data['fk']] = entity.id

        session = get_session()
        q = session.query(~xmodel_class)

        for k, v in fks.items():
            fltr = "%s=%s"%(
                k, "'%s'"%v if type(v) != int else v 
            )
            q = q.filter(fltr)

        entity = q.all()
        if entity:
            if len(entity) > 1:
                # TODO: ambiguous
                raise MalformedRequest('Ambiguous')
            else:
                entity = entity[0]
                session.delete(entity)
                session.commit()

                return make_result_repr(
                    xmodel_class, 
                    [xmodel_class(entity=entity)], 
                    msg='DELETED')

        raise HTTPNotFound('Resource not found')
                
    except Exception as e:
        raise
    finally:
        try:
            session.close()
        except:pass


def xmodel_upsert(request):
    """
    Update/Insert Entities for Model.

    HTTP action: POST

    Raw request body data is JSON formatted

    JSON formatted argument example

    .. code-block:: python

        {
        'UserXUserTypeLookup':{
            'User': {
                'id':1,
                'key':'4c'
            },
            'UserTypeLookup': {
                'id':2,
                'key':'e4'
            }
        }


    Result format example

    .. code-block:: python
        
        xrossable data = {
            u'UserTypeLookup': {
                u'id': 2, u'key': u'e4'
            }, 
            u'User': {
                u'id': 1, 
                u'key': u'4c'
            }
        }

    Returns `result_repr` structured JSON of the updated entity.

    .. code-block:: python

        '{"UserXUserTeam": 
            {"User": {"phone_number": null, "last_name": "Mathews",
                "key": "4nbq", "pin": null, "address1": null,
                "address2": null, "is_active": null, "post_code": null,
                "country_code": "USA", "device_tokens": null,
                "password": null, "email_address": "mat@miga.me",
                "id": 10000, "city": null, 
                "first_name": "Mat", "open_id": null,
                "access_token": null,
                "region": null, "user_name": "mat"}, 
            "UserTeam": {"team_manager_id": 10000, "name": "Test Team",
                "key": "43", "id": 2}}}'
    """

    try:

        upserts = {}
        xmodel_class, entity, kwds, opts = None, None, None, None
        
        # yield xmodel_name, entity, kwds, opts
        for xmodel_class, entity, kwds, opts_ in \
            _process_xmodel_args(
                request, 
                formUrlEncodedParams=request.POST, 
                rawBodyData=request.body
            ):

            upserts.setdefault(xmodel_class, {})[entity] = {
                'kwds': kwds,
                'fk': entity.PrimaryKeyName,
            }

            opts = copy.copy(opts_)

        upserts['opts'] = opts
        session = get_session()
        
        for k,v in upserts.items():
            if k != 'opts' and k not in opts:
                xmodel_class = k
                fks = {}
                for entity, data in v.items():

                    if not entity.id:
                        for k,v in data['kwds'].items():
                            setattr(entity, k, v)
                        entity.save(session)
                    else:
                        entity = entity.__class__(entity=session.merge(entity))
                        for k,v in data['kwds'].items():
                            setattr(entity, k, v)
                        entity.save(session, upsert=True)

                    fks[data['fk']] = entity.id

                XM = ~xmodel_class
                q = session.query(XM)
                for fkn, fkv in fks.items():
                    q = q.filter(getattr(XM, fkn)==fkv)
                xent = q.first()
                if not xent:
                    xent = xmodel_class(**fks)
                else:
                    xent.last_upd = datetime.datetime.now()
                    xent = xmodel_class(entity=xent)

                if 'xmodel_kwds' in opts and opts['xmodel_kwds']:
                    for k,v in opts['xmodel_kwds'].items():
                        setattr(xent, k, v)

                xent.save(session, upsert=True)

        result = make_result_repr(xmodel_class, [xent])
        return result
                    
    except IntegrityError:
        log.debug(traceback.format_exc())
        raise exception_response(409)
    except MalformedRequest:
        log.debug(traceback.format_exc())
        raise exception_response(400)
    except:
        log.debug(traceback.format_exc())
        raise exception_response(500)
    finally:
        try:
            session.close()
        except:pass


def lookup_table_get_jsonp(request):
    try:
        session = get_session()
        args = list(request.subpath)
        model = MODELS.__dict__[args.pop(0)]
        return retrieve_lut_values(model, session=session)
    except MalformedRequest:
        log.debug(traceback.format_exc())
        raise exception_response(400)
    except:
        log.debug(traceback.format_exc())
        raise exception_response(500)
    finally:
        session.close()


class SearchQueryBuilder(object):

    def build_eq_filter(self, query, model, param, arg):
        entity = model()
        type_ = entity.field_py_type(param)
        arg = type_(arg)
        fltr = "%s=%s"%(
            param, "'%s'"%arg if type(arg) != int else arg
        )
        return query.filter(fltr)

    def __init__(self, query_string):
        try:
            self._orig_qs = query_string
            self._kwds = {}
            self._search_params = {}
            for term in query_string.split('&'):
                k,v = term.split("=")
                if k == 'search_query':
                    v = parse.unquote(v).decode('utf8')
                    filters = v.split(';')
                    for f in filters:
                        statement = f.lstrip('+').rstrip().rstrip('+')
                        arg = f[f.index('"'):f.rindex('"')+1]
                        statement = statement.split(arg)[0]
                        arg = arg[1:-1]
                        arg = parse.unquote_plus(arg).decode('utf8')
                        arg = arg.strip()
                        kw = statement[:statement.index('+')]
                        oper = \
                            statement[
                                statement.index('+')+1:statement.rindex('+')
                            ]
                        self._search_params[kw] = (oper, arg)
                else:
                    self._kwds[k] = parse.unquote(v).decode('utf8')
        except:
            log.debug(traceback.format_exc())
            raise

    @property
    def ModelName(self):
        return self._kwds['model_name']

    def get_eq_param_args(self):
        for param in self._search_params:
            oper, arg = self._search_params[param]
            if oper in ['is', '=', '==']:
                yield (param, arg,)



