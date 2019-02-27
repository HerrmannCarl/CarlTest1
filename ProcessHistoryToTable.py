#Carl Herrmann

#2019-02-27 V0.3 - Initial commit to Git.
#2019-02-15 V0.2
#2017-10-06 V0.1

# Takes data logs, organized serially, and organizes them into a table.
# Give it a starting number, and a repeat #, and let it do the rest.
# 
# Input is a log file, from FlexAuto
# Setup file shows the entries to be in the as-filtered version 
# Output is a table, tab-delimited, with headers, that can be copied into Excel
# Output is a serially-organized log file, with only the values we care about.
# Double-clicking on the script will run it automatically.

debug = False

#Import modules
import os
import time
import datetime
import math
import shutil
import sys
import re

def get_txt(filename):
    txt = ""
    with open(filename) as f:
        data = f.readlines()
    for l in data:
        txt = txt + l
    return txt

def get_txt_as_list(filename):
    l = []
    with open(filename) as f:
        data=f.readlines()
    for e in data:
        l.append(e)
    return l

def Gen_Focus_Text(f_list):
    #Old Script - In-Elegant way to generate the focus values, and only the focus values
    f0_list = []
    f1_list = []
    f2_list = []
    f3_list = []
    f4_list = []

    for f in f_list:
        for i in range(len(f)):
            if f[i:i+7]=="FOCUS0=":
                f0_list.append(f[i+7:i+13])
            if f[i:i+7]=="FOCUS1=":
                f1_list.append(f[i+7:i+13])
            if f[i:i+7]=="FOCUS2=":
                f2_list.append(f[i+7:i+13])
            if f[i:i+7]=="FOCUS3=":
                f3_list.append(f[i+7:i+13])
            if f[i:i+7]=="FOCUS4=":
                f4_list.append(f[i+7:i+13])

    txt = ''
    txt = txt + f_list[0][0:7] + '\t'+"FOCUS0\tFOCUS1\tFOCUS2\tFOCUS3\tFOCUS4\n"
    for i in range(len(f_list)-1):
        line = ''
        line += f_list[i][0:7]
        line += "\t" + f0_list[i]
        line += "\t" + f1_list[i]
        line += "\t" + f2_list[i]
        line += "\t" + f3_list[i]
        line += "\t" + f4_list[i]
        line += "\n"
        txt += line
    return txt

def GiveKeyGetLines(key,txt_list,debug=False):
    if debug: print '\nGiveKeyGetLines is starting...'  
    #Input a key, as a string.
    #Input a list of text lines
    #Returns a list of all lines that contain that string
    tst_list = []
    for lin in txt_list:
        if key in lin:
            tst_list.append(lin)
    return tst_list

def GiveKeysGetLines(key_list,txt_list,debug=False):
    if debug: print '\nGiveKeysGetLines is starting...'     
    #Input a list of keys, (each key is a string)
    #Input a list of text lines
    #Returns a list of lists - see reference funtion for what's inside the list.
    lis = []
    for k in key_list:
        if debug:print'\nKey = ',k
        tmp = GiveKeyGetLines(k,txt_list,debug)
        if debug:print'\nLine = ',tmp
        lis.extend(tmp)
    return lis

def GiveKeyGetIndexes(key,txt_list,debug=False):
    if debug: print '\nGiveKeyGetIndexes is starting...'  
    #Input a key, as a string
    #Input a list of text lines
    #Returns an list of indexes (from the list) of all lines that contain that string
    lst = []
    for i in range(len(txt_list)):
        if key in txt_list[i]:
            lst.append(i)
    return lst

def SplitByIndex(index_list,txt_list):
    #Input a list of index lines
    #Input a lit of text lines
    #Returns a list of lists - each loser level list is a list of text lines.
    index_list.sort()
    a = []
    i1 = 0
    i2 = 0
    for i in range(len(index_list)-1):
        d = index_list[i]
        e = index_list[i+1]
        lis = txt_list[d:e]
        a.append(lis)
    return a

def TextClean(txt,debug=False):
    if debug: print '\nTextClean is starting...'  
    for i in range(3):
        txt = txt.lstrip(' ')
        txt = txt.lstrip('.')
        txt = txt.lstrip('\t')
        txt = txt.lstrip('\n')
        txt = txt.rstrip(' ')
        txt = txt.rstrip('.')
        txt = txt.rstrip('\t')
        txt = txt.rstrip('\n')
    return txt

def ForceCharRight(txt,char,debug=False):
    # Input is a text line (no newline charachters)
    # Input is a single charachter you want to force on the right
    # function removes any duplicates of the charachter, and adds exatly one back in
    if debug: print '\nForceCharRight is starting...'
    if debug: print 'Txt before: ', txt
    for i in range(5):
        txt=txt.rstrip(char)
    txt=txt+char
    if debug: print 'Txt after: ', txt
    return txt

def ListStrip(lis,debug = False):
    if debug: print '\nListStrip is starting...'    
    #Input is a list, each item in the list is a list of length: 1
    #Output is a list
    #for each item in the list, removes some extra characters
    n = []
    # Test - print 'heres the list: ', lis
    for nam in lis:
        if debug: print 'Printing name before strip', nam
        # num = nam[0]
        num = nam
        num = TextClean(num)
        if debug: print 'Printing name after strip', num
        if not num == '': # don't put it in the list if it's empty
            n.append(num)
    numbers = n
    return numbers

