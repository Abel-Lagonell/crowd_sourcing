# options.py
# Author: Quentin Goss
# The options parser options are here
import optparse
import env
import sys
import os

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
    opt_parser.add_option('--point.spawn',type='string',dest='point_spawn',default=None,help='The point where vehicles spawn around x.xx,y.yy.')
    opt_parser.add_option('--point.sink',type='string',dest='point_sink',default=None,help='The point where vehicles sink around x.xx,y.yy.')
    opt_parser.add_option('--radius.spawn.sink',type=int,dest='radius_spawn_sink',default=1000,help='The radius around the spawn and sink points where vehicles may spawn.')
    #
    opt_parser.add_option('-o','--out.dir',type='string',dest='out_dir',default='out',help='Output directory.')
    #
    opt_parser.add_option('-m','--method',type='string',dest='method',default='baseline',help='Target selection algorithm.')
    #
    opt_parser.add_option('-R','--nash.R',type='float',dest='nash_R',default=None,help='R value for nash algorithm.')
    opt_parser.add_option('--nash.tau',type='float',dest='nash_tau',default=None,help='tau value for nash algorithm.')
    #
    opt_parser.add_option('--target.cone.size',type='int',dest='target_cone_size',default=10000,help='The size of the middle line used in the target cone selection region. (Should be large)')
    opt_parser.add_option('--target.cone.angle',type='float',dest='target_cone_angle',default=20,help='The angle of the target cone spread. (In degrees)')
    opt_parser.add_option('--target.file',type='string',dest='target_file',default=None,help='Targets files (If specific targets are desired.)')
    opt_parser.add_option('--target.generate',dest='target_generate',default=False,action='store_true',help='Select targets and save them to file, then exit.')
    opt_parser.add_option('--target.n',type='int',dest='target_n',default=None,help='Number of Targets')
    #
    options, args = opt_parser.parse_args()

    # Validate Options
    if options.map_dir == None:
        print('Please specify a map directory with --map-dir')
        sys.exit(1)
    elif options.point_spawn == None:
        print("Please specify a spawn point with --point.spawn=x.xx,y.yy.")
        sys.exit(1)
    elif options.point_sink == None:
        print("Please specify a sink point with --point.spawn=x.xx,y.yy.")
        sys.exit(1)
    elif not options.method.lower() in ['baseline','nash']:
        print('Unknown method. Please specify a valid method with --method.')
        sys.exit(1)
    elif options.method.lower() == 'nash':
        if options.nash_R == None:
            print("Please specify an R value with --nash.R")
            sys.exit(1)
        elif options.nash_tau == None:
            print("Please specify a taur value with --nash.tau")
            sys.exit(1)
    if options.target_file == None and options.target_n == None:
        print("Please specify a target file with --target.file or number of targets to generate with --target_n.")
        sys.exit(1)
        
    # Set variables
    env.veh_total = options.veh_total
    env.veh_exists_max = options.veh_exists_max
    env.point_spawn = parse_point(options.point_spawn)
    env.point_sink = parse_point(options.point_sink)
    env.radius_spawn_sink = options.radius_spawn_sink
    env.out_dir = options.out_dir
    options.method = options.method.lower()
    env.method = options.method
    env.R = options.nash_R
    env.tau = options.nash_tau
    env.target_cone_size = options.target_cone_size
    env.target_cone_angle = options.target_cone_angle
    env.target_file = options.target_file
    env.target_generate = options.target_generate
    env.target_n = options.target_n
    env.seed = options.seed
    
    # Splash
    if env.target_generate:
        splash_generate()
    else:
        if env.method == 'baseline':
            splash_baseline()
        elif env.method == 'nash':
            splash_nash()

    return options

# For parsing spawn and sink points
def parse_point(point):
    point = point.strip('()').split(',')
    return (float(point[0]),float(point[1]))
    
def splash_baseline():
    msg = """
    ▄▄▄▄·  ▄▄▄· .▄▄ · ▄▄▄ .▄▄▌  ▪   ▐ ▄ ▄▄▄ .
    ▐█ ▀█▪▐█ ▀█ ▐█ ▀. ▀▄.▀·██•  ██ •█▌▐█▀▄.▀·
    ▐█▀▀█▄▄█▀▀█ ▄▀▀▀█▄▐▀▀▪▄██▪  ▐█·▐█▐▐▌▐▀▀▪▄
    ██▄▪▐█▐█ ▪▐▌▐█▄▪▐█▐█▄▄▌▐█▌▐▌▐█▌██▐█▌▐█▄▄▌
    ·▀▀▀▀  ▀  ▀  ▀▀▀▀  ▀▀▀ .▀▀▀ ▀▀▀▀▀ █▪ ▀▀▀ 
    """
    print(msg)
    return

def splash_nash():
    msg = """
     ▐ ▄  ▄▄▄· .▄▄ ·  ▄ .▄
    •█▌▐█▐█ ▀█ ▐█ ▀. ██▪▐█
    ▐█▐▐▌▄█▀▀█ ▄▀▀▀█▄██▀▐█
    ██▐█▌▐█ ▪▐▌▐█▄▪▐███▌▐▀
    ▀▀ █▪ ▀  ▀  ▀▀▀▀ ▀▀▀ ·
    """
    print(msg)
    return

def splash_generate():
    msg = """
     ▄▄ • ▄▄▄ . ▐ ▄      ▄▄▄▄▄ ▄▄▄· ▄▄▄   ▄▄ • ▄▄▄ .▄▄▄▄▄.▄▄ · 
    ▐█ ▀ ▪▀▄.▀·•█▌▐█     •██  ▐█ ▀█ ▀▄ █·▐█ ▀ ▪▀▄.▀·•██  ▐█ ▀. 
    ▄█ ▀█▄▐▀▀▪▄▐█▐▐▌      ▐█.▪▄█▀▀█ ▐▀▀▄ ▄█ ▀█▄▐▀▀▪▄ ▐█.▪▄▀▀▀█▄
    ▐█▄▪▐█▐█▄▄▌██▐█▌      ▐█▌·▐█ ▪▐▌▐█•█▌▐█▄▪▐█▐█▄▄▌ ▐█▌·▐█▄▪▐█
    ·▀▀▀▀  ▀▀▀ ▀▀ █▪▀     ▀▀▀  ▀  ▀ .▀  ▀·▀▀▀▀  ▀▀▀  ▀▀▀  ▀▀▀▀ 
    """
    print(msg)
    return

