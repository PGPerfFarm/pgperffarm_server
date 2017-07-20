
class MultiCollector(object):
    'a collector combining multiple other collectors'

    def __init__(self):
        self._collectors = {}

    def register(self, name, collector):
        self._collectors[name] = collector

    def start(self):
        for name in self._collectors:
            self._collectors[name].start()

    def stop(self):
        for name in self._collectors:
            self._collectors[name].stop()

    def result(self):
        r = {}
        for name in self._collectors:
            r.update({name: self._collectors[name].result()})

        return r
