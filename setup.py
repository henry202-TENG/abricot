from setuptools import setup, find_packages

setup(
    name="abricot",
    version="0.0.2",
    author="TENG, CHIHHENG",
    author_email="wiiiy5505aa@gmail.com",
    description="henry teng's functions",

    # project main page
    url="http://google.com/",

    python_requires='>=3',

    # install_requires
    # package==version
    # setuptools==38.2.4
    install_requires=[''],

    # 你要安裝的包，通過 setuptools.find_packages 找到當前目錄下有哪些包
    packages=find_packages(),

    # The documents which are going to be packaged.
    package_data={
        'abc':['*.txt'],
               },
    # The documents which are NOT going to be packaged.
    exclude_package_data={
        '':['main.py']
               }
)