SET REQUIREMENTS="dev_requirements.txt --upgrade"
IF "%PYTHON_VERSION%" == "2.6.x" SET REQUIREMENTS="dev_requirements-2.6.txt"

%WITH_COMPILER% %PYTHON%\\Scripts\\pip.exe install -r %REQUIREMENTS% --quiet || EXIT 1
%WITH_COMPILER% %PYTHON%\\python.exe setup.py sdist bdist_wheel bdist_msi --quiet || EXIT 1
%WITH_COMPILER% %PYTHON%\\Scripts\\pip.exe install . --quiet || EXIT 1

