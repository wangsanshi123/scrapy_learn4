# -*- coding: utf-8 -*-

import json

import requests
import sys


def test1(url):
    reload(sys)
    sys.setdefaultencoding('utf8')
    # url = "https://www.zhihu.com/search?type=content&q=vivo+x20"
    # url = "https://www.zhihu.com/r/search?q=vivo+x20&correction=1&type=content&offset=10"

    time = 0
    offset = 0
    runFlag = True
    keyword = 'vivo+x20'
    while runFlag:
        if time > 0:
            break
        # url = "https://www.zhihu.com/r/search?q={}&correction=1&type=content&offset={}".format(keyword, offset)
        print url
        user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"
        authorization = "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
        headers = {"User-Agent": user_agent, "authorization": authorization}
        result = requests.get(url, headers=headers)
        result = result.text
        with open('temp.json', 'w') as f:
            # f.write(json.dumps(result))
            f.write(result)

        result = json.loads(result)
        data = result['data']
        for item in data:
            name = item['author']['name']
            print name

        # is_end = result['paging']['is_end']
        # print "is_end:", is_end
        # if is_end is "false" or "False":
        #     url = result['paging']['next']
        #     test(url)
        # else:
        #     print u'结束了'

        time += 1
        offset += 10


def test2(url):
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"
    authorization = "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
    headers = {"User-Agent": user_agent, "authorization": authorization}
    result = requests.get(url, headers=headers)
    # result = requests.get(url)
    result = result.text
    with open('temp_comments.json', 'w') as f:
        f.write(result.encode('utf-8'))
    pass
    data = json.loads(result)['data']
    for item in data:
        content = item['content']
        print content, "\n"


def test3(url):
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"
    authorization = "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
    headers = {"User-Agent": user_agent, }
    result = requests.get(url, headers=headers)
    result = result.text
    htmls = json.loads(result)['htmls']
    time = 0
    for html in htmls:
        if time > 0:
            break
        with open('temp_search.html', 'w') as f:
            f.write(html.encode('utf-8'))
        pass
        time += 1

    pass


def test4(url):
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"
    authorization = "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
    headers = {"User-Agent": user_agent, "authorization": authorization}
    result = requests.get(url, headers=headers)
    result = result.text
    print result

    pass

    pass


if __name__ == '__main__':
    url_search = "https://www.zhihu.com/r/search?q=vivo+x20&correction=1&type=content&offset=10"
    url_answers = "https://www.zhihu.com/api/v4/questions/65073334/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0&sort_by=default"
    url_answers = "https://www.zhihu.com/api/v4/questions/20814939/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0&sort_by=default"
    url_answers = "https://www.zhihu.com/api/v4/questions/25598282/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0&sort_by=default"

    url_comments = "https://www.zhihu.com/api/v4/questions/65073334/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=10&offset=0&status=open"
    url_comments = "https://www.zhihu.com/api/v4/questions/20814939/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=10&offset=0&status=open"
    url_comments = "https://www.zhihu.com/api/v4/questions/65073334/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=10&offset=0&status=open"

    url_comment = "http://www.zhihu.com/api/v4/comments/333941280"
    # test1(url_answers)
    # test2(url_comments)
    test3(url_search)
    test4(url_comment)
