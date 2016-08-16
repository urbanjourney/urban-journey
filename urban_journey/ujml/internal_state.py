import copy


class InternalState(object):
    def save(self, instance):
        instance.backup_states_repo[id(self)] = copy.deepcopy(instance.current_states_repo[id(self)])

    def restore(self, instance):
        instance.current_states_repo[id(self)] = instance.backup_states_repo[id(self)]

    def __get__(self, instance, owner):
        if id(self) in instance.current_states_repo:
            return instance.current_states_repo[id(self)]

    def __set__(self, instance, value):
        instance.current_states_repo[id(self)] = value
