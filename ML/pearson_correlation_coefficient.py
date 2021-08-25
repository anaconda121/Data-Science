def filter_features_by_cor(df):
    m = len(df.columns)
    output = df.iloc[:, m - 1] 
    output_list = output.tolist()
    corrcoef_array = []

    for i in range(0, m - 2):
        input_list = df.iloc[:, i].tolist()
        cols = [input_list, output_list]
        corrcoef = abs(np.corrcoef(cols)) 
        corrcoef_array = np.append(corrcoef_array,corrcoef[0, 1])

    feature_names = list(df)
    feature_names = feature_names[0:m-2]
    
    output_df = pd.DataFrame(feature_names, columns = ['Features'])
    output_df['CorrCoef'] = corrcoef_array
    output_df = output_df.sort_values('CorrCoef')
    output_df = output_df.reset_index()
    output_df = output_df.drop(columns = "index")
    
    return output_df

output_df = filter_features_by_cor(train_df)
output_df = output_df.sort_values(by = ['CorrCoef'], ascending = False)
