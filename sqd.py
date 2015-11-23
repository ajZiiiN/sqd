
'''

This is the main daemon which acts as Leader, Client and Worker.

Few workers and one Leader forms a cluster.

Each sqd-W is started with a worker argument.
Further, on Leader not this worker must be added, with command add worker.

Each sqd-C is starte with a client argument.
Further, on leader node this Client must be added.

Each sqd-L is started with a leader argument.
It can be initialized with set of clients and workers.

'''

