#del /f/s/q dist/

Remove-Item -LiteralPath "dist" -Force -Recurse

py -m pip install --upgrade pip

py -m pip install --upgrade build

 py -m build

py -m pip install --upgrade twine

 py -m twine upload --repository pypi dist/*

