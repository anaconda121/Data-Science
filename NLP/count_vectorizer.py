def count_vectorizer(X_train, X_test, X_valid, token_pattern = None):
    # Initialize a CountVectorizer object: count_vectorizer
    count_vectorizer = CountVectorizer(stop_words = "english", analyzer = 'word', token_pattern = token_pattern)

    # Transform the training data using only the 'text' column values: count_train 
    count_train = count_vectorizer.fit_transform(X_train)
    count_test = count_vectorizer.transform(X_test)
    count_valid = count_vectorizer.transform(X_valid)

    # Create the CountVectorizer DataFrame: count_train
    count_train = pd.DataFrame(count_train.A, columns=count_vectorizer.get_feature_names())
    count_test = pd.DataFrame(count_test.A, columns=count_vectorizer.get_feature_names())
    count_valid = pd.DataFrame(count_valid.A, columns=count_vectorizer.get_feature_names())
    
    return count_train, count_test, count_valid
