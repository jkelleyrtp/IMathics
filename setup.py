#!/usr/bin/env python

import sys
import subprocess

from distutils import log

from setuptools import setup
from setuptools.command.install import install

# Ensure user has the correct Python version
if sys.version_info[:2] != (2, 7):
    print("IMathics supports Python 2.7. \
Python %d.%d detected" % sys.version_info[:2])
    sys.exit(-1)

# General Requirements
SETUP_REQUIRES = ['ipython', 'ipykernel']

# TODO relies on 'mathics' sn6uv/Mathics jupyter branch
INSTALL_REQUIRES = [] + SETUP_REQUIRES


kernel_json = {
    'argv': [sys.executable,
             '-m', 'mathics',
             '-f', '{connection_file}'],
    'display_name': 'mathics',
    'language': 'Wolfram',
    'name': 'mathics',
}


class InstallIMathics(install):

    def run(self):
        # The recommended way is with the setup_requires argument to setup
        # This fails because ipython doesn't build under easy_install
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + SETUP_REQUIRES)

        # Unfortunately the recommended call to 'install.run(self)'
        # will completely ignore the install_requirements.
        # So we trick it by calling the underlying bdist_egg instead:
        self.do_egg_install()

        self.install_kernelspec()

    def install_kernelspec(self):
        from ipykernel.kernelspec import write_kernel_spec
        from jupyter_client.kernelspec import KernelSpecManager

        kernel_spec_manager = KernelSpecManager()

        log.info('Writing kernel spec')
        kernel_spec_path = write_kernel_spec(overrides=kernel_json)

        log.info('Installing kernel spec')
        try:
            kernel_spec_manager.install_kernel_spec(
                kernel_spec_path,
                kernel_name=kernel_json['name'],
                user=self.user)
        except:
            log.error('Failed to install kernel spec')

setup(
    name="imathics",
    cmdclass={'install': InstallIMathics},
    version='0.1',

    packages=['imathics'],

    install_requires=INSTALL_REQUIRES,

    entry_points={
        'console_scripts': [
            'imathics = imathics.terminalapp:main',
        ],
    },

    # metadata for upload to PyPI
    author="Angus Griffith",
    author_email="imathics@angusgriffith.com",
    description="A jupyter kernel for mathics",
    url="http://www.mathics.github.io/",

    keywords=['Mathematica', 'Wolfram', 'Interpreter', 'Shell', 'Math', 'CAS'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
    ],
)
