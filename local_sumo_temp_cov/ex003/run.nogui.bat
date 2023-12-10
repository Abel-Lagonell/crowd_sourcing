@echo off
set python=C:\Users\luis_\AppData\Local\Microsoft\WindowsApps\python.exe
set map=..\london-seg4\data\
set target_file=temp/targets.json
set point_spawn=(1534.51,1148.80)
set point_sink=(7009.58,5560.75)
set radius_spawn_sink=250
set veh_total=100
set veh_exists_max=100
set targets=100
set R=500
set tau=1

:: Generate Targets
%python% runner.py ^
--nogui ^
--map-dir=%map% ^
--point.spawn=%point_spawn% ^
--point.sink=%point_sink% ^
--radius.spawn.sink=%radius_spawn_sink% ^
--method=baseline ^
--veh.total=1 ^
--veh.exists.max=1 ^
--target.n=%targets% ^
--target.generate
cls

:: Baseline
%python% runner.py ^
--nogui ^
--map-dir=%map% ^
--point.spawn=%point_spawn% ^
--point.sink=%point_sink% ^
--radius.spawn.sink=%radius_spawn_sink% ^
--method=baseline ^
--veh.total=%veh_total% ^
--veh.exists.max=%veh_exists_max% ^
--target.file=%target_file% ^
--out.dir=baseline%targets%
cls

:: Nash
%python% runner.py ^
--nogui ^
--map-dir=%map% ^
--point.spawn=%point_spawn% ^
--point.sink=%point_sink% ^
--radius.spawn.sink=%radius_spawn_sink% ^
--method=nash ^
--nash.R=%R% ^
--nash.tau=%tau% ^
--veh.total=%veh_total% ^
--veh.exists.max=%veh_exists_max% ^
--target.file=%target_file% ^
--out.dir=nash%targets%

pause
