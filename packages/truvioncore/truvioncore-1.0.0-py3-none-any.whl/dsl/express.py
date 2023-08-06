__author__ = 'mat mathews'
__version__ = '0.1.0'

import re
import functools
import unicodedata
import unittest

from dsl import *


__all__ = [
    'Expressible',
    'list_from_options',
    'exp_as_bin',
    'exp_as_type',
    'exp_rounded',
    'set_int',
    'check_int',
    'exp_as_str',
    'set_boolean',
    'set_float',
    'twk_txt',
    'twk_hammer',
    'twk_quot',
    'twk_cap_after',
    'twk_nullable_quot',
    'twk_cap_in_between',
    'twk_standard_title_caps',
    'titlecase',
    'singularize',
    'pluralize',
    'create_attr_name',
    'split_list',
    'VOWELS',
    'CONSONETS',
    'TRUES',
    'NULLS',
    'STATES_ABV',
    'STATES_ABV_FOR_NAME'
]


VOWELS = 'aeiouAEIOU'
CONSONETS = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
TRUES = [True, 'True', 'true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh', 'sure']
NULLS = [None, '', ' ']


STATES_ABV = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL',
'IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM',
'NY','NC','ND','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV',
'WI','WY']


CANADA_PROV_ABV =[
    'AB','BC','MB','NB','NL','NT','NS','NU','ON','PE','QC','SK', 'YT'
]


STATES_ABV_FOR_NAME = {
    'ALABAMA':'AL',
    'ALASKA':'AK',
    'ARIZONA':'AZ',
    'ARKANSAS':'AR',
    'CALIFORNIA':'CA',
    'COLORADO':'CO',
    'CONNECTICUT':'CT',
    'DELAWARE':'DE',
    'DISTRICT OF COLUMBIA':'DC',
    'FLORIDA':'FL',
    'GEORGIA':'GA',
    'HAWAII':'HI',
    'IDAHO':'ID',
    'ILLINOIS':'IL',
    'INDIANA':'IN',
    'IOWA':'IA',
    'KANSAS':'KS',
    'KENTUCKY':'KY',
    'LOUISIANA':'LA',
    'MAINE':'ME',
    'MARYLAND':'MD',
    'MASSACHUSETTS':'MA',
    'MICHIGAN':'MI',
    'MINNESOTA':'MN',
    'MISSISSIPPI':'MS',
    'MISSOURI':'MO',
    'MONTANA':'MT',
    'NEBRASKA':'NE',
    'NEVADA':'NV',
    'NEW HAMPSHIRE':'NH',
    'NEW JERSEY':'NJ',
    'NEW MEXICO':'NM',
    'NEW YORK':'NY',
    'NORTH CAROLINA':'NC',
    'NORTH DAKOTA':'ND',
    'OHIO':'OH',
    'OKLAHOMA':'OK',
    'OREGON':'OR',
    'PENNSYLVANIA':'PA',
    'RHODE ISLAND':'RI',
    'SOUTH CAROLINA':'SC',
    'SOUTH DAKOTA':'SD',
    'TENNESSEE':'TN',
    'TEXAS':'TX',
    'UTAH':'UT',
    'VERMONT':'VT',
    'VIRGINIA':'VA',
    'WASHINGTON':'WA',
    'WEST VIRGINIA':'WV',
    'WISCONSIN':'WI',
    'WYOMING':'WY',
}


def is_num(val):
    if type(val) == str:
        if '.' in val:
            try:
                return True, float(val)
            except ValueError:
                return False, None
        else:
            try:
                return True, int(val)
            except ValueError:
                return False, None
    else:
        if type(val) == int or type(val) == float:
            return True, val


