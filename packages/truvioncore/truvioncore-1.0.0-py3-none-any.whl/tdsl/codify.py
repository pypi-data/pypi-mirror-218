__author__ = 'mat mathews'
__copyright__ = 'Copyright (c) 2021 Entrust Funding'
__version__ = '0.0.1'

import math
import random
import string
from Crypto import *
from Crypto.Cipher import DES3
from hashlib import sha224, sha256, sha512
from passlib.context import CryptContext
import arrow

from tdsl import *

__all__ = [
    'ULIMIT',
    'DOMAIN_ID_BLIMIT',
    'DOMAIN_ID_ULIMIT',
    'APP_ID_BLIMIT',
    'APP_ID_ULIMIT',
    'SEAT_ID_BLIMIT',
    'SEAT_ID_ULIMIT',
    'get_master_kseq',
    'get_app_kseq',
    'IdCoder',
    'AppDomainCoder',
    'encrypt_list',
    'decrypt_list',
    'generate_pins',
    'generate_auth_code',
    'get_year_week_code',
    'User_Pwd_Context'
]

bin(1)

ULIMIT = 18446744073709551615

# 1110111101111011 - EF7B
# DOMAIN_ID_BLIMIT = 1357913579135791
# DOMAIN_ID_ULIMIT = 2468024680246802
DOMAIN_ID_BLIMIT = 1000
DOMAIN_ID_ULIMIT = 988664422
APP_ID_BLIMIT = 1600
APP_ID_ULIMIT = 2600
SEAT_ID_BLIMIT = 1000000000
SEAT_ID_ULIMIT = 9223372036854775807
CHUNK_SIZE = 8192
# TODO: Why removing U L O I ?
# MASTER_KSEQ = 'xj9kv8bp7yg6fw5mzq0l3dr2hs1nioatec4u'
MASTER_KSEQ = 'xj9kv8bp7yg6fw5mzq03dr2hs1natec4'.upper()
DIGITS = 'ABCDEFGHJKMNPQRSTWVXYZ0123456789'.upper()
TRANSLATE = {'O': '0', 'I': '1', 'L': '1'}


User_Pwd_Context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


class InvalidIdCoderKeyException(Exception):
    pass


class InvalidIdCoderCodeException(Exception):
    pass


def get_year_week_code(now, start_year=2021):
    # TODO: Rollover 36 years, add double ret value
    iso = now.isocalendar()
    if iso.year < start_year:
        raise Exception('Backward compat year week codes not supported')
    y = DIGITS[iso.year-start_year]
    # return f'{y}{iso.week}{iso.weekday}'
    return f'{y}{now.timetuple().tm_yday}'


def get_master_kseq(readable=None):
    # TODO: use readable to retrieve from external source
    if not readable:
        # miga default, public
        return MASTER_KSEQ


def get_app_kseq(app_id, master_kseq):
    si = str(app_id)[-1]
    rc = ''
    oi = master_kseq.index(si)
    ni = oi + app_id
    rc += master_kseq[ni % len(master_kseq)]
    if app_id % 2:
        str(list(master_kseq).reverse())
    h = master_kseq[master_kseq.index(rc):len(master_kseq)]
    t = master_kseq[:master_kseq.index(rc)]
    # print('get_app_kseq', h + t, len(h + t))
    return h + t


