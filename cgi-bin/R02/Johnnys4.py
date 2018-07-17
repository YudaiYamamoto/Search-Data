
import cgitb
import cgi, sys, io, sqlite3
cgitb.enable()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
form=cgi.FieldStorage()

con = sqlite3.connect("johnnys.sqlite3")
cur = con.cursor()

search = form.getvalue('search', '0')
data = form.getvalue('detail', '0')
comment = ""
if search != "0" or data == "0":
    cur.execute("SELECT * FROM cd WHERE title = ?", (search,))
    s = cur.fetchall()
    if s == [] and search != "0":
        comment = "該当するものはありません"
    else:
        comment = """
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
        for x in s:
            comment = comment + """
          <tr>
            <td>{}</td>
            <td>{}</td>
            <td><button type="submit" name="detail" value="{}"> 詳細 </button></td>
          </tr>""".format(x[1],x[0],x[0])
        comment = comment + "</table>"
    
    comment = comment + """<p> 再検索 <input type="text" name="search"> </p>
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
                           <pre><button type="submit" name="detail" value="0"> 戻る </button></pre>"""
        

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
     <form method="POST" action="/cgi-bin/R02/Johnnys4.py"> 
     {comment}
     </form>
    </body>
</html>

"""
    
result = template.format(comment=comment)
print("Content-type: text/html\n")
print(result)

