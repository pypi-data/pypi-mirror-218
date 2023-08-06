from setuptools import setup
import setuptools

setup(
    name='SGtSNEpiPy',
    version='1.0.4',
    description='SGtSNEpiPy is a Python interface for the SG-t-SNE-П algorithm, a powerful tool for visualizing large, sparse, stochastic graphs.',
    long_description= "This is a Python wrapper for SG-t-SNE-П (https://github.com/fcdimitr/SGtSNEpi.jl), implemented using the JuliaCall module (https://cjdoris.github.io/PythonCall.jl/stable/juliacall) from PythonCall & JuliaCall package (https://cjdoris.github.io/PythonCall.jl). If you meet any issue, feel free to contact authors.\nEmail:\nchenshuhao.qin@duke.edu\nyihua.zhong@duke.edu",
    author=['Chenshuhao Qin','Yihua Zhong'],
    author_email="cq27@duke.edu, yz737@duke.edu,",
    packages=setuptools.find_packages(),
    install_requires=[
        'juliacall',
    ]
)