import matplotlib.pyplot as plt

PID_performance = ["0p0", "1p0", "2p0", "3p0", "4p0", "5p0", "10p0"]
sensitivity = [
    0.0090,
    0.0078,
    0.0070,
    0.0065,
    0.0050,
    0.0047,
    0.0049,
]

plt.scatter(PID_performance, sensitivity)
plt.xlabel(r"$K/\pi Separation \sigma$")
plt.ylabel(r"$\sqrt{S+B}/S$")
plt.title("Preliminary Result")
plt.savefig("PID_plot.png", dpi=1000)
plt.savefig("PID_plot.pdf")