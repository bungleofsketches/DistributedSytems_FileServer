# DistributedSytems_FileServer

###General Design
So far I have completed 3 parts out of the full 4.

###File Server

A simple upload download server. It includes a nice wrapper as evidenced in client.py. Called proxy.py this provides transparency.

###Cache

A simple cache using write-last wins. It is implemented on the client side in their proxy.

###Directory Server

A much more complicated build. It is based off the fileserver. In this model both client and file server contact the Directory Server first. The client contacts it before every read or write call to ask it where it goes.

The file server registers with the directory server as it's first call. After that only updates the directory server when there is a succesful write to it.

In effect the Directory server just keeps a list of available fileservers to write to and which already existing files are at which fileservers.

Read Request : A read request is thus done in the order of
    a) requesting what server the file is on 
    b) then reading from that server.

Write Request : A write request is done by
    a) checking if the file exists and if it does checking where
    b) if it does not exist then asking the Directory server for a the latest available server.
    c) Then writing to the servr and getting confirmation back

To keep some balance the Directory server puts the ports for the fileservers in a queue and chooses from that the next fileserver to write to.
