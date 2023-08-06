from setuptools import setup, find_packages

setup(
    name='PPTX2MD2REVEALJS',
    version='1.0.0',
    packages=find_packages(),
    author='Vijay Kasibhatla',
    author_email='vijay.kasibhatla@gmail.com',
    description='Converts a pptx file to MD File.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vijayk1981/pptx2md2reveal',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.6',
)
