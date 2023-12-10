# updatespeeds3.py
import pantherine as purr
import statistics

def main():
    map_dir = "../london-seg4/data/100"
    edges = purr.readXMLtag(purr.mrf(map_dir,r'*.edg.xml'),'edge')
    connections = purr.readCSV(purr.mrf(map_dir,r'*.conn.csv'))
    stats = purr.readCSV('edges.stats.csv')
    purr.head(edges)
    purr.head(connections)
    purr.head(stats)
    
    # ~ return
    
    eids = [edge['id'] for edge in edges]
    connections = purr.flattenlist(purr.batchfilterdicts(connections,'CONNECTION ID',eids,show_progress=True))
    print()
    
    total = len(connections)-1
    for i,conn in enumerate(connections):
        try:
            speeds = purr.flattenlist(purr.batchfilterdicts(stats,'ID',conn['EDGE IDS']))
        except TypeError:
            speeds = purr.flattenlist(purr.batchfilterdicts(stats,'ID',[conn['EDGE IDS']]))
        mean = [float(speed['mean']) for speed in speeds]
        std = [float(speed['std']) for speed in speeds]
        p50 = [float(speed['p50']) for speed in speeds]
        p85 = [float(speed['p85']) for speed in speeds]
        edges[i]['mean'] = "%.3f" % (statistics.mean(mean))
        edges[i]['std'] = "%.3f" % (statistics.mean(std))
        edges[i]['p50'] = "%.3f" % (statistics.mean(p50))
        edges[i]['p85'] = "%.3f" % (statistics.mean(p85))
        purr.update(i,total,"Correlating speeds with edges ")
        continue
    
    with open("edg.xml",'w') as f:
        f.write("<edges>")
        for edge in edges:
            f.write("\n\t<edge")
            for key,val in edge.items():
                f.write(' %s="%s"' % (key,val))
            f.write("/>")
            continue
        f.write("\n</edges>")
    
    print("COMPLETE!")
    
    return
    
if __name__ == "__main__":
    main()
