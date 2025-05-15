import numpy as np
import matplotlib.pyplot as plt
import fdtd
import matplotlib.patches as patches

#Зададим параметры объекта, на котором будет происходить рассеяние электромагнитного поля. Объект - квадрат
a = b = 250 #размеры сетки
x = y = 70 #координаты источников и детектеров
thickness = 13 #толщина
n = 1.75 #покаатель преломления
side_length = 100 #длина стороны квадрата
time = 500
lym = 750 * 10**-9

c=3*10**8

def square_scatter(a, b, x1, x2, y1, y2, thickness, n, side_length, lym):
    fdtd.set_backend("numpy")
    grid = fdtd.Grid(shape=(a, b, 1), grid_spacing=0.0000001, permittivity=1)

    # Сетка
    grid[y1:y2, x1, 0] = fdtd.LineSource(period=lym / c, name="source")
    grid[y1:y2, x2, 0] = fdtd.LineDetector(name="detector")

    grid[0:thickness, :, :] = fdtd.PML(name="pml_xlow")
    grid[-thickness:, :, :] = fdtd.PML(name="pml_xhigh")
    grid[:, 0:thickness, :] = fdtd.PML(name="pml_ylow")
    grid[:, -thickness:, :] = fdtd.PML(name="pml_yhigh")

    # Создание квадрата
    X, Y = np.ogrid[:a, :b]
    half_side = side_length // 2
    center_x, center_y = a // 2, b // 2

    # Маска для квадрата
    square_mask = (np.abs(X - center_x) <= half_side) & (np.abs(Y - center_y) <= half_side)

    permittivity = np.ones([a, b, 1])
    permittivity[square_mask, 0] = n ** 2
    grid[:, :, 0] = fdtd.Object(permittivity=permittivity, name="square")

    return grid

# Построение графика
def visualize_field(tension, a, b):
    """Визуализация поля с квадратным рассеивателем"""
    plt.figure(figsize=(10, 8))

    # Отображаем поле
    img = plt.imshow(np.transpose(tension),
                     extent=[0, a, 0, b],
                     cmap='RdBu',
                     origin='lower',
                     vmin=-0.02,
                     vmax=0.02)

    # Добавляем квадратный рассеиватель
    center_x, center_y = a // 2, b // 2
    square = patches.Rectangle((center_x - side_length / 2, center_y - side_length / 2),
                               side_length,
                               side_length,
                               linewidth=2,
                               edgecolor='black',
                               facecolor='none',
                               linestyle='--')
    plt.gca().add_patch(square)

    # Добавляем источник и детектор
    plt.scatter([x], [y], c='green', marker='*', s=100, label='Source')
    plt.scatter([a - x], [b - y], c='red', marker='o', s=100, label='Detector')

    # Настройки графика
    plt.colorbar(img, label='Ez field amplitude')
    plt.title(f'Рассеяние на квадрате (t)')
    plt.xlabel('x (узлы сетки)')
    plt.ylabel('y (узлы сетки)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Запуск симуляции
grid = square_scatter(a, b, x, a-x, y, b-y, thickness, n, side_length, lym)
grid.run(time)
visualize_field(grid.E[:, :, 0, 2].real, a, b)