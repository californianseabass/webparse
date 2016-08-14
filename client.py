import io
import json
import random
import socket
import struct
import avro.datafile
import avro.schema as avro_schema
import avro.io
import avro.ipc

SCHEMA = avro_schema.Parse(open("avro_schemas/page.avsc", "rt").read())

CONST_URLS = [
    'http://www.codethatgrows.com/lessons-learned-from-rust-the-result-monad/',
    'http://blog.pnkfx.org/blog/2015/11/10/gc-and-rust-part-1-specing-the-problem/',
    'http://blog.pnkfx.org/blog/2015/10/27/gc-and-rust-part-0-how-does-gc-work/',
    'http://julienblanchard.com/2015/rust-on-aws-lambda/',
    'https://medium.com/@paulcolomiets/async-io-for-rust-part-ii-33b9a7274e67#.y66omtugh'
]

def send_message(connection, message):
    buf = io.BytesIO()
    writer = avro.datafile.DataFileWriter(buf, avro.io.DatumWriter(), SCHEMA)
    writer.append(message)
    writer.flush()
    data_length = buf.tell()
    buf.seek(0)
    data = buf.read()
    bytes_written = connection.send(struct.pack("!L", data_length))
    print("Wrote bytes", bytes_written)
    bytes_written = connection.send(data)
    print("Wrote bytes", bytes_written)

def main():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(('127.0.0.1', 12345))
    for url in CONST_URLS:
        send_message(connection, {
            'url': url,
            'tags': []
        })

if __name__ == '__main__':
    main()