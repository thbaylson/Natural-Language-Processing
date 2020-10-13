import pandas as pd
import math
import numpy as np
from debuglog import DebugLog as debug

class Reporter:
    """ Reads the contents of log.json into a Pandas DataFrame. The provided methods can be used to
    run analytics on the data. All methods return a Pandas DataFrame."""
    def __init__(self):
        self.log_df = pd.read_json("log.json", orient= "table")
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
    
    # Unsure where to put this. Depends on spacy to create an svg graph
    """
    def spacy_graph(self):
        tokens = nlp("Bob can edit Alice's documents")
        svg = displacy.render(tokens, style="dep", jupyter=False)
        file_name = '-'.join([word.text for word in tokens if not word.is_punct]) + ".svg"
        output_path = Path(file_name)
        output_path.open("w", encoding="utf-8").write(svg)
    """
