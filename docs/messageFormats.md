
MessageFormats

Basic Format:

msgId::type::senderName/Fname:recieverName:time:operationName:operationArgs

msgId - MD5 hash of time
Messagetype - R for Request and A for ack [msgId of ack is same as Request, but time is the time of acknowledgement]

Ex.
68926bc9cb24244f919aa03a090aa535::R::sqdC/Fname::sqdL::2015-12-02 00:02:30::addClient:<Args>

===================
Worker to Client:

* no messages
* yes|no :: [1, A]


-----
Client to Worker:

* are you my worker :: [1, R]

------
Leader to Worker (These whould be minimal)

* check is alive :: [2, R]  [DONE]
* average sum of files size and count transfered till date and today :: [3, R]
* take this client :: [4: R] 
* ok | !ok :: [5, A]

------
Worker to Leader

* ask to join :: [5, R]
* yes|no :: [2, A]  [DONE]
* data :: [3, A]
* accepted| rejected :: [4: A]

----------------
Client to leader

* i am a client :: [6, R]

---------------
Leader to Client

* Use this worker :: [6, A]

===============
CLI:

sqd [--mode [client|leader|worker] [start|stop|restart]] 
    [--status [full|mode] ]

CLI::[mode|status]::args

===============
Handle timeouts
1. Using reviev timeout socket.recv(timeout=1024)
2. Using hearbeats
3. using socket polls for events

http://zguide.zeromq.org/py%3alpclient
http://zguide.zeromq.org/py%3alpserver

http://zguide.zeromq.org/page%3aall#Chapter-Reliable-Request-Reply-Patterns
ALL: http://zguide.zeromq.org/page%3aall#top