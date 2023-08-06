from setuptools import setup, find_packages

setup(name="achat_srv_jul",
      version="0.0.2",
      description="mess_server_proj",
      author="Viktor Isupov",
      author_email="viktor.isup@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
