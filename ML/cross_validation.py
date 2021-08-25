def cross_validation_split(dataset, n_folds):
    # ensuring straftification across label
    # change based on class count
    yes = cross_validation[cross_validation["annotator_label"] == 2].reset_index(drop = True)
    no = cross_validation[cross_validation["annotator_label"] == 0].reset_index(drop = True)
    ntr = cross_validation[cross_validation["annotator_label"] == 1].reset_index(drop = True)
    
    yes_count = len(yes) // n_folds
    no_count = len(no) // n_folds
    ntr_count = len(ntr) // n_folds
    
    split = list()
    fold_size = len(cross_validation) // n_folds

    # shuffling data to avoid having to generate random nums through while loop
    yes = yes.sample(frac=1).reset_index(drop=True)
    no = no.sample(frac=1).reset_index(drop=True)
    ntr = ntr.sample(frac=1).reset_index(drop=True)
    
    # creating folds
    for i in tqdm(range(n_folds)):
        fold = pd.DataFrame(columns = cross_validation.columns)
        fold = fold.append(yes[yes_count * i : (yes_count * i) + yes_count])
        fold = fold.append(no[no_count * i : (no_count * i) + no_count])
        fold = fold.append(ntr[ntr_count * i : (ntr_count * i) + ntr_count])
        split.append(fold)
        
    return split

def evaluate_algorithm(dataset, n_folds, label):
    splits = cross_validation_split(dataset, n_folds)
    
    for fold in splits:
        train = splits.copy()
        del train[counter]
        train = pd.concat(train)
        
        y_train = train[label].reset_index(drop = True)
        y_train = y_train.astype(int)
        
        y_test = fold[label].reset_index(drop = True)
        y_test = y_test.astype(int)
        
        # model loop
        # e.g. code in logistic_regression.py
