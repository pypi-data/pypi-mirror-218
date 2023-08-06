import os
import sys
import yaml
import importlib
import datetime
import traceback
from optparse import OptionParser
from mako.template import Template
from mako.lookup import TemplateLookup
from sqlalchemy import *
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from tdsl.dinj import get_lexical_tokens, LexicalToken, parse_lgcl_mdl_rl_name

# from tdsl import orm
# from tdsl.orm import *

DECLBASE = None
METACLS = None
REFLMETACLS = None
SUPERCLS = None

sch = None


def dump(sql, *multiparams, **params):
    print((sql.compile(dialect=engine.dialect)))


def _doc(all_):
    sorted_all = list(all_)
    sorted_all.sort()

    autoclass_str = \
        '''
        .. autoclass:: Kasayama.models.%s
            :members:
            :special-members:
        '''
    for cn in sorted_all:
        print((autoclass_str % cn))


def doit():
    global sch

    if not options.LEXICON:
        raise Exception('Domain schema file required')

    domainfp = os.path.abspath(options.LEXICON)

    decl_order = []
    with open(domainfp, 'r') as f:
        for line in f.readlines():
            if line:
                if line[0] not in ['', ' ', '\n', '\t', '#', '^']:
                    line = line.strip('\n')
                    if line.endswith(':'):
                        # line = line.strip(':')
                        if line[:-1].upper() not in ['LEXC', 'REFLECTIVE', 'AFTER_CREATE_SQL']:
                            line = line.strip()
                            if line[0] == '(':
                                name, opts = parse_lgcl_mdl_rl_name(line[:-1])
                                decl_order.append(name)

    # print('Declarative order', decl_order)

    sch = get_lexical_tokens(domainfp) \
        if os.path.exists(domainfp) \
        else None

    print(('Domain schema', sch))

    print(('Compiling domain - %s' % domainfp))

    if 'LEXC' not in sch:
        raise Exception('LEXC directives required in Domain schema file')

    DECLBASE = sch.LEXC.DeclBase
    METACLS = sch.LEXC.MetaCls
    REFLMETACLS = sch.LEXC.ReflMetaCls
    SUPERCLS = sch.LEXC.SuperCls

    docstrings = {}  # k: classname, v: docstring

    cn = decl_order

    geod = []
    for c in cn:
        field = sch[c].Fields if 'Fields' in sch[c] else None
        if field:
            for k, v in list(field.items()):
                if k == 'geom':
                    geod.append(c)
        if 'Doc' in sch[c]:
            doclines = sch[c].Doc.split('\n')
            for i in range(0, len(doclines)):
                doclines[i] += '\n'
            doclines[-1] = doclines[-1].strip('\n')
            ds = '\t'.join(doclines)
            docstrings[c] = ds

    mixables = [c for c in cn if 'EntityMixes' in sch[c]]

    rcn = []
    if 'REFLECTIVE' in sch:
        rcn = [k for k, v in list(sch['REFLECTIVE'].items())]

    print(('reflective classes', rcn))

    model_def_classes = {}
    for c in rcn:
        print(f". model_def_classes {sch['REFLECTIVE'][c]}")
        if sch['REFLECTIVE'][c] != None:
            # use ModelDef and not default
            model_def_classes[c] = sch['REFLECTIVE'][c]

    info = {
        'decl_base': DECLBASE,
        'reflect_decl_base': 'ReflectiveBase',
        'metacls_name': METACLS,
        'refl_metacls_name': REFLMETACLS,
        'supercls_name': SUPERCLS,
        'class_names': cn,
        'docstrings': docstrings,
        'reflective_class_names': rcn,
        'geometry_classes': geod,
        'model_def_classes': model_def_classes,
        'mixable_classes': mixables,
        'date': datetime.datetime.now(),
        'domain_schema_file': os.path.basename(domainfp) or None
    }

    print(f'class info {info}')

    tmpl_file = ''
    if options.TMPLFILE in [None, '']:
        tmpl_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'tmpl', 'pdm.mako')
    else:
        tmpl_file = os.path.abspath(options.TMPLFILE)

    t = Template(filename=os.path.abspath(tmpl_file))
    result = t.render(**info)
    if options.OUTPUTFILE:
        with open(os.path.abspath(options.OUTPUTFILE), 'w') as f:
            f.write(result)
    else:
        print(result)


def parseArgs(args=None):
    parser = OptionParser()

    parser.add_option("-d", dest="LEXICON", help="Domain file")
    parser.add_option("-t", dest="TMPLFILE", help="Template file")
    parser.add_option("-o", dest="OUTPUTFILE", help="Output file")

    parser.add_option("--html-form", dest="DOHTMLFORM",
        action='store_true', 
        default=False, 
        help="Generate HTML Form")

    (options, args) = parser.parse_args()

    if options != None:
        return options

def output_html_form():
    #__import__(options.OUTPUTFILE)

    new_module = str(options.OUTPUTFILE).lstrip('./').replace('/', '.').replace('.py', '')

    print(f'{new_module}')

    domain = importlib.import_module(new_module)

    print(f'domain {domain}')

    print(f'{domain.__all__}')

    data_models = dict([(name, cls)
                        for name, cls in domain.__dict__.items()
                        if isinstance(cls, type) and name in domain.__all__])

    model_tmpl_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'server', 'defaults', 'templates', 'postentity.mako')
    model_tmpl_file_lu = TemplateLookup(directories=['/Users/mat/Documents/Pyaella3/dsl/server/defaults/templates/'])

    for n, dm in data_models.items():
        print(f'Initd {n} {dm}')
        model = dm()
        tmpl_info = {
            'model': {},
            'model_name': model.Name,
            'entity': None,
            'override_method': 'POST'
        }

        print(f'{n} - fields {model.Fields}')
        for field in model.Fields:
            fld_def = model.field_def(field).get_html_presentable()
            tmpl_info['model'][field] = {
                'fld_def': fld_def
            }

        print(f'{n} - relations {model.Relations}')
        for relation in model.Relations:
            print(f'relation - {relation}')
            try:
                fld_def = model.field_def(relation).get_html_presentable()
                tmpl_info['model'][relation] = {
                    'fld_def': fld_def
                }
            except:
                print(traceback.format_exc())

        oflds = model.Fields
        try:
            oflds.remove('id')
            oflds.remove('key')
        except:
            pass

        tmpl_info['ordered_fields'] = oflds
        # exclude NotSupported
        tmpl_info['ordered_fields'].extend(r for r in model.Relations if r in tmpl_info['model'])

        print(f'tmpl_info: {tmpl_info}')

        tmpl_pe = Template(filename=os.path.abspath(model_tmpl_file), lookup=model_tmpl_file_lu)

        result = tmpl_pe.render(**tmpl_info)
        print(f'{n} templated: {result}')

        try:
            os.makedirs('/Users/mat/Documents/Pyaella3/Kasayama/svelte/src/models/', exist_ok=True)
        except:
            print(traceback.format_exc())
            pass

        output_js_file = os.path.join(
            '/Users/mat/Documents/Pyaella3/Kasayama/svelte/src/models/',
            n + '.html'
        )

        with open(output_js_file, 'w') as of:
            of.write(result)


if __name__ == '__main__':

    print('starting dsl domain compilation')
    options = parseArgs()
    print('generating dsl domain {options.OUTPUTFILE} from lexicon {options.LEXICON}')
    r = doit()

    if options.DOHTMLFORM:
        output_html_form()

    print('done.')


