from django.core.exceptions import PermissionDenied


def get_allowed_channels(request, channels):
    if not request.user.is_authenticated():
        raise PermissionDenied('Not allowed to subscribe nor to publish on the Websocket!')
    else:
        return set(channels).intersection(['subscribe-broadcast', 'subscribe-group', 'subscribe-user'])
