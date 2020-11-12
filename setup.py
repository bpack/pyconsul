from setuptools import setup

def readme():
    with open('readme.md') as f:
        return f.read()

setup(
    name = 'pyconsul',
    version = '0.0.1',
    author = 'Benjamin Pack',
    author_email = '',
    description = 'Tooling to mirror a filesystem to Consul',
    long_description = readme(),
    long_description_content_type = 'text/markdown',
    packages = ['pyconsul'],
    entry_points = {
        'console_scripts': [
            'pyconsul=pyconsul.cli:main'
        ]
    },
    install_requires = [
    ]
)
