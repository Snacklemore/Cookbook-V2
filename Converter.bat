@echo off

for %%f in (*) do (
	if "%%~xf"==".html" (
    		weasyprint.exe %%f %%f.pdf
	)

)

pause