from setuptools import setup

setup(
    name='bcc',
    packages=['bcc'],
    include_package_data=True,
    install_requires=[
        'flask',
        'PyMySQL',
        'unittest2'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
)
