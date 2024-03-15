import random
import subprocess

from instance import ServerInstance

instances: list[ServerInstance] = []
class Servor:
    @staticmethod
    def add_instance(instance: ServerInstance):
        instances.append(instance)

    @staticmethod
    def get_instances_list():
        return list(instances)

    @staticmethod
    def clear_all_instances():
        for instance in instances:
            instance.process.kill()
        print(f"Killed {len(instances)} servers.")
        instances.clear()