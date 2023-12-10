@echo off
set map=..\london-seg4\data\

:: Map
python runner.py ^
--nogui ^
--map-dir=%map%

pause
