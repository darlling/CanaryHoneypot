from traceback import format_exc

# from twisted.application import internet
# from twisted.internet.protocol import Factory
from pkg_resources import iter_entry_points
from twisted.application import service

from honeypot.config import config
from honeypot.logger import getLogger
from honeypot.modules.ftp import CanaryFTP
from honeypot.modules.git import CanaryGit
from honeypot.modules.http import CanaryHTTP
from honeypot.modules.mysql import CanaryMySQL
from honeypot.modules.ntp import CanaryNtp
from honeypot.modules.redis import CanaryRedis
from honeypot.modules.ssh import CanarySSH
from honeypot.modules.telnet import Telnet

ENTRYPOINT = "canary.usermodule"
MODULES = [
    Telnet,
    CanaryHTTP,
    CanaryFTP,
    CanarySSH,
    CanaryMySQL,
    CanaryNtp,
    CanaryGit,
    CanaryRedis,
]


logger = getLogger(config)


def start_mod(application, klass):
    try:
        obj = klass(config=config, logger=logger)
    except Exception:
        err = f"Failed to instantiate instance of class {klass.__name__} in {klass.__module__}. {format_exc()}."
        logMsg({"logdata": err})
        return

    if hasattr(obj, "startYourEngines"):
        try:
            obj.startYourEngines()
            msg = (
                f"Ran startYourEngines on class {klass.__name__} in {klass.__module__}"
            )
            logMsg({"logdata": msg})
        except Exception:
            err = f"Failed to run startYourEngines on {klass.__name__} in {klass.__module__}. {format_exc()}."
            logMsg({"logdata": err})
    elif hasattr(obj, "getService"):
        try:
            service = obj.getService()
            if not isinstance(service, list):
                service = [service]
            for s in service:
                s.setServiceParent(application)
            msg = f"Added service from class {klass.__name__} in {klass.__module__} to fake."
            logMsg({"logdata": msg})
        except Exception:
            err = "Failed to add service from class %s in %s. %s." % (
                klass.__name__,
                klass.__module__,
                format_exc(),
            )
            logMsg({"logdata": err})
    else:
        err = "The class %s in %s does not have any required starting method." % (
            klass.__name__,
            klass.__module__,
        )
        logMsg({"logdata": err})


def logMsg(msg):
    data = {}
    data["logdata"] = {"msg": msg}
    logger.log(data)


application = service.Application("honeypotd")

# List of modules to start
start_modules = []

# Add all custom modules
# (Permanently enabled as they don't officially use settings yet)
# for ep in iter_entry_points(ENTRYPOINT):
#     try:
#         klass = ep.load(require=False)
#         start_modules.append(klass)
#     except Exception as e:
#         err = "Failed to load class from the entrypoint: %s. %s" % (
#             str(ep),
#             format_exc(),
#         )
#         logMsg({"logdata": err})

# Add only enabled modules
start_modules.extend(filter(lambda m: config.moduleEnabled(m.NAME), MODULES))

for klass in start_modules:
    start_mod(application, klass)

msg = "honeypot running!!!"
logMsg({"logdata": msg})
