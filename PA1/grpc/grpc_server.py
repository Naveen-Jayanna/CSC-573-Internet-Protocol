from concurrent import futures
import logging
import os
import grpc
import sys
from protos import hello_pb2, hello_pb2_grpc

serverIP = sys.argv[1]

def get_filepath(filename, extension):
    return f'{filename}{extension}'

class Greeter(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return hello_pb2.StringResponse(message=f'Hello, {request.name}!')

    def UploadFile(self, request_iterator, context):
        data = bytearray()
        filepath = 'dummy'

        for request in request_iterator:
            if request.metadata.filename and request.metadata.extension:
                filepath = get_filepath(request.metadata.filename, request.metadata.extension)
                continue
            data.extend(request.chunk_data)
        with open(filepath, 'wb') as f:
            f.write(data)
        return hello_pb2.StringResponse(message='Success!')

    def DownloadFile(self, request, context):
        chunk_size = 1024
        print("Received")
        #filepath = f'{request.filename}{request.extension}'
        filepath = "./data_files/" + request.filename + request.extension
        print(filepath)
        if os.path.exists(filepath):
            with open(filepath, mode="rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if chunk:
                        entry_response = hello_pb2.FileResponse(chunk_data=chunk)
                        yield entry_response
                    else:  # The chunk was empty, which means we're at the end of the file
                        return


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port(serverIP + ':50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()