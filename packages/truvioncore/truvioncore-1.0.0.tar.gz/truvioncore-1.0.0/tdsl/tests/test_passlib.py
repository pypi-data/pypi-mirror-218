import hashlib
import passlib
from passlib.hash import pbkdf2_sha256

from tdsl.codify import *


__dsh = '''First Law - A robot may not injure a human being or, through inaction, allow a human being to come to harm.
Second Law - A robot must obey the orders given it by human beings except where such orders would conflict with the First Law.
Third Law - A robot must protect its own existence as long as such protection does not conflict with the First or Second Law.
'''
Default_Salt_Hashkey = hashlib.sha256(__dsh.encode('utf-8')).hexdigest()


def encrypt_password(password):
    salted_pwd_hash = password+'<:::>'+Default_Salt_Hashkey+'<:::>'
    return User_Pwd_Context.encrypt(salted_pwd_hash)


def verify_password(password, hashed_pwd):
    salted_pwd_hash = password+'<:::>'+Default_Salt_Hashkey+'<:::>'
    return User_Pwd_Context.verify(salted_pwd_hash, hashed_pwd)



if __name__ == '__main__':

    p = 'AOEUaoeu1234!@#$'
    h = '$pbkdf2-sha256$30000$Vupda42xVurdmxNiDKFUCg$WUs5B9ZaLhrtBRQRVVSqmB4LskU2FCVCkOYAcavCCCc'
    
    print(encrypt_password(p))
    print(verify_password(p, h))

    # p = "toomanysecrets<:::>aoeustahoeunathoeunthaoeunhaoeunthaoeusthaoeusntahoeusntahoeusnathoeusnathoeusnaoheu<:::>"
    # hash = pbkdf2_sha256.hash(p)
    # print(hash)
    # t = '$pbkdf2-sha256$29000$kDImRAhBCEHo/b/3vrd2zg$Cr0X68hUxSwdlKhpBK4MS97IfT0ahS7/4YRN./Rs8NM'
    # print (pbkdf2_sha256.verify(p, t))