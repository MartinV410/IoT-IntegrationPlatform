from IntegrationPlatform import utils


def api_onewire(request, *args, **kwargs):
    return utils.send_receive_req(request.body, "tcp://127.0.0.1:5010", 5000)
    # body = json.loads(request.body)

    # context = zmq.Context()
    # poller = zmq.Poller()
    # socket = context.socket(zmq.REQ)
    # poller.register(socket, zmq.POLLIN)
    
    # socket.connect("tcp://127.0.0.1:5001")

    # socket.send_string(json.dumps(body))
    # #socket.send_string(request.body)

    # pool_result = poller.poll(timeout=18000)
    # if pool_result:
    #     response = socket.recv().decode()
    #     return JsonResponse(json.loads(response))
    # else:
    #     return Response({"error": "Timeout"}, status=status.HTTP_408_REQUEST_TIMEOUT)