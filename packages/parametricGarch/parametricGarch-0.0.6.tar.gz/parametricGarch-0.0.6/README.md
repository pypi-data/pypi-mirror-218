# ParametricGarch
A Python library that uses parametric bootstrapping via the GARCH model to estimate volatility and Value-at-Risk (VaR) for financial assets.

### Installation
You can install parametricGarch using pip:
```
pip install parametricGarch
```

## Dependencies
The package dependencies are:
- arch
- numpy
- pandas
- scipy

## Usage

To get started with parametricGarch, import the necessary modules and create an instance of the `Garch` class:

```python
from parametricGarch import Garch

# Create an instance of the Garch class to fit and forecast the model
model = Garch(data, vol='Garch', p=1, q=1, dist='normal', update_freq=0, disp='off', horizon=1, start=None, reindex=False)

# View the summary of the fitted model
model.summary

# View the conditional volatility of the fitted model
model.conditional_volatility

# View the standardised residuals of the fitted model
model.standardised_residuals

# View the forecasted conditional mean of the fitted model
model.forecast_mean

# View the forecasted conditional variance of the fitted model
model.forecast_variance

# View the forecasted conditional variance of the residuals of the fitted model
model.forecast_residual_variance

# Perform parametric bootstrapping
model.bootstrap()

# View the summary of the bootstrapped model
model.bootstrap_summary

# View the forecasted mean and volatility list from the bootstrapped model
model.bootstrap_samples

# Estimate volatility and VaR
risk_estimates = model.estimate_risk()
```

## Documentation
Please refer to the [documentation](https://parametricgarch.readthedocs.io/en/latest/index.html#) for detailed information on the available parameters, methods, and properties of the Garch class.

## Examples

Please refer to [```example.ipynb```](https://github.com/chideraani/ParametricGarch/blob/main/example.ipynb) for a detailed example to help you get started quickly with parametricGarch. The examples cover various use cases and demonstrate the library's capabilities.

## License
parametricGarch is licensed under the GNU General Public License v3.0 License. See the [LICENSE](https://github.com/chideraani/ParametricGarch/blob/main/LICENSE) file for more details.