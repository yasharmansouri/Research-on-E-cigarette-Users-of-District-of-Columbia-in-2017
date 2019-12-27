import pandas as pd


def full_clean(df):
    """for data cleaning, the function
    drops the unnecessary columns by keeping/reordering the required ones analysis
    drops null values based on the data_value and sample_size
    drops 2 consecutive years/cumulative data
    changes the the data type in the specified columns
    creates a column of count in case further analysis requires the average number of people"""

    cols_to_keep = ['year', 'locationabbr', 'locationdesc', 'topicdesc',
                    'measuredesc', 'age', 'gender', 'race', 'education',
                    'response', 'sample_size', 'data_value', 'data_value_std_err',
                    'low_confidence_limit', 'high_confidence_limit']
    df = df[cols_to_keep]

    df = df.dropna(subset=['data_value', 'sample_size'])

    year_idx_drop = df.query('(year == "2011-2012") | (year == "2012-2013") |\
                              (year == "2013-2014") | (year == "2014-2015") |\
                              (year == "2015-2016") | (year == "2016-2017") |\
                              (year == "2017-2018")').index

    df = df.drop(year_idx_drop)

    cols_to_float = ['sample_size', 'data_value', 'data_value_std_err',
                     'low_confidence_limit', 'high_confidence_limit']

    df[cols_to_float] = df[cols_to_float].astype(float)
    df[['year']] = df[['year']].astype(int)

    df['count'] = df.data_value * (df.sample_size / 100)

    return df