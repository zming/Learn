# coding=utf-8
__author__ = 'Qin'

import smtplib
from email.MIMEText import MIMEText

filename=""
subject=u"Hi,今天找到一个BTC有余额的地址"
mailto_list=["qzmjslcz@163.com","qzm775@outlook.com","757731294@qq.com"]
mail_host="smtp.qq.com"
mail_user="757731294"
mail_pass="mjpydhkxcmuzbeeh"
mail_postfix="qq.com"

def send_mail(to_list,sub,content):
    me="qzm"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,"html","utf-8")
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    #msg['Cc'] = ";".join(mail_cc)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  #连接smtp服务器
        s.starttls() #使用SSL连接
        s.login(mail_user,mail_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

def send_BTCmail(BTCinfo):
    send_mail(mailto_list,subject,BTCinfo)

if __name__ == '__main__':
    BTCinfo = "Test"
    send_mail(mailto_list,subject,BTCinfo)
