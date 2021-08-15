def logisitic_regression(X_train, y_train, X_test, y_test, c, want_report, want_conf_mat, save_model, name):
    # fitting model
    lr = LogisticRegression(penalty = 'l1', solver = 'liblinear', C = c, random_state = 0, class_weight = 'balanced')
    lr.fit(X_train, y_train)
    
    # predictions
    y_pred = lr.predict(X_test)
    y_prob = lr.predict_proba(X_test)

    # collecting results
    acc = metrics.accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob, average = 'weighted') # , multi_class = 'ovr' if mutliclasss
    
    if (save_model == True):
        pickle.dump(lr, open("example_directory" + name, 'wb'))
    
    if (want_report == True):
        target_names = ['NO', 'NTR', 'YES']
        results_lgr = classification_report(y_test, y_pred, target_names = target_names, output_dict = True)
        results_lgr = pd.DataFrame(results_lgr).transpose()
        
        if (want_conf_mat == True):
            return lr, acc, auc, c, results_lgr, confusion_matrix(y_test, y_pred)
    
        return lr, acc, auc, c, results_lgr
    
    if (want_conf_mat == True):
        return lr, acc, auc, c, confusion_matrix(y_test, y_pred)
        
    return lr, acc, auc, c

def training_loop():
    acc_list = []
    auc_list = []
    c_list = []
    
    # tuning for optimal lambda value
    for c in [0.01, 0.1, 1, 10, 100]:
        lr, acc, auc, c = logisitic_regression(X_train, y_train, X_test, y_test, c, False, False, False, "")
        acc_list.append(acc)
        auc_list.append(auc)
        c_list.append(c)
            
    # gathering model stats
    acc_df = pd.DataFrame(acc_list, columns = ['acc'])
    auc_df = pd.DataFrame(auc_list, columns = ['auc'])
    c_df = pd.DataFrame(c_list, columns = ['c_value'])

    assert len(acc_df) == len(auc_df) == len(c_df)

    iter_df = pd.concat([c_df, acc_df, auc_df], axis = 1)
    iter_df['corr_thres'] = [corr] * len(iter_df)
    iter_df['fold_number'] = [(counter + 1)] * len(iter_df)
    df_list.append(iter_df)
