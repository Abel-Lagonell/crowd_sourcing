# env.py
options = None

# Random Seed
seed = None

# Vehicles
veh_total = None      # Number of vehicles to simulate
veh_exists_max = None # Number of vehicles that may exist at any point in time.
veh_id_counter = 0
vehicles = []         # Tracked Vehicless
vehicles_active = []  # List of active vehicle dictionaries
vehicles_dest = []    # Vehicle Destination nodes ordered by vid [Node0,Node1,...,NodeN]
update_vehicle_info = False # When True, update vehicle info

# Routes
route_id_counter = 0

# Spawn and Sinks
point_spawn = None # (x.xx,y.yy)
point_sink = None  # (x.xx,y.yy)
radius_spawn_sink = None #
spawn_edges = None # [edge0,edge1,...,edgeN]
sink_edges = None  # [edge0,edge1,...,edgeN]

# Edge/Node dictionaries
edges = None # Edge dictionaries for every edge in the map
nodes = None # Node dictionaries for every node in the map

# Networkx graph
nx = None

# targets
target_nodes = None # [node0,node1,...,nodeN]
targets = [] # List of targets
samples = [] # List of samples for easy output
target_cone_size = None # The size of the target selection cone
target_cone_angle = None # The angle of the target selection cone
target_file = None # python binary filename of target data (optional)
target_generate = None # When True. Generate target binary file then exit.
target_n = None # Number of targets to select.

# output directory
out_dir = None

# Target Selection method
method = None

# NASH
dist = None              # Distance object
recalculate_nash = False # Find nash equilibrium again?
nash_assigners = None     # Nash ASsigner Instance
R = None
tau = None

# Baseline
baseline_assign = False

# traci object
traci = None

# Shortest Path Matrices
spm_tar2dest = None
spm_veh2tar = None
spm_complete = None

# First update
first_update = True


