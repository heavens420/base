import requests
import json

'''

'''

headers = {
    # 'Cookie': r'_zap=ff7e1738-8657-48a3-911d-21eee9865fcf; _xsrf=7DXVgihpnmIvN4pgTkoDGZTFm1MXzmZv; d_c0="AEBQNYlHMxSPTj94m5rB5CTCRXNGubrioOU=|1639818688"; __snaker__id=ccIqmnB58MuvlMfq; _9755xjdesxxd_=32; YD00517437729195:WM_TID=9iNW0FnFekVBVFBVBAY79qWl9OvR/wjB; YD00517437729195:WM_NI=XIue5xPfIePEEVLgnCyZI75z+ZyCyqg8LT+gIwvBQ7gmw1j57MFVNwYlRSX4dLzjRoxb7lJSQCmZOJvFntzwpnSQW8LBlorp09IdtUWH8tYMi4gsBixK6EJhY2nR3zPnWlQ=; YD00517437729195:WM_NIKE=9ca17ae2e6ffcda170e2e6ee98c26ea6acaf8cf3349ae78ab6c85b939b8e84b62581928cb8cb649ce9f7a5cc2af0fea7c3b92a9c97bb86b87494ba8786d34f878a8488ed49bb8687d8b872e986b7a4fc7ba5e884b5aa6d8ba9baa3d43da5b3b9d2e93ff5938ab7cd7d9bb49eb4db40a894b68bd165bcbef98dc959939da3bbce42b69aa295f97db4b29db2d634909ea490f17cf4e78785f75f9598f895dc47abeca994c163bc95faa6c9649beea2b3b27294b2998dd437e2a3; gdxidpyhxdE=lq8kJ5uLZRXxdjVnwzBGtRxYy5iEJCOtGm+oPntoBRmmiK1AJAU7ycgKuKAsd5z6ZGngPzhCIAql0dVLn/7N2gUT6yx\hX8AdoVduzvY9J6DdkiIHXRjhf8nW\mbbK9gI7MKbZ2CO8WV8KD3CrwsGh7M2zRJUhBMw4DXwD8\njwHZ5DD:1642040700038; z_c0="2|1:0|10:1642039916|4:z_c0|92:Mi4xWXlaQUJnQUFBQUFBUUZBMWlVY3pGQ1lBQUFCZ0FsVk5iTmpNWWdCTkVqZ2NQRUlGWVktS3NtbkVoZm5aZ25lNk9n|db8f6d69547e779b9315567ca18e7bffa940bf9cfefe4d187f4198bbfd2505e0"; q_c1=8f70d901659c4756882bc57bfa103c7f|1642125115000|1642125115000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1644546553,1644562186,1644566419,1644809701; SESSIONID=a6bZtBrtcoROrBXsfxNCtVi3iZ9RknmMrCFcFWHhJlE; JOID=VFkSBkgmApI9-o9YMSUwTd91y2kkQDLyYYvKLEdAasZwjsgHRN7Ln1z4jlw1RbNKLdIaCHIwPE69F0dv4NK80fU=; osd=V1EdBEMlCp0_8YxQPic7Ttd6yWInSD3waojCI0VLac5_jMMETNHJlF_wgV4-RrtFL9kZAH0yN021GEVk49qz0_4=; KLBRSID=9d75f80756f65c61b0a50d80b4ca9b13|1644817230|1644809696; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1644817233; tst=r',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}


def zhi_hu_request():
    # url = 'https://www.zhihu.com/api/v4/me?include=ad_type,available_message_types,default_notifications_count,follow_notifications_count,vote_thank_notifications_count,messages_count,email,account_status,is_bind_phone,is_destroy_waiting,following_question_count,is_force_renamed,renamed_fullname'
    url = 'https://www.zhihu.com/api/v4/search/preset_words'
    response = requests.get(url=url, headers=headers)
    result = json.dumps(response.json(), indent=4, ensure_ascii=False)
    print(result)


def weibo():
    url = f"https://weibo.com/ajax/feed/allGroups?is_new_segment=1&fetch_hot=1"
    response = requests.get(url=url, headers=headers)
    print(response.json())


# zhi_hu_request()
weibo()
