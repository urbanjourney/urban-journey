

verbosity_channel_transmit = False


def print_channel_transmit(*args, **kwargs):
    if verbosity_channel_transmit:
        print(*args, **kwargs)