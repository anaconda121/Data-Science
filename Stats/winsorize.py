from scipy.stats.mstats import winsorize

def get_winsorized(df, col, percentile = 0.95):
  # winsorize will take all values above 95 percentile and normalize them to value of 95 percentile. Note that the 95 is arbitrary here.
  # technique for dealing with outliers
  winsorize(df[col], limits = [0, (1 - percentile), inplace = True)