def ListsStrip(lists,debug = False):
    # input is a list of lists
    # output is a list of lists
    # Takes each list in the series, and cleans up the entries in that list.
    li = []
    for lis in lists:
        if debug: print 'List: ', lis
        # tmp = lis[0]
        tmp = lis
        l = ListStrip(tmp,debug)
        li.append(l)
    return li

def TextListToText(txt_list):
    #input is a list of text lines
    #output turns it back into a simple text file
    txt = ''
    for lin in txt_list:
        txt = txt + lin
    return txt

def TextListsToText(txt_lists):
    # Input is a list of TextLists
    # Output is a list of simple texts
    l = []
    for lis in txt_lists:
        l.append(TextListToText(lis))
    return l

def GetKeyLinesEntry(keys,entry,debug=False):
    if debug: print '\nGetKeyLinesEntry is starting...'    
    #input is a list of keys
    #input is a single data entry, formatted as a list of lines
    #output is a list of lines
    results = GiveKeysGetLines(keys,entry,debug)
    if debug: print '\nResults from GiveKeysGetLines\n',results
    return results

def GetKeyLinesEntries(keys,entries,debug=False):
    if debug: print '\nGetKeyLinesEntries is starting...'
    #input is a list of keys
    #input is a list of data entries, each formatted as a list of lines
    #output is a list of lists of lines    
    lis = []
    for entry in entries:
        tmp = GetKeyLinesEntry(keys,entry,debug)
        if debug: print '\nEntry within Lines Entries\n', tmp
        lis.append(tmp)
    if debug: print '\nLines Entries\n', lis
    return lis

def OutputLOLToText(lol,debug=False):
    # Input is a List of Lists
    ## Generates a text file, outputing a filtered process history log
    sep = '--------------------------------'

    txt = ''
    for lis in lol:
        txt = txt + sep + '\n'
        for entry in lis:
            txt = txt + entry + '\n'
    txt = txt + sep
    return txt
    
def ListSplit(lis,index):
    # Input is a list
    # input is an Index.  If the index is -1, it uses the last item in the list.
    # Output is a list
    li = lis
    # print '--li is: ', li
    list_out = []
    for l in li:
        # print 'line in is: ', l
        a = re.split(r'\t',l)
        # print a
        b = a[index]
        b = TextClean(b)
        # print 'Line Out is: ', b
        list_out.append(b)
    # print 'List Out is: ', list_out
    return list_out

def ListToText(lis,delimit):
    # Input is a list and a delimiter
    # output is a single line of text
    txt =  ''
    for li in lis:
        txt = txt + li + delimit
    return txt

def OutputLOLToTable(lol,debug=False):
    # input is a List of Lists
    # Generates a text file, outputting the filtered process history in a table format
    # generate header file
    hl = lol[0]
    el = lol[1:]
    hl0 = ListSplit(hl,0)
    #print 'Hl0: ',hl0
    table = []
    table.append(hl0)
    for e in el:
        if debug: print 'Entry Before Spiit: ',e
        ent = ListSplit(e,-1)
        if debug: print 'Entry after Split : ',ent
        table.append(ent)
    txt = ''
    delimit = '\t'
    for lin in table:
        tmp = ListToText(lin,delimit)
        tmp = tmp + '\n'
        txt = txt + tmp
    return txt

#### Input File Names

input_file = "ProcessHistory.log"
keys_file = "Setup_DataKeys.txt"
output_process_file = "Output_Process.txt"
output_table_file = "Output_Table.txt"

#### Get Input files, and massage

l = get_txt_as_list(input_file)
#l = l[0:350]

# Get keys from the input file, and massage them a bit.
keys = get_txt_as_list(keys_file)
keys = ListStrip(keys,debug=False)

#Adjust formatting, and save the new keys
keys_list = []
for k in keys:
    j = ForceCharRight(k,':')
    j = ForceCharRight(j,'\n')    
    keys_list.append(j)
keys_save = TextListToText(keys_list)

fout = open(keys_file,"w")
fout.write(keys_save)
fout.close()

#Generate new keys list, with tabs on end (helps a bit)
keys_list = []
for k in keys:
    j = ForceCharRight(k,':')
    j = ForceCharRight(j,'\t')
    keys_list.append(j)

#### Begin Splitting data up

# Split Input File into test-specific entries.
key3 = "____________________________________________________________"
c = GiveKeyGetIndexes(key3,l)
entries_list= SplitByIndex(c,l)

print 'Length of Input File: ', len(l)
print 'No of list Entries: ', len(entries_list)
print 'Number of Keys found: ', len(keys_list)

#Turn the list of entries into a list of lists
entries_LOL = GetKeyLinesEntries(keys_list,entries_list,debug=False)
entries_LOL = ListsStrip(entries_LOL,debug=False) # Cleans the list up a bit

#Generates output files, as both a filtered log and as a table
TextOutput = OutputLOLToText(entries_LOL,debug=False)
TableOutput = OutputLOLToTable(entries_LOL,debug=False)


#Write output files
fout = open(output_process_file,"w")
fout.write(TextOutput)
fout.close()

fout = open(output_table_file,"w")
fout.write(TableOutput)
fout.close()

print "Operation Complete"
for i in range(30):
    time.sleep(0.1)
print "Closing..."
for i in [30]:
    time.sleep(0.1)
