import numpy as np
import pandas as pd
from scipy import stats
from arch import arch_model

class Garch:

    """
    Parametric bootstrapping with GARCH models.
    """
    
    def __init__(self, data, vol='Garch', p=1, q=1, dist='normal', update_freq=0, disp='off', horizon=1, start=None, reindex=False):
        
        """
        Initializing the GARCH model.

        Parameters:
            data: pandas.Series, np.array, DataFrame
                Time series data
            vol: str, optional
                Name of the volatility model. Default is 'Garch'. Others are 'ARCH', 'EGARCH', 'FIGARCH', 'APARCH', and 'HARCH'
            p: int, optional
                Lag order of the symmetric innovation. Default is 1.
            q: int
                Lag order of the lagged conditional variance. Default is 1.
            dist: str, optional
                Name of the distribution assumption for the errors. Options are:
                    * Normal: 'normal', 'gaussian' (default)
                    * Students's t: 't', 'studentst'
                    * Skewed Student's t: 'skewstudent', 'skewt'
                    * Generalized Error Distribution: 'ged', 'generalized error"
            update_freq: int, optional
                Frequency of iteration updates to generate model output. Default is 0 (no updating).
            disp: str or bool optional
                Display option for the model estimation. Either 'final' to print optimization result or 'off' (default) to display
                nothing. If using a boolean, False is "off" and True is "final"
            horizon: int, optional
                Forecast horizon. Default is 1.
            start: int or str or datetime or Timestamp, optional
                Starting index or date for forecasting. Default is None.
            reindex: bool, optional
                Reindex the forecasted series to match the original data. Default is False.
        """

        if vol not in ['Garch', 'ARCH', 'EGARCH', 'FIGARCH', 'APARCH', 'HARCH']:
            raise ValueError("Invalid value for 'vol' parameter. Allowed values are 'Garch', 'ARCH', 'EGARCH', 'FIGARCH', 'APARCH', and 'HARCH'.")

        if not isinstance(p, int) or p < 1:
            raise ValueError("The 'p' parameter must be an integer greater than or equal to 1.")
        
        if not isinstance(q, int) or q < 1:
            raise ValueError("The 'q' parameter must be an integer greater than or equal to 1.")

        allowed_dists = ['normal', 'gaussian', 't', 'studentst', 'skewstudent', 'skewt', 'ged', 'generalized error']
        if dist not in allowed_dists:
            raise ValueError("Invalid value for 'dist' parameter. Allowed values are: " + ", ".join(allowed_dists) + ".")

        if not isinstance(update_freq, int) or update_freq < 0:
            raise ValueError("The 'update_freq' parameter must be a non-negative integer.")

        if isinstance(disp, bool):
            if disp:
                disp = 'final'
            else:
                disp = 'off'
        elif not isinstance(disp, str):
            raise ValueError("The 'disp' parameter must be a string or a boolean.")
            
        if not isinstance(horizon, int) or horizon < 1:
            raise ValueError("The 'horizon' parameter must be an integer greater than or equal to 1.")

        self.vol = vol
        self.p = p
        self.q = q
        self.dist = dist
        self.horizon = horizon

        try:
            self.model = arch_model(data, vol=self.vol, p=self.p, q=self.q, dist=self.dist)
            self.result = self.model.fit(disp=disp)
            self.prediction = self.result.forecast(horizon=self.horizon, start=start, reindex=reindex)
        except Exception as e:
            raise ValueError("An error occurred while fitting the GARCH model. Error message: " + str(e))

    @property
    def summary(self):
        """
        Get the summary of the fitted model.

        Returns:
            arch.univariate.base.ARCHModelResultSummary: Summary of the fitted model.
        """
        if self.result is None:
            raise ValueError("No model result available. Please fit the GARCH model first.")

        return self.result.summary()

    @property
    def conditional_volatility(self):
        """
        Get the conditional volatility of the fitted model.

        Returns:
            pandas.Series: Conditional volatility series.
        """
        if self.result is None:
            raise ValueError("No model result available. Please fit the GARCH model first.")

        return self.result.conditional_volatility

    @property
    def standardised_residuals(self):
        """
        Get the standardized residuals of the fitted model.

        Returns:
            pandas.Series: Standardized residuals series.
        """
        if self.result is None:
            raise ValueError("No model result available. Please fit the GARCH model first.")

        return self.result.std_resid

    @property
    def forecast_mean(self):
        """
        Get the forecasted conditional mean of the model.

        Returns:
            pandas.DataFrame: Forecasted conditional mean series.
        """
        if self.prediction is None:
            raise ValueError("No forecast available. Please fit the GARCH model and generate forecast first.")

        return self.prediction.mean

    @property
    def forecast_variance(self):
        """
        Get the forecasted conditional variance of the model.

        Returns:
            pandas.DataFrame: Forecasted conditional variance series.
        """
        if self.prediction is None:
            raise ValueError("No forecast available. Please fit the GARCH model and generate forecast first.")

        return self.prediction.variance

    @property
    def forecast_residual_variance(self):
        """
        Get the forecasted conditional variance of the residuals of the model.

        Returns:
            pandas.DataFrame: Forecasted conditional residual variance series.
        """
        if self.prediction is None:
            raise ValueError("No forecast available. Please fit the GARCH model and generate forecast first.")

        return self.prediction.residual_variance

