@echo off
set python=C:\Users\luis_\AppData\Local\Microsoft\WindowsApps\python.exe
set map=..\london-seg4\data\
set target_file=temp/targets.json
set point_spawn=(1534.51,1148.80)
set point_sink=(7009.58,5560.75)
set radius_spawn_sink=250
set veh_total=10
set veh_exists_max=5
set targets=5
set R=1000
set tau=1

:: Generate Targets
REM ~ %python% runner.py ^
REM ~ --nogui ^
REM ~ --map-dir=%map% ^
REM ~ --point.spawn=%point_spawn% ^
REM ~ --point.sink=%point_sink% ^
REM ~ --radius.spawn.sink=%radius_spawn_sink% ^
REM ~ --method=baseline ^
REM ~ --veh.total=1 ^
REM ~ --veh.exists.max=1 ^
REM ~ --target.n=%targets% ^
REM ~ --target.generate
REM ~ cls

:: Baseline
REM ~ %python% runner.py ^
REM ~ --nogui ^
REM ~ --map-dir=%map% ^
REM ~ --point.spawn=%point_spawn% ^
REM ~ --point.sink=%point_sink% ^
REM ~ --radius.spawn.sink=%radius_spawn_sink% ^
REM ~ --method=baseline ^
REM ~ --veh.total=%veh_total% ^
REM ~ --veh.exists.max=%veh_exists_max% ^
REM ~ --out.dir=baseline%targets% ^
REM ~ --target.n=%targets%
REM ~ cls


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
--out.dir=nash%targets% ^
--target.n=%targets%
pause
