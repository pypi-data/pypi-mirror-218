import os
import sys
import time
import socket
import threading
import hashlib
from optparse import OptionParser
from wsgiref.simple_server import make_server
import waitress
from pyramid.config import Configurator
from pyramid.renderers import JSONP
# from pyramid.response import Response
# from pyramid.authentication import AuthTktAuthenticationPolicy
# from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory

from tdsl import *
from tdsl import dinj
from tdsl.dinj import Lexicon, BorgLexicon, __borg_lex__, __borg_cls__


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

    parser.add_option(
        "--ns", dest="NS",
        action='store_true',
        default=False, help="Run local Name Server")

    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error("incorrect number of arguments.")
        sys.exit(0)
    return options


OPTS = parse_args()
print(f'. INSTANCE OPTS {OPTS}')
runtime = dinj.Runtime(opts=OPTS)

# now safely import the rest with dinj initialized
# from tdsl.server.api import *
from tdsl.server import ApplicationRuntimeBorg
from tdsl.server.adminviews import *
from tdsl.auth import *
from tdsl.tasks import *
from tdsl.codify import *

__all__ = [
    'PyaellaServer', 'start_instance'
]


APP_CONFIG = None
PSDC = 'PYAELLA_SERVER_DINJ_CONFIG'
BG = []

# def dinj_imports():
#     xsqlalchemy.import_config_for_xsqlalchemy()


