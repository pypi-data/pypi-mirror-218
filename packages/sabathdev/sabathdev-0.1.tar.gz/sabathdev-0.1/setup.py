from setuptools import setup, find_packages

setup(
    name='sabathdev',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'py-cpuinfo',
        'gputil',
        'tabulate',
        'aws-shell',
        'matplotlib',
        'scikit-learn',
        'pandas',
        'wandb',
        'h5py==2.10.0',
        'horovod==0.19.*',
        'jupyterlab-nvdashboard==0.2.*',
        'jupyter-tensorboard==0.2.*',
    ],
    extras_require={
        'cosmoflow': [],
        'miniweather': [],
    },
    # add any additional packages or data that your package needs
)

