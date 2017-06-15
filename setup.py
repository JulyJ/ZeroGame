from os import path
from uuid import uuid1

from pip.req import parse_requirements
from setuptools import setup, find_packages


basedir = path.dirname(__file__)


def get_version():
    with open(path.join(basedir, 'zerogame/__init__.py')) as f:
        variables = {}
        exec(f.read(), variables)
        return '.'.join(str(x) for x in variables['VERSION'])


def get_requirements(filename):
    requirements_path = path.join(basedir, filename)
    requirements = parse_requirements(requirements_path, session=uuid1())
    return [str(r.req) for r in requirements]


setup(
    name='ZeroGame',
    version=get_version(),
    url='https://github.com/JulyJ/ZeroGame',
    license='MIT',
    author='Julia Koveshnikova',
    author_email='julia.koveshnikova@gmail.com',
    description='Zero Play Game',
    long_description='Zero Play Game',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    entry_points={
        'console_scripts': [
            'zerogame = zerogame.run:run',
        ],
    },
    classifiers=[
        # As from https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Framework :: AsyncIO',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Games/Entertainment :: Simulation',
    ],
)
