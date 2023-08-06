from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='lktbotfb',
  version='0.0.2',
  description='This makes it easy for you to create a chatbot for your Facebook page',
  long_description=open('README.txt').read(),
  url='',  
  author='Salah Louktaila',
  author_email='amir.Louktila@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='chatbot', 
  packages=find_packages(),
  install_requires=['django'] 

)