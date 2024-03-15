from threading import Thread
import time

from instance import ServerInstance
from managers.porter import Porter
from utils import kill_process_tree

# Main instances running
instances: list[ServerInstance] = []

# Closed instances, ran through ServorThread to check if the servers are indeed closed
closed_instances: dict[int, ServerInstance] = {}

class Servor:
    @staticmethod
    def add_instance(instance: ServerInstance):
        instances.append(instance)

    @staticmethod
    def get_instances_list():
        return list(instances)

    @staticmethod
    def close_instance(instance: ServerInstance, hard_close: bool):
        if hard_close:
            # Kill immediately if required
            kill_process_tree(instance.process.pid)
            instance.cleanup_after_close()
        else:
            # Otherwise queue for kill if still exists after 1 minute
            closed_instances[time.time_ns() + 60000000000] = instance
        # In any case remove from "running" instances
        instances.remove(instance)

    @staticmethod
    def close_all_instances():
        for instance in instances:
            instance.process.kill()
        print(f"Killed {len(instances)} servers.")
        instances.clear()


class ServorThread(Thread):
    def check_closed_instances(self):
        # Get time rn & make list of processes confirmed dead
        yoink_out: list[int] = []
        time_rn = time.time_ns()

        # Perform the check (& cleanup directly if found)
        for check_time, instance in closed_instances.items():
            if check_time <= time_rn and not kill_process_tree(instance.process.pid):
                instance.cleanup_after_close()
                yoink_out.append(check_time)
            
        # If anything found to pass the check, remove it from the dict
        for check_time in yoink_out:
            closed_instances.pop(check_time)

    def run(self):
        while True:
            self.check_closed_instances()
            time.sleep(10)


ServorThread().start()