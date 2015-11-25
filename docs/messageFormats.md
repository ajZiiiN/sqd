
MessageFormats

Basic Format:

msgId::Messagetype::senderName/Fname:recieverName:time:operationName:operationArgs

msgId - MD5 hash of time
Messagetype - R for Request and A for ack [msgId of ack is same as Request, but time is the time of acknowledgement]

Ex.
'68926bc9cb24244f919aa03a090aa535'::S::sqdC/Fname'::'sqdL'::'2015-12-02 00:02:30'::'addClient':<Args>

===================
Client to Leader:


-----
Client to Woker:

'sqdC/pollWorker'::'sqdW'::'2015-12-02 00:02:30'::'getInfoOnClientData

----------------
Handle timeouts
1. Using reviev timeout socket.recv(timeout=1024)
2. Using hearbeats
3. using socket polls for events
