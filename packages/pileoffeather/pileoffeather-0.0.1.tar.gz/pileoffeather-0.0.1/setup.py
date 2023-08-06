from setuptools import setup

setup(
    name='pileoffeather',
    version='0.0.1',
    license='MIT',
    url = 'https://github.com/usedToBeTomas/pile-of-feather',
    author='Daniele Tomaselli',
    description='Lightweight and easy to use ml library for small projects, create a neural network in minutes. (Fun project)',
    packages=['pileoffeather'],
    keywords = ['neural network', 'ml', 'ai', 'machine learning','simple','nn'],
    install_requires=[
        'opencv-python',
        'numpy'
    ]
)
