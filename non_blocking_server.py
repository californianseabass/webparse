import avro.datafile
import avro.io
import io
import socket
import struct

from core import process_url


# https://gist.github.com/meatcar/081f9c852928934a7029
# http://nbviewer.jupyter.org/github/hammerlab/bdgenomics-notebook/blob/master/Big-Data-Genomics-Tutorial.ipynb
# PROTOCOL = protocol.parse(open("avro_schemas/page.avpr").read())

class ClientDisconnect(Exception):
    pass

def read_block(connection, message_size):
    bytes_read = 0
    block = b''
    print('Receiving message of size: {}'.format(message_size))
    while bytes_read < message_size:
        data = connection.recv(message_size - bytes_read)
        if len(data) == 0:
            raise ClientDisconnect()
        block += data
        bytes_read += len(data)
        print("Read {} bytes".format(len(data)))
    print("Read {} byte block".format(len(block)))
    print('Here is the block I have read {}'.format(block))
    return block

def handle_client(connection, address):
    try:
        while True:
            size_block = read_block(connection, 4)
            message_size, = struct.unpack("!L", size_block)
            message_block = read_block(connection, message_size)

            message_buf = io.BytesIO(message_block)
            view = message_buf.getbuffer()
            print('////////////////')
            print(message_buf.getvalue())
            print(view)

            # reader = avro.datafile.DataFileReader(message_buf, avro.io.DatumReader())
            # for thing in reader:
            #     page = process_url(thing['url'])
            #     print('New es page generated with id:\t', page._id)
            # reader.close()
    except ClientDisconnect as e:
        print("Client Disconnected")

def start_server(host='127.0.0.1', port=12345):
    """ http://layer0.authentise.com/getting-started-with-avro-and-python-3.html"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(10)
    print('serving at {}:{}'.format(host, port))

    while True:
        print('waiting on client to connect')
        conn, addr = sock.accept()
        handle_client(conn, addr)
        conn.close()

if __name__ == '__main__':
    start_socket_server()
