import facebook

graph = facebook.GraphAPI(access_token="your_token", version="2.12")

app_id = "Gameso12"
canvas_url = "https://domain.com/that-handles-auth-response/"
perms = ["manage_pages","publish_pages"]
fb_login_url = graph.get_auth_url(app_id, canvas_url, perms)
print(fb_login_url)

print('graph: ', graph)