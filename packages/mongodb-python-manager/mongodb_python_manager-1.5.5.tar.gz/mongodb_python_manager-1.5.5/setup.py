from setuptools import setup

setup(
    name='mongodb_python_manager',
    version='1.5.5',
    packages=['mongodb_python_manager'],
    install_requires=[
        'pymongo==4.3.3',
        'python-dotenv==1.0.0',
        'tqdm==4.65.0',
        'structlog==23.1.0',
        'pandas==1.5.3',
    ],
    description=""""
        MongoDB Python manager is a python package that helps developers interact with MongoDB Database using Python.
    """,
    author='Louis Giron',
    author_email='louis@giron-dom.eu',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
