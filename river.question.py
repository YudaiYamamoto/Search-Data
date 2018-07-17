#15K1039 山本ゆう大
#問題1

import sqlite3, collections

con = sqlite3.connect("river1.sqlite3")
cur = con.cursor()

#(1)
sum_dam = 0
cur.execute("SELECT dam FROM river1")
for x in cur.fetchall():
    sum_dam = sum_dam + x[0]
print("ダムの合計: {}箇所".format(sum_dam))

#(2)
cur.execute("SELECT prefecture FROM prefectures WHERE river='利根川'")
tone = cur.fetchall()
tone_p = []
for x in tone:
    tone_p.append((x[0]))
print("利根川を流域とする都道府県: {}".format(tone_p))

#(3)
print("信濃川を流域とする都道府県が持つ一級河川の総流域面積が3000km^2以上の一級河川とその総和を出力")
cur.execute("SELECT prefecture FROM prefectures WHERE river='信濃川'")
shina = cur.fetchall()
print("信濃川を流域とする都道府県: {}".format(shina))
s = 0
pre = set()
for x in shina:
    cur.execute("SELECT river FROM prefectures WHERE prefecture = ?", x)
    for y in cur.fetchall():
        pre.add(y[0])
river = []
for x in pre:
    cur.execute("SELECT * FROM river1 WHERE river = ?", (x,))#executeの第二引数は(_,)でないといけない
    for y in cur.fetchall():
        if y[3] >= 3000:
            river.append(y[1])
            s = s + y[3]
print("{}が持つ総流域面積が3000km^2以上の一級河川: {}".format(shina, river))
print("その総和: {}km^2".format(s))

#(4)
cur.execute("SELECT * FROM river1")
rivers = cur.fetchall()
sort = sorted(rivers, key = lambda river:river[2], reverse = True)
print("一級河川の長さ")
for s in range(10):
    print("NO.{}: 一級河川名: {}, 長さ: {}".format(s+1,sort[s][1],sort[s][2]))

#(5)
rx=[]
ry=[]
cur.execute("SELECT river FROM river1 WHERE region LIKE '__地方整備局管轄'")
remove_h_rivers = cur.fetchall()
for river in remove_h_rivers:
    cur.execute("SELECT prefecture FROM prefectures WHERE river = ?",river)
    for x in cur.fetchall():
        rx.append(x)

count_dict = collections.Counter(rx)
print(count_dict.most_common(2))

