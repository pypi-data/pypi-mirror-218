from setuptools import setup
import setuptools

setup(
    name='SGtSNEpiPy',
    version='1.0.3',
    description='SGtSNEpiPy is a Python interface for the SG-t-SNE-П algorithm, a powerful tool for visualizing large, sparse, stochastic graphs.',
    long_description= "This is a Python wrapper for SG-t-SNE-П, implemented using the JuliaCall module from PythonCall & JuliaCall package. /nIf you meet any issue, feel free to contact authors.\nEmail:\nchenshuhao.qin@duke.edu\nyihua.zhong@duke.edu",
    author=['Chenshuhao Qin','Yihua Zhong'],
    author_email="cq27@duke.edu, yz737@duke.edu,",
    packages=setuptools.find_packages(),
    install_requires=[
        'juliacall',
    ]
)