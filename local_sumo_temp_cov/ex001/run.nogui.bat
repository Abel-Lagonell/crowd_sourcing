@echo off
set map=..\london-seg4\data\

:: Map
python runner.py ^
--nogui ^
--map-dir=%map% ^
--targets=targets.txt ^
--veh.total=100 ^
--veh.exists.max=5 ^
--point.spawn=(1534.51,1148.80) ^
--point.sink=(7009.58,5560.75) ^
--radius.spawn.sink=1000 ^
--method=nash

pause
