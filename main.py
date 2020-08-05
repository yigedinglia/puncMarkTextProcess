# -*- coding: utf-8 -*-
import os
import os.path
import re
import itertools

re_entry = '(☆)(\d{8})(☆)(.*)'
re_punc = '(\.+|-+|ー+|~|～|『|』|。」)'
pattern_entry = re.compile(re_entry)
pattern_punc = re.compile(re_punc)
punc_type = {'.':'……','-':'——', 'ー':'——','~':'〜','～':'〜','『':'“','』':'”','。':'」'}

#/output/filename.txt
output_path = os.path.abspath('.') + '/output'
#/output/logs/log_filename.txt
log_path = output_path + '/logs'
#output texts
texts = []
#output logs
logs = []
files = os.listdir()

def main():
    is_exists = os.path.exists(log_path)
    if not is_exists:
        os.makedirs(log_path)
    for file in files:
        if re.search(r'\.txt', file):
            txt_path = '' + file
            contents = open(txt_path,'r',encoding='utf-8')
            #clear before process every file
            texts.clear()
            logs.clear()
            for content in contents:
                o_content = content
                #process text
                r_content = strEntry(content)
                if len(r_content) != 0 and r_content['log_flag'] != 0:
                    #if content changed: append it and its log
                    texts.append(r_content['w_str'])
                    setLog(r_content['o_str'], r_content['r_str'], r_content['str_id'])
                else:
                    #if not: just append origin text 
                    texts.append(o_content)
            #new file path
            new_text_path = f"{output_path}/output_{file}"
            new_log_path = f"{log_path}/log_{file}"
            new_text = open(new_text_path, 'w', encoding='utf-8')
            new_log = open(new_log_path, 'w', encoding='utf-8')
            #write text and log in file
            for text in texts:
                new_text.write(text)    
            for log in logs:
                new_log.write(log)
            new_text.close()
            new_log.close

#argu: origin text, formed text, line number of the text
def setLog(o_str, r_str, str_id):
    log = f"place: {str_id}\norigin_text: {o_str}\nformed_text: {r_str}\n——————————————————————\n"
    logs.append(log)

#start
def strEntry(string):
    strarr = re.match(re_entry,string)
    rdata = []
    if strarr != None:
        rdata = mainProcess(strarr)
    return rdata
        
#main process
def mainProcess(string_array):
    white_star = string_array.group(1)
    #line number of the text
    str_id = string_array.group(2)
    #origin text(no line number)
    ostr = string_array.group(4)
    #formed text(no line number)
    rstr = strB2Q(quoteE2C(puncModify(ostr)))
    #formed text(has line number)
    wstr = f"{white_star}{str_id}{white_star}{rstr}\n"
    #1=changed,0=no change
    log_flag = 0
    if rstr != ostr:
        log_flag = 1
    return {'o_str':ostr, 'r_str':rstr, 'w_str':wstr, 'str_id':str_id, 'log_flag':log_flag}

#SBC to DBC
def strB2Q(string):
    rstring = ""
    for uchar in string:
        inside_code = ord(uchar)
        #空格
        if inside_code == 32:
            inside_code = 12288
        #数字和字母
        elif inside_code > 32 and inside_code <= 126:
            inside_code += 65248         
        rstring += chr(inside_code)
    return rstring

#english quotation marks to chinese
def quoteE2C(string):
    rstring = string
    obj1 = itertools.cycle(['“','”'])
    obj2 = itertools.cycle(['‘','’'])
    _obj1 = lambda x: next(obj1)
    _obj2 = lambda x: next(obj2)
    quote_num = len(re.findall(r"[\"“”'‘’]",string))
    #only process when they are in pairs
    if quote_num % 2 == 0 and quote_num > 0:
        rstring = re.sub(r"[\"“”]", _obj1, string)
        rstring = re.sub(r"['‘’]", _obj2, rstring)
    return rstring

#process the punctuation mark
def puncModify(string):
    rstr = re.sub(pattern_punc, puncReplace, string)
    return rstr
    
#replace the punctuation mark  
def puncReplace(key):
    keychar = key[0][0]
    return punc_type[keychar]

if __name__ == '__main__':
    print('Processing......')
    main()
    print('Processed. Press any key to continue.')
    input()