# generate_delta_tracking_timeline.py
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(11, 5), dpi=300)

# Define core data series metrics collected across execution iterations
rounds = ['Round 1\n(Textbook Baseline)', 'Round 2\n(Trace Expansion: 1k)', 'Round 3\n(Calibrated Dual-Mask)']
max_corr = [0.1965, 0.2014, 0.2481]  # Highest guess correlation magnitude
exp_corr = [0.0864, 0.1102, 0.2481]  # True expected key correlation magnitude
deltas   = [0.1102, 0.0912, 0.0000]  # Statistical margin distance delta (Δρ)

x = np.arange(len(rounds))
width = 0.25

bar1 = ax.bar(x - width, max_corr, width, label='Max Guess Correlation (ρ_max)', color='#0d47a1')
bar2 = ax.bar(x, exp_corr, width, label='Expected Key Correlation (ρ_exp)', color='#42a5f5')
bar3 = ax.bar(x + width, deltas, width, label='Statistical Distance Delta (Δρ)', color='#ffb300', alpha=0.9)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        if height > 0.0:
            ax.annotate(f'{height:.4f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='semibold')

autolabel(bar1)
autolabel(bar2)
autolabel(bar3)

ax.axvspan(1.6, 2.4, color='#e8f5e9', alpha=0.6, linestyle=':', edgecolor='#4caf50', linewidth=1.5)
ax.text(2.0, 0.15, 'CRITICAL convergence\nKey Broken (Δρ = 0.0000)', 
        color='#1b5e20', fontsize=10, fontweight='bold', ha='center', bbox=dict(boxstyle="square,pad=0.4", fc="white", ec="#a5d6a7", lw=1))

ax.set_title('Multi-Round Diagnostic Attack Timeline: Evolution of Statistical Separation', fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Statistical Coefficient Magnitude', fontsize=11, labelpad=10)
ax.set_xticks(x)
ax.set_xticklabels(rounds, fontsize=10, fontweight='medium')
ax.set_ylim(0, 0.30)

ax.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='#cfd8dc')

plt.tight_layout()
plt.savefig('multi_round_attack_timeline.png', bbox_inches='tight')
print("Successfully generated: 'multi_round_attack_timeline.png'")
plt.show()