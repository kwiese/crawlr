# distutils: language=c++

from libcpp.algorithm cimport sort as stdsort
from libcpp.vector cimport vector
from libcpp.string cimport string

def meldSubtours(edgeArray, subtours):
    if len(subtours) == 1:
        return subtours

    elif len(subtours) == 2:

        s1 = subtours[0]
        s2 = subtours[1]

        metaTour = []

        s1ToS2 = (None, None, float('inf'))
        s2ToS1 = (None, None, float('inf'))
        best = float('inf')

        for i in range(len(s1)):
            p1 = s1[i]
            p2 = s1[((i+1) % len(s1))]
            for j in range(len(s2)):
                q1 = s2[j]
                q2 = s2[((j+1) % len(s2))]

                q1p2 = None
                p1q2 = None
            
                for k in range(len(edgeArray)):
                    frm = edgeArray[k][0]
                    to = edgeArray[k][1]

                    if frm == q1 and to == p2:
                        q1p2 = edgeArray[k][3]
                        if p1q2 is not None:
                            break
                    elif frm == p1 and to == q2:
                        p1q2 = edgeArray[k][3]
                        if q1p2 is not None:
                            break
                
                if (q1p2 + p1q2) < best:
                    best = (q1p2 + p1q2)
                    s1ToS2 = (p1, q2, p1q2)
                    s2ToS1 = (q1, p2, q1p2)
        
        for i in range(len(s1)):
            p = s1[i]
            metaTour.append(p)
            if p == s1ToS2[0]:
                j = 0
                for k in range(len(s2)):
                    if s2[k] == s1ToS2[1]:
                        j = k
                        break
                for k in range(len(s2)):
                    ind = (j + k) % len(s2)
                    q = s2[ind]
                    metaTour.append(q)
        
        return metaTour

    else:
        l = int(len(subtours)/2)
        m1 = meldSubtours(edgeArray, subtours[:l])
        m2 = meldSubtours(edgeArray, subtours[l:])
        return meldSubtours(edgeArray, [m1, m2])

def collectSubtoursFast(edgeArray, int length):
    cdef int ledges = 0
    cdef int i
    edges = []
    for i in range(length):
        if edgeArray[i][2].X:
            edges.append((edgeArray[i][0], edgeArray[i][1]))
            ledges += 1
 
    subtours = []
    cdef int j
    cdef vector[int] seen
    cdef int exists

    while(ledges > 0):
        start = edges[0][0]
        to = edges[0][1]
        subtour = [ start ]
        del edges[0]
        ledges -= 1
        while to != start:
            subtour.append(to)
            exists = 0
            for i in range(ledges):
                x = edges[i]
                frm = x[0]
                n = x[1]
                if frm == to:
                    seen.push_back(i)
                    to = n
                    exists = 1
                    break
            if exists == 0:
                return []
        subtours.append(subtour)
        stdsort(seen.begin(), seen.end())
        while not seen.empty():
            x = seen.back()
            del edges[x]
            ledges -= 1
            seen.pop_back()

    return subtours

def collectRelated(subtour, edgeArray):
    inBound = []
    outBound = []
    for i in range(len(subtour)):
        for j in range(len(edgeArray)):
            if edgeArray[j][1] == subtour[i] and edgeArray[j][0] not in subtour:
                inBound.append(edgeArray[j][2])
            elif edgeArray[j][0] == subtour[i] and edgeArray[j][1] not in subtour:
                outBound.append(edgeArray[j][2])
    return (inBound, outBound)

def collectSubtoursFastTest(edges, int length):
#    cdef int ledges = 0
    cdef int ledges = length
    cdef int i
    #edges = []
    #for i in range(length):
    #    if edgeArray[i][2].X:
    #        edges.append((edgeArray[i][0], edgeArray[i][1]))
    #        ledges += 1
 
    subtours = []
    cdef int j
    cdef vector[int] seen
    cdef int exists

    while(ledges > 0):
        start = edges[0][0]
        to = edges[0][1]
        subtour = [ start ]
        del edges[0]
        ledges -= 1
        while to != start:
            subtour.append(to)
            exists = 0
            for i in range(ledges):
                x = edges[i]
                frm = x[0]
                n = x[1]
                if frm == to:
                    seen.push_back(i)
                    to = n
                    exists = 1
                    break
            if exists == 0:
                return []
        subtours.append(subtour)
        stdsort(seen.begin(), seen.end())
        while not seen.empty():
            x = seen.back()
            del edges[x]
            ledges -= 1
            seen.pop_back()

    return subtours
