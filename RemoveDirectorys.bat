@echo off
setlocal enabledelayedexpansion

for /d %%d in (*) do (
    echo Deleting directory: "%%d"
    rmdir /s /q "%%d"
)

endlocal