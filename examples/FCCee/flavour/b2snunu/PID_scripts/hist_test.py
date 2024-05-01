import matplotlib.pyplot as plt
import numpy.random as random

spruced_counts = {"a->b": {"counts": 10, "candidate_mass": random.normal(0.5, 0.25, 100)},
                  "c->d": {"counts": 10, "candidate_mass": random.normal(0.75, 0.25, 100)},
                  "e->f": {"counts": 10, "candidate_mass": random.normal(1.5, 0.25, 100)}}

#for decay, values in spruced_counts.items():
plot_values = [values["candidate_mass"] for values in spruced_counts.values()]
total_entries = sum(len(values) for values in plot_values)
bins = total_entries/10
print(bins)
plt.hist(plot_values, int(bins), stacked=True)
plt.legend(spruced_counts.keys())
plt.tight_layout()
plt.savefig("hist_test.png")
