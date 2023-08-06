# -*- coding: UTF-8 -*-
# name = 'extLog'

from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING


def genLogger(name=None, lvl=DEBUG):
    import os
    from logging import getLogger, StreamHandler, FileHandler, Formatter
    from time import strftime

    logger = getLogger(name)

    log_path = os.path.join(os.curdir, "Log", "")
    os.makedirs(log_path, 777, True)
    log_filename = log_path + f"{strftime('%m-%d')}.log"

    # 输出日志到终端
    ch = StreamHandler()
    ch.setFormatter(Formatter("%(filename)12s:%(lineno)3d - %(levelname)5s: %(message)s"))
    logger.addHandler(ch)

    # 输出日志到文件
    fh = FileHandler(log_filename, "a", encoding="UTF-8")
    fh.setFormatter(Formatter("%(asctime)s %(filename)12s :%(lineno)3d - %(levelname)5s: %(message)s"))
    logger.addHandler(fh)

    logger.setLevel(lvl)
    return logger
