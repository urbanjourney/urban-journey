from collections import defaultdict

from urban_journey.pubsub.trigger.base import TriggerBase
from urban_journey.pubsub.descriptor.instance import DescriptorInstance


class ConditionAnd(TriggerBase):
    """
    This class is a trigger that can be used to combine multiple triggers. It will
    only trigger once all of the child triggers have triggered at least once.

    :param *args: Child triggers that this trigger will wait for.
    """

    def __init__(self, *args):
        super().__init__()

        self.trigger_received = defaultdict(self.trigger_received_factory)
        """
        Dictionary holding a boolean for each child trigger. If True the trigger has already been triggered.
        """

        self.trigger_params = defaultdict(dict)
        """
        Dictionary holding the data sed by each trigger.
        """

        # Create the list of triggers and loop through all parameters.
        self.triggers = []  #: List of child triggers.
        for trigger in args:
            if not isinstance(trigger, TriggerBase):
                raise TypeError("All parameters must inherit from urban_journey.TriggerBase")

            # If the trigger is an other ConditionAnd concatenate.
            if isinstance(trigger, ConditionAnd):
                for tr in trigger.triggers:
                    self.add_trigger(tr)
                    tr.remove_activity(trigger)
            else:
                self.add_trigger(trigger)

    def add_trigger(self, trigger):
        """
        Add a trigger to the ConditionAnd

        :param urban_journey.TriggerBase trigger: Trigger to add
        """

        self.triggers.append(trigger)
        trigger.add_activity(self)
        for trigger_received_instance in self.trigger_received:
            trigger_received_instance[trigger] = False

    def trigger_received_factory(self):
        """
        Factory function used by trigger_params to create new empty dictionary for any new triggers.

        :return: A dictionary with each trigger as a key with None value.
        """
        r = {}
        for trigger in self.triggers:
            r[trigger] = False
        return r

    def all_received(self, instance):
        """Returns True if all triggers have been received."""
        for _, value in self.trigger_received[instance].items():
            if not value:
                return False
        return True

    async def trigger(self, senders, sender_params, instance, *args, **kwargs):
        """
        Triggers all activities connected to this trigger.

        :param senders:
        :param sender_params:
        :param instance:
        :param args:
        :param kwargs:
        """

        # TODO: Write proper documetation for the trigger function parameters.

        sender = senders[0]
        trigger_received_instance = self.trigger_received[instance]

        # Check if it's one of the expected triggers
        if sender not in trigger_received_instance:
            # It's not, but it might be an instance descriptor trigger. In this case the static counterpart will be in
            # the dictionary. So if this is the case, replace the static descriptor trigger with the instance.
            if isinstance(sender, DescriptorInstance):
                # Sanity check.
                if sender.static_descriptor in trigger_received_instance:
                    trigger_received_instance.pop(sender.static_descriptor)
                    trigger_received_instance[sender] = True
                else:
                    # If this happens you where doing some kind of dark voodoo. Don't do it.
                    raise Exception("Received trigger from non registered trigger.")
            else:
                # See comment above.
                raise Exception("Received trigger from non registered trigger.")

        # Mark trigger as received
        trigger_received_instance[sender] = True

        # Add or replace sender parameters.
        trigger_params_instance = self.trigger_params[instance]
        for param, value in sender_params.items():
            trigger_params_instance[param] = value

        # Check if all triggers have been received.
        if self.all_received(instance):
            # If they have, then trigger the activity.
            for activity in self._activities:
                await activity.trigger([self] + senders, trigger_params_instance, instance, *args, **kwargs)

            # Reset the received and parameter dictionaries.
            for trigger in trigger_received_instance:
                trigger_received_instance[trigger] = False
            trigger_params_instance.clear()
