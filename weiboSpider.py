import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree
import traceback

class weibo:
	cookie = {"Cookie": "your cookie"} #将your cookie替换成自己的cookie
	#weibo类初始化
	def __init__(self,user_id,filter = 0):
			self.user_id = user_id #用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
			self.filter = filter #取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
			self.userName = '' #用户名，如“Dear-迪丽热巴”
			self.weiboNum = 0 #用户全部微博数
			self.weiboNum2 = 0 #爬取到的微博数
			self.following = 0 #用户关注数
			self.followers = 0 #用户粉丝数
			self.weibos = [] #微博内容
			self.num_zan = [] #微博对应的点赞数
			self.num_forwarding = [] #微博对应的转发数
			self.num_comment = [] #微博对应的评论数
			self.date = [] # 微博对应的时间
			
	#获取用户昵称		
	def getUserName(self):
	  try:
		url = 'http://weibo.cn/%d/info'%(self.user_id)
		html = requests.get(url, cookies = weibo.cookie).content
		selector = etree.HTML(html)
		userName = selector.xpath("//title/text()")[0]
		self.userName = userName[:-3].encode(sys.stdout.encoding)
		#print '用户昵称：' + self.userName
	  except Exception,e:		 
		print "Error: ",e 
		traceback.print_exc()
		
	#获取用户微博数、关注数、粉丝数
	def getUserInfo(self):
	  try:
		url = 'http://weibo.cn/u/%d?filter=%d&page=1'%(self.user_id,self.filter)
		html = requests.get(url, cookies = weibo.cookie).content
		selector = etree.HTML(html)	
		pattern = r"\d+\.?\d*"

		#微博数
		str_wb = selector.xpath("//div[@class='tip2']/span[@class='tc']/text()")[0]
		guid = re.findall(pattern, str_wb, re.S|re.M)	
		for value in guid:	 
			num_wb = int(value)	 
			break
		self.weiboNum = num_wb	
		#print '微博数: ' + str(self.weiboNum)	
  
		#关注数
		str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
		guid = re.findall(pattern, str_gz, re.M)  
		self.following = int(guid[0])  
		#print '关注数: ' + str(self.following)

		#粉丝数
		str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
		guid = re.findall(pattern, str_fs, re.M)  
		self.followers = int(guid[0]) 
		#print '粉丝数: ' + str(self.followers)
	  except Exception,e:		 
		print "Error: ",e
		traceback.print_exc()
		
	#获取用户微博内容及对应的点赞数、转发数、评论数	
	def getWeiboInfo(self):
	  try:
		url = 'http://weibo.cn/u/%d?filter=%d&page=1'%(self.user_id,self.filter)
		html = requests.get(url, cookies = weibo.cookie).content
		selector = etree.HTML(html)
		if selector.xpath('//input[@name="mp"]')==[]:
		   pageNum = 1
		else:
		   pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
		pattern = r"\d+\.?\d*"
		date_pattern = r'\d+-\d+-\d+.*\d+:\d+:\d+'
		for page in range(1,pageNum+1):
		  url2 = 'http://weibo.cn/u/%d?filter=%d&page=%d'%(self.user_id,self.filter,page)
		  html2 = requests.get(url2, cookies = weibo.cookie).content
		  selector2 = etree.HTML(html2)
		  info = selector2.xpath("//div[@class='c']")
		  #print len(info)
		  if len(info) > 3:
			for i in range(0,len(info)-2):
			  self.weiboNum2 = self.weiboNum2 + 1
			  #微博内容
			  str_t = info[i].xpath("div/span[@class='ctt']")
			  weibos = str_t[0].xpath('string(.)').encode(sys.stdout.encoding,'ignore')
			  self.weibos.append(weibos)
			  #print '微博内容：'+ weibos
			  #点赞数
			  str_zan = info[i].xpath("div/a/text()")[-4]
			  guid = re.findall(pattern, str_zan, re.M)	 
			  num_zan = int(guid[0])
			  self.num_zan.append(num_zan)
			  #print '点赞数: ' + str(num_zan)
			  #转发数
			  forwarding = info[i].xpath("div/a/text()")[-3]
			  guid = re.findall(pattern, forwarding, re.M)	
			  num_forwarding = int(guid[0])
			  self.num_forwarding.append(num_forwarding)			  
			  #print '转发数: ' + str(num_forwarding)
			  #评论数
			  comment = info[i].xpath("div/a/text()")[-2]
			  guid = re.findall(pattern, comment, re.M)	 
			  num_comment = int(guid[0]) 
			  self.num_comment.append(num_comment)
			  #print '评论数: ' + str(num_comment)
			  #时间
			  date = info[i].xpath("div[last()]/span[last()]/text()")[0]
			  match = re.findall(date_pattern, date, re.M)
			  date = str(match[0])
			  self.date.append(date)
			  # print '时间: ' + date
		if self.filter == 0:
		  print '共'+str(self.weiboNum2)+'条微博'
		else:
		  print '共'+str(self.weiboNum)+'条微博，其中'+str(self.weiboNum2)+'条为原创微博'
	  except Exception,e:		 
		print "Error: ",e
		traceback.print_exc()
	
	#主程序
	def start(self):
	  try:
		weibo.getUserName(self)
		weibo.getUserInfo(self)
		weibo.getWeiboInfo(self)
		print '信息抓取完毕'
		print '==========================================================================='
	  except Exception,e:		 
		print "Error: ",e
    
    #将爬取的信息写入文件	
	def writeTxt(self):
	  try:
		if self.filter == 1:
		   resultHeader = '\n\n原创微博内容：\n'
		else:
		   resultHeader = '\n\n微博内容：\n'
		result = '用户信息\n用户昵称：' + self.userName + '\n用户id：' + str(self.user_id) + '\n微博数：' + str(self.weiboNum) + '\n关注数：' + str(self.following) + '\n粉丝数：' + str(self.followers) + resultHeader
		for i in range(1,self.weiboNum2 + 1):
		  text=str(i) + ':' + self.weibos[i-1] + '\n'+'点赞数：' + str(self.num_zan[i-1]) + '	 转发数：' + str(self.num_forwarding[i-1]) + '	 评论数：' + str(self.num_comment[i-1]) + '         时间：' + str(self.date[i-1])' + '\n\n'
		  result = result + text
		if os.path.isdir('weibo') == False:
		   os.mkdir('weibo')
		f = open("weibo/%s.txt"%self.user_id, "wb")
		f.write(result)
		f.close()
		file_path=os.getcwd()+"\weibo"+"\%d"%self.user_id+".txt"
		print '微博写入文件完毕，保存路径%s'%(file_path)
	  except Exception,e:		 
		print "Error: ",e 
		traceback.print_exc()		
		
		
#使用实例,输入一个用户id，所有信息都会存储在wb实例中		
user_id = 1669879400 #可以改成任意合法的用户id（爬虫的微博id除外）
filter = 1 #值为0表示爬取全部的微博信息（原创微博+转发微博），值为1表示只爬取原创微博
wb = weibo(user_id,filter) #调用weibo类，创建微博实例wb
wb.start() #爬取微博信息
print '用户名：' + wb.userName
print '全部微博数：' + str(wb.weiboNum)
print '关注数：' + str(wb.following)
print '粉丝数：' + str(wb.followers)
print '最新一条微博为：' + wb.weibos[0] #若filter=1则为最新的原创微博，如果该用户微博数为0，即len(wb.weibos)==0,打印会出错，下同
print '最新一条微博获得的点赞数：' + str(wb.num_zan[0])
print '最新一条微博获得的转发数：' + str(wb.num_forwarding[0])
print '最新一条微博获得的评论数：' + str(wb.num_comment[0])
wb.writeTxt() #wb.writeTxt()只是把信息写到文件里，大家可以根据自己的需要重新编写writeTxt()函数
