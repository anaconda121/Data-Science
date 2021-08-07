def split_data(df, X_col, y_col, train_percent, valid_percent):
    X = df[X_col]
    y = df[y_col]
    
    y_label = y.to_numpy()
    X_train, X_test_valid, y_train, y_test_valid = train_test_split(X, y, random_state = 0, test_size = (1 - train_percent), stratify = y_label)

    y_test_valid_label = y_test_valid.to_numpy()
    X_valid, X_test, y_valid, y_test = train_test_split(X_test_valid, y_test_valid, random_state = 0, test_size = (1 - valid_percent), stratify = y_test_valid_label)
    
    return X_train, y_train, X_valid, y_valid, X_test, y_test

def split_data_multiple_df(df1, df2, df1_X_col, df1_y_col, df2_X_col, df2_y_col, df1_train_percent, df1_valid_percent, df2_train_percent, df2_valid_percent):
    X = df1[df1_X_col]
    y = df1[df1_y_col]
    
    X_train, y_train, X_valid, y_valid, X_test, y_test = split_data(df1, df1_X_col, df1_y_col, df1_train_percent, df1_valid_percent)
    X_train_2, y_train_2, X_valid_2, y_valid_2, X_test_2, y_test_2 = split_data(df2, df2_X_col, df2_y_col, df2_train_percent, df2_valid_percent)
    
    X_train = X_train.append(X_train_2)
    y_train = y_train.append(y_train_2)
    
    X_test = X_test.append(X_test_2)
    y_test = y_test.append(y_test_2)
    
    X_valid = X_valid.append(X_valid_2)
    y_valid = y_valid.append(y_valid_2)
    
    return X_train, y_train, X_valid, y_valid, X_test, y_test