class Expressible:
    """ numeric emulation methods """

    def __getattr__(self, attr):
        try:
            return {
                'add': self.__add__,
                'subtract': self.__sub__,
                'filter': self.__mod__,
                'to_ordered_dict': self.__pow__,
                'transform_by': self.__lshift__,
                'and': self.__and__,
                'or': self.__or__,
                'inplace_add': self.__iadd__,
                'inplace_sub': self.__isub__,
                'inplace_transform_by': self.__ilshift__,
                'positive': self.__pos__,
                'negative': self.__neg__,
                'invert': self.__invert__,
                'represent': self.__repr__
            }[attr]
        except KeyError:
            raise NotImplementedError

    def __add__(self, other):
        """ op: +

            create relation between self and other
        """
        raise NotImplementedError

    def __sub__(self, other):
        """ op: -

            remove relation between self and other
        """
        raise NotImplementedError

    def __mod__(self, other):
        """ op: %

            yield filtered results of self % other
        """
        raise NotImplementedError

    def __pow__(self, other):
        """ op: **

            object expansion to OrderedDict
        """
        raise NotImplementedError

    def __lshift__(self, other):
        """ op: <<

            transformative result of self by other
        """
        raise NotImplementedError

    def __and__(self, other):
        """ op: &

            boolean result from self and other
        """
        raise NotImplementedError

    def __or__(self, other):
        """ op: or, |

            boolean result from self or other
        """
        raise NotImplementedError

    def __iadd__(self, other):
        """ op: +=

            inplace transform of self by additional relation to other
        """
        raise NotImplementedError

    def __isub__(self, other):
        """ op: +-

            inplace transform of self by subtraction of relation from other
        """
        raise NotImplementedError

    def __ilshift__(self, other):
        """ op: <<=

            inplace transformation of self by other
        """
        raise NotImplementedError

    def __pos__(self):
        """ op: +

            positive repr of self
        """
        raise NotImplementedError

    def __neg__(self):
        """ op: -

            negative repr of self
        """
        raise NotImplementedError

    def __invert__(self):
        """ op: ~

            topmost or canonical repr of self
        """
        raise NotImplementedError

    def __repr__(self):
        """ op: ` `

            programatic representation of self
        """
        raise NotImplementedError


def list_from_options(opts):
    if opts.startswith('[') and opts.endswith(']'):
        return [x.strip() for x in opts[1:len(opts) - 1].split(',')]


def exp_as_bin(v):
    """ integer to binary ascii string """
    b = lambda n: n > 0 and b(n >> 1) + str(n & 1) or ''
    return '0b' + b(v)


def exp_as_type(type_=False, frmt=None):
    """ """

    def f(func):
        """closurue func"""

        @functools.wraps(func)
        def w(*args, **kwds):
            r = func(*args, **kwds)
            if frmt is not None:
                r = frmt(r)
            if r and type_ is not False:
                return type_(r)

        return w

    return f


def exp_rounded(input):
    """ """
    if input not in [None, 'NULL', '', ' ']:
        return round(float(input))


def set_int(func):
    """ """

    def check(self, arg=None):
        if (arg != None):
            arg = int(arg)
        return func(self, arg)

    return check


def check_int(func):
    """ """

    def check(self, arg=None):
        if arg:
            if type(arg) == int and arg > -1:
                return arg
        return ''

    return check


def exp_as_str(func):
    """ """

    def check(self, arg=None):
        return str(func(self, arg))

    return check


def set_boolean(func):
    """ """

    def check(self, arg=None):
        if (arg != None):
            arg = bool(arg)
        return func(self, arg)

    return check


def set_float(func):
    """ """

    def check(self, arg=None):
        if (arg != None):
            arg = float(arg)
        return func(self, arg)

    return check


