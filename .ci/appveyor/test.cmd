cd C:\project

%WITH_COMPILER% %PYTHON%\Scripts\nosetests.exe --with-coverage --cover-package pywincffi -v tests
%PYTHON%\Scripts\coverage.exe xml
%PYTHON%\Scripts\codecov.exe --required
