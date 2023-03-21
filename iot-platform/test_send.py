import zmq, time, json


start = time.time()

# context = zmq.Context()
# socket = context.socket(zmq.REQ)
# print("connecting")
# socket.connect("tcp://127.0.0.1:5001")
# print("connected")

# print("sending")
# #socket.send_string("hello")
# socket.send_string(json.dumps({"find_available": {}}))
# print("waiting for response")
# print(socket.recv().decode())

# print(f"Response time from start: {round(time.time() - start, 4)}")


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5021")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

while True:
    message = socket.recv()
    if message:
        print(f"Got: {message}")
