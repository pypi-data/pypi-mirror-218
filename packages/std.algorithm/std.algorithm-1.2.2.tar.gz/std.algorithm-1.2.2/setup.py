from setuptools import setup

if __name__ == "__main__":
    setup(package_data={'': [
        'lib/eigen.dll',
        'lib/libeigen.so',
        'assets/cn/segment/vocab.csv',
        'assets/jp/segment/vocab.csv',
    ]})
    
# usage of twine:
# pip install twine
# python setup.py install
# del dist\*.tar.gz && python setup.py sdist && twine upload dist/*.tar.gz 
# del dist\*.tar.gz && python setup.py sdist && twine upload -r nexus dist/*.tar.gz
# pip uninstall -y std.algorithm && pip install --upgrade std.algorithm
# pip install --upgrade std.algorithm -i https://pypi.Python.org/simple/