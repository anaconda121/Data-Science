def SMOTE(X_train, y_train, X_test, y_test, k_train, k_test):
    # balancing classes in train set
    oversample = SMOTE(k_neighbors = k_train)
    X_train_new, y_train_new = oversample.fit_resample(X_train, y_train)
    counter = Counter(y_train_new)
    print("Train Data after SMOTE")
    
    for k,v in counter.items():
        print('Class=%d, n=%d' % (k, v))
    
    # balancing classes in test_set
    oversample2 = SMOTE(k_neighbors = k_test)
    X_test_new, y_test_new = oversample2.fit_resample(X_test, y_test)
    counter2 = Counter(y_test_new)
    print("Test Data after SMOTE")
    
    for k,v in counter2.items():
        print('Class=%d, n=%d' % (k, v))
    
    # converting back to DataFrame and Series, respectively
    X_train_new = pd.DataFrame(X_train)
    y_train_new = pd.Series(y_train)
    X_test_new = pd.DataFrame(X_test)
    y_test_new = pd.Series(y_test)
    
    return X_train_new, y_train_new, X_test_new, y_test_new
