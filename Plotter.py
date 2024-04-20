import matplotlib.pyplot as plt
import datetime
# import tikzplotlib

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "pgf.texsystem": "pdflatex",
    "pgf.rcfonts": False,
})

def plot_triangles(points, triangles):
    plt.figure()
    for triangle in triangles:
        tx = [p.x for p in triangle] + [triangle[0].x]
        ty = [p.y for p in triangle] + [triangle[0].y]
        plt.plot(tx, ty, 'b-')
    x = [p.x for p in points]
    y = [p.y for p in points]
    plt.scatter(x, y, color='r')
    
    plt.tight_layout()
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    png_filename = f"out/delaunay_triangulation_{timestamp}.png"
    pgf_filename = f"out/delaunay_triangulation_{timestamp}.pgf"
    
    plt.savefig(png_filename, dpi=500)
    print(f"Delaunay triangulation plot saved to {png_filename}")
    
    # plt.savefig(pgf_filename)
    # print(f"Delaunay triangulation plot saved to {pgf_filename}")

    plt.close()
    
