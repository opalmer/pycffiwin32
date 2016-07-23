@ECHO OFF

IF "%PYTHON_VERSION%" == "" (
    ECHO "PYTHON_VERSION is not set"
    EXIT 1
)

%PYTHON%\\Scripts\\pep8.exe pywincffi tests || EXIT 1

IF NOT "%PYTHON_VERSION%" == "2.6.x" (
    %PYTHON%\\Scripts\\pylint.exe pywincffi --reports no || EXIT 1
    %PYTHON%\\Scripts\\pylint.exe tests --reports no ^
        --disable missing-docstring,invalid-name,too-many-arguments ^
        --disable protected-access,no-self-use,unused-argument ^
        --disable too-few-public-methods || EXIT 1

:: Python 2.6's lint step is a little different.  We're using an older
:: version of pylint which has some bugs resulting on false-positives.
) ELSE (
    %PYTHON%\\Scripts\\pylint.exe pywincffi --reports no ^
        --disable bad-option-value,unpacking-non-sequence,maybe-no-member ^
        --disable star-args || EXIT 1
    %PYTHON%\\Scripts\\pylint.exe tests --reports no ^
        --disable missing-docstring,invalid-name,too-many-arguments ^
        --disable protected-access,no-self-use,unused-argument,maybe-no-member ^
        --disable too-few-public-methods,too-many-public-methods ^
        --disable unpacking-non-sequence,bad-option-value,star-args ^
        --disable no-member,import-error || EXIT 1
)
