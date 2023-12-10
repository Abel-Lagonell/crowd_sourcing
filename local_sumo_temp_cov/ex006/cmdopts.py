# options.py
# Author: Quentin Goss
# The options parser options are here
import optparse
import env
import sys
import os
import pantherine as purr

def get_options():
    opt_parser = optparse.OptionParser()
    # GUI
    opt_parser.add_option("--nogui",action="store_true",default=False, help="run the commandline version of sumo")
    #
    opt_parser.add_option('--seed',type='int',dest='seed',default=8635839050,help='Random Seed')
    opt_parser.add_option('--map-dir',type='string',dest='map_dir',default=None,help='Directory of SUMO map files')
    #
    opt_parser.add_option('--veh.total',type='int',dest='veh_total',default=1000,help='Total amount of vehicles.')
    opt_parser.add_option('--veh.exists.max',type='int',dest='veh_exists_max',default=50,help='The amount of vehicles that exist in the simulation at any time.')
    #
    #
    opt_parser.add_option('-o','--out.dir',type='string',dest='out_dir',default='out',help='Output directory.')
    #
    opt_parser.add_option('-m','--method',type='string',dest='method',default='baseline',help='Target selection algorithm.')
    #
    opt_parser.add_option('-R','--nash.R',type='float',dest='nash_R',default=None,help='R value for nash algorithm.')
    opt_parser.add_option('--nash.tau',type='float',dest='nash_tau',default=None,help='tau value for nash algorithm.')
    #
    opt_parser.add_option('--points.file',type='string',dest='points', default=None,help="Pickle file with vPs, vPd, and tP.")
    #
    opt_parser.add_option('--debug',action='store_true',dest='debug',default=False,help="Debug operations.")
    #
    options, args = opt_parser.parse_args()
    

    # Validate Options
    if options.map_dir == None:
        print('Please specify a map directory with --map-dir')
        sys.exit(1)
    elif not options.method.lower() in ['greedy','smart','validate.pts']:
        print('Unknown method. Please specify a valid method with --method.')
        sys.exit(1)
    elif options.method.lower() == 'nash':
        if options.nash_R == None:
            print("Please specify an R value with --nash.R")
            sys.exit(1)
        elif options.nash_tau == None:
            print("Please specify a taur value with --nash.tau")
            sys.exit(1)
    elif options.points == None:
        print("Please specify the points file that has vPs, vPd, and tP.")
        sys.exit(1)
        
    # Set variables
    env.veh_total = options.veh_total
    env.veh_exists_max = options.veh_exists_max
    env.out_dir = options.out_dir
    options.method = options.method.lower()
    env.method = options.method
    env.R = options.nash_R
    env.tau = options.nash_tau
    env.seed = options.seed
    env.debug = options.debug
    env.vPs, env.vPd, env.tP = purr.load(options.points)
    
    
    
    # Splash
    if env.method == 'greedy':
        splash_greedy()
    elif env.method == 'smart':
        splash_smart()
    elif env.method == 'validate.pts':
        splash_validate_pts()

    return options
    
def splash_greedy():
    msg = """
     ▄▄ • ▄▄▄  ▄▄▄ .▄▄▄ .·▄▄▄▄   ▄· ▄▌
    ▐█ ▀ ▪▀▄ █·▀▄.▀·▀▄.▀·██▪ ██ ▐█▪██▌
    ▄█ ▀█▄▐▀▀▄ ▐▀▀▪▄▐▀▀▪▄▐█· ▐█▌▐█▌▐█▪
    ▐█▄▪▐█▐█•█▌▐█▄▄▌▐█▄▄▌██. ██  ▐█▀·.
    ·▀▀▀▀ .▀  ▀ ▀▀▀  ▀▀▀ ▀▀▀▀▀•   ▀ • 
    """
    print(msg)
    return

def splash_smart():
    msg = """
    .▄▄ · • ▌ ▄ ·.  ▄▄▄· ▄▄▄  ▄▄▄▄▄
    ▐█ ▀. ·██ ▐███▪▐█ ▀█ ▀▄ █·•██  
    ▄▀▀▀█▄▐█ ▌▐▌▐█·▄█▀▀█ ▐▀▀▄  ▐█.▪
    ▐█▄▪▐███ ██▌▐█▌▐█ ▪▐▌▐█•█▌ ▐█▌·
     ▀▀▀▀ ▀▀  █▪▀▀▀ ▀  ▀ .▀  ▀ ▀▀▀ 
    """
    print(msg)
    return

def splash_validate_pts():
    msg = """
     ▌ ▐· ▄▄▄· ▄▄▌  ▪  ·▄▄▄▄   ▄▄▄·▄▄▄▄▄▄▄▄ .     ▄▄▄·▄▄▄▄▄.▄▄ · 
    ▪█·█▌▐█ ▀█ ██•  ██ ██▪ ██ ▐█ ▀█•██  ▀▄.▀·    ▐█ ▄█•██  ▐█ ▀. 
    ▐█▐█•▄█▀▀█ ██▪  ▐█·▐█· ▐█▌▄█▀▀█ ▐█.▪▐▀▀▪▄     ██▀· ▐█.▪▄▀▀▀█▄
     ███ ▐█ ▪▐▌▐█▌▐▌▐█▌██. ██ ▐█ ▪▐▌▐█▌·▐█▄▄▌    ▐█▪·• ▐█▌·▐█▄▪▐█
    . ▀   ▀  ▀ .▀▀▀ ▀▀▀▀▀▀▀▀•  ▀  ▀ ▀▀▀  ▀▀▀     .▀    ▀▀▀  ▀▀▀▀ 
    """
    print(msg)
    return
