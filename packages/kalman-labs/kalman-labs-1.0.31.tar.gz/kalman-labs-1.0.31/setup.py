from setuptools import setup, find_packages

setup(
    name='kalman-labs',
    version='1.0.31',
    author='Aditya',
    author_email='aditya@kalman.in',
    description='The Global Kalman Package',
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
