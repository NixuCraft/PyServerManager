import random

free_ports = list(range(20000, 20500))

class PortManager:
    @staticmethod
    def get_use_random_port():
        choosen_port = random.choice(free_ports)
        PortManager.use_port(choosen_port)
        return choosen_port

    @staticmethod
    def use_port(port: int):
        free_ports.remove(port)
    
    @staticmethod
    def free_port(port: int):
        if not port in free_ports:
            free_ports.append(port)