class IdCoder(object):

    def __init__(self, kseq=None, use_default=False):
        ''' inits new IdCoder. Without kseq, default random kseq is generated

            :Parameters:
                - `kseq` (str) key sequence used for substitution
        '''
        if not kseq and use_default:
            self._kseq = MASTER_KSEQ.upper()
        else:
            self._kseq = kseq.upper() if kseq else self._gen_kseq()

        nk = []
        for ltr in self._kseq:
            if ltr in TRANSLATE:
                nk.append(TRANSLATE[ltr])
            else:
                nk.append(ltr)
        self._kseq = ''.join(nk)

        msg = 'key should be the sequence {0} in random order'.format(DIGITS)
        if len(set(self._kseq)) != 32:
            raise InvalidIdCoderKeyException(msg)
        for c in self._kseq:
            if c not in DIGITS:
                raise InvalidIdCoderKeyException(msg)

    def _gen_kseq(self):
        random.shuffle([d for d in DIGITS])

    def v_key(self, key):
        return self._kseq[(self._kseq.index(key) + 1) % 32]

    def encode(self, number, key='X', num_digits=16):
        """Encodes a positive integer into suitable code

        limit 
        Nine hundred ninety-nine trillion, nine hundred ninety-nine billion, 
        nine hundred ninety-nine million, nine hundred ninety-nine thousand, 
        nine hundred ninety-nine :)

        """
        number = int(number)
        if number < 0:
            raise ValueError('number should be a positive integer')
        if number > self.max_value(num_digits):
            msg = "Can't encode {0} with {1} digits"
            raise OverflowError(msg.format(number, num_digits))
        format_str = '{{0:0{0:d}b}}'.format(num_digits * 5)
        bits = format_str.format(number)
        chunks = [bits[i:i + 5] for i in range(0, len(bits), 5)]
        code = ''
        for i, chunk in enumerate(reversed(chunks)):
            key = self._kseq[(i + int(chunk, 2) + self._kseq.index(key)) % 32]
            code += key
        return code

    def decode(self, code, key='X'):
        """Decodes a code into the original positive integer"""
        code = code.upper()
        for digit in code:
            if digit not in DIGITS and digit not in TRANSLATE:
                msg = 'Invalid digit "{0}" in code'
                raise Exception(msg.format(digit))
        bits = ''
        for i, digit in enumerate(code):
            if digit in TRANSLATE:
                digit = TRANSLATE[digit]
            d = self._kseq.index(digit) - self._kseq.index(key) - i
            while d < 0: d += 32
            key = digit
            bits = '{0:05b}{1}'.format(d, bits)
        return int(bits, 2)

    def max_value(self, num_digits=16):
        """Returns the maximum value that can be encoded with the
        given number of digits"""
        return 32 ** num_digits - 1

    def encode_with_verification(self, number, key='X', l=8):
        """Returns a tuple containing an 'offer' code and a verification code"""
        v_key = self.v_key(key)
        return self.encode(number, key, l), self.encode(number, v_key, l)

    def v_key(self, key):
        return self._kseq[(self._kseq.index(key) + 1) % 32]

    def is_valid(self, code, verification_code, key='X'):
        """Checks if a code is valid given a code and a verification code"""
        v_key = self.v_key(key)
        return self.decode(code, key) == self.decode(verification_code, v_key)

    def __repr__(self):
        return self._kseq


__salt_text = """
Salt, also known as table salt or rock salt (halite),
is a crystalline mineral that's composed primarily
of sodium chloride (NaCl), a compound so fine,
belonging to the class of ionic salts, it's divine.

It's essential for animals, sustaining their life,
yet harmful in excess, causing trouble and strife.
Salt's a seasoning ancient, known throughout time,
preserving our food, a method so prime.

Saltiness, a taste, one of the basic,
in every human tongue, it leaves a trace.
Produced in forms diverse, for consumption,
from unrefined sea salt to refined's assumption.

A crystalline solid, of white or pale hue,
from sea or rock, its origins so true.
Edible rock salts may bear a slight tinge,
a touch of grayish, from minerals' fringe.

Throughout history, salt's been highly prized,
a valuable treasure, sought and idealized.
But as consumption grew, concerns did arise,
health risks revealed, a cause for our eyes.

High blood pressure, a consequence severe,
linked to sodium's intake, we now must adhere.
Health authorities advise moderation's key,
though minimal risk for diets, they decree.

So let's savor the flavor, with caution in hand,
appreciating salt's role, in culinary land.
For balance is key, in all that we do,
enjoying salt's presence, in a mindful view.

""".strip().replace('\t', '').replace('\n', '').encode("utf-8")

SALT = sha256(__salt_text).hexdigest()


