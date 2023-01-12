from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='logic4py',
    version='0.0.3',
    license='MIT',
    author="Davi Romero de Vasconcelos",
    author_email='daviromero@ufc.br',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/daviromero/logic4py',
    description='''logic4py is a libray for teaching logic to computer science students.''',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='Propositional Logic, First-Order Logia, Teaching Logic, Educational Software', 
    install_requires=[
          'rply',
      ],

)
