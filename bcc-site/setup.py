from setuptools import setup

setup(
    name='bcc',
    packages=['bcc'],
    include_package_data=True,
    install_requires=[
        'flask',
        'PyMySQL'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
)
