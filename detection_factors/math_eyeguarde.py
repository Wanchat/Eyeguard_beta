import math
class Math_eyeguarde:
    def tanRounded(self, x, num=2):
        Radiansx = math.radians(x)
        tanx = math.tan(Radiansx)
        tanRoundedx = round(tanx, num)
        return tanRoundedx


if __name__ == '__main__':
    t = Math_eyeguarde()
    t2 = t.tanRounded(60,8)
    print(t2)