class PyaellaServer(threading.Thread):
    """ """

    def __init__(self,
        opts, ns=None, daemon=None, make_app=None, settings={}, *args, **kwds):
        """ """
        threading.Thread.__init__(self, group=None, name='PyaellaServerThread')

        print('PyaellaServer Init', args, kwds)

        self.__arb = ApplicationRuntimeBorg

        self._go = threading.Event()
        self._opts = opts
        print(f'. PyaellaServer set _opts {self._opts}')
        self._ns = ns
        self._daemon = daemon
        for k,w in kwds.items():
            setattr(self, k, w)
        self._config = self._load_config()

        # dinj_imports()

        self._session_fctry = None
        self._settings = settings
        self._task_list_proctor = None
        self._task_list = None
        self._task_list_lock = None
        self._pyramid_server = None
        self._pyramid_app = self._make_app() if not make_app else make_app()
        self._load_optional_services()

    @property
    def App(self):
        return self._pyramid_app

    def _load_config(self):
        dinj_config = None
        if hasattr(self, 'self._config') and self._config:
            return self._config
        else:
            try:
                try:
                    # first assume opts in OptionParser
                    if self._opts and self._opts.CONFIG:
                        dinj_config = Lexicon(parsable=self._opts.CONFIG)
                except:
                    # if not assume opts are a dict, collected from ConfigParser
                    if self._opts and 'pyaella_config' in self._opts:
                        dinj_config = \
                            Lexicon(parsable=self._opts['pyaella_config'])
            except:
                # lastly, look for config in environ
                print(traceback.format_exc())
                if PSDC in os.environ:
                    dinj_config = Lexicon(
                        parsable=os.environ[PSDC])
            if dinj_config:
                # set for safe keeping
                # os.environ[PSDC] = dinj_config.__parsable
                try:

                    self.__arb = ApplicationRuntimeBorg(self._opts)

                    # TODO: deprecate, refactor to remove global
                    global APP_CONFIG
                    APP_CONFIG = self.__arb.get_app_config()

                except:
                    print('Ignoring exception', traceback.format_exc())
            else:
                raise Exception(
                    'Error during configuration injection. '
                    + 'Can not start cooking without the ingredients.'
                )

        return dinj_config

    def _load_optional_services(self):
        try:
            self._task_list = None
            self._task_list_lock = None

            if APP_CONFIG.AsyncFamily == "Threading":
                pass
                # use threads and no processes
                # self._task_list = TaskList(mix_ins=[DefaultTaskList])
                # self._task_list_lock = threading.RLock()
            else:
                #TODO: read in optional mixins
                pass
                # self._task_list_proctor = \
                #     TaskListProctor(mix_ins=[DefaultTaskList])
                # self._task_list_proctor.start()
                # self._task_list = \
                #     self._task_list_proctor.TaskList(mix_ins=[DefaultTaskList])
                # self._task_list_lock = self._task_list_proctor.Lock()

            self._task_list_proctor_factory = \
                TaskListProctorFactory(
                    task_list=self._task_list, lock=self._task_list_lock)

            bg_clz = []

            if('BackgroundModules' in APP_CONFIG.__dict__
                    and APP_CONFIG.BackgroundModules):

                if 'RunBackgroundModulesInApp' in APP_CONFIG.__dict__ and APP_CONFIG.RunBackgroundModulesInApp:
                    print('. Starting BgProcs in App')
                    for m_name in APP_CONFIG.BackgroundModules:
                        m = __import__(m_name, fromlist=[m_name])
                        bg_clz.extend(
                            [   cls
                                for _, cls in m.__dict__.items()
                                if _ in m.__procs__
                                and (
                                        hasattr(cls, 'AsyncFamily')
                                        and
                                        cls.AsyncFamily == APP_CONFIG.AsyncFamily
                                )
                            ]
                        )

            if('JobModules' in APP_CONFIG.__dict__
                    and APP_CONFIG.JobModules):

                if 'RunJobModulesInApp' in APP_CONFIG.__dict__ and APP_CONFIG.RunJobModulesInApp:
                    print('. Starting Async Jobs in App')
                    for m_name in APP_CONFIG.JobModules:
                        m = __import__(m_name, fromlist=[m_name])
                        bg_clz.extend(
                            [   cls
                                for _, cls in m.__dict__.items()
                                if _ in m.__procs__
                                and (
                                        hasattr(cls, 'AsyncFamily')
                                        and
                                        cls.AsyncFamily == APP_CONFIG.AsyncFamily
                                )
                            ]
                        )

            num_bg = 1 if 'NumBackgroundProcs' not in APP_CONFIG.__dict__ else APP_CONFIG.NumBackgroundProcs
            if bg_clz:
                print(f'. bg_clz {bg_clz}')
                global BG
                for bg_cls in bg_clz:
                    for i in range(0, num_bg):
                        bg_inst = bg_cls()
                        bg_inst.start()
                        BG.append(bg_inst)
        except:
            print(traceback.format_exc())

    def _make_app(self):
        """ returns a default Pyramid application """

        # defaults
        default_tmpl_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'defaults/templates')
        tmpl_dir = self._config.Web.TemplateDir
        tmpl_dir = os.path.abspath(tmpl_dir)
        tmpl_dirs = [default_tmpl_dir, tmpl_dir]
        for r, ds, f in os.walk(tmpl_dir):
            if ds:
                for d in ds:
                    if not d.startswith('_') or not d.startswith('jade'):
                        tmpl_dirs.append(os.path.join(r, d))
        self._settings['mako.directories'] = tmpl_dirs

        package = self._config.Web.ScanPackage

        print(f'SCAN PACKAGE: {package}')

        context_clz = None
        if( 'Contexts' in self._config.Resources and
            self._config.Resources.Contexts not in [None, 'None', 'False']):

            context_module = \
                __import__(
                    self._config.Resources.Contexts,
                    fromlist=[self._config.Resources.Contexts]
                )
            context_clz = \
                [c for c in context_module.__dict__
                        if c in context_module.__all__]

        AppRoot = None
        if context_clz:
            AppRoot = context_module.__dict__['AppRoot'] \
                if 'AppRoot' in context_clz \
                else None
            print(f'APP ROOT {AppRoot}')

        try:
            print(f'. self.__arb {self.__arb}')
            models = self.__arb.get_models()

            with SQLAlchemySessionFactory() as session:
                APP = ~models.Application
                apps = session.query(APP).all()
                should_commit = False
                for app in apps:
                    if not app.key_sequence:
                        app.key_sequence = get_app_kseq(app.id, get_master_kseq())
                        session.add(app)
                if should_commit:
                    session.commit()
        except:
            try:
                session.close()
            except:
                pass
            print(traceback.format_exc())
            print('No ETFDsl application configuration.... Ignoring and continuing')
            # raise Exception("Cannot configure Applications. Bailing out.")

        pyramid_config = Configurator(
            root_factory=AppRoot or WebRoot, settings=self._settings)

        pyramid_config.include('pyramid_mako')

        # add authentication and authorization

        # TODO: These is deprecated, refactor to Security Policies
        # Default Authorization Polity
        authz_policy = ACLAuthorizationPolicy()

        # Default Athentication Policcy
        authn_policy = \
            AuthTktAuthenticationPolicy(
                default_auth_hashkey,
                callback=user_group_finder,
                hashalg='sha512'
            )

        # Needed for non-SecurityPolicy based JWT
        pyramid_config.set_authorization_policy(authz_policy)

        ########
        # Set Authentication Policy
        # TODO: Refactor this into Security Policy and comment out
        # pyramid_config.set_authentication_policy(authn_policy)
        #
        # TODO: upgrade to use SecurityPolicy when supporting JWT is possible
        # pyramid_config.set_security_policy(PyaellaSecurityPolicy('secret'))
        ########

        ########
        # Enable JWT authentication
        #
        # config,
        # private_key = None,
        # public_key = None,
        # algorithm = None,
        # expiration = None,
        # leeway = None,
        # http_header = None,
        # auth_type = None,
        # callback = None,
        # json_encoder = None,
        # audience = None,
        # cookie_name = None,
        # https_only = None,
        # samesite = None,
        # reissue_time = None,
        # cookie_path = None,
        # accept_header = None,
        # header_first = None,
        # reissue_callback = None,
        pyramid_config.include('dsl.pyramid_jwt')
        pyramid_config.set_jwt_cookie_authentication_policy(
            private_key='secret',
            auth_type='Bearer',
            reissue_time=7200,
            callback=user_group_finder,
            algorithm='HS256',
            http_header="X-Token",
            https_only=False,
            cookie_name='Token'
            )
        ########

        scss = SignedCookieSessionFactory('itsaseekreet')
        pyramid_config.set_session_factory(scss)

        # pyramid_config.include('pyramid_debugtoolbar')

        pyramid_config.add_renderer(
            'pyaella_json', 'dsl.render.Pyaella_JSON_Renderer')
        pyramid_config.add_renderer(
            'pyaella_xml', 'dsl.render.Pyaella_XML_Renderer')
        pyramid_config.add_renderer(
            'jsonp', JSONP(param_name='callback'))

        # TODO: debug default paths in eggs, not just develop eggs
        default_css_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'defaults/css')
        if os.path.exists(default_css_dir):
            pyramid_config.add_static_view(
                name='pyaellacss', path=default_css_dir)

        default_scripts_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'defaults/scripts')
        if os.path.exists(default_scripts_dir):
            pyramid_config.add_static_view(
                name='pyaellascripts', path=default_scripts_dir)

        if self._config.Web.StaticDirs != None:
            for name, dir_ in self._config.Web.StaticDirs.items():
                dir_ = os.path.abspath(dir_)
                if not os.path.exists(dir_):
                    os.makedirs(dir_)
                pyramid_config.add_static_view(name=name, path=dir_)
                print(f'Added static view {name, dir_}')

        if 'AssetDepot' in self._config.App and self._config.App.AssetDepot:
            try:
                ad_dir_ = os.path.abspath(self._config.App.AssetDepot.Root)
                if not os.path.exists(ad_dir_) and 's3:' not in ad_dir_:
                    os.makedirs(ad_dir_)
                pyramid_config.add_static_view(
                    name='depot', path=ad_dir_)
            except:
                print(f'. ignoring {traceback.format_exc()}')

        print(f'. scanning dsl.server.api/adminviews....')
        pyramid_config.scan(package='dsl.server.api')
        pyramid_config.scan(package='dsl.server.adminviews')

        print(f'. scanning configured view packages....')
        if package != 'dsl.server':
            print(f'. scanning package {package}')
            pyramid_config.scan(package=package)

        print(f'. adding server views....')
        pyramid_config.add_view(
            'dsl.server.api.model_edit_get',
                       request_method = 'GET',
                       context='dsl:server.api.ModelContext',
                       renderer='json',
                       name='edit',
                       permission='edit',
                       #http_cache=(3600*5, {'public':True})
                    )
        pyramid_config.add_view(
            'dsl.server.api.model_edit_put',
                       request_method = 'PUT',
                       context='dsl:server.api.ModelContext',
                       renderer='json',
                       name='edit',
                       permission='edit'
                    )
        pyramid_config.add_view(
            'dsl.server.api.model_edit_post',
                       request_method = 'POST',
                       context='dsl:server.api.ModelContext',
                       renderer='json',
                       name='edit',
                       permission='edit'
                    )
        pyramid_config.add_view(
            'dsl.server.api.model_edit_delete',
                       request_method = 'DELETE',
                       context='dsl:server.api.ModelContext',
                       renderer='json',
                       name='edit',
                       permission='edit'
                    )
        pyramid_config.add_view(
            'dsl.server.api.model_search_get',
                       #request_method = 'GET',
                       context='dsl:server.api.ModelContext',
                       renderer='jsonp',
                       name='search',
                       permission='edit',
                       #http_cache=(3600*4, {'public':True})
                    )
        pyramid_config.add_view(
            'dsl.server.api.model_search_form',
                       context='dsl:server.api.ModelContext',
                       renderer='searchentity.mako',
                       name='s',
                       permission='edit',
                       #http_cache=(3600*4, {'public':True})
                    )
        pyramid_config.add_view(
            'dsl.server.api.model_search_ajax_autocomplete',
                       context='dsl:server.api.ModelContext',
                       renderer='jsonp',
                       name='jxauto',
                       permission='edit',
                       #http_cache=(3600*4, {'public':True})
                    )
        pyramid_config.add_view(
            'dsl.server.api.lookup_table_get_jsonp',
                        name='jsonp',
                        context='dsl:server.api.LookupTableContext',
                        renderer='jsonp',
                        permission='edit',
                        #http_cache=(3600*4, {'public':True})
                    )
        pyramid_config.add_view(
            'dsl.server.api.xmodel_upsert',
                       name='edit',
                       request_method = 'POST',
                       context='dsl:server.api.XModelContext',
                       renderer='json',
                       permission='edit',
                       #http_cache=(3600*4, {'public':True})
                    )
        pyramid_config.add_view(
            'dsl.server.api.xmodel_delete',
                       name='edit',
                       request_method = 'DELETE',
                       context='dsl:server.api.XModelContext',
                       renderer='json',
                       permission='edit',
                       #http_cache=(3600*4, {'public':True})
                    )

        print(f'. created middleware. creating wsgi app....')
        # handle RequestURITooLong issues
        return HttpMethodOverrideMiddleware(pyramid_config.make_wsgi_app())

    def run(self):
        """ """
        self._go.set()
        self._pyramid_server = \
            make_server(
                '0.0.0.0', int(self._config.Web.Port), self._pyramid_app)
        print('PyaellaServer running')
        while self._go.isSet():
            try:
                self._pyramid_server.handle_request()
            except:
                time.sleep(.005)

    def stop(self):
        """ """
        self._go.clear()


