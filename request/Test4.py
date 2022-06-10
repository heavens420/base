import requests
from urllib.parse import urlencode
import time
import random
referer='https://weibo.com/u/7599147183/home?wvr=5' #referer按照网页自己提供，防止反爬虫
# 设置请求头
headers = {
    'cache-control': 'no-cache',
    #cookie关键数据，
    'cookie': 'SINAGLOBAL=3779177080662.532.1645452320428; ULV=1645452321096:1:1:1:3779177080662.532.1645452320428:; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFqRIIR7pA9whK9.friJdXu5JpX5KMhUgL.FoMf1K.pShMp1he2dJLoIp.LxK.LB-eLB.eLxK.LB-eLB.e_eK.4SK27; ALF=1677055165; SSOLoginState=1645519172; SCF=AijeE3G_wmgToRkorOyZxujibCQmlorGAlhuQuhj7Qwm2D-FKfgsXS-Bd-rzGJ3cs8cp-iwO_1K_YS-mfPml2cQ.; SUB=_2A25PENEQDeRhGeFL4lsQ9CnNwz-IHXVsZEXYrDV8PUNbmtB-LUjYkW9NfWwn12cdERvHe_HCZiNMLiYl_3p1lbNj; XSRF-TOKEN=BzvEHogQaXvGcAqgZKuJEqDZ; WBPSESS=Dt2hbAUaXfkVprjyrAZT_DkKWdHt4MULd107nvww8yuOBGbb2n3wRxAjagfU4PoZVAc6Bv8j8AiF7Mj6pieBiwLVHXGvfXmEPpRwkWgepfEIwLtL75iA0M-NgEg-7hY6DFLWCfklYYhQ_j4e-xi3wc9nd-Ib4KS5U7PQjhlt4wHtranAUhanD9Yout_IbQCS4yJU94GFPHNFpRGMa5yOZg==',
    'referer': referer,
    'traceparent': '00-5c81397f0ccf06af48cb59bfd2a68ead-033bf99f9cfd7101-00',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': 'gDR78zPCFLY9og9lVBU6FgGJ'
}

def get_categroy_code(category):#获取类别的id号
    url="https://weibo.com/ajax/feed/allGroups?is_new_segment=1&fetch_hot=1"
    response=requests.get(url=url,headers=headers).json()
    category_list=response.get('groups')[4].get('group')#频道推荐
    category_list_2=response.get('groups')[3].get('group')#我的频道
    for category_grop in category_list+category_list_2:
        if category_grop.get('title') == category :
            return category_grop.get('containerid'),category_grop.get('gid')
        else:
            pass
    print("对不起，输入的类别有误")
    return None
def get_single_page(page,containerid,gid):# 按页数抓取数据
    # 请求参数
    # https://weibo.com/ajax/feed/hottimeline?# https://weibo.com/ajax/feed/hottimeline? # https://weibo.com/ajax/feed/hottimeline?
    # since_id=0&refresh=1&group_id=1028034288&containerid=102803_ctg1_4288_-_ctg1_4288&extparam=discover|new_feed&max_id=0&count=10
               # refresh=2&group_id=1028034288&containerid=102803_ctg1_4288_-_ctg1_4288&extparam=discover|new_feed&max_id=1&count=10
               # refresh=2&group_id=1028034288&containerid=102803_ctg1_4288_-_ctg1_4288&extparam=discover|new_feed&max_id=2&count=10
    if(page==0):
        base_url = f'https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=1&group_id={gid}&containerid={containerid}&extparam=discover|new_feed&count=10'
    else:
        base_url=f'https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id={gid}&containerid={containerid}&extparam=discover|new_feed&count=10'
    params={
        'max_id ':page
    }
    url=base_url+urlencode(params)
    try:
        response = requests.get(url=url, headers=headers)
        return response.json()
    except Exception :
        print(Exception.args)
        return None

def detail_doc(isLongText,mblogid):# 获取微博的正文内容
    if isLongText:
        #  https://weibo.com/ajax/statuses/longtext?id=Lc6j2szcX
        text_url = f'https://weibo.com/ajax/statuses/longtext?id={mblogid}'
        respons = requests.get(url=text_url, headers=headers).json()
        detail_text = respons.get('data').get('longTextContent')
    else:
        #       https: // weibo.com / ajax / statuses / show?id = LewWPFL6m
        text_url = f'https://weibo.com/ajax/statuses/show?id={mblogid}'
        respons = requests.get(url=text_url, headers=headers).json()
        detail_text = respons.get('text_raw')
    return detail_text

