# -*- coding: utf-8 -*-
import os
import re
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import PyPDF2


def remove_nonstr(self):
    # remove all the unwanted str
    remove_list = ['',
                   '(cid:129)',
                   '©'
                   'For\nExaminer’s\nUse\n',
                   '[Turn over',
                   'BLANK PAGE'
                   ]
    for x in remove_list:
        self = self.replace(x, '')
    self = self.replace('\n ', '\n')
    for i in range(10):
        self = self.replace('\n\n', '\n')
    return self


def pdf_pagenum(self):
    # self is the address of pdf file
    self = file_address + '/' + self
    pdf_file = open(self)
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    # print number_of_pages
    return number_of_pages


def convert(fname, pages=None):
    # pages is range（）
    fname1 = fname
    fname_txt = file_address + '/' + fname[:-4] + '.txt'
    fname_txt = open(fname_txt, 'wb')
    fname = file_address + '/' + fname

    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    # print pagenums

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    pagenums = pdf_pagenum(fname1)
    pagenums = range(1, pagenums + 1)

    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    text = remove_nonstr(text)
    fname_txt.write(text)
    fname_txt.close()

    return text


def txt2evernote(self):
    # self is the txt file
    txt1 = self
    q_str = ''
    q_list_pdf = []
    a_txt = open(file_address + '/' + txt1, 'r')
    for str3 in a_txt:
        # print str3
        if len(str3.strip()) < 3:
            pass
        else:
            if '9700' in str3 or 'UCLES' in str3:
                if len(str3) > 30:
                    q_str = q_str + str3

            else:
                q_str = q_str + str3
                # print q_str

                if str3.strip().endswith(']'):
                    q_list_pdf.append(q_str)
                    q_str = ''
    print q_list_pdf
    html_name = self[:-4] + '.html'
    html_str = open(file_address + '/' + html_name, 'wb')
    html_end = '</tbody></table><div><br/></div></body></html>'
    html_start = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/><meta name="exporter-version" content="Evernote Mac 9.0.2 (457849)"/><meta name="author" content="backyang@qq.com"/><meta name="created" content="2019-05-17 12:00:01 +0000"/><meta name="source" content="desktop.mac"/><meta name="updated" content="2019-05-17 12:01:44 +0000"/><title>%s</title></head><body><div><br/></div><table style="border-collapse: collapse; min-width: 100%%;"><colgroup><col style="width: 71px;"/><col style="width: 668px;"/><col style="width: 745px;"/></colgroup><tbody>' % html_name[
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 :-5]
    html_str.write(html_start + '\n')
    i = 1
    for str5 in q_list_pdf:
        que = str5.replace('\n', '<br>')
        ans = ''
        html_row = '<tr><td style="border: 1px solid rgb(219, 219, 219); width: 71px; padding: 8px;"><div>%s</div><div><br/></div></td><td style="border: 1px solid rgb(219, 219, 219); width: 668px; padding: 8px;">%s</td><td style="border: 1px solid rgb(219, 219, 219); width: 745px; padding: 8px;">%s</td></tr>' % (
        less_than_10(i), que, ans)
        i = i + 1
        html_str.write(html_row)
    html_str.write(html_end)
    html_str.close()


def replace_p_key(self):
    # 为了切小题， international ed , part key = (1) or (i)
    # 小题的分数一般是(1),(2)
    for i in range(10):
        self = self.replace('%s)' % str(i), '%s)@#cut#@' % str(i))
    self.replace('marks)', 'marks)@#cut#@')
    a_list = self.split('@#cut#@')
    return a_list


def less_than_10(self):
    # 补0，为了排序方便
    if self < 10:
        str_num = str(0) + str(self)
    else:
        str_num = str(self)
    return str_num


# pdfs文件的路径

def list2str(self):
    x = ''
    for str_1 in self:
        x = x + str_1
    return x


def remove_str(self):
    if '' in self:
        self = self.split('')[1]
        for x in remove_list:
            # 如果每一行中有remove_list中的数据，那么就要移除整行
            if x in self:
                self = ''
            else:
                self = self.strip()
    else:
        for x in remove_list:
            # 如果每一行中有remove_list中的数据，那么就要移除整行
            if x in self:
                self = ''
            else:
                self = self.strip()
    return self


def cut_que(self):
    # self is the txt文档
    # keyword is used to cut the question
    # 9700 '【Total'
    # ‘internaltiaon ED’ ，the key is  ‘(Total’ and ‘marks’
    txt_raw = ''  # 初始str字段为空，从来		q_num = q_num +1储存题目str
    # 打开文本文件，逐行读取
    txt_lines = open(self).readlines()
    # 初始list为空，为了储存数据
    txt_raw_list = []
    # 逐行读取txt数据
    for txt_line in txt_lines:
        # print txt_line
        # 移除不需要的数据
        txt_line = remove_str(txt_line)
        # print txt_line
        # 如果txt_line 不存在，pass
        if txt_line == None or len(txt_line.strip()) < 3:
            pass
        else:
            txt_raw = txt_raw + txt_line + '\n'  # +'\n'
            # 当出现Total marks 就将生成的题目加入list中
            if big_que_mark in txt_line:
                # 将从开始到现在的str数据存进list
                txt_line1 = txt_line.replace(big_que_mark, '%s#@#' % big_que_mark).split('#@#')[0]
                txt_raw = txt_raw.replace(txt_line, txt_line1)
                txt_raw_list.append(txt_raw)
                # 清空str，准备读取第二题
                txt_raw = ''
            else:
                pass
    # 返回的数据为一个列表
    # len(txt_raw_list)就是题目的数量
    return txt_raw_list


