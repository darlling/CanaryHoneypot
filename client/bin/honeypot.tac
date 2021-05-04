import traceback

from twisted.application import service
from twisted.application import internet
from twisted.internet.protocol import Factory
from pkg_resources import iter_entry_points

from honeypot.config import config
from honeypot.logger import getLogger
from honeypot.modules.http import CanaryHTTP
from honeypot.modules.ftp import CanaryFTP
from honeypot.modules.ssh import CanarySSH
from honeypot.modules.telnet import Telnet
from honeypot.modules.httpproxy import HTTPProxy
from honeypot.modules.mysql import CanaryMySQL
from honeypot.modules.mssql import MSSQL
from honeypot.modules.ntp import CanaryNtp
from honeypot.modules.tftp import CanaryTftp
from honeypot.modules.vnc import CanaryVNC
from honeypot.modules.sip import CanarySIP
from honeypot.modules.git import CanaryGit
from honeypot.modules.redis import CanaryRedis
from honeypot.modules.tcpbanner import CanaryTCPBanner

#from honeypot.modules.example0 import CanaryExample0
#from honeypot.modules.example1 import CanaryExample1

ENTRYPOINT = "canary.usermodule"
MODULES = [Telnet, CanaryHTTP, CanaryFTP, CanarySSH, HTTPProxy, CanaryMySQL,
           MSSQL, CanaryVNC, CanaryTftp, CanaryNtp, CanarySIP, CanaryGit,
           CanaryTCPBanner, CanaryRedis]
           #CanaryExample0, CanaryExample1]
try:
    #Module needs RDP, but the rest of Honeypot doesn't
    from honeypot.modules.rdp import CanaryRDP
    MODULES.append(CanaryRDP)
except ImportError:
    print("Can't import RDP. Please ensure you have RDP installed.")
    pass


try:
    #Module need Scapy, but the rest of Honeypot doesn't
    from honeypot.modules.snmp import CanarySNMP
    MODULES.append(CanarySNMP)
except ImportError:
    print("Can't import SNMP. Please ensure you have Scapy installed.")
    pass

# NB: imports below depend on inotify, only available on linux
import sys
if sys.platform.startswith("linux"):
    from honeypot.modules.samba import CanarySamba
    from honeypot.modules.portscan import CanaryPortscan
    MODULES.append(CanarySamba)
    MODULES.append(CanaryPortscan)

logger = getLogger(config)

def start_mod(application, klass):
    try:
        obj = klass(config=config, logger=logger)
    except Exception as e:
        err = 'Failed to instantiate instance of class %s in %s. %s' % (
            klass.__name__,
            klass.__module__,
            traceback.format_exc()
        )
        logMsg({'logdata': err})
        return

    if hasattr(obj, 'startYourEngines'):
        try:
            obj.startYourEngines()
            msg = 'Ran startYourEngines on class %s in %s' % (
                klass.__name__,
                klass.__module__
                )
            logMsg({'logdata': msg})

        except Exception as e:
            err = 'Failed to run startYourEngines on %s in %s. %s' % (
                klass.__name__,
                klass.__module__,
                traceback.format_exc()
            )
            logMsg({'logdata': err})
    elif hasattr(obj, 'getService'):
        try:
            service = obj.getService()
            if not isinstance(service, list):
                service = [service]
            for s in service:
                s.setServiceParent(application)
            msg = 'Added service from class %s in %s to fake' % (
                klass.__name__,
                klass.__module__
                )
            logMsg({'logdata': msg})
        except Exception as e:
            err = 'Failed to add service from class %s in %s. %s' % (
                klass.__name__,
                klass.__module__,
                traceback.format_exc()
            )
            logMsg({'logdata': err})
    else:
        err = 'The class %s in %s does not have any required starting method.' % (
            klass.__name__,
            klass.__module__
        )
        logMsg({'logdata': err})

def logMsg(msg):
    data = {}
#    data['src_host'] = device_name
#    data['dst_host'] = node_id
    data['logdata'] = {'msg': msg}
    logger.log(data, retry=False)

application = service.Application("honeypotd")

# List of modules to start
start_modules = []

# Add all custom modules
# (Permanently enabled as they don't officially use settings yet)
for ep in iter_entry_points(ENTRYPOINT):
    try:
        klass = ep.load(require=False)
        start_modules.append(klass)
    except Exception as e:
        err = 'Failed to load class from the entrypoint: %s. %s' % (
            str(ep),
            traceback.format_exc()
            )
        logMsg({'logdata': err})

# Add only enabled modules
start_modules.extend(filter(lambda m: config.moduleEnabled(m.NAME), MODULES))

for klass in start_modules:
    start_mod(application, klass)

msg = 'honeypot running!!!'
logMsg({'logdata': msg})
