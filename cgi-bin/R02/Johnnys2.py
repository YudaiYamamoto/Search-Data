#q5K1039 山本ゆう大
#課題２
import cgitb
import cgi, sys, io, sqlite3
cgitb.enable()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
form=cgi.FieldStorage()

j = form.getvalue('judge', '0')
action="Johnnys2.py"

con = sqlite3.connect("johnnys.sqlite3")
cur = con.cursor()

comment = ""
if j == "a":
    comment = comment + """<p> 検索したいアーティスト名を入力してください <input type="text" name="search"> </p>"""
    action = "Johnnys1.py"

elif j == "w":
    comment = comment + """<p> 検索したい作品名を入力してください <input type="text" name="search"> </p>"""
    action = "Johnnys4.py"
    
elif j == "0":
    comment = comment + """
     <button type="submit" name="judge" value="a"> アーティスト名から検索 </button>
     <button type="submit" name="judge" value="w"> 曲名から検索 </button>
     """
template ="""
<html>
 <head>
    <meta charset="utf-8">
   <title> searching </title>
  </head>
    <body>
     <strong><font size = "5"> 検索機 </font></strong>
     <form method="POST" action="/cgi-bin/R02/{action}">
     {comment}
     </form>
    </body>
</html>

"""
    
result = template.format(action=action,comment = comment)
print("Content-type: text/html\n")
print(result)

