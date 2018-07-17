
import cgitb
import cgi, sys, io, sqlite3
cgitb.enable()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
form=cgi.FieldStorage()

con = sqlite3.connect("johnnys.sqlite3")
cur = con.cursor()

cart = form.getvalue('cart','0')
cancel = form.getvalue('cancel','0')
x = form.getvalue('cancel','0')
a = int(form.getvalue('pen','0'))
aa = 100
a0 = int(form.getvalue('0','0'))
b = int(form.getvalue('pencil','0'))
bb = 75
b1 = int(form.getvalue('1','0'))
c = int(form.getvalue('eraser','0'))
cc = 60
c2 =  int(form.getvalue('2','0'))
d = int(form.getvalue('ruler','0'))
dd = 150
d3 = int(form.getvalue('3','0'))
e = int(form.getvalue('glue','0'))
ee = 100
e4 = int(form.getvalue('4','0'))
f = int(form.getvalue('appointment_book','0'))
ff = 1000
f5 = int(form.getvalue('5','0'))
g = int(form.getvalue('paper_clip','0'))
gg = 150
g6 = int(form.getvalue('6','0'))
h = int(form.getvalue('highlighter','0'))
hh = 100
h7 = int(form.getvalue('7','0'))
i = int(form.getvalue('notebook','0'))
ii = 500
i8 = int(form.getvalue('8','0'))
j = int(form.getvalue('scissors','0'))
jj = 600
j9 = int(form.getvalue('9','0'))

room = form.getvalue('room','0')
passward = form.getvalue('pas','0')
search = form.getvalue('search', '0')
selected_group = form.getvalue('gro','0')

filepath = "GUI.txt"
passfile = "passward.txt"
roomfile = "room.txt"

grouping = ""


s = []
rooms = []
minus = [a0,b1,c2,d3,e4,f5,g6,h7,i8,j9]
name = ["ペン","鉛筆","消しゴム","定規","のり","手帳","クリップ","蛍光ペン","ノート","はさみ"]

cur.execute("SELECT team FROM johnnys WHERE name = ?", (search,))
searched_team = cur.fetchall()

if searched_team == []:
  searched_team = [(0,)]
for x in searched_team:
  cur.execute("SELECT title FROM cd WHERE team = ?", x)
  searched = cur.fetchall()
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

try:
  file = open(filepath, 'r', encoding = "utf-8")
  p = open(passfile,"r",encoding="utf-8-sig")
  r = open(roomfile, "r", encoding="utf-8-sig")
  real_passward=p.readline().rstrip("\n")
  for line in file:
      s.append(int(line.rstrip("\n")))
  for line in r:
      rooms.append(line.rstrip("\n"))
except IOError:
  pass
else:
  file.close()
  p.close()
  r.close()

if s == [] or cancel == "4":
  s = [0,0,0,0,0,0,0,0,0,0]

s[0] = s[0] + a
s[1] = s[1] + b
s[2] = s[2] + c
s[3] = s[3] + d
s[4] = s[4] + e
s[5] = s[5] + f
s[6] = s[6] + g
s[7] = s[7] + h
s[8] = s[8] + i
s[9] = s[9] + j

count = 0
for x in s:
  if x < 0:
    s[count] = 0
  count = count + 1

count = 0
for m in minus:
  if m != "0":
    s[count] = s[count] - m
  count = count + 1

present = ""
count = 0
for x in s:
    if x != 0:
        present = present + """<pre> {} ×{}個 <input type="number" name="{}"></pre>""".format(name[count],x,count)
    count = count + 1
check = s[0]*aa + s[1]*bb + s[2]*cc + s[3]*dd + s[4]*ee + s[5]*ff + s[6]*gg + s[7]*hh + s[8]*ii + s[9]*jj

comment = ""
if passward != "0":
  cart = "pas"
if cart == "pas":
  comment = comment + """パスワードを入力してください。\n<input type="text" name="pas">
                         <p><a href="/cgi-bin/R02/Hci_10_15K1039_3.py"> パスワードを変更する </a></p>
                         <pre>請求先を選択してください。</pre>
                           <select name = "room">"""
  for x in sorted(rooms, key = lambda room:room):
      comment = comment + """ 
                           <option value="{}">{}</option>""".format(x,x)
  comment = comment + """  </select>
                          <p><a href="/cgi-bin/R02/Hci_10_15K1039_2.py"> 請求先の追加 </a></p>
                          <p><a href="/cgi-bin/R02/Hci_10_15K1039_1.py"> 注文画面に戻る </a></p>"""
  if passward == real_passward:
      present = ""
      count = 0
      for x in s:
          if x != 0:
              present = present + """<pre> {} ×{}個 </pre>""".format(name[count],x)
          count = count + 1
      check = s[0]*aa + s[1]*bb + s[2]*cc + s[3]*dd + s[4]*ee + s[5]*ff + s[6]*gg + s[7]*hh + s[8]*ii + s[9]*jj
      comment = """<pre>ご注文完了いたしました。ご利用ありがとうございます。\n</pre>
                   <pre>請求先: {}</pre>
                   <pre>ご購入商品 \n{}</pre>
                   <strong> 合計金額: {}円</strong>
      <p><a href="/cgi-bin/R02/Hci_10_15K1039_1.py"> 注文画面に戻る </a></p>""".format(room,present,check)
      s = [0,0,0,0,0,0,0,0,0,0]
  elif passward == "0":
    pass
  elif passward != real_passward:
    comment = comment + "パスワードが違います。もう一度やり直してください。"


