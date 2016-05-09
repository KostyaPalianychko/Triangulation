from numpy import fromfile
from calculations import triangulate

FILE = "data.txt"

size = 0.5
coef = 5
deltacoef = 1.2

data = fromfile(FILE, sep=' ').reshape(-1, 2)

triangulate(data, size, coef, deltacoef)