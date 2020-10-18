import logging
import sys
from pathlib import Path

import yaml


class 假面:
    配置 = {}

    def 加載配置(self, 工程路徑):
        工程路徑 = Path(工程路徑)
        with open(工程路徑 / '工程配置.yaml', encoding='utf8') as f:
            a = yaml.safe_load(f)
            for i in a:
                self.配置.update(a[i])
        self.配置['工程路徑'] = 工程路徑
        self.配置['psd立繪路徑'] = 工程路徑 / self.配置['立繪文件夾']

    def __getattr__(self, x):
        return self.配置[x]


sys.modules[__name__] = 假面()
