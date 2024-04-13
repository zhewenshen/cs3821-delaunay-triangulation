import argparse
import random
import time
from Point import Point
from Delaunay import DelaunayTriangulation
from Plotter import plot_triangles

def generate_random_points(num_points, x_range, y_range):
    return [Point(random.uniform(x_range[0], x_range[1]), random.uniform(y_range[0], y_range[1])) for _ in range(num_points)]

def main(args):
    random.seed(42)
    num_points = args.num_points
    x_range = (args.x_min, args.x_max)
    y_range = (args.y_min, args.y_max)

    random_points = generate_random_points(num_points, x_range, y_range)
    triangulation = DelaunayTriangulation(random_points)

    algo = args.algorithm.lower()
    if algo == 'brute':
        print("Brute force")
        triangles = triangulation.brute_force_delaunay()
    elif algo == 'incremental':
        print("Incremental")
        triangles = triangulation.incremental_delaunay()
    elif algo == 'divide':
        print("Divide and conquer")
        triangles = triangulation.divide_and_conquer_delaunay()
    else:
        raise ValueError("Unsupported algorithm. Choose from 'brute', 'incremental', or 'divide'.")

    plot_triangles(random_points, triangles)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Delaunay triangulation for random points.")
    parser.add_argument("num_points", type=int, help="Number of random points to generate.")
    parser.add_argument("x_min", type=float, help="Minimum x-value for the range of points.")
    parser.add_argument("x_max", type=float, help="Maximum x-value for the range of points.")
    parser.add_argument("y_min", type=float, help="Minimum y-value for the range of points.")
    parser.add_argument("y_max", type=float, help="Maximum y-value for the range of points.")
    parser.add_argument("--algorithm", choices=['brute', 'incremental', 'divide'], default='brute', help="The Delaunay triangulation algorithm to use.")
    args = parser.parse_args()
    main(args)
