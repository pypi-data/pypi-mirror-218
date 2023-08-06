import unittest
import ftplib
import ssl
from dateutil import parser

class ImplicitFTP_TLS(ftplib.FTP_TLS):
    """FTP_TLS subclass that automatically wraps sockets in SSL to support implicit FTPS."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sock = None

    @property
    def sock(self):
        """Return the socket."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """When modifying the socket, ensure that it is ssl wrapped."""
        if value is not None and not isinstance(value, ssl.SSLSocket):
            value = self.context.wrap_socket(value)
        self._sock = value


class TestSetup(unittest.TestCase):
    def test_setup(self):

        ftps = ftplib.FTP_TLS('QuantariumFTP.hostedftp.com', timeout=5)
        # TLS is more secure than SSL
        ftps.ssl_version = ssl.PROTOCOL_TLS
        # login before securing control channel
        ftps.login('Entrust', 'Rwmjd4cM&QcrXn')
        # switch to secure data connection
        ftps.prot_p()
        # ftps.dir()
        ftps.nlst()

        # ftps.retrlines('LIST')
        ftps.retrlines('MLSD')

        ftps.cwd('/Open Lien Full Set V2.6')

        ftps.cwd('/Weekly Deltas V2.6')
        ftps.retrlines('MLSD')

        # filenames = ftps.nlst()
        # print(f'. filesnames {filenames}')
        # ftps.retrlines('LIST')
        # ftps.retrlines('MLSD')
        # file = open("test_download.zip", 'wb')
        # ftps.retrbinary('RETR '+ 'Quantarium_OpenLien_20210414_00001.zip', file.write)
        # print(f'. retr files')
        ftps.close()

        # with ftplib.FTP('https://QuantariumFTP.hostedftp.com') as ftp:
        #     ftp.login('Entrust', 'Rwmjd4cM&QcrXn')

        # ftp_client = ImplicitFTP_TLS()
        # ftp_client.connect(host='https://QuantariumFTP.hostedftp.com' port=990)
        # ftp_client.login(user='Entrust', passwd='Rwmjd4cM&QcrXn')
        # ftp_client.prot_p()
        
        # print("starting unittests for FTP, checking setup...")

        # with ftplib.FTP('127.0.0.1') as ftp:

            # ftp.login('mat', '12345678')
            # ftp.cwd('TestFiles')

            # example file path structure on azure
            # TestFTPSite/bstacy@entrustfunding.com/1_8_2020/8605918512\ by\ bstacy@entrustfunding.com\ @\ 4_55_38\ PM.wav

            # # is all files and dir
            # ftp.retrlines('LIST')
            # dirs = ftp.dir()
            # print('dirs ', dirs)
            #
            # ftp.cwd('bstacy@entrustfunding.com')
            # dirs = ftp.dir()
            # print('dirs ', dirs)
            # print('----')
            #
            # ftp.cwd('1_8_2020')
            #
            # dirs = ftp.dir()
            # print('dirs ', dirs)
            # print('----')

            # files = ftp.mlsd()
            # print('files', files)

            # try:
            #     for f in files:
            #         print('file ', f, type(f))
            #         # name = f[0]
            #         # timestamp = f[1]['modify']
            #         # time = parser.parse(timestamp)
            #         # print(name + ' - ' + str(time))
            # except:
            #     print("error. MSLD not supported?")
            #     files = ftp.nlst()
            #     files = []
            #     ftp.dir(files.append)
            #     for f in files:
            #         print("line: ", f)
            #         tokens = f.split(maxsplit=9)
            #         name = tokens[8]
            #         time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]
            #         time = parser.parse(time_str)
            #         print(name + ' time: ' + str(time))

            # print('done')

            # self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
