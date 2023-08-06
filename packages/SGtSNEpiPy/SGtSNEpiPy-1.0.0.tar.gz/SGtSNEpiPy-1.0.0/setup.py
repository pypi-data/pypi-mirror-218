from setuptools import setup
import setuptools

setup(
    name='SGtSNEpiPy',
    version='1.0.0',
    description='SGtSNEpiPy is a Python interface for the SG-t-SNE-П algorithm, a powerful tool for visualizing large, sparse, stochastic graphs.',
    author=['Yihua Zhong','Chenshuhao Qin'],
    author_email="yz737@duke.edu,cq27@duke.edu",
    packages=setuptools.find_packages(),
    install_requires=[
        'juliacall',
    ]
)