# nxopy.py
# Author: Quentin Goss
# Performs common network x operations
import networkx as nx

# Loads a graph from file
# @param string _file = filename
def load_graph(_file):
    return nx.read_edgelist(_file,data=(("weight",float),("id",str),),nodetype=str,comments='%',create_using=nx.MultiDiGraph())

# Determines path weight and the edge ids of the edges along the path
# @param nx.*Graph g = networkx graph
# @param [str] = path of node ids
# @return (float,[str]) = (weight,[edge ids])
def path_info(g,path):
    weight = 0.0
    eids = []
    for eid in range(1,len(path)):
        nxedges = g.get_edge_data(path[eid-1],path[eid])
        edge_weight = None
        shortest_eid = None
        for i in range(0,len(nxedges)):
            if edge_weight == None or nxedges[i]['weight'] < edge_weight:
                edge_weight = nxedges[i]['weight']
                shortest_eid = nxedges[i]['id']
            continue
        weight += edge_weight
        eids.append(shortest_eid)
        continue
    return (weight,eids)

# Get the real non-internal edge of a vehicle
# @param traci = traci instance
# @param string vid = vehicle ID
def get_edge(traci,vid):
    return traci.route.getEdges(traci.vehicle.getRouteID(vid)[traci.vehicle.getRouteIndex(vid)+1]
    
def test():
    map_nx = "london-seg4.nx"
    g = load_graph(map_nx)
    node_list = ["cluster_2322273086_2322273094_2322284839_2322284842_2322284843_2322284844_2322288196_3110025107_5167408001", "26592030", "2322279896", "5164153626", "2322279893", "cluster_2322273093_26592033_26592053", "18129872", "26592042", "1691695943", "1691695945", "1694551474", "104397", "12197627", "490256321", "cluster_109710_1960905159_4844728863", "cluster_1016023571_1016037815_1016037841_1016037850_1016037856_109712_109713_2198691217_2314788134_2314788141_2314788147_2314788152_2314788162_2314788164_2314788166_4840780351_4840780352_4840780356", "25507332", "25507331", "cluster_108292_1232048350_2213529577_2213529578_2213529585_983839050", "983839003", "108290", "25524224", "5393917733", "5393917732", "2527750343", "2527750340", "108283", "108285", "6366384688", "108286", "1784656260", "1270370717", "108277", "6366384082", "108275", "6366384701", "6366384692", "603749192", "6366384694", "2684141453", "686339678", "3783436255", "2620932404", "28782062", "26630783", "345881288", "107777", "2058516816", "2058516819", "26630792", "5521427549", "1531272586", "1531272560", "5521427550", "5034506700", "256794579", "4347922046", "256794580", "cluster_1239525734_25504190_25504191_256794570_26671719", "2726861270", "26671717", "107774", "25504189", "2390039152", "256794588", "256794589", "2390036511", "2390036493", "1697691548", "3397689897", "3326326761", "4350193651", "1497135177", "1106056856", "3326326775", "2338578968", "2338578984", "2105659653", "1106056876", "1947257513", "cluster_1106056861_9515387", "cluster_109838_1106056866", "1947276620", "1106056858", "4350208170", "cluster_107715_1106056846", "1106056863", "1947257517", "cluster_107710_1106056850_1934197347_2663048864_2663048865_280412702", "1685903440", "6283521240", "282569745", "cluster_108895_368279307", "3497406876", "4068974160", "cluster_108896_281454959", "1685903446", "3140855372", "3140855394", "3140965156", "3140855395", "3140855396", "3141011326", "3149029366", "2586621166", "2586635284", "2586614735", "1697772135", "2586616722", "1419565097", "21583366", "5006065039", "cluster_33141178_5006063180", "5006063176", "5006065040", "107693", "5006063170", "5736692334", "25495697", "1816038230", "cluster_25495617_25495769", "25495640", "1953202903", "6279388821", "cluster_6279388822_6279388824", "2458257573", "108389", "cluster_5265953455_5265953456_5265953457_5265953459", "1832248449", "1364168178", "25151180", "1832248458", "cluster_14672924_1832248457_5374174120_5374174223_5374174224_5374183741_5374183742_5573931377", "5573931385", "595709482", "10607626", "108553", "6329692703", "1601832340", "cluster_14673851_1591088620_1601832358_25497323_806373621", "25499288", "109944", "25499294", "25475678", "25499655", "5711517565", "25632683", "cluster_108409_25632684", "25499808", "282719", "25438732", "25438730", "cluster_25438630_25438637", "cluster_25438609_25438655", "25438575", "5784145765", "110137", "25438574", "5683492730", "5683492727", "109365", "5683492745", "5683490019", "4724450101", "4724446335", "cluster_110234_25499953", "5683492748", "242245", "383665923", "5933125752", "5683492736", "1685760099", "5683492739", "5933125746", "25500414", "6525672671", "381448575", "5683503199", "110159", "6512151839", "6154905994", "6008524258", "6508648093", "6512151829", "419243848", "2360780144", "1694591925", "6512171668", "6512151843", "6512151832", "707469214", "6512151844", "2360786282", "6512151830", "6512151834", "378809078", "1694671757", "cluster_1694671786_2312416640", "1694671806", "cluster_10870454_1954751967_1954751981_4035081933_4039317446_4040619140", "4034102515", "4037557120", "5683490018", "249667766", "248175135", "5683526637", "2058136559", "10530335", "49479229", "5830976700", "1770308182", "1692502411", "1770308190", "5830976697", "1762952912", "10870255", "1764426966", "108596", "47318718", "1763037872", "6375004530", "3683048298", "cluster_106839_3683048296_371587496_47318723", "10530334", "648861176", "5659807624", "1761166280", "900714117", "10530339", "106840", "48695355", "198242", "48695361", "cluster_1841340870_28800409", "5659817721", "672650549", "48695367", "198247"]
    weight, edge_list = path_info(g,node_list)
    print("Weight: %.3f" % (weight))
    print("# Edges: %d" % (len(edge_list)))
    print("# Nodes: %d" % (len(node_list)))
    return
    
if __name__ == "__main__":
    test()
