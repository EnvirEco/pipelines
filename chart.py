import matplotlib.pyplot as plt
import numpy as np

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

# ============================================
# CHART 1: OIL VOLUMES WATERFALL (BY PIPELINE)
# ============================================

categories_oil = ['Baseline', 'Line 3\nProduction\n(Oct 2021)', 'TMX\nProduction\n(May 2024)', 
                  'Rail Decline\n(Modal Shift)', 'Adjustments', 'Net Pipeline\nThroughput']
values_oil = [0, 343, 201, 129, -18, 0]  # Last value will be computed
colors_oil = ['lightgray', 'darkblue', 'navy', 'steelblue', 'orange', 'darkgreen']

# Calculate cumulative
cumulative_oil = [0]
for i in range(1, len(values_oil)):
    if i < len(values_oil) - 1:
        cumulative_oil.append(cumulative_oil[-1] + values_oil[i])
    else:
        cumulative_oil.append(cumulative_oil[-1])  # Final total

# Create bars
for i in range(len(categories_oil)):
    if i == 0:
        ax1.bar(i, 0, color=colors_oil[i], edgecolor='black', linewidth=1.5, width=0.6)
    elif i == len(categories_oil) - 1:
        ax1.bar(i, cumulative_oil[i], color=colors_oil[i], edgecolor='black', linewidth=1.5, width=0.6)
    else:
        if values_oil[i] > 0:
            ax1.bar(i, values_oil[i], bottom=cumulative_oil[i-1], 
                   color=colors_oil[i], edgecolor='black', linewidth=1.5, width=0.6)
        else:
            ax1.bar(i, abs(values_oil[i]), bottom=cumulative_oil[i], 
                   color=colors_oil[i], edgecolor='black', linewidth=1.5, width=0.6)

# Add connecting lines
for i in range(len(categories_oil) - 1):
    if i < len(categories_oil) - 2:
        ax1.plot([i + 0.3, i + 0.7], [cumulative_oil[i], cumulative_oil[i]], 
                'k--', linewidth=1, alpha=0.5)

# Add value labels
for i in range(1, len(categories_oil)):
    if i < len(categories_oil) - 1:
        y_pos = cumulative_oil[i-1] + values_oil[i]/2 if values_oil[i] > 0 else cumulative_oil[i] - abs(values_oil[i])/2
        label = f"+{values_oil[i]}" if values_oil[i] > 0 else f"{values_oil[i]}"
        ax1.text(i, y_pos, label, ha='center', va='center', fontweight='bold', fontsize=12)
    else:
        ax1.text(i, cumulative_oil[i]/2, f"{cumulative_oil[i]:.0f}", 
                ha='center', va='center', fontweight='bold', fontsize=13, color='white')

ax1.set_xticks(range(len(categories_oil)))
ax1.set_xticklabels(categories_oil, fontsize=10, fontweight='bold')
ax1.set_ylabel('Oil Volume (kb/d)', fontsize=13, fontweight='bold')
ax1.set_title('Pipeline Impact: Production & Modal Shift by Pipeline', fontsize=14, fontweight='bold', pad=20)
ax1.axhline(0, color='black', linewidth=0.8)
ax1.grid(axis='y', alpha=0.3)
ax1.set_ylim(-50, 750)

# Add annotations
ax1.annotate('DiD Effect:\n+343 kb/d', xy=(1, 343/2), xytext=(1, 400),
            arrowprops=dict(arrowstyle='->', color='darkblue', lw=1.5),
            fontsize=9, ha='center', color='darkblue', fontweight='bold')
ax1.annotate('DiD Effect:\n+201 kb/d', xy=(2, 343 + 201/2), xytext=(2, 600),
            arrowprops=dict(arrowstyle='->', color='navy', lw=1.5),
            fontsize=9, ha='center', color='navy', fontweight='bold')

# ============================================
# CHART 2: EMISSIONS WATERFALL (BY PIPELINE)
# ============================================

