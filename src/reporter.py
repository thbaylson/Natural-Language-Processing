import pandas as pd
import math
import numpy as np
from debuglog import DebugLog as debug

class Reporter:

    debuglog = debug()
    debuglog.set_calling_class = "Reporter"
    debuglog.set_debugging(True)

    def __init__(self):
        """ 
        Reads the contents of log.json into a Pandas DataFrame. Orient= table and 
        convert_date= False keep the file in the correct format. The provided methods 
        can be used to run analytics on the data. All methods return a Pandas DataFrame.
        """
        self.log_df = pd.read_json("log.json", orient= "table", convert_dates= False)
        
        # Here we replace the empty strings JSON creates with NaN values for analytics
        self.log_df.replace(r'^$', np.nan, regex=True, inplace = True)

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

    def find_suspicious_activity(self, n=5):
        """
        Searches through the log file to identify suspicious activity. This kind of activity may
        take the form of too many policies created too quickly or a large amount of policies
        focused on a single resource.
        """
        ## Too many back-to-back rules from one person
        sus_df = pd.DataFrame(columns= self.log_df.columns)
        sus_df["suspicion_type"] = ""

        sus_thresh_freq = 4
        sus_thresh_fast = 5
        current_user = ""
        current_date = ""
        current_hour_min = ""
        current_seconds = 0

        repeat_access = 0
        fast_repeat_access = 0
        for i in range(1, self.log_df.shape[0]+1):
            # Record user
            prev_user = current_user
            current_user = str(self.log_df.loc[self.log_df.shape[0]-i]['acting_user']).lower()
            
            # Record mm/dd/yy
            prev_date = current_date
            current_date = self.log_df.loc[self.log_df.shape[0]-i]['date']
            
            # Record hh:mm
            prev_hour_min = current_hour_min
            current_hour_min = self.log_df.loc[self.log_df.shape[0]-i]['time'][:5]
            
            # Record ss
            prev_seconds = current_seconds
            current_seconds = int(self.log_df.loc[self.log_df.shape[0]-i]['time'][6:])
            
            if(current_user != 'nan'):
                if(current_user == prev_user):
                    repeat_access += 1
                    if(repeat_access == sus_thresh_freq):
                        new_series = self.log_df.loc[self.log_df.shape[0]-i]
                        new_series.loc["suspicion_type"] = 'too_frequent'
                        sus_df = sus_df.append(new_series, ignore_index=True)
                    
                    if(current_date == prev_date and current_hour_min == prev_hour_min):   
                        # See if the last rule was within a second of the current rule
                        if(current_seconds <= (prev_seconds + 1)):
                            fast_repeat_access += 1
                            if(fast_repeat_access == sus_thresh_fast):
                                new_series = self.log_df.loc[self.log_df.shape[0]-i]
                                new_series.loc["suspicion_type"] = 'too_fast'
                                sus_df = sus_df.append(new_series, ignore_index=True)
                        else:
                            fast_repeat_access = 0
                else:
                    repeat_access = 0
                    fast_repeat_access = 0

        sus_df.sort_values(by= 'date', inplace= True)
        return sus_df.tail(n)
        
    
    # Unsure where to put this. Depends on spacy to create an svg graph
    """
    def spacy_graph(self):
        tokens = nlp("Bob can edit Alice's documents")
        svg = displacy.render(tokens, style="dep", jupyter=False)
        file_name = '-'.join([word.text for word in tokens if not word.is_punct]) + ".svg"
        output_path = Path(file_name)
        output_path.open("w", encoding="utf-8").write(svg)
    """
