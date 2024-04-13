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
    
    
    # def sweep_line_delaunay(self):
    #     points = sorted(self.points, key=lambda p: p.x)
    #     triangles = []
    #     event_queue = []
    #     beach_line = []

    #     for point in points:
    #         event_queue.append((point.x, point, 'site_event'))

    #     while event_queue:
    #         event = event_queue.pop(0)
    #         if event[2] == 'site_event':
    #             self._handle_site_event(event[1], beach_line, event_queue, triangles)
    #         else:
    #             self._handle_circle_event(event[1], beach_line, event_queue, triangles)

    #     return triangles

    # def _handle_site_event(self, point, beach_line, event_queue, triangles):
    #     if not beach_line:
    #         beach_line.append((point, None, None))
    #         return

    #     arc_above = self._find_arc_above(point, beach_line)
    #     if arc_above is None:
    #         return

    #     i = beach_line.index(arc_above)
    #     if i == 0:
    #         beach_line.insert(0, (point, None, arc_above[0]))
    #     else:
    #         prev_arc = beach_line[i - 1]
    #         beach_line.insert(i, (point, prev_arc[0], arc_above[0]))

    #     self._check_circle_event(i, beach_line, event_queue)
    #     self._check_circle_event(i + 1, beach_line, event_queue)

    # def _handle_circle_event(self, arc, beach_line, event_queue, triangles):
    #     if arc not in beach_line:
    #         return

    #     i = beach_line.index(arc)
    #     if i == 0 or i == len(beach_line) - 1:
    #         return

    #     prev_arc = beach_line[i - 1]
    #     next_arc = beach_line[i + 1]

    #     p1, p2, p3 = prev_arc[0], arc[0], next_arc[0]
    #     triangles.append((p1, p2, p3))

    #     beach_line.pop(i)

    #     self._check_circle_event(i - 1, beach_line, event_queue)
    #     self._check_circle_event(i, beach_line, event_queue)

    # def _find_arc_above(self, point, beach_line):
    #     for arc in beach_line:
    #         if arc[1] is None or arc[2] is None:
    #             return arc
    #         if self._is_point_above_arc(point, arc):
    #             return arc
    #     return None

    # def _is_point_above_arc(self, point, arc):
    #     p1, p2 = arc[1], arc[2]
    #     a = (p1.y - point.y) * (p2.x - p1.x)
    #     b = (p1.x - point.x) * (p2.y - p1.y)
    #     return a > b

    # def _check_circle_event(self, i, beach_line, event_queue):
    #     if i < 1 or i >= len(beach_line) - 1:
    #         return

    #     p1, p2, p3 = beach_line[i - 1][0], beach_line[i][0], beach_line[i + 1][0]
    #     center, radius = circumcircle(p1, p2, p3)

    #     if center is not None and center.x > p3.x:
    #         event_queue.append((center.x, beach_line[i], 'circle_event'))
    #         event_queue.sort(key=lambda e: e[0])

    # def is_delaunay_triangle(self, p1, p2, p3):
    #     center, radius = circumcircle(p1, p2, p3)
    #     if center is None:
    #         return False
    #     for p in self.points:
    #         if p not in (p1, p2, p3) and distance(p, center) < radius:
    #             return False
    #     return True
    
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

