# runner.py
# Author: Quentin Goss
# Last Modified: 01/23/2019
#
# <!><!><!> !!!!DO NOT MODIFY THIS FILE!!!! <!><!><!>
# <!> This does all the work for starting and     <!>
# <!> connecting to SUMO. Edit core.py instead.   <!>
# <!><!><!><!><!><!><!><!><!><!><!><!><!><!><!><!><!>
#
# Run this file! Refer to the --help flag for argument help.
#
import os
import sys
import optparse
import core
import time
import config
import env
import pantherine as purr
from core import *

__IS_DEBUG_MODE = False # global flag used when calling debug()
__F_START_TIME = time.time()

###############################
#      Import sumolib_and_traci and TracI
###############################
try:
  sys.path.append(config.s_sumo_tools_dir) # Path to SUMO python modules
  from sumolib import checkBinary  
  print("sumolib sucessfully imported.")
except ImportError:  
  sys.exit("Could not locate sumolib in " + config.s_sumo_tools_dir + ".")
import traci


###############################
# Uses optparse to add a --nogui option to run without using the gui.
###############################
def get_options():
    opt_parser = optparse.OptionParser()
    # GUI
    opt_parser.add_option("--nogui",action="store_true",default=False, help="run the commandline version of sumo")
    opt_parser.add_option("--debug",action="store_true",default=False, help="Adds additional print statements for debugging.")
    #
    opt_parser.add_option('--seed',type='int',dest='seed',default=8635839050,help='Random Seed')
    opt_parser.add_option('--map-dir',type='string',dest='map_dir',default=None,help='Directory of SUMO map files')
    #
    options, args = opt_parser.parse_args()

    # Validate Options
    if options.map_dir == None:
        print('Please specify a map directory with --map-dir')
        sys.exit(1)

    # Set our debug global so we only check once
    global __IS_DEBUG_MODE
    __IS_DEBUG_MODE = options.debug

    return options
# end get_options()


###############################
# @param s_msg = message to be printed to console.
# Check if options.debug=true, then print to console.
###############################
def debug(s_msg):
  global __IS_DEBUG_MODE
  if __IS_DEBUG_MODE:
    print(s_msg)
# end debug(s_msg)


###############################
# A quick pause
###############################
def pause():
  input("Press return to continue...")
# end def pause()

###############################
# Execute the TraCI control loop
###############################
def run():
  n_step = 0
  initialize(traci)
  
  while True:
    traci.simulationStep()
    if not timestep(traci,n_step):
        break
    n_step += 1
    continue
  
  finalize()
  
  traci.close()
# end run()

###############################
# Load in the neccesary libraries and launch SUMO + TraCI
###############################
def main():
  if __name__ == "__main__":
    debug("The main script is running.")
    options = get_options()
    env.options = options
    config.s_sumocfg_file = purr.mrf(env.options.map_dir,r'*.sumocfg')
    config.s_net_file = purr.mrf(env.options.map_dir,r'*.net.xml')
    debug("options.nogui=" + str(options.nogui))
    
    # This script has been called from the command line.
    # It will start sumo as a server, then connect and run.
    if options.nogui:
      s_sumo_binary = checkBinary('sumo')
    else:
      s_sumo_binary = checkBinary('sumo-gui')
    debug("s_sumo_binary=" + s_sumo_binary)
    
    # Have TraCI start sumo as a subprocess, then the python script
    # can connect and run
    debug("config.s_sumocfg_file="+config.s_sumocfg_file)
    
    sumo_cmd = [s_sumo_binary, "-c", config.s_sumocfg_file]
    traci.start(sumo_cmd)
    
    run()
    global __F_START_TIME
    print("\n----- runtime takes %s seconds -----" % (time.time() - __F_START_TIME))
# End main

###############################
# The main entry point of the script.
###############################
main()

