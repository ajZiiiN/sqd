# sqd
Squirrel management daemon

#Terms

* Client:
The guy who recieves logs and responsible to send them to Squirrel cluster eventually

* Leader:
All clients talk to leader and eventually gets a worker node, who is gonna process their logs from now on.

* Worker:
Responsible to handle stats files from one client and eventually make them available fo squirrel.

## Design

# Client:
starts sqd as client.
Confirms learder as a client to Given Cluster.
Recieves acknowledgement from Learder.
Starts communicating to one of the Worker.

IF Either of client or worker dies, the guy who is alive tels the leader that the other partner has died and
gets the replacement from Leader.

# Worker:
start sqd as a worker.
Confirms leader as a worker to given cluster.
Revieves and ack from Leader

Starts communicating with the Client


#Leader:
Maked sure each of worker are running same squirrel version.

#config
All config files are created from base file in src/config directory and resides in /etc/sqd


###############################

##sqd

-------
INITIALIZE:

sqd -[C|L|W] init
	creates a sqd as client worker or Leader
	creates a config file, from a sample file for each of client worker and leader
	does sanity check like, no two leaders in same cluster
	
[L]sqd --addCl <client-ip>
[L]sqd [stop|start|restart|config]
[L]sqd 

-------
HANDSHAKE:

CLIENT:
	checkout leader
	get leader info
	send leader its ssh pem keys
	get info about worker
	contact worker and confirm worker

LEADER:
	checkout all workers
	keep and maintain for dead and alive workers
	keep listning for new clients
	keep a new worker ready for new client
	keep checking load on each workers

WORKER:
	Get client info from Leader
	do job for all clients
	maintain client info and connection
	keep record of load from each client and complain Leader if overloaded

--------
WORK:

CLIENT:
	keep an eye on files produced and are they getting consumed by the worker
	if worker is dead ask leader for new worker
	if worker is alive and not cleaning fast, complain Leader

WORKER:
	keep getting files from Client and pass them over to squirrel
	make sure to tell Leader is client is dead or has no data.
	Confirm leader about data being processed, workLoad Index

LEADER:
	keep checking on Client and Workers being alive and doing their job
	keep tuning data load
	