from setuptools import setup, find_packages

setup(
    name='gargant.dispatch',
    version='0.0',
    packages=find_packages(exclude=['tests']),
    namespace_packages=['gargant'],
    url='https://github.com/hirokiky/gargant.dispatch',
    license='MIT',
    author='hirokiky',
    author_email='hirokiky@gmail.com',
    description='Dispatcher for WSGI Applications',
    tests_require=['pytest==2.3.5']
)