# Calculate emissions by pipeline
# Line 3: 343 kb/d × 67 kg/bbl × 365.25 / 1,000,000 = 8.4 Mt (constant)
# TMX: 201 kb/d × 67 kg/bbl × 365.25 / 1,000,000 = 4.9 Mt (constant)
# Line 3 with declining: 343 kb/d × 70.6 kg/bbl (2021 avg) × 365.25 / 1,000,000 = 8.8 Mt
# TMX with declining: 201 kb/d × 66.4 kg/bbl (2024 avg) × 365.25 / 1,000,000 = 4.9 Mt
# Actually from your analysis: Line 3 = 2.7 Mt, TMX = 2.0 Mt with declining

categories_emissions = ['Baseline', 'Line 3\n(Constant\nIntensity)', 'TMX\n(Constant\nIntensity)', 
                       'Technology\nOffset\n(2%/year)', 'Net Upstream\nEmissions']
values_emissions = [0, 8.4, 4.9, -8.3, 0]  # Total constant = 13.3, offset = -8.3, net = 5.0
colors_emissions = ['lightgray', 'darkred', 'red', 'green', 'maroon']

# Calculate cumulative
cumulative_emissions = [0]
for i in range(1, len(values_emissions)):
    if i < len(values_emissions) - 1:
        cumulative_emissions.append(cumulative_emissions[-1] + values_emissions[i])
    else:
        cumulative_emissions.append(cumulative_emissions[-1])

# Create bars
for i in range(len(categories_emissions)):
    if i == 0:
        ax2.bar(i, 0, color=colors_emissions[i], edgecolor='black', linewidth=1.5, width=0.6)
    elif i == len(categories_emissions) - 1:
        ax2.bar(i, cumulative_emissions[i], color=colors_emissions[i], edgecolor='black', linewidth=1.5, width=0.6)
    else:
        if values_emissions[i] > 0:
            ax2.bar(i, values_emissions[i], bottom=cumulative_emissions[i-1], 
                   color=colors_emissions[i], edgecolor='black', linewidth=1.5, width=0.6)
        else:
            ax2.bar(i, abs(values_emissions[i]), bottom=cumulative_emissions[i], 
                   color=colors_emissions[i], edgecolor='black', linewidth=1.5, width=0.6)

# Add connecting lines
for i in range(len(categories_emissions) - 1):
    if i < len(categories_emissions) - 2:
        ax2.plot([i + 0.3, i + 0.7], [cumulative_emissions[i], cumulative_emissions[i]], 
                'k--', linewidth=1, alpha=0.5)

# Add value labels
for i in range(1, len(categories_emissions)):
    if i < len(categories_emissions) - 1:
        y_pos = cumulative_emissions[i-1] + values_emissions[i]/2 if values_emissions[i] > 0 else cumulative_emissions[i] - abs(values_emissions[i])/2
        label = f"+{values_emissions[i]:.1f}" if values_emissions[i] > 0 else f"{values_emissions[i]:.1f}"
        ax2.text(i, y_pos, label, ha='center', va='center', fontweight='bold', fontsize=12)
    else:
        ax2.text(i, cumulative_emissions[i]/2, f"{cumulative_emissions[i]:.1f}", 
                ha='center', va='center', fontweight='bold', fontsize=13, color='white')

ax2.set_xticks(range(len(categories_emissions)))
ax2.set_xticklabels(categories_emissions, fontsize=10, fontweight='bold')
ax2.set_ylabel('Emissions (Mt CO2e/year)', fontsize=13, fontweight='bold')
ax2.set_title('Emissions Impact: Technology Offset by Pipeline', fontsize=14, fontweight='bold', pad=20)
ax2.axhline(0, color='black', linewidth=0.8)
ax2.grid(axis='y', alpha=0.3)
ax2.set_ylim(-2, 16)

# Add breakdown annotation
ax2.text(3.5, cumulative_emissions[3] + 0.5, 
         'Actual:\nLine 3: 2.7 Mt\nTMX: 2.0 Mt', 
         fontsize=9, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7),
         ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('pipeline_waterfall_charts_detailed.png', dpi=300, bbox_inches='tight')
print("✓ Saved: pipeline_waterfall_charts_detailed.png")
plt.show()
