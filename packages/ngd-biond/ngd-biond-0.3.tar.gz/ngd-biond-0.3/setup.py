# ONE TIME  -----------------------------------------------------------------------------
#
# pip install --upgrade setuptools wheel twine
#
# Create account:
# PyPI test: https://test.pypi.org/account/register/
# or PyPI  : https://pypi.org/account/register/
#
# EACH TIME -----------------------------------------------------------------------------
#
# Modify version code in "setup.py" (this file)
#
# Build:
# python3 setup.py sdist bdist_wheel
#
# Upload:
# PyPI test: twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*
# or PyPI  : twine upload --skip-existing dist/*
#
# INSTALL   ------------------------------------------------------------------------------
#
# PyPI test: pip install --index-url https://test.pypi.org/simple/ --upgrade biond
# PyPI     : pip install --upgrade biond
# No PyPI  : pip install -e <local path where "setup.py" (this file) is located>
#
from setuptools import setup
from os import path

"""
python3 setup.py sdist bdist_wheel
twine upload --skip-existing dist/*
"""
package_name = 'ngd-biond'
version = '0.3'

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=package_name,
    version=version,
    packages=['biond', 'biond.processes', 'biond.processes.data_selectors', 'biond.processes.resources'],
    install_requires=['requests', 'pandas', 'marshmallow', 'urllib3', 'typing'],
    python_requires='>=3.8',
    url='https://github.com/nextgendem/bcs-bond',
    license='BSD3',
    author='Rafael Nebot, Daniel Reyes',
    author_email='rnebot@itccanarias.org, dreyes@itccanarias.org',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Client to NGD backend'
)