#-------------------------------------------------------------------------------------------
 
    
    def bootstrap(self, num_iterations=1000):
        """
        Perform parametric bootstrapping to estimate the forecast distribution.

        Parameters:
            num_iterations: int, optional
                Number of bootstrap iterations. Default is 1000.

        Returns:
            bool: True if the bootstrap is successful.
        """
        if num_iterations < 1 or not isinstance(num_iterations, int):
            raise ValueError("The 'num_iterations' parameter must be an integer greater than or equal to 1.")

        if self.standardised_residuals is None:
            raise ValueError("No standardised residuals available. Please fit the GARCH model first.")

        std_resid = self.standardised_residuals

        bootstrap_samples = []

        try:
            for _ in range(num_iterations):
                bootstrap_residuals = std_resid.sample(n=len(std_resid), replace=True)
                bootstrap_model = arch_model(
                    bootstrap_residuals,
                    vol=self.vol,
                    p=self.p,
                    q=self.q,
                    dist=self.dist
                )
                bootstrap_result = bootstrap_model.fit(disp='off')
                forecasted_mean = bootstrap_result.forecast(horizon=self.horizon, start=None, reindex=False).mean
                forecasted_volatility = bootstrap_result.forecast(horizon=self.horizon, start=None, reindex=False).variance
                bootstrap_samples.append((forecasted_mean, forecasted_volatility))

            self._bootstrap_samples = bootstrap_samples
            self.bootstrap_result = bootstrap_result

            return True
        except Exception as e:
            raise ValueError("An error occurred during bootstrapping. Error message: " + str(e))

    @property
    def bootstrap_summary(self):
        """
        Get the summary of the bootstrapped model.

        Returns:
            arch.univariate.base.ARCHModelResultSummary: Summary of the bootstrapped model.
        """
        if self.bootstrap_result is None:
            raise ValueError("No bootstrap result available. Please run the 'bootstrap' method first.")

        return self.bootstrap_result.summary()

    @property
    def bootstrap_samples(self):
        """
        Get the forecasted mean and volatility list from the bootstrapped model.

        Returns:
            list: List of tuples containing forecasted mean and volatility for each bootstrap iteration.
        """
        if self._bootstrap_samples is None:
            raise ValueError("No bootstrap samples available. Please run the 'bootstrap' method to generate bootstrap samples.")

        return self._bootstrap_samples

#-------------------------------------------------------------------------------------------

    def estimate_risk(self, confidence_level=0.95, q='empirical'):
        """
        Estimate risk measures: volatility and Value-at-Risk (VaR) using the bootstrapped model.

        Parameters:
            confidence_level: float, optional
                Confidence level for calculating VaR and volatility. Default is 0.95.
            q: str, optional
                Quantile calculation method. 'empirical' for empirical quantile, 'parametric' for parametric quantile.
                Default is 'empirical'.

        Returns:
            dict: Dictionary containing risk estimates including mean volatility, volatility confidence interval,
                  mean VaR, and VaR confidence interval.
        """
        if not (0 < confidence_level < 1):
            raise ValueError("The 'confidence_level' parameter must be a float between 0 and 1 (exclusive).")

        if q not in ['empirical', 'parametric']:
            raise ValueError("Invalid value for 'q' parameter. Allowed values are 'empirical' and 'parametric'.")

        if self.bootstrap_samples is None:
            raise ValueError("No bootstrap samples available. Please run the 'bootstrap' method to generate bootstrap samples.")

        volatility_estimates = np.sqrt([vol for _, vol in self.bootstrap_samples])
        volatility_ci = np.percentile(volatility_estimates, [(1 - confidence_level) / 2 * 100, (1 + confidence_level) / 2 * 100])

        var_estimates = []

        for forecasted_mean, forecasted_volatility in self.bootstrap_samples:
            if q == 'empirical':
                if self.result.std_resid is None:
                    raise ValueError("No standardized residuals available. Please fit the GARCH model first.")
                quantile = self.result.std_resid.quantile(1 - confidence_level)
            elif q == 'parametric':
                quantile = stats.norm.ppf(1 - confidence_level, loc=forecasted_mean, scale=np.sqrt(forecasted_volatility))
            var_estimate = forecasted_mean + np.sqrt(forecasted_volatility) * quantile
            var_estimates.append(var_estimate)

        mean_var = np.mean(var_estimates)
        var_ci = np.percentile(var_estimates, [(1 - confidence_level) / 2 * 100, (1 + confidence_level) / 2 * 100])

        return {
            'Mean Volatility': np.mean(volatility_estimates),
            'Volatility Confidence Interval': volatility_ci,
            'Mean VaR': mean_var,
            'VaR Confidence Interval': var_ci
        }
