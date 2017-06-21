import operator


class Selector(object):
    def __init__(self):
        pass

    @staticmethod
    def median(vals):
        assert(len(vals) > 0)
        srt = sorted(vals)
        if len(srt) % 2 == 1:
            return srt[len(srt)//2]
        else:
            return (srt[len(srt)//2-1] + srt[len(srt)//2]) / 2

    def __call__(self, recognized_points):
        data = {}
        for x, ys, in recognized_points.items():
            if len(ys) > 0:
                data[x] = self.median(ys)
        return data


class Nearest(object):
    def __init__(self, values):
        self.values = values

    def __call__(self, v):
        return min(list(map(lambda ref: (ref, abs(ref - v)), self.values)), key=operator.itemgetter(1))[0]