import grpc
from concurrent import futures
import analytics_pb2
import analytics_pb2_grpc
import numpy as np
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# gRPC class
class AnalyticsService(analytics_pb2_grpc.AnalyticsServiceServicer):
    def Compute(self, request, context):
        data = np.array(request.data)

        return analytics_pb2.AnalyticsResponse(mean=np.mean(data), max=np.max(data), min=np.min(data), sum=np.sum(data))

# gRPC server
def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    analytics_pb2_grpc.add_AnalyticsServiceServicer_to_server(AnalyticsService(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()

# retrieve gRPC analytics
def get_grpc_analytics():
    channel = grpc.insecure_channel('localhost:50051')
    grpc_client = analytics_pb2_grpc.AnalyticsServiceStub(channel)

    request = analytics_pb2.AnalyticsRequest(data=[32.5,45.2,28.9,22.1])

    response = grpc_client.Compute(request)

    return { "mean": response.mean, "max": response.max, "min": response.min, "sum": response.sum }

# dashboard
@app.get("/dashboard")
def dashboard():
    analytics_data = get_grpc_analytics()

    return analytics_data
    #return {"status":"Analytics service is running"}

if __name__ == "__main__":
    from multiprocessing import Process
    p1 = Process(target=start_grpc_server)
    p1.start()
    uvicorn.run(app, host="0.0.0.0", port=8010)

