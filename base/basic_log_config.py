import logging
fmt = '%(asctime)s %(levelname)s %(message)s'
formatter = logging.Formatter(fmt)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

fh = logging.FileHandler('../log/test.log')
fh.setFormatter(formatter)
logger.addHandler(fh)