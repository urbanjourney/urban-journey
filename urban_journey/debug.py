

# If True, the dta transmitted through ports and channels will be printed.
verbosity_channel_transmit = False


def print_channel_transmit(*args, **kwargs):
    if verbosity_channel_transmit:
        print(*args, **kwargs)