import avro.datafile
import avro.io
import io
import socket
import struct

from core import process_url

class ClientDisconnect(Exception):
    pass

def read_block(connection, message_size):
    bytes_read = 0
    block = b''
    while bytes_read < message_size:
        data = connection.recv(message_size - bytes_read)
        if len(data) == 0:
            raise ClientDisconnect()
        block += data
        bytes_read += len(data)
        print("Read {} bytes".format(len(data)))
    print("Read {} byte block".format(len(block)))
    return block

def handle_client(connection, address):
    try:
        while True:
            size_block = read_block(connection, 4)
            message_size, = struct.unpack("!L", size_block)
            message_block = read_block(connection, message_size)

            message_buf = io.BytesIO(message_block)
            reader = avro.datafile.DataFileReader(message_buf, avro.io.DatumReader())
            for thing in reader:
                page = process_url(thing['url'])
                print('New es page generated with id:\t', page._id)
            reader.close()
    except ClientDisconnect as e:
        print("Client Disconnected")

def start_server(port=12345):
    """ http://layer0.authentise.com/getting-started-with-avro-and-python-3.html"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', port))
    sock.listen(10)

    while True:
        conn, addr = sock.accept()
        handle_client(conn, addr)
        conn.close()

if __name__ == '__main__':
    start_socket_server()
