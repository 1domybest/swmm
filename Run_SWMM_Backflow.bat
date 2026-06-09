@echo off
setlocal

set "ROOT=%~dp0"
set "MODEL=%ROOT%models\seoul_pilot_backflow.inp"
set "OUTDIR=%ROOT%run-results"
set "RPT=%OUTDIR%\seoul_pilot_backflow.rpt"
set "OUT=%OUTDIR%\seoul_pilot_backflow.out"

if not exist "%OUTDIR%" mkdir "%OUTDIR%"

call :find_swmm
if "%SWMM_EXE%"=="" (
  echo EPA SWMM command-line executable was not found.
  echo.
  echo Install EPA SWMM 5.2, then run this file again.
  echo If runswmm.exe is installed in a custom folder, add that folder to PATH.
  echo.
  pause
  exit /b 1
)

echo Running river backflow scenario...
echo Model: %MODEL%
echo SWMM : %SWMM_EXE%
echo.
"%SWMM_EXE%" "%MODEL%" "%RPT%" "%OUT%"
echo.
echo Done.
echo Report: %RPT%
echo Output: %OUT%
echo.
pause
exit /b 0

:find_swmm
set "SWMM_EXE="
where runswmm.exe >nul 2>nul
if not errorlevel 1 (
  for /f "delims=" %%P in ('where runswmm.exe') do (
    set "SWMM_EXE=%%P"
    exit /b 0
  )
)
for %%P in (
  "C:\Program Files\EPA SWMM 5.2.4\runswmm.exe"
  "C:\Program Files\EPA SWMM 5.2.3\runswmm.exe"
  "C:\Program Files\EPA SWMM 5.2.2\runswmm.exe"
  "C:\Program Files\EPA SWMM 5.2.1\runswmm.exe"
  "C:\Program Files\EPA SWMM 5.2.0\runswmm.exe"
  "C:\Program Files (x86)\EPA SWMM 5.2.4\runswmm.exe"
  "C:\Program Files (x86)\EPA SWMM 5.2.3\runswmm.exe"
  "C:\Program Files (x86)\EPA SWMM 5.2.2\runswmm.exe"
  "C:\Program Files (x86)\EPA SWMM 5.2.1\runswmm.exe"
  "C:\Program Files (x86)\EPA SWMM 5.2.0\runswmm.exe"
) do (
  if exist "%%~P" (
    set "SWMM_EXE=%%~P"
    exit /b 0
  )
)
exit /b 0
