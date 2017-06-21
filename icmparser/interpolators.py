import bisect

class LinearInterpolator(object):
    def __init__(self, discrete_function_values):
        self.dfv = discrete_function_values
        self.dfv_keys = sorted(self.dfv.keys())
        self.averaging = 5

    def __call__(self, x):
        le = bisect.bisect_right(self.dfv_keys, x) -1
        ri = le + 1

        if le == -1:
            le = 0
            ri = 1
            while ri < len(self.dfv_keys)-1 and self.dfv[self.dfv_keys[ri]] == self.dfv[self.dfv_keys[le]]:
                ri += 1
        if ri >= len(self.dfv_keys):
            ri = len(self.dfv_keys) - 1
            le = ri - 1
            while le > 0 and self.dfv[self.dfv_keys[le]] == self.dfv[self.dfv_keys[ri]]:
                le -= 1

        le = max(0, le-self.averaging)
        ri = min(len(self.dfv_keys)-1, ri+self.averaging)

        a = (x - self.dfv_keys[le]) / (self.dfv_keys[ri] - self.dfv_keys[le])
        return a*self.dfv[self.dfv_keys[ri]] + (1-a)*self.dfv[self.dfv_keys[le]]