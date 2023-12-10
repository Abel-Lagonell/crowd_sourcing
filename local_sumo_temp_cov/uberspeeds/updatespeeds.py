# updatespeeds.py
# Updates speeds of a sumo SN with UBER data

import os
import sys
import pantherine as purr
import speedhist

def main():
    global OPTIONS; OPTIONS = get_options()
    edg_xml = purr.mrf(OPTIONS.map_dir,r'*.edg.xml')
    edges = purr.readXMLtag(edg_xml,'edge')
    
    original_edges = speedhist.load_edges()
    connections  = speedhist.load_connections()
    
    fn = 'hhh.edg.xml'
    
    with open(fn,'w') as f:    
        f.write('<edges>')
        
        n = 0; total = len(edges)
        for edge in edges:
            conn = purr.filterdicts(connections,'ID',edge['id'])[0]
            child_edges = speedhist.get_edges(conn,original_edges)
            _sum = 0
            for ce in child_edges:
                _sum += ce['mean']
            speed = _sum/len(child_edges)

            f.write('\n\t<edge id="%s" from="%s" to="%s" priority="%s" numLanes="%s" speed="%.3f"/>' % (edge['id'],edge['from'],edge['to'],edge['priority'],edge['numLanes'],speed))
            
            n += 1; purr.update(n,total)
            continue
        
        f.write('\n</edges>')
    return
    
# Parse arguments from Command Line
def get_options():
    from optparse import OptionParser
    parser = OptionParser()
    # Input
    parser.add_option('-m','--map.dir',dest='map_dir', type='string', default=None, help='Directory of sumo map.')
    #
    (options,args) = parser.parse_args()

    if options.map_dir == None:
        print("Please specify a SUMO map directory with -m.")
        sys.exit(0)
    return options
    
if __name__ == "__main__":
    main()
