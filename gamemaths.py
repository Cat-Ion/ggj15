from math import sqrt
def fit_line(points, length):
    xe = points[-1][0]
    ye = points[-1][1]

    xs = [i[0] for i in points]
    ys = [i[1] for i in points]

    mx = sum(xs) * 1.0 / len(xs)
    my = sum(ys) * 1.0 / len(ys)

    dx = xe-mx
    dy = ye-my
    
    l = length / sqrt(dx*dx+dy*dy)

    return ((int(xe - l*dx), int(ye - l*dy)),
            (int(xe),int(ye)))

#    sxx = sum([x*x for x in xs]) - len(xs) * mx*mx
#    sxy = sum([i[0]*i[1] for i in points]) - len(points) * mx * my
#    
#    s = sxy / sxx
#
#    print(mx, my)
#
#    if mx > points[-1][0]:
#        x = (s*s*xe + xe + length * abs(1+s*s)) / (1+s*s)
#    else:
#        x = (s*s*xe + xe - length * abs(1+s*s)) / (1+s*s)
#
#    print(s)
#    return [(int(x), int(ye+(x-xe)*s)),
#            (int(xe),int(ye))]
