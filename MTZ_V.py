import Convertation
import numpy as np
import math
import matplotlib.pyplot as plt


def mtz_sol(file_data):
    if file_data.endswith('.xlsx'):
        file_data = Convertation.convert_ex(file_data)
    file = open(file_data, 'r')

    mas = list(map(int, file.readline().strip().split()))
    hz = list(map(int, file.readline().strip().split()))
    hy = list(map(int, file.readline().strip().split()))
    rho = np.empty((len(hy), len(hz)), dtype=float)

    for i in range(len(hy)):
         rho[i] = list(map(int, file.readline().strip().split()))

    file.close()

    x_data, y_data = [], []

    for i in range(len(hy)):
        x_data.append(np.sum(hy[:i])/1000)

    for i in range(len(hz)):
        y_data.append(np.sum(hz[:i])/1000)

    pos_y = np.arange(len(x_data))
    pos_z = np.arange(len(y_data))

    n = mas[1]

    ro_sol = []
    phi_sol = []

    for i in range(mas[0]):
        temp = mtz_calc([j[i] for j in rho], hz, n)
        ro_sol.append(temp[0])
        phi_sol.append(temp[1])

    def plot_creation():


        figure, axs = plt.subplots(figsize=(15, 15), constrained_layout=True)
        axs.set_yscale("linear")
        axs.set_xticks(pos_y)
        axs.set_yticks(pos_z)
        axs.set_xticklabels(x_data)
        axs.set_yticklabels(y_data)
        axs.set_xlabel("Расстояние по горизонтали, км")
        axs.set_ylabel("Расстояние по вертикали, км")
        axs.set_xlim([0, pos_y[-1]])
        axs.set_ylim([pos_z[-1], 0])
        vs = axs.imshow(rho, cmap='jet', aspect='auto', interpolation='bilinear', origin="upper")
        dbr = plt.colorbar(vs)
        dbr.set_label(r'$lg[\Omega\cdot m]$', fontsize=18)
        plt.savefig('saved_figure.png')
        res = 'saved_figure.png'
        return ('saved_figure.png')

    t1 = 0.01

    def visual_ro():

        figure, axs = plt.subplots(figsize=(15, 15), constrained_layout=True)

        temp_mas = np.log10(np.array(ro_sol))
        axs.plot([i + 1 for i in range(len(temp_mas))], temp_mas)

        axs.set_yscale('log')
        axs.set_xticks([i + 1 for i in range(len(ro_sol))])
        axs.set_xticklabels([i + 1 for i in range(len(ro_sol))])
        axs.set_xlim([1, len(ro_sol)])
        axs.set_xlabel("Номер пикета")
        axs.set_ylabel(r"Кажущееся сопротивление, $lg(\rho_{T})$")

        legend_marks = [t1 * 2 ** (i + 1) for i in range(len(ro_sol[0]))]
        axs.legend(legend_marks, title=r"Периоды, $T [с]$")
        plt.savefig('visual_ro.png')
    def visual_ro2():
        gs_kw = dict(width_ratios=[15, 1])
        figure, (axs, cax) = plt.subplots(1, 2, figsize=(15, 15),  constrained_layout=True, gridspec_kw=gs_kw)
        axs.set_xticks(pos_y)
        axs.set_xticklabels(x_data)
        axs.set_xlim([0, pos_y[-1]])
        axs.set_xlabel("Расстояние по горизонтали, км")

        periods = [t1 * 2 ** (i + 1) for i in range(len(ro_sol[0]))]

        axs.set_yticks([i for i in range(len(periods))])
        axs.set_yticklabels(periods)
        axs.set_ylabel(r"Периоды, $T [с]$")

        temp_mas = np.log10(np.array(ro_sol).transpose())
        p2 = axs.imshow(temp_mas, cmap='jet', aspect='auto', interpolation='bilinear', origin="upper")
        figure.colorbar(p2, cax=cax)
        cax.set_ylabel(r"Кажущееся сопротивление, $lg(\rho_{T})$", rotation=90)
        plt.savefig('visual_ro2.png')



    def visual_phi():


        figure, axs = plt.subplots(figsize=(15, 15), constrained_layout=True)

        axs.plot([i + 1 for i in range(len(phi_sol))], phi_sol)

        axs.set_xticks([i + 1 for i in range(len(phi_sol))])
        axs.set_xticklabels([i + 1 for i in range(len(phi_sol))])
        axs.set_xlim([1, len(phi_sol)])
        axs.set_xlabel("Номер пикета")
        axs.set_ylabel(r"Фаза импеданса, $\phi$")

        legend_marks = [t1 * 2 ** (i + 1) for i in range(len(phi_sol[0]))]
        axs.legend(legend_marks, title=r"Периоды, $T [с]$")
        plt.savefig('visual_phi.png')

    def visual_phi2():
        gs_kw = dict(width_ratios=[15, 1])
        figure, (axs, cax) = plt.subplots(1, 2, figsize=(15, 15), constrained_layout=True, gridspec_kw=gs_kw)
        axs.set_xticks(pos_y)
        axs.set_xticklabels(x_data)
        axs.set_xlim([0, pos_y[-1]])
        axs.set_xlabel("Расстояние по горизонтали, км")

        periods = [t1 * 2 ** (i + 1) for i in range(len(phi_sol[0]))]

        axs.set_yticks([i for i in range(len(periods))])
        axs.set_yticklabels(periods)
        axs.set_ylabel(r"Периоды, $T [с]$")

        temp_mas = np.array(phi_sol).transpose()
        p2 = axs.imshow(temp_mas, cmap='jet', aspect='auto', interpolation='bilinear', origin="upper")
        figure.colorbar(p2, cax=cax)
        cax.set_ylabel(r"Фаза импеданса, $\phi$", rotation=90)
        plt.savefig('visual_phi2.png')

    file_return = plot_creation()
    file2_return = visual_ro()
    file3_return = visual_ro2()
    file4_return = visual_phi()
    file4_return = visual_phi2()
    return file_return



def mtz_calc(p, h, n_size):

    m = 5
    t1 = 0.01
    q = 2
    p, h = np.array(p), np.array(h)
    T = np.array([q ** i * t1 for i in range(m)])
    w = 2 * np.pi / T
    u = 4 * np.pi * 10 ** (-7)
    r = np.empty(m, dtype=complex)
    for i, e in enumerate(w):
        rc = 1
        for j in reversed(range(n_size - 1)):
            k = np.sqrt((-1 * complex("0+1j") * e * u) / p[j])
            a = np.sqrt(p[j] / p[j + 1])
            b = np.exp(-2 * k * h[j]) * (rc - a) / (rc + a)
            rc = (1 + b) / (1 - b)
        r[i] = rc
    rc = np.abs(r) ** 2 * p[0]
    phi_t = np.angle(r) - np.pi / 4
    phi = list(map(math.degrees, (np.angle(r) - np.pi / 4)))
    return [rc, phi]