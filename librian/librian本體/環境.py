import os
import logging

import yaml
yaml.warnings({'YAMLLoadWarning': False})


def 導入全局配置(a):
    配置.update(a)
    logging.debug(配置)


with open(os.path.split(os.path.realpath(__file__))[0] + '/配置.yaml', encoding='utf8') as f:
    配置 = yaml.load(f)
    logging_config = {
        'format': '【%(filename)s - %(lineno)s】(%(levelname)s): %(message)s',
    }
    if 配置['額外信息']:
        logging_config['level'] = logging.INFO
    logging.basicConfig(**logging_config)
