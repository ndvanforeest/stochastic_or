import matplotlib.pyplot as plt

from latex_figures import apply_figure_settings

apply_figure_settings(use=True)

labda_r = 0.5  # red jobs
labda_b = 2.5  # blue jobs
labda = labda_r + labda_b
Cae = 1.0  # assumption on inter arrival times
ES0 = 15.0 / 60  # hour
Cse = 1.0  # scv of service times
VS0 = Cse * ES0**2
ER = 2.0  # setup time
VR = 1.0  # Variance of setup times

x = list(range(25, 50))
y = []

for B in x:
    ESe = ES0 + ER / B
    rho = labda * ESe

    # The time to form a red batch
    EW_r = (B - 1) / (2 * labda_r)

    # Now the time a batch spends in queue
    CaB = Cae / B
    VSe = B * VS0 + VR
    ESb = B * ES0 + ER
    CeB = VSe / ESb**2
    EW = (CaB + CeB) / 2 * rho / (1 - rho) * ESb

    # The time to unpack the batch, i.e., the time at the server.
    ES = ER + (B - 1) / 2 * ES0 + ES0

    total = EW_r + EW + ES
    y.append(total)


def cm_to_inch(cm):
    return cm / 2.54


plt.figure(figsize=(cm_to_inch(5), cm_to_inch(6)))
plt.xlim(20, 50)
plt.plot(x, y, label=r"$\mathsf{E}[J_r]$", lw=0.7)
plt.xlabel("$B$")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("../figures/setups.pdf")
plt.savefig("../figures/setups.png", dpi=300)
