from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]
    

setup(
    name='specgenerator',
    version='0.0.3',
    description='A wrapper around PyTorch for doing my own downstream tasks',
    author='harsha.v',
    author_email='vasamsettiharsha@gmail.com',
    url='https://github.com/yourusername/specgenerator',  # Optional
    packages=find_packages(include=["specgenerator"]),
    install_requires=[
        'torch',  # This makes sure PyTorch is installed alongside your package
    ],
)

