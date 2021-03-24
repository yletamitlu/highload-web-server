from utils.logger import logger
from utils import config


def config_to_map(path: str):
    conf = {}
    f = open(path)
    for line in f:
        key, value = line.split(" ", 1)
        key = key.strip()
        value = value.strip()
        conf[key] = value
    f.close()

    try:
        config.CPU_LIMIT = int(conf['cpu_limit'])
        config.ROOT_PATH = conf['document_root']
    except Exception as e:
        logger.warning('Fail parse config', str(e))
    logger.info(f'Config {path} parsed')
