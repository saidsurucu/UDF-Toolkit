@echo off
:: This script converts a scanned PDF file to UDF format

REM Check if a PDF file is provided by dragging
IF "%~1"=="" (
    echo Please drag a PDF file onto this script to convert it to UDF.
    pause
    exit /b 1
)

REM Run the conversion
python scanned_pdf_to_udf.py "%~1"

REM Check if the conversion was successful
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to convert scanned PDF to UDF.
    pause
    exit /b 1
)

echo Scanned PDF successfully converted to UDF.
pause
