# coding: utf-8
import sys
from os.path import join, dirname
from setuptools import setup
from setuptools.command.test import test

import pplmyapi


def parse_reqs(f="requirements.txt"):
    ret = []
    with open(join(dirname(__file__), f)) as fp:
        for l in fp.readlines():
            l = l.strip()
            if l and not l.startswith("#"):
                ret.append(l)
    return ret


install_requires = parse_reqs()
setup_requires = ["setuptools"] + install_requires

print("install_requires: ", install_requires)
# print('tests_require: ', tests_require)
print("setup_requires: ", setup_requires)

with open("README.md") as readmefile:
    long_description = readmefile.read()


# class PyTest(test):
#     def finalize_options(self):
#         test.finalize_options(self)
#         self.test_args = []
#         self.test_suite = True

#     def run_tests(self):
#         # import here, cause outside the eggs aren't loaded
#         import pytest

#         errno = pytest.main(self.test_args)
#         sys.exit(errno)


setup(
    name="pplmyapi",
    version=pplmyapi.__versionstr__,
    description="Python client for PPL myAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Michal Půlpán",
    author_email="michal@michalpulpan.cz",
    license="MIT",
    url="https://github.com/michalpulpan/pplmyapi",
    packages=[
        "pplmyapi",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
    ],
    zip_safe=False,
    setup_requires=setup_requires,
    install_requires=install_requires,
    # tests_require=tests_require,
    # cmdclass={"test": PyTest},
)
