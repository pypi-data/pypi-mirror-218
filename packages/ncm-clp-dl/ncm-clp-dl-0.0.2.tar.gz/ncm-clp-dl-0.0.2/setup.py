from setuptools import setup, find_packages

setup(
    name='ncm-clp-dl',
    version="0.0.2",
    description='监视剪切板下载网易云音乐',
    long_description='',
    author='luoyeah',
    author_email='dao696@foxmail.com',
    maintainer='',
    maintainer_email='',
    url='https://github.com/luoyeah/ncm-clp-dl',
    license='MIT license',
    keywords=[
        '',
    ],
    install_requires=open("requirements.txt", 'r', encoding='utf-8').read().split("\n"),
    packages=['ncm_clp_dl'],
    entry_points={
        'console_scripts': [
            'ncm-clp-dl = ncm_clp_dl.__main__:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
