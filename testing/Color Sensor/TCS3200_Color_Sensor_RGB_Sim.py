"""
Simulate Color Sensor RGBC Data to do data analysis.

-Save PRF and non-PRF data to CSV.
-Create box plots

Tests:

Q1: Increase precision of non-PRF by increasing fixed number of cycles?

Q2: Decrease speed of PRF while maintaining precision by decreasing fixed time to wait?

Q3: When switching to manual control of scaled output frequency, will 100% match previous setup?

Q4: How does precision change with 20% output? 2%? 100% is supposed to be the least accurate. Run same tests as Q1 and Q2.


Q1, data to collect:
- Number of cycles for RGBC, fixed. Cycles: 10, 100, 1000, 10k, 20k, 30k
- Elapsed time for RBC, same fixed cycles.
- Calculated: Frequency for RGBC: fixed cycles / elapsed time

Q2, data to collect:
- Number of cycles for RGB, not fixed.
- For fixed time to wait: 1s, 0.75s, 0.5s, 0.25s, 0.1s.
- External and Internal Time too, mark on box plot where fixed time is. Expected vs actual.
- Calculated: Frequency for RGBC:
   - num of cycles / external
   - num of cycles / internal
   - num of cycles / expected time to wait.

Plots:
Q1:
- RGBC are 4 columns, each column has elapsed time for each of the fixed number of cycles (if there is room)
   - Else, they all get their own figure.
- RGBC are 4 column, each color shows calculated frequency for each of the number of cycles.
*Note: Look for best case scenario to compare with PRF

Q2:
- RGBC are 4 columns, each column has external vs internal time with expected time shown as horizontal line.
   Each row is the fixed time to wait, so 5 rows. If no room, separate figure.
- RGBC are 4 columns, each column has calculated frequency for all 5 of the fixed times to wait.
* Note: Look for best case scenario to compare with non-PRF.

Q3: Repeat Q1 and Q2? Using 100% scaled output frequency. Or just aim for best case scenario.

Q4: Repeat Q1 and Q2 for different scaled outputs: 20% and 2%.


"""