def detail_ten_comments(id,uid):# 获取前十条评论
    ten_comments=[]
    # https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id=4735625313650242&is_show_bulletin=2&is_mix=0&count=10&uid=6043737633
    comments_url = f'https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id={id}&is_show_bulletin=2&is_mix=0&count=10&uid={uid}'
    respons = requests.get(url=comments_url, headers=headers).json()
    max_id=respons.get('max_id')
    if (len(respons.get('data')) == 10):  # 访问一次获取10条评论
        for temp_data in respons.get('data'):
            comment = temp_data.get('text_raw')
            ten_comments.append(comment)
        return ten_comments
    elif (len(respons.get('data'))<10):#可能是由于二级评论导致，一次访问不了10条，尝试访问2次
        if(max_id>0):
            for temp_data in respons.get('data'):#一次访问
                comment = temp_data.get('text_raw')
                ten_comments.append(comment)
            other_commnents_count=10-len((respons.get('data')))
            two_comments_url=f'https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id={id}&is_show_bulletin=2&is_mix=0&max_id={max_id}&count=20&uid={uid}'
            respons=requests.get(url=two_comments_url,headers=headers).json()
            for i in range(0,other_commnents_count+1):
                try:
                    comment = respons.get('data')[i].get('text_raw')
                    ten_comments.append(comment)
                except IndexError :
                    return None
            return ten_comments
    else:
        return None

def get_pic_url(item):#获取对应的图片地址
    pic_url=''
    if 'page_info' in item : # 纯视频
        pic_url = item.get('page_info').get('page_pic')
    elif 'pic_infos' in item:  # 纯图片
        pic_num = item.get('pic_num')
        if (pic_num > 0):
            pic_id = item.get('pic_ids')[0]
            pic_url = item.get('pic_infos').get(pic_id).get('bmiddle').get('url')

    else:
        pass
    return pic_url

def get_keword(item):#获取关键字
    key_word=''
    if 'topic_struct' in item:
        for topic in item.get('topic_struct'):
            topic_titile=topic.get('topic_title')
            key_word=key_word+'&&'+topic_titile
    else:
        pass
    return key_word

import os, csv
def save_data(seq,category,pic_file_midr,result_file_path,detail_text,ten_comments,pic_url,key_word,person):#按照数据格式保存
    pic_path = pic_file_midr + "\\" + "{:0>6d}".format(count) + ".jpg"
    src=f"C:\数据图片收集\搞笑\\" + "{:0>6d}".format(count) + ".jpg"
    with open(result_file_path, mode='a+', encoding='utf-8-sig', newline='')as f:
        writer = csv.writer(f)
        s=''
        for i in range(0, 10):
            s=seq+str(i)
            writer.writerow([s,category,key_word,detail_text,src,ten_comments[i]," ",person])
    respons=requests.get(url=pic_url,headers=headers).content
    with open(pic_path,'wb') as fp:
        fp.write(respons)


if __name__ == '__main__':
    category="搞笑"#input("请输入类别词（例如教育、政务。）：")
    person = "张玉莹"#input("请输入负责人姓名：")
    containerid,gid=get_categroy_code(category)
    result_file_midr=f"C:\数据收集任务\{category}"
    pic_file_midr=f"C:\数据收集任务\{category}图片"
    if not os.path.exists(result_file_midr):
        os.makedirs(result_file_midr)
    if not os.path.exists(pic_file_midr):
        os.makedirs(pic_file_midr)
    result_file_path=result_file_midr+f"\\{category}.csv"

    with open(result_file_path,'a+',encoding='utf-8-sig',newline='')as f:
        writer=csv.writer(f)
        writer.writerow(['序号','类别','话题(关键字)','话题内容','图片地址','评论','情感极性','负责人'])
    count=110
    for page in range(1, 5000):  # 瀑布流下拉式，加载，max_id从0开始
        print("page:\n",page)
        json_data = get_single_page(page,containerid,gid)
        if json_data == None:
            print('json is none')
            break
        items = json_data.get('statuses')
        temp_datas = []
        datas = []
        for item in items:
            if (item.get('comments_count') >= 20):  # 判断该微博的评论数量是否能达到15条，这里有个问题：评论总数是15条，而不是一级评论是15条以上。
                id = item.get('id')  # 获取id，为后面访问评论页面做准备
                uid = item.get('user').get('id')  # 获取uid，为后面访问评论页面做准备
                mblogid = item.get('mblogid')
                isLongText = str(item.get('isLongText')).replace("\n","").replace("\r","")
                #获取微博正文，获取十条评论，获取图片地址,关键字
                detail_text = detail_doc(isLongText=isLongText, mblogid=mblogid)
                ten_comments = detail_ten_comments(id, uid)
                pic_url = get_pic_url(item)
                key_word=get_keword(item)
                if ten_comments is not None:
                    if len(pic_url)>0:
                        if detail_text is not None:
                            # 存数据
                            count += 1
                            seq='18-'+str("{:0>6d}".format(count))+'-'
                            save_data(seq,category,pic_file_midr,result_file_path,detail_text,ten_comments,pic_url,key_word,person)
                            print("写完第"+str(count)+"个话题内容")
                            # if count >= 70 + 110:
                            #     break
    #         # time.sleep(random.randint(2, 6))  # 爬取时间间隔