def cut_q2part(self):
    # self is txt_raw_list | or Question list
    q_num = 1
    part_list = []
    for q_txt in self:
        q_raw = replace_p_key(q_txt)
        p_num = 1
        print q_raw


file_address = '/Users/SCIE/Desktop/qp_3'
files = [x for x in os.listdir(file_address) if x.endswith('.pdf')]
for pdf1 in files:
    print pdf_pagenum(pdf1)
    convert(pdf1)
    print 'finish to convert ' + pdf1
txt_files = [x for x in os.listdir(file_address) if x.endswith('.txt')]
for txt in txt_files:
    txt2evernote(txt)

'''

#print q_list_pdf
#print len(q_list_pdf)



le
d = 0wwwqaqlk kkdksdadkakdkd//,ik/.;
for file1 in files:p
	txt_name= file1[:-4]+'.txt'	
	print file1[:-4]
	new_file = file_address + '/' + file1
	tem_str = convert(new_file,pages=None)
	txt_name = file_address +'/file1/' +txt_name
	new_txt = open(txt_name,'a')
	new_txt.write(tem_str)
	d += 1
	new_txt.close()
	print d,  ' file (s) is/ are done!'

		for part in q_txt:
			tiny_list = []
			tiny_list.append('_Que'+ less_than_10(q_num))
			tiny_list.append('_Part'+ less_than_10(p_num))
			tiny_list.append(part)
			pattern = re.compile(r'\d+')
			raw_mark = pattern.findall(part,0,10)
			print (raw_mark)
			tiny_list.append(str(raw_mark))
			part_list.append(tiny_list)
			p_num += 1
		q_num += 1
	#tiny_list = 题号，题目， 分数
	# part_list 用来存tiny_list的数据的，题目信息和总分信息
	# len(part_list) 就是卷子小题的数量
	return (part_list)

new_txt=open('/Users/SCIE/Desktop/pra/new/2.txt','r').readlines()

str_list=[]
q_list=[]

for str2 in new_txt:
	str_list.append(str2)
	if 'UCLES' in str2:
		str_list.pop()
		str_list.pop()
	if str2.strip().endswith(']'):
		q_list.append(list2str(str_list))
		str_list=[]
print str_list
#print q_list


file_address = 'txt'
files = [x for x in os.listdir(file_address) if x.endswith('.txt')]#以txt结尾的文档
big_que_mark='marks)'
remove_list= [
	'BLANK PAGE',
	'exemplar',
	'...',
	'Turn over',
	'DRAFT',
	'turn over',
	'Blank page',
	'0610',
	'DO NOT WRITE IN THIS AREA',
	'*P',
	'Turn over']
ever_start='<html> <head>   <title>Evernote Export</title>   <basefont face="微软雅黑" size="2" />   <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />   <meta name="exporter-version" content="Evernote Windows/307027 (zh-CN, DDL); Windows/10.0.0 (Win64);"/>   <style>	 body, td {	   font-family: 微软雅黑;	   font-size: 10pt;	 }   </style> </head> <body> <a name="65954"/>  <div> <span><div><br/></div><div><div><br/></div><table style="border-collapse: collapse; min-width: 100%;">   <colgroup><col style="width: 919px;"></col><col style="width: 919px;"></col></colgroup>  <tbody>'
ever_end='</tbody></table><div><br/></div></div><div><br/></div><div></div></span></div></body></html>'

html_name=open('8BI0_01_que_20180525.html','wb')
html_name.write(ever_start)


txt_file=open('txt.txt','wb')

for file in files:
	file = file_address+'/'+file
	print len(cut_que(file))
	big_q_num = 1
	small_que=''
	small_ans=''
	for big_que in cut_que(file):
		small_que_list = replace_p_key(big_que)
		for small_que in small_que_list:
			small_qa= '<tr>\n	<td style="border: 1px solid rgb(255, 0, 0); width: 10px; padding: 8px;"><div>%s</div></td>\n   <td style="border: 1px solid rgb(255, 0, 0); width: 919px; padding: 8px;"><div>%s</div></td>\n  <td style="border: 1px solid rgb(255, 0, 0); width: 919px; padding: 8px;"><div>%s</div></td>\n  </tr>\n' % (str(big_q_num),small_que.replace('\n',''), small_ans)
			html_name.write(small_qa)
		big_q_num += 1
html_name.write(ever_end)
html_name.close()

'''