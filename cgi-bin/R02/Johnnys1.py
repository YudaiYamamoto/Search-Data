#http://localhost:8000/cgi-bin/R02/Johnnys1.py

import cgitb
import cgi, sys, io, sqlite3
cgitb.enable()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
form=cgi.FieldStorage()

con = sqlite3.connect("johnnys.sqlite3")
cur = con.cursor()
search = form.getvalue('search', '0')
group = form.getvalue('gro','0')
data = form.getvalue('detail', '0')
comment=""

if group != "0" and search == "0":
    search = group
    
if data == '0':
    grouping = ""

    cur.execute("SELECT team FROM johnnys WHERE name = ?", (search,))
    searched_team = set()
    for x in cur.fetchall():
        searched_team.add(x)
    cur.execute("SELECT * FROM cd WHERE team = ?",(search,))
    works = cur.fetchall()
    if searched_team == set() and works == [] and search != "0":
      searched = "該当するものがありません"
    else:
        searching = []
        if searched_team == set():
            for x in works:
                searching.append(x)
        elif works == []:
            for x in searched_team:
              cur.execute("SELECT * FROM cd WHERE team = ?", x)
              for y in cur.fetchall():
                  searching.append(y)
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
            <th> グループ </th>
          </tr>
        """

        for y in searching:
              searched = searched + """
          <tr>
            <td>{}</td>
            <td>{}</td>
            <td><button type="submit" name="detail" value="{}"> 詳細 </button></td>
          </tr>""".format(y[1],y[0],y[0])
        searched = searched + "</table>"
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
    comment = comment + """<p> 再検索 <input type="text" name="search"> </p>
                           <p> <input type="submit"> </P>
                           <p><a href="/cgi-bin/R02/johnnys2.py"> トップに戻る </a></p>"""
    

elif data != "0":
    cur.execute("SELECT name FROM johnnys WHERE team = ?", (data.split(",")[0].rstrip("("),))
    comment = comment + """
    <p> {} </P>
    <p>メンバー: """.format(data.split(",")[0])
    counter = 1
    member = cur.fetchall()
    for m in member:
        if len(member) != counter:
            comment = comment + "{},".format(m[0])
        else:
            comment = comment + "{}</p>".format(m[0])
        counter = counter + 1
    comment = comment + """
        <style type="type/css">
        table {
                border-collapse: collapse;
        }
        td {
                border: solid 1px;
                padding: 0.5em;
        }
        </style>
        <caption> プロフィール </caption>
          <table border="1" cellpadding="5" cellspacing="0">
          <tr>
            <th> 名前 </th>
            <th> 生年月日 </th>
            <th> 年齢 </th>
            <th> 出身地 </th>
            <th> 血液型 </th>
          </tr>"""
    for m in member:
        cur.execute("SELECT * FROM Johnnys WHERE name = ?", m)
        d = cur.fetchall()
        comment = comment + """
          <tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
          </tr>""".format(d[0][0],d[0][2],d[0][3],d[0][4],d[0][5])
        
    comment = comment + """</table>
                           <pre><button type="submit" name="detail" value="0"> 戻る </button> </pre>"""
        


con.commit()
con.close()
template ="""
<html>
 <head>
    <meta charset="utf-8">
   <title> searching </title>
  </head>
    <body>
     <strong><font size = "3"></font></strong>
     <form method="POST" action="/cgi-bin/R02/Johnnys1.py"> 
     {comment}
     </form>
    </body>
</html>

"""
    
result = template.format(comment=comment)
print("Content-type: text/html\n")
print(result)

