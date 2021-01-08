"""
Automaton runner
"""

from time import sleep, time


class AutomatonRunner:
    """
    AutomatonRunner

    This should be ran in a thread
    """

    def __init__(self, iter_per_second=10, nb_iter=100):
        '''
        Constructor
        '''
        self.sleep_time = 1 / iter_per_second
        self.nb_iter = nb_iter
        self.stop = False

    def stop(self):
        self.stop = True

    def launch(self, automaton, callback=None):
        self.stop = False
        i = 0
        while not self.stop and i < self.nb_iter:
            time_before = time()

            automaton.apply_rules()
            if callback:
                callback(automaton)

            to_sleep = self.sleep_time - time() + time_before
            if to_sleep > 0:
                sleep(self.sleep_time)
            else:
                print('iteration took too long: {} s'.format(self.sleep_time - to_sleep))
            i += 1
