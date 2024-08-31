=======================
My First Sample package
=======================

this is a demo of my first package


pip install twine wheel setuptool


python .\setup.py sdist bdist_wheel

twine check .\dist\* # to check for errors

=============================
To upload to testpypi or live
=============================

twine upload --verbose  --repository testpypi dist/*

twine upload --verbose  dist/*

==================================================
After each version update, tag the release in Git:
==================================================

```
git tag v1.0.1

git push origin v1.0.1
```