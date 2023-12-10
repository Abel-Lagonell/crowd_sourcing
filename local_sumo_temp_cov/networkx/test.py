import networkx as nx

def main():
    fh = 'graph2.nx'
    G = nx.read_edgelist(fh,data=(('weight',float),('id',str),),create_using=nx.MultiDiGraph())
    
    # ~ fh = 'graph.nx'
    # ~ G = nx.read_edgelist(fh,create_using=nx.MultiDiGraph())
    data = G.get_edge_data("A","B")
    print(data)
    print(nx.dijkstra_path(G,"A","D"))
    # ~ G = nx.read_weighted_edgelist(fh)
    # ~ print(nx.dijkstra_path(G,'-1','4'))
    return
    
if __name__ == '__main__':
    main()
