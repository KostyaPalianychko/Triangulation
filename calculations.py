from numpy import deg2rad, fromfile, cross, arccos, clip, dot, append, insert, delete, empty, fabs
from numpy.linalg import norm
from visualising import visio

EPS = 0.0000000000001


def triangulate(polygon, size, coef, deltacoef):
    lines = empty((0, 2, 2))
    animation = visio((700, 500), polygon)
    while isComplex(polygon, size*deltacoef):
        index, ang = minAngle(polygon)
        if ang < deg2rad(75):
            polygon, lines = leveling(polygon, index, lines, size, coef, deltacoef)
        else:
            polygon, lines = notch(polygon, index, lines, size, coef, deltacoef)
        animation.visualize(lines, finish=False)
    lines = append(lines, [[polygon[0], polygon[1]], [polygon[1], polygon[2]], [polygon[2], polygon[0]]], axis=0)
    animation.visualize(lines, finish=True)
    return lines


def isComplex(polygon, sidelen):
    if polygon.shape[0] != 3:
        return True
    return norm(polygon[0]-polygon[1]) > sidelen or norm(polygon[1]-polygon[2]) > sidelen or norm(polygon[2]-polygon[0]) > sidelen


def minAngle(polygon):
    min_index = 0
    min_angle = angle(polygon[-1]-polygon[0], polygon[1]-polygon[0])
    for i in range(1, len(polygon)):
        if angle(polygon[i-1]-polygon[i], polygon[(i+1)%polygon.shape[0]]-polygon[i]) < min_angle:
            min_index = i
            min_angle = angle(polygon[min_index-1]-polygon[min_index], polygon[(min_index+1)%polygon.shape[0]]-polygon[min_index])
    return min_index, min_angle


def angle(vec1, vec2):
    unit1 = unitVector(vec1)
    unit2 = unitVector(vec2)
    ang = arccos(clip(dot(unit1, unit2), -1.0, 1.0))
    if mycross(unit1, unit2) > 0:
        ang = deg2rad(360) - ang
    return ang


def unitVector(vector):
    return vector / norm(vector)


def getPoints(central, left, right, size, deltacoef):
    isNew1 = isNew2 = False
    if norm(left-central) <= size*deltacoef:
        point1 = left
    else:
        point1 = newPoint(central, left, size)
        isNew1 = True
    if norm(right-central) <= size*deltacoef:
        point2 = right
    else:
        point2 = newPoint(central, right, size)
        isNew2 = True
    return point1, point2, isNew1, isNew2


def newPoint(start, end, size):
    l = size / (norm(end-start)-size)
    return (start + l*end) / (1+l)


def leveling(polygon, index, lines, size, coef, deltacoef):
    point1, point2, isNew1, isNew2 = getPoints(polygon[index], polygon[index-1], polygon[(index+1)%polygon.shape[0]], size, deltacoef)
    if intersects(polygon, point1, point2):
        print("Line intersects polygon: size = size/2")
        return notch(polygon, index, lines, float(size)/2, coef, deltacoef)
    vertex = polygon[index]
    lines = append(lines, [[vertex, point1], [vertex, point2], [point1, point2]], axis=0)
    polygon = add2points(polygon, index, point1, point2, isNew1, isNew2)
    if isNew1:
        polygon = delete(polygon, index+1, axis=0)
    else:
        polygon = delete(polygon, index, axis=0)
    return polygon, lines


def mycross(vec1, vec2):
    result = cross(vec1, vec2)
    global EPS
    return result if fabs(result) > EPS else 0


def intersects(polygon, p1, p2):
    for i in range(len(polygon)):
        p3, p4 = polygon[i-1], polygon[i]
        if mycross(p4-p1, p2-p1)*mycross(p3-p1, p2-p1) < 0 and mycross(p1-p3, p4-p3)*mycross(p2-p3, p4-p3) < 0:
            return True
    return False


def notch(polygon, index, lines, size, coef, deltacoef):
    point1, point2, isNew1, isNew2 = getPoints(polygon[index], polygon[index-1], polygon[(index+1)%polygon.shape[0]], size, deltacoef)
    vertex = polygon[index]
    vec1 = unitVector(point1 - polygon[index])
    vec2 = unitVector(point2 - polygon[index])
    l = size
    # if not (isNew1 or isNew2):
    #     l = (norm(point1-vertex) + norm(point2-vertex)) / 2
    bisect = l * coef * unitVector(vec1 + vec2)
    newVertex = vertex + bisect
    if intersects(polygon, point1, newVertex) or intersects(polygon, point2, newVertex) or intersects(polygon, vertex, newVertex):
        return leveling(polygon, index, lines, size, coef, deltacoef)
    lines = append(lines, [[vertex, point1], [vertex, point2], [vertex, newVertex], [point1, newVertex], [point2, newVertex]], axis=0)
    polygon[index] = newVertex
    polygon = add2points(polygon, index, point1, point2, isNew1, isNew2)
    return polygon, lines


def add2points(polygon, index, point1, point2, isNew1, isNew2):
    if isNew2:
        if index+1 == polygon.shape[0]:
            polygon = append(polygon, [point2], axis=0)
        else:
            polygon = insert(polygon, index+1, point2, axis=0)
    if isNew1:
        polygon = insert(polygon, index, point1, axis=0)
    return polygon
