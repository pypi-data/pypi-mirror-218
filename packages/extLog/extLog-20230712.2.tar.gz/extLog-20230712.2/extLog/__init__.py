# -*- coding: UTF-8 -*-
# name = 'extLog'

from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, Logger


def genLogger(name: str = None, level: int = DEBUG, write_log: bool = False) -> Logger:
    import os
    from logging import getLogger, StreamHandler, FileHandler, Formatter
    from time import strftime

    logger = getLogger(name)
    logger.setLevel(level)

    # 输出日志到终端
    ch = StreamHandler()
    ch.setFormatter(Formatter("%(filename)12s:%(lineno)3d - %(levelname)5s: %(message)s"))
    logger.addHandler(ch)

    # 输出日志到文件
    if write_log:
        log_path = os.path.join(os.curdir, "Log", "")
        os.makedirs(log_path, 777, True)

        log_file = log_path + f"{strftime('%m-%d')}.log"

        fh = FileHandler(log_file, "a", encoding="UTF-8")
        fh.setFormatter(Formatter("%(asctime)s %(filename)12s :%(lineno)3d - %(levelname)5s: %(message)s"))
        logger.addHandler(fh)

    return logger
