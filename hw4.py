import argparse

def hashtable(seq,k):
    dict = {'A': [], 'C': [], 'G': [],'T':[]}
    for i in range(0,len(seq)-(k-1)):
        if(seq[i]=='A'):
            dict['A'].append([seq[i:i+k],i])
        if(seq[i]=='C'):
            dict['C'].append([seq[i:i+k],i])
        if(seq[i]=='G'):
            dict['G'].append([seq[i:i+k],i])
        if(seq[i]=='T'):
            dict['T'].append([seq[i:i+k],i])
    return dict

def indextable(hash,quer,k):
    #how many queries are there
    dimrowquer=len(quer)
    newhash=hash
    #for each query
    A=hash['A']
    G=hash['G']
    C=hash['C']
    T=hash['T']
    loc=[]
    for t in range(0,len(A)):
        for col in range(0,dimrowquer):
            newhash['A'][t].append(-1)
    for t in range(0,len(C)):
        for col in range(0,dimrowquer):
            newhash['C'][t].append(-1)
    for t in range(0,len(G)):
        for col in range(0,dimrowquer):
            newhash['G'][t].append(-1)
    for t in range(0,len(T)):
        for col in range(0,dimrowquer):
            newhash['T'][t].append(-1)
    for i in range(0,dimrowquer):
        rowquer=quer[i][:]

        for z in range(0,len(rowquer)):

            rsend=rowquer[z:z+k]
            if(rowquer[z]=='A'):

                for j in range(0,len(A)):

                    Asend=A[j][0]


                    if(rsend==Asend):
                        newhash['A'][j][i+2]=z
                        var=newhash['A'][j]

                        loc.append(var)
            if(rowquer[z]=='C'):
                for j in range(0,len(C)):
                    Csend=C[j][0]

                    if(rsend==Csend):
                        newhash['C'][j][i+2]=z
                        var=newhash['C'][j]

                        loc.append(var)

            if(rowquer[z]=='G'):
                for j in range(0,len(G)):
                    Gsend=G[j][0]

                    if(rsend==Gsend):
                        newhash['G'][j][i+2]=z
                        var=newhash['G'][j]

                        loc.append(var)

            if(rowquer[z]=='T'):
                for j in range(0,len(T)):
                    Tsend=T[j][0]

                    if(rsend==Tsend):
                        newhash['T'][j][i+2]=z
                        var=newhash['T'][j]

                        loc.append(var)


        for l in range(0,len(loc)):
            if((len(loc[l])==i+2) ):
                #print(i,loc[l])
                loc[l].append(-1)

    return loc
def seedextend(locationtable,query,T,k,threshold):
    dimrowquer=len(query)
    x=len(locationtable)
    scoreprev=k
    noquery=len(locationtable[0])-2
    fintable=[]
    output=[]

    for i in range(0,noquery):

        lookedquery=query[i]

        for j in range(0,len(locationtable)):
            if( locationtable[j][1]>-1 and locationtable[j][i+2]>-1):
                seed=scorethreshold(T,lookedquery,locationtable[j][1],locationtable[j][i+2],scoreprev,k)
                prevseed=seed
                score=seed[3]

                while(seed[3]>=score and seed[3]!=-1 ):
                    prevseed=seed
                    score=seed[3]

                    seed=scorethreshold(T,lookedquery,seed[0],seed[1],seed[3],seed[2])


                prevseed.append(locationtable[j][0])
                prevseed.append(i)

                fintable.append(prevseed)
    for x in range(0,len(fintable)):
        if(fintable[x][3]>=threshold):
            output.append(fintable[x])
    return output
