# This is the `packages` folder in the standard SDLE git repository structure.

This is the README for the XRDImage package. 

To commit any changes to the PyPI website, you will need the twine package.

1. pip install twine
2. python3 setup.py sdist bdist_wheel
3. twine upload dist/*