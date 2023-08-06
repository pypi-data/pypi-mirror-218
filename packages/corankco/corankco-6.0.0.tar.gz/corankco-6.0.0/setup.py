from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='corankco',
      version='6.0.0',
      description='Kemeny-Young method for rank aggregation of incomplete rankings with ties',
      long_description=readme(),
      url='https://github.com/pierreandrieu/corankco',
      author='Pierre Andrieu',
      author_email='pierre.andrieu@lilo.org',
      license='GPLv2',
      packages=find_packages(include=['corankco', 'corankco.*']),
      # package_data={'corankco': ['data/*']},
      python_requires='>=3.8',
      zip_safe=False,
      install_requires=['numpy~=1.22.0',
                        'python-igraph',
                        'pulp~=2.3',
                        'bioconsertinc>=1.0.0',
                        ]
      )
