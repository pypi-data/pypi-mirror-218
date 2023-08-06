import pandas as pd
import numpy as np
from ..utility.tele_logger import logger
from ..utility.exceptions import InputTypeError
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.base import BaseEstimator, TransformerMixin
from typing_extensions import Self
from typing import Union, Dict, List

class PreprocessingData: 

    def generate_time_series(self,
                df: pd.DataFrame,
                datetime_index: str,
                target: str,
                time_granularity: str = "D",
                missing_data_strategy: Union[str,int] = None,
                normalize_data: bool = False,
                ) -> pd.DataFrame:
        """
        Sequential execution of transformations to obtain a DataFrame with a time series structure

        Parameters
        ----------
        df: pd.DataFrame
            raw dataframe from which generates timeseries
        datetime_index: str
            column name identifying the columns to index on
        target: str
            column name identifying column from which to generate target
        missing_data_strategy: str or int
            Identifies whether to impute missing values and if so using which strategy/value
            Allowed parameters: 
                if str:
                    "mean" : missing values are replaced with the mean of the known values in the dataset.
                    "median": missing values are replaced with the median of the known values in the dataset.
                    "zero": missing values are replaced with the 0.
                    "bfill": missing values are replaced with the next available value in the dataset.
                    "ffill": missing values are replaced with the most recent preceding value in the dataset.
                    "interpolate": missing values are estimated based on the time index.
                if int:
                    replace NaN with the specified integer
        normalize_data: bool
            Identifies whether to normalize the timeseries using the min/max scaler.
        time_granularity: str 
           specifies temporal granularity

        Returns:
            pd.DataFrame: DataFrame identifying the timeseries generated according to specified hierarchies and time span
        """

         # Verify that df is of type pd.DataFrame
        if not isinstance(df, pd.DataFrame):
            logger.info("Input 'df' must be of type pd.DataFrame", important=True)
            raise InputTypeError('datapreparation_utils.prophet')
        # Verify that datetime_index is a non-empty string and a column in df
        if  datetime_index not in df.columns:
            logger.info("Invalid value for 'datetime_index'. It must be a column in 'df'", important=True)
            raise InputTypeError('datapreparation_utils.prophet')
        # Verify that target is a non-empty string and a column in df
        if target not in df.columns:
            logger.info("Invalid value for 'target'. It must be a column in 'df'", important=True)
            raise InputTypeError('datapreparation_utils.prophet')
        
        # Raw dataset from which to generate the time serie
        self.df = df.copy()

        logger.info('Generating the timeseries target')

        df_ts = self.df.set_index(datetime_index).resample(time_granularity.upper()).size().reset_index()
        df_ts.columns = ["Timestamp", "Target"]
        df_ts.loc[df_ts.Target==0, "Target"] = np.nan

        if missing_data_strategy:
            fillna = ReplacerNA(missing_data_strategy)
            #fillna.fit(df_ts)
            df_ts = fillna.fit_transform(df_ts)

            if normalize_data:
                normalizer = Normalizer()
                df_ts = normalizer.fit_transform(df_ts)

        return df_ts

def code_to_name(cod: pd.Series, convers_dict: Dict) -> pd.Series:
    
    """
    The function generates a new column converting the code number into a meaningful string

    Parameters
    ----------
    cod: pd.Series
       The code number column
    convers_dict: dict
        The mapping dictionary from code to string

    Returns
    -------
        pd.Series
        Returns the modified column based on the mapping dictionary
    """
    if not isinstance(cod, pd.Series):
        logger.info("Input 'cod' must be of type pd.Series")
        raise InputTypeError('datapreparation_utils.cod_to_name')
    if not isinstance(convers_dict, dict):
        logger.info("Input 'convers_dict' must be of type dict")
        raise InputTypeError('datapreparation_utils.cod_to_name')
                  
    return cod.apply(lambda i: convers_dict[int(i)])


