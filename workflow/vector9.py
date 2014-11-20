import math


class Vector9:

    def __init__(self, x):
        """type x: tuple (x1, x2, x3, ...)
        """
        self.count = len(x)
        self.x = x

    def __str__(self):
        str_format = u"(" + u", ".join([str(float(x)) for x in self.x]) + u")"
        return str_format

    def optRev(self):
        ret = Vector9([-x for x in self.x])
        return ret

    def optLog(self):
        return Vector9([math.log(x) for x in self.x])

    def optNorm(self):
        d = 0
        for i in range(0, self.count):
            d = d + self.x[i] ** 2
        d = math.sqrt(d)
        ret = Vector9([x / d for x in self.x])
        return ret

    def optLogistic(self):
        ret = Vector9([(1 / (1 + math.exp(-x))) for x in self.x])
        return ret

    def optMax(self):
        d = -10000000
        for i in range(0, self.count):
            if self.x[i] > d :
                d = self.x[i]
        ret = Vector9([d for x in self.x])
        return ret

    def operator(self, flag):
        if flag == 1:
            return self.optRev()

        if flag == 2:
            return self.optLog()

        if flag == 3:
            return self.optNorm()

        if flag == 4:
            return self.optLogistic()

        if flag == 5:
            return self.optMax()

