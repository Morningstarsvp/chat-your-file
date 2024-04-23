import os

# sqlalchemy数据库配置
# 默认使用sqlite数据库
KB_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base")
if not os.path.exists(KB_ROOT_PATH):
    os.mkdir(KB_ROOT_PATH)
DB_ROOT_PATH = os.path.join(KB_ROOT_PATH, "info.db")
# SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_ROOT_PATH}"

SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # 测试用URI
