import functools
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
        triangles = [tri for tri in triangles if super_triangle[0] not in tri and
                     super_triangle[1] not in tri and super_triangle[2] not in tri]
        return triangles

    def divide_and_conquer_delaunay(self):
        points = sorted(self.points, key=lambda p: p.x)
        return self._divide_and_conquer(points)

    def _divide_and_conquer(self, points):
        if len(points) <= 3:
            return self.brute_force_delaunay()

        mid = len(points) // 2
        left_triangles = self._divide_and_conquer(points[:mid])
        right_triangles = self._divide_and_conquer(points[mid:])

        return self._merge_triangulations(left_triangles, right_triangles)

    def _merge_triangulations(self, left_triangles, right_triangles):
        merged_triangles = left_triangles + right_triangles
        
        convex_hull = self._find_convex_hull(merged_triangles)

        triangulated_hull = self._triangulate_convex_hull(convex_hull)

        final_triangles = [tri for tri in merged_triangles + triangulated_hull
                           if self.is_delaunay_triangle(*tri)]

        return final_triangles

    def _find_convex_hull(self, triangles):
        points = set()
        for triangle in triangles:
            points.update(triangle)

        def orientation(p, q, r):
            return (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

        start = min(points, key=lambda p: (p.y, p.x))

        def compare(p1, p2):
            ori = orientation(start, p1, p2)
            if ori == 0:
                return distance(start, p1) - distance(start, p2)
            return -ori

        sorted_points = sorted(points, key=functools.cmp_to_key(compare))
        
        stack = []
        for point in sorted_points:
            while len(stack) >= 2 and orientation(stack[-2], stack[-1], point) <= 0:
                stack.pop()
            stack.append(point)

        return stack

    def _triangulate_convex_hull(self, convex_hull):
        triangles = []
        n = len(convex_hull)
        for i in range(1, n - 1):
            triangles.append((convex_hull[0], convex_hull[i], convex_hull[i + 1]))
        return triangles
    
    def is_delaunay_triangle(self, p1, p2, p3):
        center, radius = circumcircle(p1, p2, p3)
        if center is None:
            return False
        for p in self.points:
            if p not in (p1, p2, p3) and distance(p, center) < radius:
                return False
        return True

