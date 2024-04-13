import itertools
from Geometry import circumcircle, distance
from Point import Point

class DelaunayTriangulation:
    def __init__(self, points):
        self.points = points

    def brute_force_delaunay(self):
        triangles = []
        for combo in itertools.combinations(self.points, 3):
            p1, p2, p3 = combo
            if self.is_delaunay_triangle(p1, p2, p3):
                triangles.append((p1, p2, p3))
        return triangles

    def incremental_delaunay(self):
        min_x = min(p.x for p in self.points)
        max_x = max(p.x for p in self.points)
        min_y = min(p.y for p in self.points)
        max_y = max(p.y for p in self.points)
        dx = max_x - min_x
        dy = max_y - min_y
        delta_max = max(dx, dy) * 2

        super_triangle = [
            Point(min_x - delta_max, min_y - delta_max),
            Point(min_x + delta_max / 2, max_y + delta_max),
            Point(max_x + delta_max, min_y - delta_max)
        ]

        triangles = [tuple(super_triangle)]

        for point in self.points:
            bad_triangles = []
            polygon = []

            for triangle in triangles:
                center, radius = circumcircle(*triangle)
                if center and distance(point, center) < radius:
                    bad_triangles.append(triangle)

            triangles = [tri for tri in triangles if tri not in bad_triangles]
            polygon_edges = set()
            for bad in bad_triangles:
                edges = itertools.combinations(bad, 2)
                for edge in edges:
                    if edge in polygon_edges:
                        polygon_edges.remove(edge)
                    else:
                        polygon_edges.add(edge)

            for edge in polygon_edges:
                new_tri = tuple(edge) + (point,)
                triangles.append(new_tri)

        triangles = [tri for tri in triangles if super_triangle[0] not in tri and super_triangle[1] not in tri and super_triangle[2] not in tri]

        return triangles

    def is_delaunay_triangle(self, p1, p2, p3):
        center, radius = circumcircle(p1, p2, p3)
        if center is None:
            return False
        for p in self.points:
            if p not in (p1, p2, p3) and distance(p, center) < radius:
                return False
        return True
