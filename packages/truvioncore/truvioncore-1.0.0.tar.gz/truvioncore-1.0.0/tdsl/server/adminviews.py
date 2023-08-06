import sys, os
import traceback
import jsonpickle
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import *
from tdsl.server.api import *
from tdsl import dinj
from tdsl.orm import *


SASF = None
_models = None


def import_models_for_adminviews(models_module_name):
    return __import__(
        models_module_name, 
        fromlist=[models_module_name])


def get_session():
    global SASF
    global _models
    if not SASF:
        SASF = SQLAlchemySessionFactory()
        _models = import_models_for_adminviews(SASF.ModelsModuleName)
    return SQLAlchemySessionFactory().Session


def _get_app_config():
    return dinj.AppConfig()


def _get_dinj_config(app_config):
    return dinj.DinjLexicon(parsable=app_config.FullConfigPath)


@view_config(
    name='hello',
    request_method='GET',
    context='dsl:server.api.AdminContext',
    permission='edit'
    )
def hello_world(request):
    r = '''
    <html>
        <font size="7"><b>Benvingut a ETFDsl!</b></font>
    </html>
    '''
    return Response(r)


@view_config(
    name='list_paths',
    request_method='GET',
    context='dsl:server.api.AdminContext',
    permission='su'
    )
def list_paths(request):
    try:
        c = _get_dinj_config(_get_app_config())
        output = '<html>'
        for p in [
            c.App.UploadDirectory,
            c.App.AssetDepot.Root,
            c.Web.TemplateDir,
            c.Web.StaticDirs.assets,
            c.Web.StaticDirs.player,
            c.Web.StaticDirs.css,
            c.Web.StaticDirs.scripts
        ]:
            output+='<br>%s<br>'%p

        ap = os.path.join(
                "/",
                os.path.basename(os.path.dirname(c.App.AssetDepot.Root)), 
                '(owner.access_token)(asset_id)(asset_extention)')

        output+='<br>Test URL for Asset: %s<br>'%ap

        output+='</html>'
        return Response(output)
    except:
        print(traceback.format_exc())
        return HTTPNotFound('Resource not found')


@view_config(
    name='list_models',
    request_method='GET',
    context='dsl:server.api.AdminContext',
    permission='edit',
    renderer='json'
    )
def list_models(request):
    try:
        m = get_injected_models()
        r = '''
        <html>
            <p>%s</p>
        </html>
        '''%(str(m.__dict__))
        d = dict(
            model_names=[k for k in m.__all__]
        )
        return Response(body=json.dumps(d))
    except:
        print(traceback.format_exc())
        return HTTPServerError('Exception in list_models')


@view_config(
    name='postentity',
    request_method='GET',
    context='dsl:server.api.AdminContext',
    renderer='postentity.mako',
    #permission='su'
    )
def post_entity(request):
    """ """
    try:
        model_cls, args = model_cls_from_subpath(request)
        model = model_cls()
        r = {
            'model':{},
            'model_name': model.Name,
            'entity':None,
            'override_method':'POST'
        }
        for field in model.Fields:
            fld_def = model.field_def(field)
            r['model'][field] = {
                'fld_def': fld_def
            }
        for relation in model.Relations:
            fld_def = model.field_def(relation)
            r['model'][relation] = {
                'fld_def': fld_def
            }
        oflds = model.Fields
        try:
            oflds.remove('id')
            oflds.remove('key')
        except:
            pass
        r['ordered_fields'] = oflds #model.Fields
        r['ordered_fields'].extend(model.Relations)
        return r
    except:
        print(traceback.format_exc())
        return HTTPNotFound('Resource not found')


@view_config(
    name='viewentity',
    request_method='GET',
    context='dsl:server.api.AdminContext',
    renderer='viewentity.mako',
    #permission='su'
    )
def view_entity(request):
    """
        /_a/[ModelName]/id=[0] || key=['key']
    """

    print(f'view_entity called')
    try:
        model, key, kwds, entity = retrieve_entity(request)
        print(f'view_entity retrieve_entity result {model, key, kwds, entity}')
        r = {
            'model':{},
            'model_name': entity.Name,
            'entity': entity.to_dict(),
            'override_method':'PUT'
        }
        for field in entity.Fields:
            fld_def = entity.field_def(field)
            r['model'][field] = {
                'fld_def': fld_def
            }
        for relation in entity.Relations:
            fld_def = entity.field_def(relation)
            r['model'][relation] = {
                'fld_def': fld_def
            }
        r['ordered_fields'] = entity.Fields
        r['ordered_fields'].extend(entity.Relations)
        return r
    except:
        print(traceback.format_exc())
        return HTTPNotFound('Resource not found')