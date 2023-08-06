from setuptools import setup, find_packages

setup(
    name='stackviz', 
    version='0.0.5', 
    packages=find_packages(),
    package_data={
        'stackviz': ['resources/*'],
    },
    url='https://github.com/cador/stackviz',
    author='Haolin You',
    author_email='cador.ai@aliyun.com', 
    description='Quick development framework for visualization dashboards based on Python', 
    install_requires=[
        'ipython'
    ],
)
