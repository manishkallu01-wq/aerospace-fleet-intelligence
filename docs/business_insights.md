# Business Insights

## What the analysis shows

The project starts with engine-cycle data and ends with a simple maintenance-priority view. The point is to show how the data could be organized and used by a data engineering team.

## 1.  The lower tail matters

The FD001 test set has a mean RUL of **75.52 cycles**, but the values range from **7 to 145 cycles**. Looking only at the average hides the engines that are much closer to the end of their simulated run.

For this dataset, the first engines to review are therefore the ones with the lowest RUL.

## 2.  The maintenance queue depends on the threshold

For this project, engines at or below 60 cycles are placed in the planning queue.

That gives:

- **39 of 100 engines** in the queue
- **25 of 100 engines** at or below 30 cycles
- **15 engines** between 61 and 90 cycles
- **46 engines** above 90 cycles

The thresholds are only used to organize this benchmark analysis. They are not aircraft maintenance limits.

## 3.  A useful output is more than a model score

A planner usually needs a list that can be sorted and reviewed. The project therefore carries RUL, risk band, and priority into the analytical layer instead of stopping at the raw sensor data.

## 4.  Benchmark labels are not live predictions

NASA provides the true RUL vector for the FD001 test set so that predictions can be evaluated. Those values would not be available to an operator before failure.

The current dashboard uses the labels because it is showing benchmark results. A production version would replace them with predictions from a trained model using data available at that point in time.

## 5.  Costs are deliberately left out

There is no dollar-savings number in this repository because the benchmark does not contain airline maintenance costs, labor rates, downtime costs, or real intervention decisions. Adding a savings figure without those inputs would just be a guess.

## What I would do next

If this moved beyond the portfolio stage, I would add a trained RUL model, prediction-time feature checks, model monitoring, and a maintenance-capacity rule. The same Silver/Gold structure could then support the model and the reporting layer.
