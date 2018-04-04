import requests


def test():
    url = "https://m.baidu.com/mip?ext=%7B%22lid%22%3A%2213822225533373016556%22%2C%22url%22%3A%22%2F%2Fmipcache.bdstatic.com%2Fc%2Fwww.360doc.cn%2Fmip%2F301900478.html%22%7D&title=360doc%E4%B8%AA%E4%BA%BA%E5%9B%BE%E4%B9%A6%E9%A6%86"
    result = requests.get(url=url)
    result = result.text.encode('utf-8')
    with open("temp_360.html", "a")as f:
        f.write(result)
    pass
def test2():
    "【"
    pass

if __name__ == '__main__':
    test()
