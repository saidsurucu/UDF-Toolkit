@echo off
:: This script converts a UDF file to DOCX format

REM Check if a UDF file is provided by dragging
IF "%~1"=="" (
    echo Please drag a UDF file onto this script to convert it to DOCX.
    pause
    exit /b 1
)

REM Run the conversion
python udf_to_docx.py "%~1"

REM Check if the conversion was successful
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to convert UDF to DOCX.
    pause
    exit /b 1
)

echo UDF successfully converted to DOCX.
pause
