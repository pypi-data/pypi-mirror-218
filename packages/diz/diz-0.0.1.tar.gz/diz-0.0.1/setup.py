from setuptools import setup, find_packages

setup(
    name='diz',
    version='0.0.1',
    author='MJ',
    description='用来构建大模型环境的工具',
    packages=find_packages(),
    install_requires=[
        'GitPython>=3.1.31',
        'huggingface-hub>=0.16.4',
        'PyYAML>=6.0',
        'requests>=2.31.0',
        'toolz>=0.12.0',
        'typer>=0.9.0'
    ],
)