def start_instance(opts, standalone=False, **settings):
    """ """
    try:

        hostname=socket.gethostname()

        if not settings:

            if standalone:
                print(f'stand alone settings {settings}')
                ps = PyaellaServer(opts, settings=settings)
                ps.start()
                ps.join()

        if not standalone:
            # return wsgi app to be served
            print('Using WSGI PyaellaServer.App')
            return PyaellaServer(opts, settings=settings).App

    except:
        # TODO: recover if OPTS requires it
        print(traceback.format_exc())
        raise


s = '''Look again at that dot. That's here. That's home. That's us. On it everyone you love, 
everyone you know, everyone you ever heard of, every human being who ever was, 
lived out their lives. The aggregate of our joy and suffering, thousands of confident religions, 
ideologies, and economic doctrines, every hunter and forager, every hero and coward, 
every creator and destroyer of civilization, every king and peasant, every young couple in love, 
every mother and father, hopeful child, inventor and explorer, every teacher of morals, 
every corrupt politician, every "superstar," every "supreme leader," every saint and sinner 
in the history of our species lived there-on a mote of dust suspended in a sunbeam.
'''
default_auth_hashkey = hashlib.sha256(s.encode('utf-8')).hexdigest()


class ShimOpts(object):
    def __init__(self, **kwds):
        for k,v in kwds.items():
            setattr(self, k, v)

    def __contains__(self, name):
        if hasattr(self, name):
            return True

    def __getattr__(self, name):
        return self.__dict__[name]


def serve_pyaella_with_waitress(app_config, **kwds):
    opts = ShimOpts(CONFIG=app_config)
    app = start_instance(opts, standalone=False, **kwds)
    waitress.serve(app)


def main(global_config, **settings):
    """ This function returns a ETFDsl WSGI application.
    """
    import os, sys
    app_config = \
        os.path.join(
            global_config['here'], settings['pyaella_app.config'])
    opts = ShimOpts(CONFIG=app_config)

    if 'pyaella_app.root' in settings:
        root_dir = os.path.abspath(settings['pyaella_app.root'])
        sys.path.insert(0, root_dir)

    # if start_instance is called with settings
    # it is assumed to be a WSGI complaint interface
    return start_instance(opts, standalone=False, **settings)


if __name__ == '__main__':

    start_instance(OPTS, standalone=True)
    print('ETFDsl started')
