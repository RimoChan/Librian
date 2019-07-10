import yaml
yaml.warnings({'YAMLLoadWarning': False})
import logging
import os


def 導入全局配置(a):
    global 配置
    配置.update(a)
    logging.debug(配置)

with open(os.path.split(os.path.realpath(__file__))[0]+'/配置.yaml', encoding='utf8') as f:
    配置 = yaml.load(f)
    logging.basicConfig(format = '【%(filename)s - %(lineno)s】(%(levelname)s): %(message)s')
    if 配置['額外信息']:
        logging.basicConfig(level=logging.DEBUG)