def scorethreshold(T,quer,indexT,indexQ,prevscore,length):
    go=[]
    k=length
    #only right
    if((indexQ==0 or indexT==0)and (indexT+k<len(T) and indexQ+k<len(quer))):
        if(T[indexT+k]==quer[indexQ+k]):
            score=prevscore+1

            go=[indexT,indexQ,length+1,score,T[indexT:indexT+length+1],quer[indexQ:indexQ+length+1]]
            return go
        else:
            score=prevscore-1
            go=[indexT,indexQ,length+1,score,T[indexT:indexT+length+1],quer[indexQ:indexQ+length+1]]
            return go
    #only left
    elif(((indexQ>len(quer)-(k+1))or (indexT>len(T)-(k+1))) and indexQ>0):
        if(T[indexT-1]==quer[indexQ-1]):
            score=prevscore+1
            go=[indexT-1,indexQ-1,length+1,score,T[indexT-1:indexT+length],quer[indexQ-1:indexQ+length]]
            return go
        else:
            score=prevscore-1
            go=[indexT-1,indexQ-1,length+1,score,T[indexT-1:indexT+length],quer[indexQ-1:indexQ+length]]
            return go
    #left and right
    elif(indexQ>0 and indexT>0 and (indexT+length<len(T) and indexQ+length<len(quer))):
        #all equal
        if(T[indexT+length]==quer[indexQ+length] and T[indexT-1]==quer[indexQ-1] ):
            score=prevscore+2
            go=[indexT-1,indexQ-1,length+2,score,T[indexT-1:indexT+length+1],quer[indexQ-1:indexQ+length+1]]
            return go
        elif((T[indexT+length]==quer[indexQ+length] and T[indexT-1]!=quer[indexQ-1]) or (T[indexT+length]!=quer[indexQ+length] and T[indexT-1]==quer[indexQ-1])):
            score=prevscore
            go=[indexT-1,indexQ-1,length+2,score,T[indexT-1:indexT+length+1],quer[indexQ-1:indexQ+length+1]]
            return go
        else:
            score=prevscore-200
            go=[indexT-1,indexQ-1,length+2,score,T[indexT-1:indexT+length+1],quer[indexQ-1:indexQ+length+1]]
            return go
    else:
        go=[indexT,indexQ,length,-1,T[indexT-1:indexT+length+2],quer[indexQ-1:indexQ+length+1]]
        return go
def allign(nod,T,query):
    no=-1
    for i in range(0,len(nod)):
        str=""
        if(no!=nod[i][7] ):
            print("-------------------","sequence",nod[i][7],"---------------------------")
            no=nod[i][7]
        q=query[nod[i][7]]
        for x in range(0,nod[i][2]):
            if(T[nod[i][0]+x]!=q[nod[i][1]+x]):
                str=str+'-'
            else:
                str=str+T[nod[i][0]+x]
        print("reference: ",nod[i][0]," ",T[nod[i][0]:nod[i][0]+nod[i][2]]," ",nod[i][0]+nod[i][2])
        print("allign:            ",str)
        print("query:     " ,nod[i][1],"    ",q[nod[i][1]:nod[i][1]+nod[i][2]]," ",nod[i][1]+nod[i][2])




def write(nod,query):
    
    seq = []
    for i in range(0, len(query)):
        seq.append('-')
    for i in range(0, len(nod)):
        index = nod[i][7]
        if(seq[index] == '-' or seq[index] > nod[i][0]):
            seq[index] = nod[i][0]
    return seq      
    

#main function
if __name__=="__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("--ref")
    parser.add_argument("--qry")
    parser.add_argument("--k")
    parser.add_argument("--s")
    
    args = parser.parse_args()
    file1Name = args.ref
    file2Name = args.qry
    k = int(args.k)
    s = int(args.s)

    #reading sequence
    file1 = open(file1Name, 'r')
    Lines = file1.readlines()
    T = ""
    for line in Lines[1:]:
        T = T+line.strip()
    #reading query

    file2 = open(file2Name, 'r')
    lines2 = file1.readlines()
    Q=[]
    st=""
    with open(file2Name) as file:
        for line1 in file:
            if(line1[0] == '>'):
                if(len(st)!=0):

                    Q.append(st)
                st = ""
            else:
                st = st + line1.strip()
        Q.append(st)
    testquery=Q

    h=hashtable(T,k)
    f=indextable(h,testquery,k)
    resss=seedextend(f,testquery,T,k,s)
    nod=[]

    for i in resss:
        if i not in nod:
            nod.append(i)

    output=write(nod,testquery)


    for i in range(0,len(output)):
        print("> Seq",i,": ",output[i])
    #print(allign(nod,T,testquery))
