from IntegrationPlatform import utils


def api_neo(request, *args, **kwargs):
    return utils.send_receive_req(request.body, "tcp://127.0.0.1:50060", 10000)
