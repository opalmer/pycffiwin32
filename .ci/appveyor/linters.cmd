@ECHO OFF

%PYTHON%\\Scripts\\pep8.exe pywincffi tests || EXIT 1

%PYTHON%\\Scripts\\pylint.exe pywincffi --reports no || EXIT 1

%PYTHON%\\Scripts\\pylint.exe tests --reports no ^
    --disable missing-docstring,invalid-name,too-many-arguments ^
    --disable protected-access,no-self-use,unused-argument ^
    --disable too-few-public-methods || EXIT 1
