import os
from setuptools import setup

def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), 'r', encoding='UTF-8') as fp:
        return fp.read()

long_description = read("README.rst")

setup(
    name='mysqlx-generator',
    packages=['mysqlx_generator'],
    description="mysqlx-generator is a model code generator from db tables for mysqlx.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'Jinja2>=3.0.3',
        'mysqlx>=1.3.7',
        'mysql-connector-python>=8.0.20',
    ],
    version='1.0.3',
    url='https://gitee.com/summry/mysqlx/generator.md',
    author='summry',
    author_email='xiazhongbiao@126.com',
    keywords=['MySQL', 'mysqlx', 'python'],
    package_data={
        # include json and txt files
        '': ['*.rst', '*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.7.0',
    zip_safe=False
)