class Normalizer(TransformerMixin, BaseEstimator):

    """Normalization class for time series (between 0 and 1)
    """

    def __init__(self):
        pass

    def fit(self, X: pd.DataFrame) -> Self:

        """Compute value min and max useful to normalize data

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted normalizer
        """

        self.min = X.iloc[:,1].min()
        self.max = X.iloc[:,1].max()

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform normalization between 0 and 1

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """

        normalized = (X.iloc[:,1] - self.min) / (self.max - self.min)
        ris = pd.concat([X.iloc[:,0],normalized],axis=1)
        ris.columns = X.columns
        
        return ris
    
class ReplacerNA(TransformerMixin, BaseEstimator):

    def __init__(self, method: Union[str,int] = 0) -> Self:

        """class for handling of NA

        Parameters
        ----------
        method : str | int
            if str specify the method to replace NA value (mean,median,zero), if int specify the value to replace NA value

        Returns
        -------
        self : object
        """
        
        self.method = method

    def fit(self, X: pd.DataFrame) -> Self:

        """Compute value useful for replacing NA

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted replacer
        """
        
        if self.method == "mean":
            self.value = X.iloc[:,1].mean()
            self.method_for_df = None
        elif self.method == "median":
            self.value = X.iloc[:,1].median()
            self.method_for_df = None
        elif self.method == "zero":
            self.value = 0
            self.method_for_df = None
        elif self.method == "bfill":
            self.value = None
            self.method_for_df = "bfill"
        elif self.method == "ffill":
            self.value = None
            self.method_for_df = "ffill"
        elif self.method == "interpolate":
            self.value = None
            self.method_for_df = "interpolate"
        else:
            self.value = self.method
            self.method_for_df = None

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform replacement of missing values

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """
        if self.method_for_df == "interpolate":
            # Create a temporary DataFrame with a DatetimeIndex
            temp_df = pd.DataFrame({X.columns[1]: X.iloc[:, 1]})
            temp_df.index = pd.to_datetime(X.iloc[:, 0])

            # Perform time-based interpolation in the temporary DataFrame
            temp_df.iloc[:, 0] = temp_df.iloc[:, 0].interpolate(method='time')

            # Assign the interpolated values to the original column in the X DataFrame
            X.iloc[:, 1] = temp_df.iloc[:, 0].values
        else:
            X.fillna(self.value, method=self.method_for_df, inplace=True)
        return X
    
class Detrender(TransformerMixin, BaseEstimator):

    def __init__(self, period: int) -> Self:

        """Detrending time series

        Parameters
        ----------
        period : int
            specify period considered for compute additive decomposition

        Returns
        -------
        self : object
        """

        self.period = period


    def fit(self, X: pd.DataFrame) -> Self:

        """Compute additive decomposition useful to detrend time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted detrender
        """

        additive_decomp = seasonal_decompose(X.iloc[:,1], model="additive", period=self.period, extrapolate_trend="freq")
        self.trend = additive_decomp.trend

        return self

    def transform(self, X:pd.DataFrame) -> pd.DataFrame:

        """Perform detrending of time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """

        detrend_time_series = X.iloc[:,1] - self.trend
        ris = pd.concat([X.iloc[:,0],detrend_time_series],axis=1)
        ris.columns = X.columns

        return  ris
    
class Deseasoner(TransformerMixin, BaseEstimator):

    def __init__(self, period: int) -> Self:

        """Deseasonalises time series

        Parameters
        ----------
        period : int
            specify period considered for compute additive decomposition

        Returns
        -------
        self : object
        """

        self.period = period


    def fit(self, X: pd.DataFrame) -> Self:

        """Compute additive decomposition useful to deseasonalises time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted deseasoner
        """
        
        additive_decomp = seasonal_decompose(X.iloc[:,1], model="additive", period=self.period, extrapolate_trend="freq")
        self.seasonal = additive_decomp.seasonal

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform deseasonalises of time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """

        deseason_time_series = X.iloc[:,1] - self.seasonal
        ris = pd.concat([X.iloc[:,0],deseason_time_series],axis=1)
        ris.columns = X.columns

        return ris

class Differencer(TransformerMixin, BaseEstimator):

    def __init__(self, lag: int) -> Self:

        """Differencing time series
        
        Parameters
        ----------
        lag : int
            differencing time series lag

        Returns
        -------
        self : object
        """

        self.lag = lag

    def fit(self, X: pd.DataFrame) -> Self:

        """Compute value useful to compute differencing time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted normalizer
        """

        self.shape = X.shape[0]
        self.lag_time_series = X.iloc[:self.shape-self.lag,1]
        self.timestamp = X.iloc[self.lag:,0].reset_index(drop=True)

        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform differencing time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """

        time_series_lagged = X.iloc[self.lag:,1].reset_index(drop=True) - self.lag_time_series
        ris = pd.concat([self.timestamp,time_series_lagged], axis=1)
        ris.columns = X.columns
        
        return ris
     
