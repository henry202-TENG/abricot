import os

os.system('rm -r dist')
os.system('python setup.py sdist')
os.system('twine upload dist/*')