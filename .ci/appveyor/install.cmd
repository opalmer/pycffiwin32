@ECHO OFF

IF "%PYTHON_VERSION%" == "" (
    ECHO "PYTHON_VERSION is not set"
    EXIT 1
)

IF NOT "%PYTHON_VERSION%" == "2.6.x" (
    %WITH_COMPILER% %PYTHON%\\Scripts\\pip.exe install -r dev_requirements.txt --upgrade --quiet || EXIT 1
) ELSE (
    %WITH_COMPILER% %PYTHON%\\Scripts\\pip.exe install -r dev_requirements-2.6.txt --quiet || EXIT 1
)

%WITH_COMPILER% %PYTHON%\\python.exe setup.py sdist bdist_wheel bdist_msi --quiet || EXIT 1
%WITH_COMPILER% %PYTHON%\\Scripts\\pip.exe install . --quiet || EXIT 1

