

import cgitb
import cgi, sys, io
cgitb.enable()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
form=cgi.FieldStorage()

p1 = form.getvalue('p1','0')
p2 = form.getvalue('p2','0')
new_passward = form.getvalue('new','0')
action="j3.py"
passfile = "passward.txt"

try:
    p = open(passfile, "r", encoding = "utf-8-sig")
    real_passward = p.readline().rstrip("\n")
except IOError:
    pass
else:
    p.close()

comment="""古いパスワードを入力してください
         <pre><input type="text" name="p1"></pre>"""
if p1 == real_passward:
    comment = """確認のため、もう一度古いパスワードを入力してください
                 <pre><input type="text" name="p2"></pre>"""
    with open(passfile, "w", encoding = "utf-8") as file:
        file.write(real_passward + "\n")
elif p1 != real_passward and p1 != "0":
    comment = """パスワードが違います
                 <p><a href="/cgi-bin/R02/j1.py"> 注文画面に戻ります </a></p>"""
    with open(passfile, "w", encoding = "utf-8") as file:
        file.write(real_passward + "\n")
if p2 == real_passward:
    comment = """新しいパスワードを入力してください
                 <pre><input type="text" name="new"></pre>"""
    with open(passfile, "w", encoding = "utf-8") as file:
        file.write(new_passward + "\n")
elif p2 == "0":
    pass
elif p2 != real_passward:
    comment = """パスワードが違います
                 <p><a href="/cgi-bin/R02/j1.py"> 注文画面に戻ります </a></p>"""
    with open(passfile, "w", encoding = "utf-8") as file:
        file.write(real_passward + "\n")
if new_passward != "0":
    action = "j1.py"
    comment = """<pre>パスワードを設定しました。</pre>
                 <pre></button> <button type="submit" name="cart" value="pas"> パスワード入力画面へ戻る </button></pre>"""
    with open(passfile, "w", encoding = "utf-8") as file:
        file.write(new_passward + "\n")

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
     {comment}
     </form>
    </body>
</html>

"""
    
result = template.format(comment=comment,action=action)
print("Content-type: text/html\n")
print(result)
