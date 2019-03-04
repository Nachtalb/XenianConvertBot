from setuptools import find_packages, setup

version = '0.0.1.dev0'

setup(name='XenianConverterBot',
      version=version,
      description="I just convert video files to mp4.",
      long_description=f'{open("README.rst").read()}\n{open("CHANGELOG.rst").read()}',

      author='Nachtalb',
      url='https://github.com/Nachtalb/XenianConverterBot',
      license='GPL3',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['converter'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'mr.developer',
          'python-telegram-bot',
          'requests',
      ],

      entry_points={
          'console_scripts': [
              'bot = converter.bot.bot:main',
          ]
      })
