import time
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from Delaunay import DelaunayTriangulation
from Point import Point
import random
from datetime import datetime
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "pgf.texsystem": "pdflatex",
    "pgf.rcfonts": False,
    "axes.labelsize": 14,  # Sets the default axes labels size
    "axes.titlesize": 16,  # Sets the default title size
    "legend.fontsize": 12,  # Sets the default legend font size
    "xtick.labelsize": 12,  # Sets the x tick label size
    "ytick.labelsize": 12   # Sets the y tick label size
})


class Benchmark:
    def __init__(self, algorithms, num_points_start, num_points_end, num_points_step, num_runs):
        self.algorithms = algorithms
        self.num_points_start = num_points_start
        self.num_points_end = num_points_end
        self.num_points_step = num_points_step
        self.num_runs = num_runs

    def generate_random_points(self, num_points):
        return [Point(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_points)]

    def run(self):
        time_bench = {name: [] for name in self.algorithms}
        point_counts = range(self.num_points_start, self.num_points_end + 1, self.num_points_step)

        for num_points in tqdm(point_counts, desc="Benchmarking"):
            avg_times = {name: 0 for name in time_bench}
            for _ in range(self.num_runs):
                random_points = self.generate_random_points(num_points)
                for name, method in self.algorithms.items():
                    triangulation = DelaunayTriangulation(random_points)
                    start_time = time.time()
                    method(triangulation)
                    end_time = time.time()
                    avg_times[name] += (end_time - start_time)

            for name in avg_times:
                avg_times[name] /= self.num_runs
                time_bench[name].append(avg_times[name])

        return point_counts, time_bench

    def plot_time_benchmarks(self, point_counts, time_bench):
        plt.figure(figsize=(12, 6))
        for name, times in time_bench.items():
            plt.plot(point_counts, times, label=f"{name} Triangulation", marker='o')

        plt.xlabel('Number of Points')
        plt.ylabel('Average Runtime (seconds)')
        plt.title('Delaunay Triangulation Algorithms Runtime Comparison')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        png_filename = f"out/benchmark_{timestamp}.png"
        plt.savefig(png_filename, dpi=500)
        
        # filename = f"out/benchmark_{timestamp}.pgf"
        # plt.savefig(filename)
        # print(f'Benchmark results saved to {filename}')
        
        plt.close()
