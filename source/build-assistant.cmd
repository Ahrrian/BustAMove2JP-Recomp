@echo off
cd /d "%~dp0.."
"%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /nologo /target:winexe /optimize+ /out:Assistente_BAM2.exe /reference:System.Windows.Forms.dll /reference:System.Drawing.dll source\Assistente.cs
exit /b %ERRORLEVEL%
