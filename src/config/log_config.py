import logging
import os
import shutil
import tempfile

import langchain

# 日志开关
log_verbose = True
langchain.verbose = True

# 设置日志格式
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
level = logging.INFO if log_verbose else logging.WARN


def get_logger(name):
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
    return logging.getLogger(name)


# 设置日志存储路径
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

# 创建临时文件用于对话
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'chat_your_file')
try:
    # 递归删除目录树
    shutil.rmtree(TEMP_DIR)
except OSError:
    pass
os.makedirs(TEMP_DIR, exist_ok=True)
