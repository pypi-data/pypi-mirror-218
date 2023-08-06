from setuptools import setup, find_packages

setup(
    name='space_utils',
    version='0.1.0',
    author='sandhosh',
    author_email='santhoshgowravan@gmail.com',
    description='A library for space-related calculations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
