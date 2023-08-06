from setuptools import setup, find_packages

setup(
    name='ML_Toolkits',
    version='1.0.0',
    author='Mr Raj',
    author_email='arunraj14092002@gmail.com',
    description='Snippet Code that helps in ML Model Training',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'tabulate'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
