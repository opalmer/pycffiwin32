cd C:\project

%WITH_COMPILER% %PYTHON%\Scripts\nosetests.exe --with-coverage --cover-package pywincffi -v tests
%WITH_COMPILER% %PYTHON%\Scripts\coverage.exe xml
%WITH_COMPILER% %PYTHON%\Scripts\codecov.exe --required
