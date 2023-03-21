from IntegrationPlatform import utils


def api_bluetooth(request, *args, **kwargs):
    return utils.send_receive_req(request.body, "tcp://127.0.0.1:5020", 10000)