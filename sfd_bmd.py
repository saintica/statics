import matplotlib.pyplot as plt
import numpy as np

# Beam length segments
lengths = [1, 0.25, 0.75, 1, 1]  # lengths AB, BC, CD, DE, EF
positions = np.cumsum([0] + lengths)

# Reactions
R_A = -1.167  # kN
R_D = 32.167  # kN

# Point loads and moments
P1 = 8  # kN at B
P2 = 8  # kN at C
M_B = 20  # kNm at B

# Uniform distributed load
w = 15  # kN/m from D to F

# Shear Force Calculation
SF = np.zeros(len(positions))
SF[0] = R_A
SF[1] = SF[0] - P1
SF[2] = SF[1]
SF[3] = SF[2] - P2
SF[4] = SF[3] + R_D
SF[5] = SF[4] - w * lengths[4]

# Bending Moment Calculation
BM = np.zeros(len(positions))
BM[0] = 0
BM[1] = BM[0] + SF[0] * lengths[0]
BM[2] = BM[1] + SF[1] * lengths[1] + M_B  # Corrected to add positive moment at B
BM[3] = BM[2] + SF[2] * lengths[2]
BM[4] = BM[3] + SF[3] * lengths[3]

# For segment DE (with UDL):
# - Shear force decreases linearly
# - Bending moment increases quadratically
x = np.linspace(positions[4], positions[5], 100)
SF_DE = SF[4] - w * (x - positions[4])
BM_DE = BM[4] + SF[4] * (x - positions[4]) - (w / 2) * (x - positions[4])**2

# Plotting
fig, axs = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

# Beam plot
axs[0].plot(positions, [0]*len(positions), 'k-', lw=3)
axs[0].set_title('Beam Diagram with Loads')
axs[0].set_ylim(-35, 35)
# Drawing loads and supports
axs[0].plot(0, 0, 'go', markersize=10)  # Pin at A
axs[0].plot(3, 0, 'ro', markersize=10)  # Roller at D
axs[0].arrow(1, 0, 0, -8, head_width=0.05, head_length=1, fc='r', ec='r')
axs[0].arrow(2, 0, 0, -8, head_width=0.05, head_length=1, fc='r', ec='r')
axs[0].arrow(3, 0, 0, -15, head_width=0.05, head_length=1, fc='r', ec='r')
axs[0].text(1, -2, '8 kN', ha='center')
axs[0].text(2, -2, '8 kN', ha='center')
axs[0].text(3.5, -8, '15 kN/m', ha='center')

# Shear Force Diagram
axs[1].plot(positions[:5], SF[:5], 'b', drawstyle='steps-post')
axs[1].plot(x, SF_DE, 'b')
axs[1].fill_between(positions[:5], 0, SF[:5], step='post', alpha=0.2)
axs[1].fill_between(x, 0, SF_DE, alpha=0.2)
axs[1].axhline(0, color='black', linewidth=0.5)
axs[1].set_ylabel('Shear Force (kN)')
axs[1].set_title('Shear Force Diagram')

# Bending Moment Diagram
axs[2].plot(positions[:5], BM[:5], 'r', drawstyle='steps-post')
axs[2].plot(x, BM_DE, 'r')
axs[2].fill_between(positions[:5], 0, BM[:5], step='post', alpha=0.2)
axs[2].fill_between(x, 0, BM_DE, alpha=0.2)
axs[2].axhline(0, color='black', linewidth=0.5)
axs[2].set_ylabel('Bending Moment (kNm)')
axs[2].set_title('Bending Moment Diagram')

plt.xlabel('Position along the beam (m)')
plt.tight_layout()
plt.show()
