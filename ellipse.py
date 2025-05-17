import numpy as np
import matplotlib.pyplot as plt
import fdtd
import matplotlib.patches as form


def ellipse(a, b, x1, x2, y1, y2, thickness, refractive_index, r1, r2, time, wavelength, c=300000000):
    fdtd.set_backend("numpy")
    grid = fdtd.Grid(shape=(a, b, 1), grid_spacing=0.0000001, permittivity=1)

    # Сетка
    grid[y1:y2, x1, 0] = fdtd.LineSource(period=wavelength / c, name="source")
    grid[y1:y2, x2, 0] = fdtd.LineDetector(name="detector")

    grid[0:thickness, :, :] = fdtd.PML(name="pml_xlow")
    grid[-thickness:, :, :] = fdtd.PML(name="pml_xhigh")
    grid[:, 0:thickness, :] = fdtd.PML(name="pml_ylow")
    grid[:, -thickness:, :] = fdtd.PML(name="pml_yhigh")

    # Эллипс
    X, Y = np.ogrid[:a, :b]
    ellipse_mask = ((X - a // 2) / r1) ** 2 + ((Y - b // 2) / r2) ** 2 < 1
    permittivity = np.ones([a, b, 1])
    permittivity[ellipse_mask, 0] = refractive_index ** 2
    grid[:, :, 0] = fdtd.Object(permittivity=permittivity, name="circle")

    # Запуск симуляции
    grid.run(total_time=time)
    graph(grid.E[:, :, 0, 2].real, a, b, r1, r2)


# Построение графика
def graph(tension, a, b, r1, r2):
    img = plt.imshow(np.transpose(tension), extent=[0, a, 0, b], cmap="RdBu", origin="lower", vmin=-0.02, vmax=0.02)
    border = form.Ellipse((a // 2, b // 2), 2 * r1, 2 * r2, edgecolor='black', facecolor='none', linewidth=0.5)
    plt.gca().add_patch(border)

    plt.title("Распределение напряженностей")
    plt.xlabel("x")
    plt.ylabel("y")
    cbar = plt.colorbar(img)
    cbar.set_label("E(x, y)")

    plt.tight_layout()
    plt.show()


a = b = 300
x = y = 50
thickness = 10
refractive_index = 1.7
r1 = 50
r2 = 30
time = 500
wavelength = 666 / 10 ** 9
ellipse(a, b, x, (a - x), y, (b - x), thickness, refractive_index, r1, r2, time, wavelength)
