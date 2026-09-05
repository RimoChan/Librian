import setuptools
from pathlib import Path


setuptools.setup(
    name='librian',
    version='2.2.0',
    author='RimoChan',
    author_email='the@librian.net',
    description='librian',
    long_description=open('readme.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RimoChan/librian',
    packages=[
        'librian',
        'librian.librian_util',
        'librian.librian本體',
        'librian.librian本體.librian虛擬機',
    ],
    package_data={
        'librian.librian本體': [
            '前端/*', '前端/dist/*', '前端/默認標題畫面/*', '前端/黑科技/**/*', '前端/黑科技/**/**/*',
            '資源/*',
            '配置.yaml',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=open('requirements.txt', encoding='utf8').read().splitlines(),
    python_requires='>=3.6',
)
