@echo off
set map=..\london-seg4\data\100\

:: Map
python runner.py ^
--nogui ^
--map-dir=%map% ^
--targets=targets-100.txt ^
--veh.total=40 ^
--veh.exists.max=20 ^
--point.spawn=(721.93,448.23) ^
--point.sink=(4444.59,4448.14) ^
--radius.spawn.sink=500 ^
--method=nash ^
--nash.R=200 ^
--nash.tau=1

pause
