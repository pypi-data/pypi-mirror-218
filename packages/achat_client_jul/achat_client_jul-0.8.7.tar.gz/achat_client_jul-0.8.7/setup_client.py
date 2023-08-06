from setuptools import setup, find_packages

setup(name="achat_client_jul",
      version="0.8.7",
      description="mess_client",
      author="Viktor Isupov",
      author_email="viktor.isup@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )