from abc import abstractmethod

# Kinda shitty interface, not really needed
# but since this is made to work w Java things might as well go full Java mode.
class Instance:
    @abstractmethod
    def setup_and_run(self):
        raise Exception("Unimplemented method.")
    
    @abstractmethod
    def get_name(self):
        raise Exception("Unimplemented method.")