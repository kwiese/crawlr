from collection import collectSubtoursFastTest, meldSubtours
from random import randint

edges = [
    ("hi", "there"),
    ("there", "guy"),
    ("short", "one"),
    ("guy", "hi"),
    ("one", "short"),
    ("butt", "stuff"),
    ("stuff", "hurts"),
    ("hurts", "butt"),
    ("go", "there"),
    ("there", "go"),
]

#print(collectSubtoursFast(edges, len(edges)))

subtours = collectSubtoursFastTest(edges, len(edges))

s1 = subtours[0]
s2 = subtours[1]
s3 = subtours[2]
s4 = subtours[3]

edgeArray1 = [
    (frm, to, None, randint(1, 10))
    for frm in s1
    for to in s2
]
edgeArray2 = [
    (to, frm, None, randint(1, 10))
    for frm in s1
    for to in s2
]
edgeArray3 = [
    (frm, to, None, randint(1, 10))
    for frm in s1
    for to in s3
]
edgeArray4 = [
    (to, frm, None, randint(1, 10))
    for frm in s1
    for to in s3
]
edgeArray5 = [
    (frm, to, None, randint(1, 10))
    for frm in s1
    for to in s4
]
edgeArray6 = [
    (to, frm, None, randint(1, 10))
    for frm in s1
    for to in s4
]
edgeArray7 = [
    (frm, to, None, randint(1, 10))
    for frm in s2
    for to in s3
]
edgeArray8 = [
    (to, frm, None, randint(1, 10))
    for frm in s2
    for to in s3
]
edgeArray9 = [
    (frm, to, None, randint(1, 10))
    for frm in s2
    for to in s4
]
edgeArray10 = [
    (to, frm, None, randint(1, 10))
    for frm in s2
    for to in s4
]
edgeArray11 = [
    (frm, to, None, randint(1, 10))
    for frm in s3
    for to in s4
]
edgeArray12 = [
    (to, frm, None, randint(1, 10))
    for frm in s3
    for to in s4
]

edgeArray = edgeArray1 + edgeArray2 + edgeArray3 + edgeArray4 + edgeArray5 + edgeArray6 + edgeArray7 + edgeArray8 + edgeArray9 + edgeArray10 + edgeArray11 + edgeArray12

for k in edgeArray:
    print(k)

print(meldSubtours(edgeArray, subtours))
