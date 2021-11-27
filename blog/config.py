
import os

class Config(object):
    # noinspection PyPackageRequirements
    DEBUG = True
    TOKEN_EXPIRED = 3600 * 24 * 3   # 维持3天
    # SERVER_NAME = "0.0.0.0:8004"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    MEDIA_PATH = "/home/yukimura/Web/media"
    
    # LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    # LOG_LEVEL = logging.INFO

    # generate by os.urandom(16)
    SQL_SECRET_KEY = b'\xac88+r\xe2\xb1\xaf\xaf\xe5\xe6\x8f\xef\xda\xcc}'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:438552317@127.0.0.1:3306/blog?charset=utf8mb4'
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_POOL_SIZE = 5
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # es
    ELASTICSEARCH_INDEX = "blog"

    # Flask_cache 设置
    # CACHE_TYPE = 'redis'
    # CACHE_DEFAULT_TIMEOUT = 3600
    # CACHE_KEY_PREFIX = 'kacha:dev:'
    # CACHE_REDIS_URL = 'redis://172.16.24.52:6379/90'
    # SQLALCHEMY_BINDS = {
    #     'config': 'mysql+pymysql://dev:t8kfq{Ju@172.16.24.45:3306/kacha_dev?charset=utf8mb4',
    #     # 'data': 'clickhouse://ymetl:bZ4nWP0h@clickhouse.chinaeast2.cloudapp.chinacloudapi.cn:8123/kacha_dev',
    #     'data': 'clickhouse://readonly:7JDgvEZeT4rRF3@hs#M%@clickhouse.ym:18123/kacha_dev'
    # }


    
