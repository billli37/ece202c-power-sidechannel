# generate_ghost_peak_graph.py
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

# Generate a synthetic time-domain hardware trace profile (500 sample points)
x = np.arange(0, 500)
np.random.seed(42)

# Simulate baseline background environmental noise
noise_floor_ghost = np.random.normal(0.04, 0.01, 500)
noise_floor_true = np.random.normal(0.04, 0.01, 500)

# Construct a distinct sharp "Ghost Peak" signal at clock cycle index 180
ghost_peak = np.zeros(500)
ghost_peak[160:200] = 0.14 * np.exp(-((x[160:200] - 180) / 10) ** 2)
ghost_corr_series = noise_floor_ghost + ghost_peak

# Construct the true key candidate's signal (completely blinded/flat in Textbook Mode)
true_key_series = noise_floor_true + np.random.normal(0.01, 0.005, 500)

# Plot the statistical wave strings
ax.plot(x, ghost_corr_series, color='#d32f2f', linewidth=2, label='Highest Wrong Guess (Ghost Peak - 0xeb)')
ax.plot(x, true_key_series, color='#78909c', linewidth=1.5, alpha=0.8, linestyle='--', label='Expected True Key Candidate (0x4d)')

# Emphasize the peak anomaly with a targeting annotation ring
ax.annotate(
    'Ghost Peak Convergence\n(ρ_max = 0.1841)',
    xy=(180, 0.1841),
    xytext=(230, 0.16),
    arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6),
    fontweight='bold',
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.3", fc="#ffebee", ec="#d32f2f", lw=1)
)

ax.set_title('Round 1 Telemetry: Textbook Mode Correlation Over Time (Channel 0)', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Microarchitectural Temporal Samples (Time / Clock Cycles)', fontsize=11, labelpad=10)
ax.set_ylabel('Correlation Coefficient Magnitude (|ρ|)', fontsize=11, labelpad=10)
ax.set_ylim(0, 0.25)

ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='#cfd8dc')

plt.tight_layout()
plt.savefig('ghost_peak_analysis.png', bbox_inches='tight')
print("Successfully generated: 'ghost_peak_analysis.png'")
plt.show()