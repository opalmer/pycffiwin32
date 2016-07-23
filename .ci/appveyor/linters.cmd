IF "%PYTHON_VERSION%" == "" (
    ECHO "PYTHON_VERSION is not set"
    EXIT 1
)

%PYTHON%\Scripts\pep8.exe C:\project\pywincffi C:\project\tests || EXIT 1

