
import cgitb
import cgi, sys, io, sqlite3
cgitb.enable()
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
form=cgi.FieldStorage()

con = sqlite3.connect("johnnys.sqlite3")
cur = con.cursor()

search = form.getvalue('search', '0')
selected_group = form.getvalue('gro','0')


grouping = ""

comment = """<pre> 検索 <input type="text" name="search"> </pre>"""
cur.execute("SELECT team FROM johnnys WHERE name = ?", (search,))
searched_team = cur.fetchall()
a = set()
if searched_team == []:
  searched_team = [(0,)]
searched = """
<style type="type/css">
table {
	border-collapse: collapse;
}
td {
	border: solid 1px;
	padding: 0.5em;
}
</style>
<caption> 関連する作品一覧 </caption>
  <table border="1" cellpadding="5" cellspacing="0">
  <tr>
    <th> 作品名 </th>
    <th> アーティスト名 </th>
  </tr>
"""
for x in searched_team:
  cur.execute("SELECT * FROM cd WHERE team = ?", x)
  for y in cur.fetchall():
      searched = searched + """
  <tr>
    <td>{}</td>
    <td>{}</td>
  </tr>""".format(y[1],y[0])
searched = searched + "</table>"
if  searched == []:
  searched = ""

cur.execute("SELECT team FROM johnnys")
group = set()
for x in cur.fetchall():
  group.add(x[0])

grouping = grouping + """<select name = "gro">"""
for y in group:
  grouping = grouping + """<option value="{}">{}</option>""".format(y,y)
grouping = grouping + "</select>"


comment = comment + """<pre>{}</pre>
           <pre>{}</pre>""".format(searched,grouping)
con.commit()
con.close()

template ="""
<html>
 <head>
    <meta charset="utf-8">
   <title> searching </title>
  </head>
    <body>
       <style type="text/css">
.classname {
    width:200px
    font-size:24px
    font-weight:bold
    text-decoration:none
    display:block
    text-align:center
    padding:8pz 0 10px
    color:#333
    border:1px solid #333
}</style>
     <strong><font size = "3"></font></strong>
     <pre><a href="#" class="classname">任意のテキスト</a></pre>
     <form method="POST" action="/cgi-bin/R02/Johnnys1.py"> 
     {comment}
     </form>
    </body>
</html>

"""
    
result = template.format(comment=comment)
print("Content-type: text/html\n")
print(result)

