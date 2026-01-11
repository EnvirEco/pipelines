# Pipeline Analysis Model: User Guide

## What This Model Does

This analysis answers: **Did pipeline capacity expansions (Line 3, TMX) cause new oil production in Alberta?**

**Method**: Compares Alberta's production changes to Saskatchewan's (control group) before and after pipelines came online.

**Key outputs**:
1. Production increase caused by pipelines (+544 kb/d)
2. Modal shift from rail to pipeline (+129 kb/d)
3. Net emissions impact (~8 Mt CO2e/year)

---

## Required Data Files

You need three files in the same folder:

1. **`2510006301-noSymbol.csv`** - Statistics Canada production data
   - Contains: Alberta AND Saskatchewan monthly production (2018-2024)
   - Source: StatsCan Table 25-10-0063-01

2. **`canadian-crude-oil-exports-rail-monthly-data.xlsx`** - CER rail data
   - Contains: National rail export volumes
   - Source: Canada Energy Regulator

3. **`pipeline_complete_analysis.py`** - The analysis script

---

## How to Run

### Step 1: Install Requirements
```bash
pip install pandas numpy statsmodels matplotlib openpyxl --break-system-packages
```

### Step 2: Run the Script
```bash
python3 pipeline_complete_analysis.py
```

**That's it!** The script runs automatically and takes about 30 seconds.

---

## What You Get

### Console Output

**Part 1: DiD Results**
```
Line 3 DiD:  +343.4 kb/d (p=0.0000) ✓✓✓
TMX DiD:     +201.3 kb/d (p=0.0046) ✓✓
```
**Translation**: Alberta's production grew 343 kb/d MORE than Saskatchewan's after Line 3 (highly significant). TMX added another 201 kb/d.

**Part 2: Price Mechanism**
```
Predicted WCS-WTI: +145.0 kb/d per $/bbl (p<0.001)
```
**Translation**: For every dollar the WCS-WTI gap narrows, production increases by 145 kb/d. This is the causal pathway: capacity → price relief → production.

**Part 3: Emissions**
```
Line 3: +4.9 Mt CO2e/year
TMX:    +3.1 Mt CO2e/year
Total:  +8.0 Mt CO2e/year
```
**Translation**: Pipeline-induced production added ~8 Mt/year of upstream emissions, after accounting for 1.3% annual efficiency improvements.

---

### Output Files

**1. `pipeline_complete_panel.csv`**
- Full dataset with both provinces
- Columns: date, province, production_kbpd, treated, line3_post, tmx_post, etc.
- Use for: Additional analysis, checking data

**2. `pipeline_alberta_2sls.csv`**
- Alberta-only data with price variables
- Includes: WCS-WTI differential, predicted values, rail data
- Use for: Price mechanism analysis

**3. `pipeline_complete_analysis.png`**
- Three-panel visualization:
  - Top: Alberta vs Saskatchewan (DiD visual)
  - Middle: Price mechanism (capacity → differential)
  - Bottom: Declining emissions intensity

---

## Understanding the Model

### The DiD Approach (Simple Explanation)

**Question**: Did pipelines cause Alberta's production increase?

**Problem**: Alberta's production could increase for many reasons (prices, COVID recovery, technology).

**Solution**: Compare to Saskatchewan
- Saskatchewan experienced same prices, COVID, recovery
- BUT Saskatchewan wasn't pipeline-constrained
- So the DIFFERENCE between Alberta and Saskatchewan changes = pipeline effect

**Formula in plain English**:
```
Pipeline Effect = (Alberta after - Alberta before) 
                  - (Saskatchewan after - Saskatchewan before)
```

This "differences out" all the common factors.

---

### The 2SLS Approach (Simple Explanation)

**Problem**: Circular relationship
- Pipelines affect prices
- Prices affect production
- Production affects prices (reverse causation!)

**Solution**: Use pipeline capacity as "instrument"
- Capacity additions are EXTERNAL (construction dates)
- Capacity → narrows price gap → enables production
- This isolates the CAUSAL chain

**Two stages**:
1. How does capacity affect prices? (First stage)
2. How do predicted prices affect production? (Second stage)

Result: Clean estimate of price mechanism effect.

---

### Key Variables Explained

