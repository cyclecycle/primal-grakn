from pygrakn import Graph

# create a graph
# add some things
# match some things
# delete


with grakn.Graph(keyspace='cognitive_impairment') as graph:
    # data = graph.execute('match $x; limit 10; get;')
    # data = graph.execute('insert $x isa sentence has text \"hi there\";')
    # graph.commit()
    data = graph.execute('match $x isa sentence has text \"hi there\"; get;')
    # data = graph.execute('match $x isa sentence has text \"hi there\"; delete $x;')
    # graph.commit()

    pprint(data)