else:
    comment = comment +"""<pre><font size=7> 検索 </font>\n</pre>
    <button class="button8" type="submit">Button</button>
    button.button8 {
    font-size: 1.4em;
    font-weight: bold;
    padding: 10px 30px;
    color #fff;
    boder-style: none;
    box-shadow: 2px 2px 3px 1px #666;
    -moz-box-shadow: 2px 2px 3px 1px #666;
    -webkit-box-shadow: 2px 2px 3px 1px #666;
    text-shadow: 1px 1px 2px #000;
    background: -moz-linear-gradient(bottom, #36d, #248 50%, #36d);
    background: -webkit-gradient(linear, left bottom, left top, from(#36d), color-stop(0.5, #248), to(#36d));
    -moz-border-radius: 5px;
    -webkit-border-radius: 5px;
    border-radius: 5px;
    }
    	button.button8:hover {

    <pre> 検索 <input type="text" name="search"> </pre> 
    <pre> ペン　　　　￥{}:  　  <img src="http://www.sashienomori.com/110504_4/sharppen2.gif" alt="写真" width=50 height=50><input type="number" name="pen">    鉛筆　　　　￥{}:  　 <img src="http://www.civillink.net/fsozai/sozai/enpitu4.gif" alt="写真" width=50 height=50><input type="number" name="pencil"></pre>
    <pre> 消しゴム　　￥{}: <img src="http://myds.jp/illustration/stationery/eraser/a.jpg" alt="写真" width=60 height=50> <input type="number" name="eraser">       定規　　　　￥{}:　  <img src="http://illustcut.com/box/life/bungu/bungu02_21.png" alt="写真" width=50 height=50><input type="number" name="ruler"></pre>
    <pre> のり　　　　￥{}: <img src="https://t19.pimg.jp/021/908/309/1/21908309.jpg" alt="写真" width=50 height=50><input type="number" name="glue">         手帳　　　　 ￥{}:　 <img src="http://allfree-clipart-design.com/wp-content/uploads/Business-Diary-Address-Book-or-Notebook-Vector.jpg" alt="写真" width=50 height=50><input type="number" name="appointment_book"></pre>
    <pre> クリップ　　￥{}: <img src="http://01.gatag.net/img/201504/28l/gatag-00002619.jpg" alt="写真" width=50 height=50><input type="number" name="paper_clip">　　　　 蛍光ペン　 　￥{}:    <img src="http://free-illustrations-ls01.gatag.net/images/lgi01a201310121000.jpg" alt="写真" width=50 height=50><input type="number" name="highlighter"></pre>
    <pre> ノート　　　￥{}: 　<img src="http://www.oofree.net/drawing_object/p2/note.png" alt="写真" width=50 height=50><input type="number" name="notebook">       はさみ　　　￥{}: 　<img src="http://free-illustrations-ls01.gatag.net/images/lgi01a201310161400.jpg" alt="写真" width=50 height=50><input type="number" name="scissors"></pre>  
    <p>    <button type="submit" name="aaa" value="5"> カートへ入れる </button></p>
    <p>  <button type="submit" name="cancel" value="4"> キャンセル </button> <button type="submit" name="cart" value="pas"> 購入へ </button></p>
    <pre> 現在のカート      カートから削除\n {}</pre>
    <strong> 合計金額: {}円{},{}\n{}</strong>
     """.format(aa,bb,cc,dd,ee,ff,gg,hh,ii,jj,present,check,searched,grouping,selected_group)
    #comment = comment + "{},{},{},{},{},{},{},{},{},{}".format(a0,b1,c2,d3,e4,f5,g6,h7,i8,j9)
with open(filepath, "w") as file:
    for post in s:
        file.write(str(post) + "\n")
with open(passfile, "w",encoding = "utf-8") as file:
        file.write(real_passward+"\n")
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
     <pre></pre>
     <form method="POST" action="/cgi-bin/R02/j1.py"> 
     {comment}
     </form>
    </body>
</html>

"""
    
result = template.format(comment=comment)
print("Content-type: text/html\n")
print(result)

