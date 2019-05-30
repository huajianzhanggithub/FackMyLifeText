import re
import time
import requests

headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)' 
    + ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132' 
    + ' Mobile Safari/537.36'
    }

def re_scraper(url,info_lists):
    res = requests.get(url,headers=headers)
    ids = re.findall('<a href=".*?" class="username" ref="nofollow">(.*?)</a>',res.text,re.S)
    levels = re.findall('<i class="age">(.*?)</i>',res.text,re.S)
    sexes = re.findall('<div class="ageBox (.*?)Box">',res.text,re.S)
    contents = re.findall('<a href=".*?" class="text" onclick="_hmt.push.*?;">(.*?)</a>',res.text,re.S)
    laughs = re.findall('<div class="box"><i class="icon icon-laugh"></i><i class="num">(.*?)</i></div>'
                      ,res.text,re.S)
    comments=re.findall('<div class="box"><i class="icon icon-comment"></i><i class="num">(.*?)</i></div>',res.text,re.S)
    for id,level,sex,content,laugh,comment in zip(ids,levels,sexes
                                                  ,contents,laughs,comments):
        info={
            'id':id,
            'level':level,
            'sex':sex,
            'content':content,
            'laugh':laugh,
            'comment':comment
            }
        info_lists.append(info)

if __name__ == '__main__':
    info_lists=[]
    urls = ['https://www.qiushibaike.com/text/page/{}/'.format(str(i)) for 
          i in range(1,2)]
    for url in urls:
        re_scraper(url,info_lists)
        time.sleep(2)
    f = open('FuckMyLifeText.txt','w')
    try:
        for info_list in info_lists:
            try:
                f.write('\n\n\nid:'+info_list['id']+'\n')
                f.write('level:'+info_list['level']+'\n')
                f.write('sex:'+info_list['sex']+'\n')
                f.write('content:'+info_list['content'].strip()+'\n')
                f.write('laugh:'+info_list['laugh']+'人认为好笑！\n')
                f.write('comment:'+info_list['comment']+'个评论！\n')
            except UnicodeEncodeError:
                pass
    finally:
        f.close()