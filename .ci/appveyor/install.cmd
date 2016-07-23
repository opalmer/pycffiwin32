@ECHO OFF

IF "%PYTHON_VERSION%" == "" (
    ECHO "PYTHON_VERSION is not set"
    EXIT 1
)

IF NOT "%PYTHON_VERSION%" == "2.6.x" (
    %WITH_COMPILER% %PYTHON%\\Scripts\\pip.exe install -r dev_requirements.txt --upgrade || EXIT 1
) ELSE (
    %WITH_COMPILER% %PYTHON%\\Scripts\\pip.exe install -r dev_requirements-2.6.txt || EXIT 1
)

%WITH_COMPILER% %PYTHON%\\python.exe setup.py sdist bdist_wheel bdist_msi || EXIT 1
%WITH_COMPILER% %PYTHON%\\Scripts\\pip.exe install . || EXIT 1

