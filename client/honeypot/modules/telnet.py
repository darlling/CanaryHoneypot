from subprocess import DEVNULL, run
from time import sleep

from docker import from_env
from honeypot.modules import CanaryService
from twisted.application.internet import TCPServer
from twisted.conch.telnet import (
    ECHO,
    AuthenticatingTelnetProtocol,
    ITelnetProtocol,
    TelnetTransport,
)
from twisted.cred import credentials, portal
from twisted.internet.protocol import ServerFactory
from zope.interface import implementer


@implementer(portal.IRealm)
class Realm:
    def requestAvatar(self, avatarId, mind, *interfaces):
        # if ITelnetProtocol in interfaces:
        #     av = MyTelnet()
        #     av.state = "Command"
        #     return ITelnetProtocol, av, lambda: None
        raise NotImplementedError("Not supported by this realm")


class AlertAuthTelnetProtocol(AuthenticatingTelnetProtocol):
    def connectionMade(self):
        # p/Cisco telnetd/ d/router/ o/IOS/ cpe:/a:cisco:telnet/ cpe:/o:cisco:ios/a
        # NB _write() is for raw data and write() handles telnet special bytes
        self.transport._write(
            b"\xff\xfb\x01\xff\xfb\x03\xff\xfb\0\xff\xfd\0\xff\xfd\x1f\r\n"
        )
        self.transport.write(self.factory.banner)
        self.transport._write(b"User Access Verification\r\n\r\nUsername: ")

    def telnet_Password(self, line):
        # Body of this method copied from
        # twisted.conch.telnet
        username, password = self.username, line
        del self.username

        def login(ignored):
            creds = credentials.UsernamePassword(username, password)
            d = self.portal.login(creds, None, ITelnetProtocol)
            d.addCallback(self._cbLogin)
            d.addErrback(self._ebLogin)

        self.transport.wont(ECHO).addCallback(login)

        logdata = {"USERNAME": username, "PASSWORD": password}
        self.factory.canaryservice.log(logdata, transport=self.transport)
        return "Discard"


class Telnet(CanaryService):
    NAME = "telnet"

    def __init__(self, config=None, logger=None):
        CanaryService.__init__(self, config=config, logger=logger)
        self.port = int(config.getVal("telnet.port", default=23))
        self.banner = config.getVal("telnet.banner", "").encode("utf8")
        self.logtype = logger.LOG_TELNET_LOGIN_ATTEMPT
        self.listen_addr = config.getVal("device.listen_addr", default="")

        if self.banner:
            self.banner += b"\n"

    def dockerPs(self):
        client = from_env()
        containerName = "sshtel"
        running = client.containers.list()
        if running:
            pass
        else:
            run(f"docker start {containerName}", shell=True, stdout=DEVNULL)

    def supervisor(self):
        try:
            status = run(
                r"supervisorctl status cowrielog", shell=True, capture_output=True
            )
            if "STOPPED" in status.stdout.decode("utf-8"):
                run(r"supervisorctl start cowrielog", shell=True, stdout=DEVNULL)
        except:
            print("telnet.py supervisor error!!")

    def getService(self):
        self.dockerPs()
        sleep(2)
        self.supervisor()
        r = Realm()
        p = portal.Portal(r)
        f = ServerFactory()
        f.canaryservice = self
        f.logger = self.logger
        f.banner = self.banner
        f.protocol = lambda: TelnetTransport(AlertAuthTelnetProtocol, p)
        return TCPServer(self.port, f, interface=self.listen_addr)
