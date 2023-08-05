#!python3
import requests
from eyes_soatra import eyes
import re as __re
from lxml import etree as __etree
from lxml import html as __html

# a = requests.get('https://www.city.kuki.lg.jp/kosodate/kosodatesienn/hitorioya/jifu.html')
# text1 = __re.sub('(<\?.*\?>)', '', a.)
# text = __re.sub('(<\?.*\?>)', '', (a.content.decode() + a.content.decode()))


# print(text)
# __html.fromstring(text)

# __etree.strip_elements(
#     html,
#     [
#     __etree.Comment,
#     'script',
#     'link',
#     'style',
#     'button',
# ])

# con = __etree.tostring(html)

# print(con)

# a = requests.get('https://www.city.kuki.lg.jp/kosodate/kosodatesienn/hitorioya/jifu.html')

a = eyes.view_page('https://www.city.kuki.lg.jp/kosodate/kosodatesienn/hitorioya/jifu.html', show_header=True)


print(a)
