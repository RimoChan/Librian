import yaml
import logging

with open('配置.yaml',encoding='utf8') as f:
    配置=yaml.load(f)
    if 配置['額外信息']:
        logging.basicConfig(level=logging.DEBUG)

工程路徑='./project/%s' %配置['啟動工程']

with open('%s/工程配置.yaml' %工程路徑,encoding='utf8') as f:
    配置.update(yaml.load(f))
