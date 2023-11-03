@echo off

:: Set the destination directory where PDF files will be moved
set "destination_directory=C:\Users\Nico\Documents\RezeptePDF"

:: Check if the destination directory exists, and if not, create it
if not exist "%destination_directory%" (
    mkdir "%destination_directory%"
)

:: Move all PDF files to the destination directory
for %%f in (*.pdf) do (
    move "%%f" "%destination_directory%"
)

echo PDF files moved to "%destination_directory%"
pause