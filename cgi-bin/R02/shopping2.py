import cgitb
import cgi, sys, io
cgitb.enable()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
form=cgi.FieldStorage()

r = form.getvalue('room','0')

filepath = "room.txt"
passfile = "passward.txt"
action = "shopping2.py"
hoseirooms = ["ここの","赤石","尾花","狩野","小池（誠）","佐々木（晃）","佐藤","日高","廣津","黄","マクドナルド","李","劉","伊藤","小池（嵩）","佐々木（幸）","善甫","西島","花泉","藤田","細部","馬","雪田","若原","サブチェンコ"]
rooms = []
try:
    f = open(filepath, "r", encoding = "utf-8-sig")
    p = open(filepath, "r", encoding = "utf-8-sig")
    real_passward = p.readline().rstrip("\n")
    for line in f:
        rooms.append((line.rstrip("\n").rstrip("研究室")))
except IOError:
    pass
else:
    f.close()
    p.close()

comment=""
if r != "0":
    if r in rooms:
        count = 0
        for x in rooms:
            if x in hoseirooms:
                rooms[count] = rooms[count] + "研究室"
            count = count + 1
        comment = comment + """<p> 既に登録済みです。</p>"""
    elif r.rstrip("研究室") in rooms:
        count = 0
        for x in rooms:
            if x in hoseirooms:
                rooms[count] = rooms[count] + "研究室"
            count = count + 1
        comment = comment + """既に登録済みの研究室です。 </p>"""
    else:
        rooms.append(r)
        count = 0
        for x in rooms:
            if x in hoseirooms:
                rooms[count] = rooms[count] + "研究室"
            count = count + 1
        comment = comment + """<p>　登録しました。 登録請求先: {}""".format(rooms[count-1])
    action = "shopping1.py"
    comment = comment + """<pre></button> <button type="submit" name="cart" value="pas"> 購入へ </button>"""
with open(filepath, "w", encoding = "utf-8") as file:
    for post in rooms:
        file.write(str(post) + "\n")

template="""
<html>
 <head>
    <meta charset="utf-8">
   <title> page </title>
  </head>
    <body>
     <strong><font size = "3"></font></strong>
     <pre></pre>
     <form method="POST" action="/cgi-bin/R02/{action}">
     <strong> 追加したい請求先を入力してください。 <input type="text" name="room"></strong>
     {comment}
     </form>
    </body>
</html>

"""
    
result = template.format(comment=comment,action=action)
print("Content-type: text/html\n")
print(result)
