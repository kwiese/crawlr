# distutils: language=c++

from libcpp.algorithm cimport sort as stdsort
from libcpp.vector cimport vector
from libcpp.string cimport string

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

    while(ledges > 0):
        start = edges[0][0]
        to = edges[0][1]
        subtour = [ start ]
        del edges[0]
        ledges -= 1
        while to != start:
            subtour.append(to)
            for i in range(ledges):
                x = edges[i]
                frm = x[0]
                n = x[1]
                if frm == to:
                    seen.push_back(i)
                    to = n
                    break
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
