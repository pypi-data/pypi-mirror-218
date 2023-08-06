from setuptools import setup, find_packages

setup(name="async_chat_client_kd",
      version="0.1",
      description="chat_client",
      author="Dmitry K",
      author_email="k-d@bk.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
