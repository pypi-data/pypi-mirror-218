from setuptools import setup

setup(name='dbbkp',
      version='0.1.20',
      description='dbbkp Package',
      packages=['dbbkp', 'dbbkp/engines', 'dbbkp/utils'],
      install_requires=["numpy", "pandas",
                        "matplotlib", "utilum", "sql_formatter"],
      zip_safe=False,
      )
