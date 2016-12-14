import inspect
import logging
import functools


nlog = logging.getLogger("networking")


class NetworkCommandBase:
    pass


def network_command(command_id: int):
    class NetworkCommandDecorator(NetworkCommandBase):
        def __init__(self, target):
            self.__target = target
            self.name = target.__name__
            self.__doc__ = inspect.getdoc(target)
            self.command_id = command_id

            # If you get some error about NoneType is not callable on the
            # handler_func attribute. You've most likely forgotten to define a handler.
            self.handler_func = None

        def __get__(self, instance, owner):
            if instance is None:
                return self
            return functools.partial(self.__target, instance)

        async def call_handler(self, *args, **kwargs):
            return await self.__target(*args, **kwargs)

        def handler(self, target):
            if target.__name__ == self.name:
                self.handler_func = target
                return self
            else:
                raise Exception("'{}' handler function must have the same name as the command. The current handler name is '{}'.".format(
                    self.name, target.__name__
                ))

    return NetworkCommandDecorator
