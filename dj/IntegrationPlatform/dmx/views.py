from IntegrationPlatform import utils


def api_dmx(request, *args, **kwargs):
    return utils.send_receive_req(request.body, "tcp://127.0.0.1:5040", 5000)
