"""Read tydex file."""
import re

import pandas as pd


def read_tydex_file(file_path):  
    # open file
    fid = open(file_path, 'r')
    
    # initialize struct
    tydex_struct = {}
    tydex_struct['Header'] = ""
    tydex_struct['Comments'] = ""
    tydex_struct['Constants'] = pd.DataFrame()
    tydex_struct['MeasurChannels'] = pd.DataFrame()
    tydex_struct['MeasurChannelsNotes'] = ""
    tydex_struct['MeasurData'] = pd.DataFrame()
    
    # dump variables
    constants_dump = []
    channels_dump = []
    data_dump = []
    
    # flag
    read_entries_header = False
    read_entries_comments = False
    read_entries_constants = False
    read_entries_channels = False
    read_entries_data = False
    
    for line in fid:
        current_line = line.strip()
        
        # Header
        if current_line == '**HEADER':
            read_entries_header = True
        elif current_line == '**COMMENTS':
            read_entries_header = False
        
        if read_entries_header:
            tydex_struct['Header'] += current_line + "\n"
        
        # Comments
        if current_line == '**COMMENTS':
            read_entries_comments = True
        elif current_line == '**CONSTANTS':
            read_entries_comments = False
        
        if read_entries_comments:
            tydex_struct['Comments'] += current_line + "\n"
        
        # Constants
        if current_line == '**CONSTANTS':
            read_entries_constants = True
        elif current_line == '**MEASURCHANNELS':
            read_entries_constants = False
        
        if read_entries_constants and current_line != "**CONSTANTS" and current_line:
            constants_dump.append(current_line)
        
        # MeasurChannels
        if current_line == '**MEASURCHANNELS':
            read_entries_channels = True
        elif current_line == '**MEASURDATA':
            read_entries_channels = False
        
        if read_entries_channels and current_line != "**MEASURCHANNELS" and current_line:
            if current_line.startswith('!'):
                tydex_struct['MeasurChannelsNotes'] = current_line
            else:
                channels_dump.append(current_line)
        
        # MeasurData
        if current_line == '**MEASURDATA':
            read_entries_data = True
        
        if (read_entries_data and current_line != "**MEASURDATA" 
                and any(char.isdigit() for char in current_line)):
  
            # cut string
            tempStr = current_line.strip().split()
            # safe to array
            tempArray = list(map(float, tempStr))
            # add array to dump
            data_dump.append(tempArray)
    
    # create constants table
    temp_constants_table = []
    for i in range(len(constants_dump)):
        str = constants_dump[i]
        split_str = re.split('^(.{10})(.{30})(.{10})(.*)$', str.strip())
        temp_constants_table.append(split_str[1:5])
    
    tydex_struct['Constants'] = pd.DataFrame(
        temp_constants_table, 
        columns=['Name', 'Description', 'Unit', 'Value']
    )

    
    # create measurchannels table
    temp_channels_table = []
    for i in range(len(channels_dump)):
        str = channels_dump[i]
        split_str = re.split('^(.{10})(.{30})(.{10})(.*)$', str.strip())
        # Umwandeln in double
        split_str[4] = float(split_str[4])
        temp_channels_table.append(split_str[1:5])
    
    tydex_struct['MeasurChannels'] = pd.DataFrame(
        temp_channels_table,
        columns=['Name', 'Description', 'Unit', 'Conversion_factor']
    )

    
    # create measuredata table
    tydex_struct['MeasurData'] = pd.DataFrame(data_dump)
    
    # name rows
    tydex_struct['MeasurData'].columns = tydex_struct['MeasurChannels']['Name']
    
    # apply conversion_factor
    for i in range(tydex_struct['MeasurData'].shape[1]):
        tydex_struct['MeasurData'].iloc[:, i] *= tydex_struct['MeasurChannels'].iloc[i, 3]
    
    
    
    
    return tydex_struct


#file_path = "C:/Users/ssy/Desktop/hiwi-test/code/TEST1.tdx"
#result = read_tydex_file(file_path)
#print(result['MeasurData'])
#print(result['MeasurChannels'])
#print(result['Constants'])