def twk_hammer(unicrap):
    """
        This takes a UNICODE string and replaces Latin-1 characters with
        something equivalent in 7-bit ASCII. It returns a plain ASCII string.
        This function makes a best effort to convert Latin-1 characters into
        ASCII equivalents. It does not just strip out the Latin-1 characters.
        All characters in the standard 7-bit ASCII range are preserved.
        In the 8th bit range all the Latin-1 accented letters are converted
        to unaccented equivalents. Most symbol characters are converted to
        something meaningful. Anything not converted is deleted.
    """
    xlate = {0xc0: 'A', 0xc1: 'A', 0xc2: 'A', 0xc3: 'A', 0xc4: 'A', 0xc5: 'A',
             0xc6: 'Ae', 0xc7: 'C',
             0xc8: 'E', 0xc9: 'E', 0xca: 'E', 0xcb: 'E',
             0xcc: 'I', 0xcd: 'I', 0xce: 'I', 0xcf: 'I',
             0xd0: 'Th', 0xd1: 'N',
             0xd2: 'O', 0xd3: 'O', 0xd4: 'O', 0xd5: 'O', 0xd6: 'O', 0xd8: 'O',
             0xd9: 'U', 0xda: 'U', 0xdb: 'U', 0xdc: 'U',
             0xdd: 'Y', 0xde: 'th', 0xdf: 'ss',
             0xe0: 'a', 0xe1: 'a', 0xe2: 'a', 0xe3: 'a', 0xe4: 'a', 0xe5: 'a',
             0xe6: 'ae', 0xe7: 'c',
             0xe8: 'e', 0xe9: 'e', 0xea: 'e', 0xeb: 'e',
             0xec: 'i', 0xed: 'i', 0xee: 'i', 0xef: 'i',
             0xf0: 'th', 0xf1: 'n',
             0xf2: 'o', 0xf3: 'o', 0xf4: 'o', 0xf5: 'o', 0xf6: 'o', 0xf8: 'o',
             0xf9: 'u', 0xfa: 'u', 0xfb: 'u', 0xfc: 'u',
             0xfd: 'y', 0xfe: 'th', 0xff: 'y',
             0xa1: '!', 0xa2: '{cent}', 0xa3: '{pound}', 0xa4: '{currency}',
             0xa5: '{yen}', 0xa6: '|', 0xa7: '{section}', 0xa8: '{umlaut}',
             0xa9: '{C}', 0xaa: '{^a}', 0xab: '<<', 0xac: '{not}',
             0xad: '-', 0xae: '{R}', 0xaf: '_', 0xb0: '{degrees}',
             0xb1: '{+/-}', 0xb2: '{^2}', 0xb3: '{^3}', 0xb4: "'",
             0xb5: '{micro}', 0xb6: '{paragraph}', 0xb7: '*', 0xb8: '{cedilla}',
             0xb9: '{^1}', 0xba: '{^o}', 0xbb: '>>',
             0xbc: '{1/4}', 0xbd: '{1/2}', 0xbe: '{3/4}', 0xbf: '?',
             0xd7: '*', 0xf7: '/'
             }
    r = ''
    for i in unicrap:
        if ord(i) in xlate:
            r += xlate[ord(i)]
        elif ord(i) >= 0x80:
            pass
        else:
            r += str(i)
    return r


def twk_txt(input, useStr=False, allowPadding=False):
    """ """
    output = re.sub('"', '', str(input))
    if not allowPadding:
        output = re.sub('\s+', ' ', output)
    output = re.sub(u'\u2018', '', output)  # left fancy quote
    output = re.sub(u'\u2019', '', output)  # right fancy quote
    output = re.sub(u'\u201c', '', output)  # left fancy double quote
    output = re.sub(u'\u201d', '', output)  # right fancy double quote
    output = re.sub("'", "", output)
    output = re.sub("\t", " ", output)
    output = re.sub("\n", " ", output)
    if useStr:
        return str(output)
    return output


def twk_quot(input, quotChar="'"):
    """ """
    try:
        return str('%s%s%s' % (quotChar, twk_txt(input), quotChar))
    except Exception as e:
        return str('%s%s%s' % (quotChar, twk_hammer(str(input)), quotChar))


def twk_nullable_quot(input, useUnicode=False, allowPadding=False):
    """ """
    if useUnicode:
        if input == None or str('%s' % input).lower() == 'null':
            return u'NULL'
        return str(
            '%s%s%s' % ("'", twk_txt(input, allowPadding=allowPadding), "'"))
    else:
        try:
            if input == None or str('%s' % input).lower() == 'null':
                return 'NULL'
            return str('%s%s%s' % (
                "'",
                twk_txt(input, useStr=True, allowPadding=allowPadding), "'"))
        except Exception as e:
            return str(
                '%s%s%s' % ("'", twk_hammer(str(input)), "'"))


