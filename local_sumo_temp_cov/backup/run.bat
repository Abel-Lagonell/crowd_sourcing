@echo off
set map=..\london-seg4\data\

:: Map
python runner.py ^
--map-dir=%map%

pause
