from setuptools import setup
setup(
    name = "memolife",
    version = "0.2",
    packages = ['memolife'],
    install_requires = [
        'Flask>=0.10.1',
        'mongokit>=0.9.1.1',
        'PyJWT>=0.4.3'
    ]
)