SMALL = 'f/|a|an|and|as|at|but|by|en|for|if|in|of|on|or|the|to|v\.?|via|vs\.?'
PUNCT = "[!\"#$%&'‘()*+,-./:;?@[\\\\\\]_`{|}~]"
SMALL_WORDS = re.compile(r'^(%s)$' % SMALL, re.I)
INLINE_PERIOD = re.compile(r'[a-zA-Z][.][a-zA-Z]')
UC_ELSEWHERE = re.compile(r'%s*?[a-zA-Z]+[A-Z]+?' % PUNCT)
CAPFIRST = re.compile(r"^%s*?([A-Za-z])" % PUNCT)
SMALL_FIRST = re.compile(r'^(%s*)(%s)\b' % (PUNCT, SMALL), re.I)
SMALL_LAST = re.compile(r'\b(%s)%s?$' % (SMALL, PUNCT), re.I)
SUBPHRASE = re.compile(r'([:.;?!][ ])(%s)' % SMALL)


def titlecase(text):
    """ Titlecases input text

    This filter changes all words to Title Caps, and attempts to be clever
    about *un*capitalizing SMALL words like a/an/the in the input.

    The list of "SMALL words" which are not capped comes from
    the New York Times Manual of Style, plus 'vs' and 'v'.

    """
    words = re.split('\s', text)
    line = []
    for word in words:
        if INLINE_PERIOD.search(word) or UC_ELSEWHERE.match(word):
            line.append(word)
            continue
        if SMALL_WORDS.match(word):
            line.append(word.lower())
            continue
        line.append(CAPFIRST.sub(lambda m: m.group(0).upper(), word))

    line = " ".join(line)

    line = SMALL_FIRST.sub(lambda m: '%s%s' % (
        m.group(1),
        m.group(2).capitalize()
    ), line)

    line = SMALL_LAST.sub(lambda m: m.group(0).capitalize(), line)

    line = SUBPHRASE.sub(lambda m: '%s%s' % (
        m.group(1),
        m.group(2).capitalize()
    ), line)

    return line


def twk_cap_after(theText, after):
    """ """
    split = theText.split(after)
    split[len(split) - 1] = split[len(split) - 1].strip()
    split[len(split) - 1] = titlecase(split[len(split) - 1])
    return ('%s' % (after)).join(split)


def twk_cap_in_between(theText, key, tween):
    """ """
    split = theText.split(key)
    # split[len(split)-1] = split[len(split)-1].strip()
    split[len(split) - 1] = titlecase(split[len(split) - 1])
    return ('%s' % (tween)).join(split)


def twk_standard_title_caps(theText):
    """ """
    a = theText
    try:
        a = twk_hammer(theText)
    except:
        if type(theText) == str:
            a = unicodedata.normalize('NFKD', theText).encode('ascii', 'ignore')
    try:
        a = titlecase(str(a).lower())
    except Exception as iie:
        pass

    toReplace = {
        ' Ii ': ' II ',
        'Dj': 'DJ'
    }
    toCapAfter = {
        'f/': '/f ',
        'F/': '/f ',
        'W/': '/w ',
        'w/': '/w ',
        " o'": " O'",
        " O'": " O'",
        ' Mc': ' Mc',
        ' Mac': ' Mac'
    }

    for afterK, afterV in toCapAfter.items():
        if afterK in a:
            a = twk_cap_after(a, afterV)

    for replaceK, replaceV in toReplace.items():
        if replaceK in a:
            a = twk_cap_in_between(a, replaceK, replaceV)

    if '.' in a:
        split = a.split('.')
        if len(split) > 1:
            # Junior m.A.F.I.A.
            if (split[0][len(split[0]) - 2] == '\s' or
                    split[0][len(split[0]) - 2] == ' '):
                splitFront = split[0].split(' ')
                split[0] = '%s %s' % (splitFront[0], splitFront[1].upper())

                # split[0][len(split[0])-1] ==
                # split[0][len(split[0])-1].capitalize()

        for i in range(1, len(split)):
            st = split[i].strip()
            if len(st) != len(split[i]):
                split[i] = ' %s' % (titlecase(st))
            else:
                split[i] = '%s' % (titlecase(st))
        a = '.'.join(split)

    if '-' in a:
        split = a.split('-')
        for i in range(1, len(split)):
            split[i] = titlecase(str(split[i]))
        a = '-'.join(split)

    a = a[:1].capitalize() + a[1:]
    return a