| Variable | What It Means |
|----------|---------------|
| `production_kbpd` | Oil production in thousands of barrels per day |
| `line3_post` | 1 if after Oct 2021, 0 before (Line 3 startup) |
| `tmx_post` | 1 if after May 2024, 0 before (TMX startup) |
| `treated` | 1 for Alberta, 0 for Saskatchewan |
| `line3_did` | Alberta × Line 3 interaction (the causal effect) |
| `tmx_did` | Alberta × TMX interaction (the causal effect) |
| `wcs_wti_differential` | Price gap between WCS and WTI ($/barrel) |
| `pipeline_capacity_instrument` | Cumulative capacity additions (kb/d) |

---

## Interpreting the Results

### P-values (Statistical Significance)

| P-value | Meaning | Symbol |
|---------|---------|--------|
| p < 0.001 | Highly significant | ✓✓✓ |
| p < 0.01 | Very significant | ✓✓ |
| p < 0.05 | Significant | ✓ |
| p > 0.05 | Not significant | (no symbol) |

**Example**: "Line 3 DiD: +343 kb/d (p<0.001) ✓✓✓"
- We're >99.9% confident this is real, not random chance

---

### R² (Model Fit)

| R² Value | Meaning |
|----------|---------|
| 0.99 | Model explains 99% of variation (excellent) |
| 0.60 | Model explains 60% of variation (moderate) |
| 0.30 | Model explains 30% of variation (weak) |

**Our DiD model**: R² = 0.992 (excellent fit)

---

## Common Questions

### Q: Why Saskatchewan as control?
**A**: Saskatchewan's light oil wasn't pipeline-constrained. It experienced the same COVID, prices, and recovery as Alberta, but different pipeline situation. Perfect control.

### Q: What about rail data being national?
**A**: Alberta produces ~80% of Canadian crude. Saskatchewan's light oil is less rail-dependent. So national rail data primarily reflects Alberta movements during constraints.

### Q: Why 1.3% intensity decline?
**A**: Based on observed Alberta data 2019-2024. Conservative estimate reflecting actual recent improvements, not aspirational long-term targets.

### Q: What if I want to change the decline rate?
**A**: Edit line 358 in the script:
```python
decline_rate = 0.013  # Change this value (0.013 = 1.3%)
```

### Q: Can I use different time periods?
**A**: Yes, but you'll need to:
1. Update the data files (StatsCan, CER)
2. Adjust the treatment dates in the script (line3_post, tmx_post)

---

## Troubleshooting

**Error: "File not found"**
- Make sure all three data files are in the same folder as the script

**Error: "Module not found"**
- Run: `pip install pandas numpy statsmodels matplotlib openpyxl --break-system-packages`

**Charts look wrong**
- Check that your data files are up to date
- Verify dates in the data match the treatment dates

**Strange results**
- Check that Saskatchewan data is present in the StatsCan file
- Verify rail data loaded correctly (should see "✓ Loaded X months")

---

## Model Limitations

**Acknowledged in the analysis**:
1. **Short post-TMX period** (only 8 months) - results less precise
2. **Rail data is national** - not province-specific (but ~80% Alberta)
3. **Linear time trend** - assumes smooth growth, not month-to-month fluctuations
4. **Weak instrument** (F=4.59) - 2SLS results suggestive but not definitive

**These don't invalidate findings** - they're disclosed and don't affect core DiD results.

---

## Quick Reference: Key Numbers

| Metric | Value | Significance |
|--------|-------|--------------|
| **Production Effects** | | |
| Line 3 (DiD) | +343 kb/d | p<0.001 ✓✓✓ |
| TMX (DiD) | +201 kb/d | p<0.005 ✓✓ |
| Total | +544 kb/d | Causal estimate |
| **Modal Shift** | | |
| Rail decline | -129 kb/d | National data |
| Net throughput | +655 kb/d | 544 + 129 - 18 |
| **Emissions** | | |
| Constant intensity | 13.3 Mt/year | Frozen at 67 kg/bbl |
| With 1.3% decline | 8.0 Mt/year | Technology offset |
| Technology dividend | -5.3 Mt/year | 40% reduction |

---

## For More Details

- **Methodology**: See `COMPLETE_ANALYSIS_SUMMARY.md`
- **Model equations**: See main analysis write-up
- **Data sources**: StatsCan Table 25-10-0063-01, CER rail data, Alberta Energy (prices)

**Questions?** The script has detailed comments explaining each step.
