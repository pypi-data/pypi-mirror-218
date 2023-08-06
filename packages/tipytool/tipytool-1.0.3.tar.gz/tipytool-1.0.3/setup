from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tipytools',
    version='1.0.0',
    author='Mauly dotDev',
    author_email='mauly.dev@email.com',
    description='A tool for generating boilerplate for creating command-line tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tipytools/tipytools',
    py_modules=['tipytools.tipytools'],
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'fire',
        # Add any other dependencies required by your tool
    ],
    entry_points='''
        [console_scripts]
        tipy=tipytools.tipytools:main
    ''',
)