def singularize(word):
    sing_rules = [lambda w: w[-3:] == 'ies' and w[:-3] + 'y',
                  lambda w: w[-4:] == 'ives' and w[:-4] + 'ife',
                  lambda w: w[-3:] == 'ves' and w[:-3] + 'f',
                  lambda w: w[-4:] == 'uses' and w[:-3] + 's',
                  lambda w: w[-2:] == 'es' and w[:-2],
                  lambda w: w[-1:] == 's' and w[:-1],
                  lambda w: w[-2:] == 'ii' and w[:-2] + 'ius',
                  lambda w: w[-1:] == 'i' and w[:-1] + 'us',
                  lambda w: w,
                  ]
    word = word.strip()
    return [f(word) for f in sing_rules if f(word) is not False][0]


def pluralize(word):
    plur_rules = [
        lambda w: (w[-1] == 'y' and w[-2] not in VOWELS) and w[:-1] + 'ies',
        lambda w: (
                          w[-1] == 's' and w[-4] in VOWELS and w[-3:] == 'ius'
                  ) and w[:-3] + 'i',
        lambda w: (
                          w[-1] == 's' and w[-2:] == 'us' and len(w) > 6
                  ) and w[:-2] + 'i',
        lambda w: (w[-1] == 's' and w[-2:] == 'us') and w + 'es',
        lambda w: (w[-1] == 's' and w[-2] in VOWELS) and w[:-1] + 'ses',
        lambda w: (w[-1] == 's' and w[-2] not in VOWELS) and w + 'es',
        lambda w: w[-2:] in ('ch', 'sh') and w + 'es',
        lambda w: w and w + 's'
    ]
    word = word.strip()
    return [f(word) for f in plur_rules if f(word) is not False][0]


def create_attr_name(s, do_singularize=True):
    """ with _ """
    parts = s.split('_')
    last = parts[len(parts) - 1]
    if do_singularize:
        last = singularize(last)
    parts[len(parts) - 1] = last
    return ''.join(map(str.capitalize, parts))


def split_list(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class Mock_X:
    def __init__(self, num):
        self.num = num

    def __int__(self):
        return self.num


class Mock_Y:
    def __init__(self, num):
        self.num = num

    def __add__(self, other_obj):
        print('Mock_Y.__add__ called')
        if(type(other_obj) is Mock_Y):
            return Mock_Y(self.num+other_obj.num)
        else:
            return NotImplemented

    def __radd__(self, other_obj):
        print('Mock_Y.__radd__ called')
        return Mock_Y(self.num+other_obj.num)

    def __str__(self):
        return str(self.num)

    def __repr__(self):
        return self.num

    def __int__(self):
        return self.num


class Mock_Z:

    def __init__(self, num):
        self.num = num

    def __add__(self, other_obj):
        print('Mock_Z.__add__ called')
        return Mock_Y(self.num+other_obj.num)

    def __radd__(self, other_obj):
        print(f'Mock_Z.__radd__ called with other {type(other_obj)}')
        return Mock_Y(self.num+other_obj.num)

    def __str__(self):
        return str(self.num)

    def __repr__(self):
        return self.num

    def __int__(self):
        return self.num


class TestExpressSetup(unittest.TestCase):

    def test__add_setup(self):

        x = Mock_X(2)

        y = Mock_Y(3)
        y_2 = Mock_Y(4)

        z = Mock_Z(8)

        print(f'returns from y -> (y + y_2) {(y + y_2)} \n')

        print(f'returns from y -> (y + z) { (y + z) } \n')

        # # returns from y
        # print(f'returns from y -> (x + y)')
        # new_val = (x + y)
        # print('\n')

        # # cast the returned Mock_Y to int
        # self.assertEqual(5, int(new_val))
        #
        # caught_exc = False
        # try:
        #     # returns from x (which doesn't implement it, should raise exception
        #     print(y + x)
        # except TypeError as te:
        #     self.assertEqual(type(te), TypeError)
        #     caught_exc = True
        #
        # self.assertTrue(caught_exc)
