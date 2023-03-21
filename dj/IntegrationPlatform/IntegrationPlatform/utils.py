from django.http import JsonResponse
import zmq, json
from rest_framework.response import Response
from rest_framework import status


def send_receive_req(data, url, timeout):
    body = json.loads(data)

    context = zmq.Context()
    poller = zmq.Poller()
    socket = context.socket(zmq.REQ)
    poller.register(socket, zmq.POLLIN)
    
    socket.connect(url)

    socket.send_string(json.dumps(body))

    pool_result = poller.poll(timeout=timeout)
    if pool_result:
        response = socket.recv().decode()
        return JsonResponse(json.loads(response), safe=False)
    else:
        return Response({"error": "Timeout"}, status=status.HTTP_408_REQUEST_TIMEOUT)