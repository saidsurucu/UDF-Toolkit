@echo off
:: This script converts a DOCX file to UDF format

REM Check if a DOCX file is provided by dragging
IF "%~1"=="" (
    echo Please drag a DOCX file onto this script to convert it to UDF.
    pause
    exit /b 1
)

REM Run the conversion
python docx_to_udf.py "%~1"

REM Check if the conversion was successful
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to convert DOCX to UDF.
    pause
    exit /b 1
)

echo DOCX successfully converted to UDF.
pause
