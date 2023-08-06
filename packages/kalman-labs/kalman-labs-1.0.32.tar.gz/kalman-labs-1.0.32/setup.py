from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='kalman-labs',
    version='1.0.32',
    author='Aditya',
    author_email='aditya@kalman.in',
    description='The Global Kalman Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('signal_processing_packages/src'),
    package_dir={'': 'signal_processing_packages/src'},
    install_requires=[
        'numpy',
        'pandas',
        'librosa',
        'scikit-learn',
        'xgboost',
        'imbalanced-learn',
        'tensorflow',
        'keras'
    ],
)
