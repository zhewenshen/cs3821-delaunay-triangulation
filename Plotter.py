import matplotlib.pyplot as plt
import datetime

def plot_triangles(points, triangles):
    plt.figure()
    for triangle in triangles:
        tx = [p.x for p in triangle] + [triangle[0].x]
        ty = [p.y for p in triangle] + [triangle[0].y]
        plt.plot(tx, ty, 'b-')
    x = [p.x for p in points]
    y = [p.y for p in points]
    plt.scatter(x, y, color='r')
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"out/delaunay_triangulation_{timestamp}.png"
    plt.savefig(filename, dpi=500)
    print(f"Delaunay triangulation plot saved to {filename}")
    plt.close()
