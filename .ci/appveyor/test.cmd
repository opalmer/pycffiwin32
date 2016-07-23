cd C:\project

%WITH_COMPILER% %PYTHON%\Scripts\nosetests.exe --with-coverage --cover-package pywincffi -v tests || EXIT 1
%PYTHON%\Scripts\coverage.exe xml || EXIT 1
%PYTHON%\Scripts\codecov.exe --required || EXIT 1
