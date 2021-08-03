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

def get_match_locations(df, col, regex_df, output_col):
    locations = []
    for r in tqdm(df[col]):
        for k in (regex):
            for match in re.finditer(k):
                locations.append(match.span())

    df[output_col] = locations


def get_sequences(df, col, location_col, output_col, before_after_length):
    # make sure col contains strings (doctor's notes, etc.)
    # location_col is column that contains character locations of each match
    # before_after_length is how many chars you want before and after each keyword match
    l = []
    for i in tqdm(range(len(df[location_col]))):
        s = []
        try:
            for j in df[location_col][i]:
                s.append(df[col][i][j[0] - before_after_length : j[0] + before_after_length])
        except: 
            pass
        l.append(s)

    df[output_col] = l

# only run if you need sequences (generated from get_sequences) to be merged based on whether they have same value from another column
def get_location_merge_sequences(df, location_col, string_col, output_col):
    # location col is column with character locations of matches
    # string_col is column with entire string from which you would like to extract snippets from around each match
    # output col is col which will hold character locations that will comprise merged_sequences
    total_merged = []

    for index, row in df.iterrows():
        curr = str(row[location_col])
        curr = curr[1:len(curr) - 1]
        curr = list((eval(curr)))
        #print("CURR: ", len(curr))
        # print(curr)
        merged = []

        start = 0
        end = 0
        length = 0

        if (len(curr) == 2 and isinstance(curr[1], int)):
            start = curr[0]
            end = curr[1]
            
            length = len(row[string_col])
            if (start < 100):
                start = 100
            elif (end > length - 100):
                end = length - 100
            curr = [(start - 100, end + 100)]

        else:
            loc_list = []
            for j in range(len(curr)):
                start = curr[j][0]
                end = curr[j][1]
                loc_list.append((start, end))
            length = len(row[string_col])
            for k in range(len(loc_list)):
                start = loc_list[k][0]
                end = loc_list[k][1]
                if (start < 100):
                    start = 100
                elif (end > length - 100):
                    end = length - 100
                loc_list[k] = (start - 100, end + 100)
            curr = loc_list

        for interval in curr:
            if not merged:
                merged.append(interval)
                continue

            prevInterval = merged.pop()
            if prevInterval[0] <= interval[0] <= prevInterval[1]:
                startTime = prevInterval[0]
                endTime = prevInterval[1] if prevInterval[1] > interval[1] else interval[1]
                merged.append((startTime, endTime))
            else:
                merged.append(prevInterval)
                merged.append(interval)

        total_merged.append(merged)
    df[output_col] = total_merged

def get_merged_sequence_content(df, location_col, string_col, ouput_col):
    total_merged_note_txt = []
    for index, row in df.iterrows():
        curr = df[location_col]
        merged_note_txt = ""

        for i in range(len(curr)):
            start = curr[i][0]
            end = curr[i][1]

            merged_note_txt += " ------- " + row[string_col][start:end]
        total_merged_note_txt.append(merged_note_txt)

    df[ouput_col] = total_merged_note_txt

# only use if you need sequences to be a certain length
# make sure df is filtered for only rows that have sequences that need padding and char_count col exists and contains length of each sequence
def get_location_padded_sequences(df, string_col, output_col):
    total_padded_intervals = []
    for index, row in tqdm(need_padding.iterrows()):
        curr = str(row[location_col])
        curr = curr[1:len(curr) - 1]
        curr = list((eval(curr)))

        curr_char_count = row["char_count"]
        padded_len = int((800 - curr_char_count) / 2)

        if len(curr) == 2 and isinstance(curr[1], int):
            start = curr[0]
            end = curr[1]
            #print("b4", start, end)

            length = len(row[string_col])
            #print("length: ", length)
            if (start - padded_len < 0):
                start = 0

            if (end + padded_len > length):
                #print("reached")
                end = length - 1
                diff = 800 - (end - start)
                if (start - diff < 0):
                    start = 0
                else:
                    start -= diff

            if (start - padded_len > 0 and end + padded_len < length):
                start -= padded_len
                end += padded_len

            if (end - start < 750):
                curr_length = end - start
                add_to_end = 750 - curr_length
                if (end + add_to_end >= length):
                    end = length  - 1
                else:
                    end += add_to_end

            curr = [(start, end)]
        else:
            start = curr[0]
            end = curr[len(curr) - 1]
            length = len(row[string_col])
            if (start[0] - padded_len < 0):
                curr[0] = (0, curr[0][1])
            else:
                curr[0] = (curr[0][0] - padded_len, curr[0][1])
            if (end[1] + padded_len > length):
                curr[len(curr) - 1] = (curr[len(curr) - 1][0], length - 1)
            else:
                curr[len(curr) - 1] = (curr[len(curr) - 1][0], curr[len(curr) - 1][1] + padded_len)

        total_padded_intervals.append(curr)

    df[output_col] = total_padded_intervals

def get_padded_sequence_contents(df, string_col, location_col, output_col):  
    total_merged_note_txt = []
    for index, row in tqdm(df.iterrows()):
        curr = str(row[location_col])
        curr = curr[1:len(curr) - 1]
        curr = list((eval(curr)))

        merged_note_txt = ""

        if (len(curr) == 2 and isinstance(curr[1], int)):
            start = int(curr[0])
            end = int(curr[1])

            merged_note_txt += row[string_col][start:end]

        else:
            for i in range(len(curr)):
                start = curr[i][0]
                end = curr[i][1]
                if (start == 0):
                    merged_note_txt += row[string_col][start:end]
                else:
                    merged_note_txt += " ------- " + row[string_col][start:end]
                    
        total_merged_note_txt.append(merged_note_txt)

    need_padding[output_col] = total_merged_note_txt

# regex = create_list(regex_df), where regex_df is a df with col of regex pattern and col for case (0 being case insenstive, and 1 being case sensitive)
def find_matches(regex, df, col, output_col):
    for seq in tqdm(df[col]):
        curr = []

        for k in (regex):
            m = list(set(re.findall(k, seq)))
            m = list(set(map(str.lower, m)))
            if (m != []):
                curr.append("".join(m))
    
    df[output_col] = curr
