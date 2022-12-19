import os

os.system('rmdir /s /q dist')
# os.system('python setup.py sdist')
os.system('py -m build')
# os.system('py -m twine upload --repository testpypi dist/*') # 測試
os.system('twine upload dist/*') # 正式發布
