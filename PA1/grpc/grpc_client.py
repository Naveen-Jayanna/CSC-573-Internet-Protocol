import logging
import os
import grpc
import time
import statistics
import sys
from protos import hello_pb2, hello_pb2_grpc
from objsize import get_deep_size
from pprint import pprint
import pickle

serverIP = sys.argv[1]
filename = sys.argv[2]
runs = int(sys.argv[3])
extension = ''
file_size = 1000    #size of the file transferred in kb

def get_filepath(filename, extension):
    return f'{filename}{extension}'

def read_iterfile(filepath, chunk_size=1024):
    split_data = os.path.splitext(filepath)
    filename = split_data[0]
    extension = split_data[1]

    metadata = hello_pb2.MetaData(filename=filename, extension=extension)
    yield hello_pb2.UploadFileRequest(metadata=metadata)
    with open(filepath, mode="rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                entry_request = hello_pb2.UploadFileRequest(chunk_data=chunk)
                yield entry_request
            else:  # The chunk was empty, which means we're at the end of the file
                return

def run():
    total_time = 0
    throughput = []
    with grpc.insecure_channel(serverIP + ':50051') as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(hello_pb2.HelloRequest(name='GRPC Client', age=30))
        print("Greeter client received: " + response.message)

        for i in range(runs):
            start = time.time()
            responses = stub.DownloadFile(hello_pb2.MetaData(filename=filename, extension=extension))
            end = time.time()
            sum = 0
            for response in responses:
                # size_estimate of each chunk + headers
                sum += len(pickle.dumps(response))
            print("Total application layer response size:", sum)
            total_time += end - start
            throughput.append(8*file_size/(end-start))

        print("Std dev = ", statistics.stdev(throughput))
        print("mean = ", statistics.mean(throughput))


if __name__ == '__main__':
    logging.basicConfig()
    run()