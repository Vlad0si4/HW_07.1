from setuptools import setup, find_namespace_packages

setup(name = 'Clean_folder',
      version = '0.0.2',
      author = 'Boiko Vlad',
      license = 'MIT',
      packages = find_namespace_packages(),
      entry_points = {'console_scripts' : ['clean_folder = clean_folder.clean: main']})