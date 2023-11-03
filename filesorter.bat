@echo off

REM Set the source directory
set "source_directory=E:\Cookbook V2\Recepts_docx"

REM Set the destination directories
set "html_destination=E:\Cookbook V2\Recepts_html"
set "doc_destination=E:\Cookbook V2\Recepts_docx"
set "pdf_destination=E:\Cookbook V2\Recepts_pdf"

REM Move .html files
for /r "%source_directory%" %%I in (*.html) do (
    move "%%I" "%html_destination%"
)

REM Move .doc and .docx files
for /r "%source_directory%" %%I in (*.doc *.docx) do (
    move "%%I" "%doc_destination%"
)

REM Move .pdf files
for /r "%source_directory%" %%I in (*.pdf) do (
    move "%%I" "%pdf_destination%"
)

echo All files have been moved.