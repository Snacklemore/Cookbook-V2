@echo off
setlocal enabledelayedexpansion

for %%f in (*) do (
    if "%%~xf" neq ".bat" (
        set "filename=%%f"
        set "new_filename=!filename: =!"
        if not "!filename!"=="!new_filename!" (
            echo Renaming "!filename!" to "!new_filename!"
            ren "%%f" "!new_filename!"
        )
    )
)

endlocal