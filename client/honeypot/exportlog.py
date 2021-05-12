from json import loads
from time import sleep

from honeypot.config import config
from honeypot.logger import getLogger

LOG_PATH = r"/var/log/cowrie/cowrie.json"


def cowrieLogPostServer():
    # 文件读取指针
    index = 0
    # logdata  shell交互命令
    log, cmds = {}, []
    # 重复打开文件进行读取以获得新加入的内容
    while True:
        try:
            with open(LOG_PATH, "r") as file:
                file.seek(index)
                line = file.readline()
                # 是否有数据
                if line:
                    jsondata = line.strip()
                    # 数据存在则处理
                    if jsondata:
                        jsonline = loads(jsondata)
                        event = jsonline["eventid"]
                        if event.endswith("session.connect"):
                            # 1: 正在 shell 交互
                            flag = 1
                            protocol = jsonline["protocol"]
                            log["dst_host"] = jsonline["dst_ip"]
                            log["dst_port"] = jsonline["dst_port"]
                            log["src_host"] = jsonline["src_ip"]
                            log["src_port"] = jsonline["src_port"]
                            log["node_id"] = config.getVal("device.node_id")
                            log["logtype"] = f"{protocol} shell interaction"
                        elif event.endswith("client.version") and flag:
                            remoteVer = jsonline["version"].replace("'", "")[1:]
                        elif event.endswith("login.success") and flag:
                            log["logdata"] = dict(
                                (
                                    ("USERNAME", jsonline["username"]),
                                    ("PASSWORD", jsonline["password"]),
                                )
                            )
                            if protocol == "ssh":
                                log["logdata"].update(
                                    dict(
                                        (
                                            ("LOCALVERSION", config.getVal("ssh.version")),
                                            ("REMOTEVERSION", remoteVer),
                                        )
                                    )
                                )
                        elif event.endswith("command.input") and flag:
                            cmds.append(jsonline["input"])
                        elif event.endswith("session.closed"):
                            # 0: shell 交互已完成，连接已关闭
                            flag = 0
                            try:
                                log["logdata"].update({"INPUT": ";;".join(cmds)})
                                getLogger(config).log(log, retry=False, m_i=True)
                            except:
                                pass
                            finally:
                                log.clear()
                                cmds.clear()
                    # 文件读取指针推进
                    index = file.tell()
                else:
                    # 没有数据，等待新内容写入
                    sleep(6)
        except:
            sleep(6)


if __name__ == "__main__":
    cowrieLogPostServer()
