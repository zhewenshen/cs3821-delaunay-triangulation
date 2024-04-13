from Point import Point
from Delaunay import DelaunayTriangulation
from Plotter import plot_triangles
import random

def generate_random_points(num_points, x_range, y_range):
    return [Point(random.uniform(x_range[0], x_range[1]), random.uniform(y_range[0], y_range[1])) for _ in range(num_points)]

# Parameters for point generation
num_points = 50
x_range = (0, 10000)
y_range = (0, 10000)

# Generate points and compute Delaunay triangulation
random_points = generate_random_points(num_points, x_range, y_range)
triangulation = DelaunayTriangulation(random_points)
triangles = triangulation.incremental_delaunay()

# Plotting the results
plot_triangles(random_points, triangles)
