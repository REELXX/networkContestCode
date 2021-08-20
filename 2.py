url_dict = {'用户': '/userlist.html', '站点': '/other.html'}
for i in url_dict.keys():
    print(i)
    if i in "进入站点页面":
        url = url_dict[i]
        print(url)