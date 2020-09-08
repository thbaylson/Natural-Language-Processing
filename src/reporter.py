import pandas as pd
import math

import numpy as np

class Reporter:
    """ Do Stuff """
    def __init__(self):
        self.log_df = pd.read_csv("log.csv")
        #self.log_df.set_index("id", inplace= True)

    def log_tail(self, n=5):
        return self.log_df.tail(n)

    def not_null(self, n=5):
        return self.log_df.dropna().tail(n)

    def employee_policy_count(self, n=5):
        log_df_by_count = self.log_df.groupby('acting_user').count()
        log_df_by_count.reset_index(inplace= True)
        action_count_df = log_df_by_count[['acting_user', 'action']]
        action_count_df.set_index("acting_user", inplace= True)
        return action_count_df.tail(n)

    def col_errors(self, n=5):
        null_columns = self.log_df.columns[self.log_df.isnull().any()]
        return self.log_df[null_columns].isnull().sum().tail(n)

    def find_errors(self, n=5):
        return self.log_df[self.log_df.isnull().any(axis=1)].tail(n)
