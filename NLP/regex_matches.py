def create_list(regex_df):
    k = regex_df["REGEX"].to_list()
    c = regex_df["CASE"].to_list() # if some regex are case-sensitive
    regex_list = []

    for i in range(len(k)):
        if (c[i] == 0):
            regex_list.append(re.compile(k[i][5:], re.IGNORECASE))
        elif (c[i] == 1):
            regex_list.append(re.compile(k[i]))
    return regex_list

def find_matches(regex, df, col):
    for seq in tqdm(df[col]):
        curr = []

        for k in (regex):
            m = list(set(re.findall(k, seq)))
            m = list(set(map(str.lower, m)))
            if (m != []):
                curr.append("".join(m))
    
    df[col] = curr
