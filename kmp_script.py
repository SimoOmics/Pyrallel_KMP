import numpy as np
import os
from joblib import Parallel, delayed

# function to retrive and clean the input text 
def get_text(textfile):
    
    with open(textfile, 'rt') as t_file:
        
        tmp_text = t_file.readlines()
        
        tmp_text2 = [i.strip() for i in tmp_text] # clean
        s = ''
        clean_text = s.join(tmp_text2)
        return clean_text


# function to retrive and clean the input list of patterns
def get_patterns(patternfile):
    
    tmp_ptrn = []
    with open(patternfile, 'r') as p_file:
        for p in p_file:
            tmp_ptrn.append(p.strip())
            
    return tmp_ptrn


def make_LPS_array(ptrn):
    l = len(ptrn)
    lps_array= np.zeros(l, dtype=int) # initialize arraay
    
    i = 0 # to scan the string
    j = 1 # index of lps array

    while j<l:
        
        if ptrn[j] == ptrn[i]: # check for presence of a prefix = suffix
            i += 1 
            lps_array[j] = i
            j += 1

        else: # no match
            
            if i != 0: # pref/suff was longer than 1 
                i = lps_array[i-1]  # imagine ABCABA with j = 5 
                 
            else: # bruteforce
                #i = 0
                lps_array[j] = 0
                j += 1
    
    return(lps_array)


def KMPsearch(pattern, text_string):
    
    lps_array  = make_LPS_array(pattern)
       
    # real KMP search
    j = 0  # 'pointer' for the input text
    i = 0  # 'pointer' for the pattern
    counter = 0
        
    while j < len(text_string): # while not at the end of the pattern
        #print(lps[i],'i',i,text_string[j],'j',j)
        if text_string[j] ==pattern[i]: # if match between pattern and text
            i += 1 # continue checking
            j += 1 #
            
            if i == (len(pattern)): # reached the end of the pattern
                
                counter += 1         
                i = lps_array[i-1]
                
        elif text_string[j] != pattern[i]: # not match
             # this is the 'magic' of KMP algorithm
            if i != 0:
                i = lps_array[i-1] # skips part of the text to read (there isn't any possible match)
            
            else: # otherwise bruteforce
                j +=1
        
    return(f'{pattern} : {counter}')
   


def par_KMPsearc(pattern_list, text_to_scan):
    
    cores = os.cpu_count()
    
    pattern_list = get_patterns(pattern_list)
    text_to_scan = get_text(text_to_scan)
    
    #compute search
    rex =  Parallel(n_jobs= cores, verbose=0)(delayed(KMPsearch)(pattern_list[i], text_to_scan) for i in range(len(pattern_list)))
    
    # init. output file with a sort of header
    with open('KMP_Output.txt', 'wt') as file:
        file.writelines(f'Total entries: {len(pattern_list)} \n')
        file.writelines(f'Text length: {len(text_to_scan)} \n')
        file.writelines('\n')
        file.writelines(f'Entry : Frequency\n')
    
    # write results to the file
    with open("KMP_Output.txt","a") as f:
        Parallel(n_jobs=cores, prefer='threads', verbose = 0)(delayed(f.write) (f'{i} \n') for i in rex)
    