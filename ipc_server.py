from http.server import BaseHTTPRequestHandler, HTTPServer
import avro.ipc as ipc
import avro.protocol as avro_protocol
import avro.schema as schema

PROTOCOL = avro_protocol.Parse(open("avro_schemas/page.avpr").read())

class PageResponder(ipc.Responder):
    def __init__(self):
        ipc.Responder.__init__(self, PROTOCOL)

    def invoke(self, msg, req):
        if msg.name == 'save_url':
            print(msg)
            print(req)
            # message = req['message']
            # return ("Sent message to " + message['to']
            #         + " from " + message['from']
            #         + " with body " + message['body'])
        else:
            raise schema.AvroException("unexpected message:", msg.getname())

class PageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.responder = PageResponder()
        call_request_reader = ipc.FramedReader(self.rfile)
        call_request = call_request_reader.read_framed_message()
        resp_body = self.responder.respond(call_request)
        self.send_response(200)
        self.send_header('Content-Type', 'avro/binary')
        self.end_headers()
        resp_writer = ipc.FramedWriter(self.wfile)
        resp_writer.write_framed_message(resp_body)



def simple_server(port=12345):
    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    serversocket.bind((socket.gethostname(), port))
    # become a server socket
    serversocket.listen(5)

def start_server(port=12345):
    server_addr = ('localhost', port)
    server = HTTPServer(server_addr, PageHandler)
    server.allow_reuse_address = True
    server.serve_forever()

if __name__ == '__main__':
    start_server()
