import sys

class Cache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.videos = []

class EndPoint:
    def __init__(self):
        self.conns = {} # cache -> latency
        self.reqs = {}  # video -> requests

class Graph:
    @classmethod
    def read(cls, f):
        g = cls()

        V, E, R, C, X = intline(f)
        g.videos = intline(f)
        assert len(g.videos) == V
        g.caches = [Cache(X) for i in xrange(C)]
        g.endpoints = []

        for e in xrange(E):
            ep = EndPoint()
            ep.latency, nconns = intline(f)
            g.endpoints.append(ep)
            ep.reqs = dict((i, 0) for i in xrange(V))

            for i in xrange(nconns):
                cacheid, latency = intline(f)
                ep.conns[cacheid] = latency
                #ep.conns[g.caches[cacheid]] = latency

        g.requests = {}
        for r in xrange(R):
            vidid, epid, nreq = intline(f)
            g.endpoints[epid].reqs[vidid] += 1

        return g

    def dump(self):
        print 'graph {'

        for i, cache in enumerate(self.caches):
            label = '%dMB' % cache.capacity
            if cache.videos:
                label += ' (%s)' % ', '.join(map(str, cache.videos))
            print 'cache_%d [shape=box, label="%s"]' % (i, label)

        for i, ep in enumerate(g.endpoints):
            print 'endpoint_%d [shape=circle, label="%d"]' % (i, i)

            for cacheid, latency in ep.conns.iteritems():
                print 'cache_%d -- endpoint_%d [label="%d"]' % (cacheid, i, latency)

        print '}'

def intline(f):
    return map(int, f.readline().split())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python %s FILE' % sys.argv[0]
        sys.exit(0)

    with open(sys.argv[1]) as f:
        g = Graph.read(f)
        g.dump()
