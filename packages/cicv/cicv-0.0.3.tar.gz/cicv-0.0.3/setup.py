from setuptools import setup

setup(
    name='cicv',
    version='0.0.3',
    author='Max Chang',
    author_email='p513817@gmail.com',
    description='A common interface for opencv',
    packages=['cicv'],
    python_requires='>=3.6',
    install_requires=[
        "opencv-python>=4"
    ],
)