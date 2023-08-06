from sklearn.base import BaseEstimator, TransformerMixin
from typing_extensions import Self, Any
import pandas as pd
import pickle

from ..utility.tele_logger import logger
from ..utility.resources import *
from .datapreparation_utils import ModelPreprocess

class PreprocessingClass(BaseEstimator, TransformerMixin):

    def __init__(self,
                 target_col : str,
                 date_col : str,
                 usecase: str = "teleconsulto",
                 model: str = "prophet"
                 ):
        """Pass all the parameters that can be set as explicit keyword
        arguments.
        
        Parameters
        ----------
        target_col: str
            Column name identifying column from which to generate target aggregate
        date_col: str
            Column name identifying the datetime column to index on
        usecase: str
            Parameter identifying usecase into account
        model: str
            Parameter identifying model to use
            
        """

        self.usecase = usecase
        self.model = model

        if self.usecase == "teleconsulto":
            self.preprocessing = ModelPreprocess(target_col=target_col, date_col=date_col)
        elif self.usecase == "televisita":
            pass
        elif self.usecase == "teleassistenza":
            pass
        elif self.usecase == "telemonitoraggio":
            pass
        return
    
    @log_exception(logger)
    def fit(self,
            X: pd.DataFrame,
            time_granularity: str,
            y: Any = None) -> Self:
        """Learn parameters useful for transforming data.

        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame.
        time_granularity: str 
            specifies temporal granularity
        y : None
            Ignored (only for compatibility).
        """

        if self.usecase == "teleconsulto":
            if self.model == "prophet":
                self.time_granularity = time_granularity
                pass
        return self


    def transform(self,
                X: pd.DataFrame) -> pd.DataFrame:
        """Preparing Data to feed models"

        Must be called only after calling fit method.
        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame
        time_granularity: str 
            specifies temporal granularity

        Returns
        -------
        pd.DataFrame 
            DataFrame identifying the timeseries 
        """

        if self.usecase == "teleconsulto":
            if self.model == "prophet":
                X = self.preprocessing.prophet(X, self.time_granularity)
            else:
                pass
        elif self.usecase == "televisita":
            pass
        elif self.usecase == "teleassistenza":
            pass
        elif self.usecase == "telemonitoraggio":
            pass
        
        return X
    

    def save(self,
             path: str) -> None:
        """Store instance to file.
        Parameters
        ----------
        path : str
            Path to the file where the object must be stored.
        """

        with open(path, 'wb') as f:
            pickle.dump(self, f)
        
        return

    @classmethod
    def load(cls,
             path: str) -> Self:
        """Load instance from file.
        Parameters
        ----------
        path : str
            Path to the file where the object must be stored.
        """
        with open(path, 'rb') as f:
            return pickle.load(f)

