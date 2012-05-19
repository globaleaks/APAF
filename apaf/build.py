"""
Apaf module for handling the download and building of binary files.

This must be refactored usign the apaf configuration and the
twisted.client.HTTPDownaloader class.
"""
from apaf.config import config
import os.path

# pgp = gnupg.PGP(gnupghome=HOME, gpgbinary=GPG_BINARY)

class Downloader:
    """
    Thw downloader class manages a single binary download,
    using urllib to retrive the content and gnupg to check the signature.
    """

    def __init__(self, name, url, sig):
        self.name = name
        self.url = url[config.platform]
        # the signature file name will be self.name + '.sig'
        self.sig = sig[config.platform]

    def download(self):
        """
        Download the binary.
        """
        urllib.urlretrieve(self.url,
                           os.path.join(config.binary_kits, self.name))

    def verify_signature(self):
        """
        Checks the signature.
        XXX: Return ALWAYS True.
        """
        # gpg.verify
        return True


tor = Downloader(
        name = 'tor.exe',
        url = dict(win32='https://www.torproject.org/dist/win32/tor-0.2.2.35-win32-1.exe',
                   linux2='foo.bar.b.az/tor.exe',
                   darwin='foo.bar.b.az/tor.exe'),
        sig = dict(win32='https://www.torproject.org/dist/win32/tor-0.2.2.35-win32-1.exe.asc',
                   linux2='spam.che.es/tor.exe.sig',
                   darwin='spam.che.es/tor.exe.sig')
)


# from apaf import config
if __name__ == '__main__':
    tor.download()
