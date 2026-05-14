@echo off
cls
echo Junk Software Detection Tool
echo ===========================
echo.

:: Scan for installed programs
echo Scanning installed programs...
echo.

:: Create temporary files
type nul > "%temp%\x86_software.txt"
type nul > "%temp%\x64_software.txt"

:: Scan 32-bit software
echo Scanning 32-bit software...
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /s /f "DisplayName" 2>nul > "%temp%\x86_software.txt"

:: Scan 64-bit software
echo Scanning 64-bit software...
reg query "HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall" /s /f "DisplayName" 2>nul > "%temp%\x64_software.txt"

echo.
echo Detected Junk Software:
echo =======================
echo.

:: Check for junk software
findstr /i "360 2345 sogou baidu tencent" "%temp%\x86_software.txt" "%temp%\x64_software.txt"

:: Check if any junk software was found
if %errorlevel% equ 1 (
    echo No junk software detected.
)

echo.
echo Instructions:
echo 1. To uninstall: Open Control Panel - Programs and Features
echo 2. To locate: Check C:\Program Files or C:\Program Files (x86)
echo.

:: Clean up temporary files
del "%temp%\x86_software.txt" 2>nul
del "%temp%\x64_software.txt" 2>nul
echo.
echo Press any key to exit...
pause >nul