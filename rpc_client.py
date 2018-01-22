
import sys

import avro.ipc as ipc
import avro.protocol as protocols

PROTOCOL = protocols.Parse(open("avro_schemas/page.avpr").read())

server_addr = ('localhost', 65111)

class UsageError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

if __name__ == '__main__':

    # client code - attach to the server and send a message
    client = ipc.HTTPTransceiver(server_addr[0], server_addr[1])
    requestor = ipc.Requestor(PROTOCOL, client)
    
    # fill in the Message record and send it
    message = dict()
    message['url'] ='http://blog.pnkfx.org/blog/2015/11/10/gc-and-rust-part-1-specing-the-problem/'

    params = dict()
    params['save'] = message
    print("Result: " + requestor.Request('saves', params))

    # cleanup
    client.close()