
import math

len1 = 10.0
len2 = 10.0

def LawOfCosines(a, b, c):
	C = math.acos((a*a + b*b - c*c) / (2 * a * b))
	return C


def distance(x, y):
	return math.sqrt(x*x + y*y)


def angles(x, y):
	dist = distance(x, y)

	D1 = math.atan2(y, x)

	D2 = LawOfCosines(dist, len1, len2)

	A1 = D1 + D2

	A2 = LawOfCosines(len1, len2, dist)

	return A1, A2


def deg(rad):
	return rad * 180 / math.pi


x = float(raw_input("x>"))
y = float(raw_input("y>"))
a1, a2 = angles(x, y)

print "x=",x
print "y=",y
print "A1(degrees)=", deg(a1)
print "A2(degrees)=", deg(a2)