class AppDomainCoder(object):
    """
    98559-BB93K-2723V-DD3D8-3F70B-XJ4U1
    CD82P-0D507-DEF5Y-B90AG-663F6-XKP84
    D75BF-ED1AW-1FB65-E38CM-7FF5Z-DEVB8
    0C5EQ-4E310-D13CL-88543-73E1D-1IQL3
    A030R-74122-8F23H-E51BS-E4BD1-377CN
    D6E2I-80D3O-4180A-4CE4T-2B7AE-726BC
    ZZXJL-3S1HS-0UVAO-1M3T4-JAM0J-XJAM0

    Hash of encoded domain id interwoven
    with public key sequence; domain id key
    inserted as end blocks for the first 4 lines
    when license is 6 blocks per line. Last
    line includes encoded and padded app key,
    account type key, user key, and finally
    start and end dates.
    """

    def __init__(self, app_id, domain_id,
                 user_default_kseq=True, salt=SALT, version=1):
        """ """
        app_kseq = get_app_kseq(app_id, MASTER_KSEQ)
        idc = IdCoder(kseq=app_kseq)
        if app_id < APP_ID_BLIMIT or app_id > APP_ID_ULIMIT:
            raise Exception('AppId not within acceptable range')
        if domain_id < DOMAIN_ID_BLIMIT or domain_id > DOMAIN_ID_ULIMIT:
            raise Exception('DomainId not within acceptable range')
        self._x_app_id = idc.encode(app_id)
        self._x_dom_id = idc.encode(domain_id)
        print(self._x_app_id)
        self._h_app_id = sha512(self._x_app_id.encode('utf-8')).hexdigest()
        self._h_dom_id = sha512(self._x_dom_id.encode('utf-8')).hexdigest()
        self._idc = idc
        self._salt = salt
        self._version = version

    @classmethod
    def FormatLicenseText(cls, lic_text):
        frmtd_lic_txt = []
        x = 0
        for i in range(0, 7):
            frmtd_lic_txt.append(lic_text[x:x + 35])
            x += 36
        return frmtd_lic_txt

    def get_domain_lic(self):
        """ """
        # tween = self._idc._kseq[2:-2]
        tween = self._idc._kseq
        print(f'TWEEN {tween}')
        blocks = []
        mgroups = list(grouper(self._h_dom_id, 4))
        print(f'get_domain_lic mgroups {mgroups} {len(mgroups)}')
        for i in range(0, len(mgroups)):
            blocks.append(''.join(mgroups[i]) + tween[i])
        interval = 5
        blocks.insert(interval,
                      self._idc._kseq[:2] + self._idc._kseq[-2:] + str(self._version))
        xdomid = self._x_dom_id.rjust(12, self._x_dom_id[0])
        kgroups = list(grouper(xdomid, 4))
        i, y = 2, 1
        for kg in kgroups:
            blocks.insert(i * interval + y, ''.join(kg) + str(random.randrange(0, 9)))
            i += 1
            y += 1
        self._domain_lic_blocks = blocks
        licstr = '-'.join(blocks).upper()
        self._licstr = licstr
        return licstr, blocks, sha512((licstr + self._salt).encode('utf-8')).hexdigest()

    def get_seat_lic(self, user_id, account_type_id, start_date, end_date):
        """ """
        if not hasattr(self, '_domain_lic_blocks'):
            self.get_domain_lic()
        uk = list(self._get_encoded_user_key(user_id))
        uk.insert(5, str(random.randint(1, 9)))
        uk.append(str(random.randint(1, 9)))
        self._x_usr_id = ''.join(uk)
        usr_blocks = [''.join(uk[:5]), ''.join(uk[5:])]
        datestr = '%s%s%s' % (start_date.year, start_date.month, start_date.day)
        dateint = int(datestr)
        x_start_date = self._idc.encode(dateint)
        if len(x_start_date) == 6:
            x_start_date = x_start_date[1:]
        if end_date:
            datestr = '%s%s%s' % (end_date.year, end_date.month, end_date.day)
            dateint = int(datestr)
        x_end_date = self._idc.encode(dateint - 1)
        if len(x_end_date) == 6:
            x_end_date = x_end_date[1:]
        blocks = list(self._domain_lic_blocks)
        blocks.append(self._x_app_id.rjust(5, self._idc._kseq[16]))
        blocks.append(self._get_encoded_account_type_key(account_type_id))
        blocks.extend(usr_blocks)
        blocks.append(x_start_date)
        blocks.append(x_end_date)

        licstr = '-'.join(blocks).upper()
        # TODO: Take the noise out of the lic for the hash
        return licstr, blocks, sha512((licstr + self._salt).encode('utf-8')).hexdigest()

    def get_contract_lic(
            self, contract_id, licensor_id,
            licensee_id, start_date, end_date):
        """ """

        k = list(self._idc._kseq)
        k = k[8:] + k[:8]
        kseq = ''.join(k)
        idc = IdCoder(kseq=kseq)
        x_contract_id = idc.encode(contract_id)
        y = 8 - len(x_contract_id)
        if y > 0:
            x = list(x_contract_id.rjust(8, '0'))
            x[0] = str(y)
            for i in range(1, y):
                x[i] = k[i]
            x_contract_id = ''.join(x)
        x_licensor_id = self._get_encoded_user_key(licensor_id)
        x_licensee_id = idc.encode(licensee_id).rjust(8, k[18])

        datestr = '%s%s%s' % (end_date.year, end_date.month, end_date.day)
        dateint = int(datestr)
        x_end_date = idc.encode(dateint)[1:]

        datestr = '%s%s%s' % (start_date.year, start_date.month, start_date.day)
        dateint = int(datestr)
        x_start_date = idc.encode(dateint)[1:]

        return (x_contract_id, x_licensor_id,
                x_licensee_id, x_start_date, x_end_date,)

    def get_api_key(self, user_id, access_token_cnt):
        user_key = self._get_encoded_user_key(user_id)
        datestr = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss ZZ')
        datestr = sha256((datestr + self._salt).encode('utf-8')).hexdigest()
        n = 4
        api_key_seg = [datestr[i:i+n] for i in range(0, len(datestr), n)]
        api_key = ''
        i = 0
        for x in api_key_seg:
            api_key = api_key + x + user_key[i]
            i += 1
        atc_suffix = self._idc.encode(access_token_cnt, num_digits=4)
        return (api_key+atc_suffix).upper()

    def get_user_data_from_api_key(self, api_key):
        n = 5
        user_key = ''
        prefix = api_key[:-4]
        suffix = api_key[-4:]
        for x in [prefix[i:i+n] for i in range(0, len(prefix), n)]:
            user_key += x[-1:]
        return self._get_decoded_user(user_key), self._idc.decode(suffix)

    def _get_encoded_user_key(self, user_id):
        if user_id > SEAT_ID_ULIMIT:
        # if user_id < SEAT_ID_BLIMIT or user_id > SEAT_ID_ULIMIT:
            raise Exception(f'UserId not within acceptable range {SEAT_ID_ULIMIT}')
        k = list(self._idc._kseq)
        k.reverse()
        kseq = ''.join(k)
        idc = IdCoder(kseq=kseq)
        x = idc.encode(user_id)
        return x.zfill(8)

    def _get_decoded_user(self, code):
        k = list(self._idc._kseq)
        k.reverse()
        kseq = ''.join(k)
        idc = IdCoder(kseq=kseq)
        return idc.decode(code)

    def _get_encoded_account_type_key(self, account_type_id):
        k = list(self._idc._kseq)
        k = k[24:] + k[:24]
        kseq = ''.join(k)
        idc = IdCoder(kseq=kseq)
        x_account_type_id = idc.encode(account_type_id)
        y = 5 - len(x_account_type_id)
        if y > 0:
            x = list(x_account_type_id.rjust(5, '0'))
            x[0] = str(y)
            for i in range(1, y):
                x[i] = k[i]
            x_account_type_id = ''.join(x)
        return x_account_type_id

    def _get_encoded_property_key(self, property_id):
        k = list(self._idc._kseq)
        k = k[12:] + k[:12]
        kseq = ''.join(k)
        idc = IdCoder(kseq=kseq)
        x_property_id = idc.encode(property_id)
        y = 8 - len(x_property_id)
        if y > 0:
            x = list(x_property_id.rjust(8, '0'))
            x[0] = str(y)
            for i in range(1, y):
                x[i] = k[i]
            x_property_id = ''.join(x)
        return x_property_id


# iv = Random.get_random_bytes(8)

def encrypt_list(input, chunk_size, key, iv):
    """ """
    des3 = DES3.new(key, DES3.MODE_CFB, iv)
    output = []
    for chunk in input:
        if len(chunk) == 0:
            break
        elif len(chunk) % 16 != 0:
            chunk += ' ' * (16 - len(chunk) % 16)
        output.append(des3.decrypt(chunk))
    return output


def decrypt_list(input, chunk_size, key, iv):
    """ """
    des3 = DES3.new(key, DES3.MODE_CFB, iv)
    output = []
    for chunk in input:
        if len(chunk) == 0:
            break
        output.append(des3.decrypt(chunk))
    return output


def generate_pins(length, count):
    return [''.join(random.choice(string.digits) for x in range(length))
            for x in range(count)]


def generate_auth_code(length, count):
    return [''.join(random.choice(string.ascii_letters) for x in range(length))
            for x in range(count)]
