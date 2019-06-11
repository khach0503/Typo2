import codecs

class Context:
    prepre = "";
    pre = "";
    token = "";
    next = "";
    nextnext = "";

def StrIn(strin):
    strOut = ""
    list = []
    ldc = [",", ".", "?", "!"]
    for x in strin:
        if x in ldc:
            list.append(strOut)
            strOut = ""
            list.append(x)
            continue
        elif x.isspace():
            if strOut == "":
                continue
            list.append(strOut)
            strOut = ""
        else:
            strOut = strOut + x
    return list

def lstToken(lstin):
    lstCtx = []
    ldc = [",", ".", "?", "!"]
    for x in range(len(lstin)):
        if x == 0:
            tok = Context()
            tok.token = lstin[x]
            if lstin[x+1] not in ldc:
                tok.next = lstin[x+1]
            if lstin[x+2] not in ldc:
                tok.nextnext = lstin[x+2]
            lstCtx.append(tok)
        elif x == 1 and lstin[x] not in ldc:
            tok = Context()
            tok.token = lstin[x]
            if lstin[x+1] not in ldc:
                tok.next = lstin[x+1]
            if lstin[x+2] not in ldc:
                tok.nextnext = lstin[x+2]
            if lstin[x-1] not in ldc:
                tok.pre = lstin[x-1]
            lstCtx.append(tok)
        elif x == len(lstin) - 2 and lstin[x] not in ldc:
            tok = Context()
            tok.token = lstin[x]
            if lstin[x+1] not in ldc:
                tok.next = lstin[x+1]
            if lstin[x-2] not in ldc:
                tok.prepre = lstin[x-2]
            if lstin[x-1] not in ldc:
                tok.pre = lstin[x-1]
            lstCtx.append(tok)
        elif x == len(lstin) - 1 and lstin[x] not in ldc:
            tok = Context()
            tok.token = lstin[x]
            if lstin[x-2] not in ldc:
                tok.prepre = lstin[x-2]
            if lstin[x-1] not in ldc:
                tok.pre = lstin[x-1]
            #print("hello")
            lstCtx.append(tok)
        else:
            if lstin[x] not in ldc:
                tok = Context()
                tok.token = lstin[x]
                if lstin[x+1] not in ldc:
                    tok.next = lstin[x+1]
                if lstin[x+2] not in ldc:
                    tok.nextnext = lstin[x+2]
                if lstin[x-2] not in ldc:
                    tok.prepre = lstin[x-2]
                if lstin[x-1] not in ldc:
                    tok.pre = lstin[x-1]
                lstCtx.append(tok)
    return lstCtx
  
def fixit(tokenin):
    tokentmp = tokenin
    amtietfile = codecs.open("filteredUni.txt", encoding="utf-8")
    amtiet = amtietfile.read()
    dtrfile = codecs.open("bigram.txt", encoding="utf-8")
    dtr = dtrfile.read()
    #if (tokentmp[4].token + " ") in amtiet:
     #   print("yes")
    for x in range(len(tokentmp)):
        if (tokentmp[x].token + " ") not in amtiet:
            if tokentmp[x].token not in dtr:
                bipre = tokentmp[x].pre + " " + tokentmp[x].token
                binext = tokentmp[x].token + " " + tokentmp[x].next
                if bipre.isupper() or binext.isupper():
                else:
                    candi = candidate(tokentmp[x])
                    if len(candi) > 0 and candi[0] != tokentmp[x].token:
                        tokentmp[x].token = candi[0]
        else:
            if checkerror(tokentmp[x]) == True:
                candi = candidate(tokentmp[x])
                if len(candi) > 0 and candi[0] != tokentmp[x].token:
                    tokentmp[x].token = candi[0]
    return tokentmp

def checkerror(tokin):
    tokin.prepre.lower()
    tokin.pre.lower()
    tokin.token.lower()
    tokin.next.lower()
    tokin.nextnext.lower()
    biprecount = 0
    binextcount = 0
    #if tokin.token in compnoun:
        #return False
    bipre = tokin.pre + " " + tokin.token
    binext = tokin.token + " " + tokin.next
    with codecs.open("bigram_word.txt", "r", encoding="utf8") as file:
        for line in file:
            x = 0
            space = 0
            subword = ""
            subnum = 0
            while space < 2:
                if line[x] != " ":
                    subword = subword + line[x]
                    x+=1
                else:
                    if space < 1:
                        space+=1
                        subword = subword + line[x]
                        x+=1
                    else:
                        space+=1
                        x+=1
            subnum = int(line[x:])
            #print(subword)
            if bipre == subword:
                biprecount = subnum
            if binext == subword:
                binextcount = subnum
    tri1 = tokin.pre + " " + tokin.token + " " + tokin.next
    tri2 = tokin.prepre + " " + tokin.pre + " " + tokin.token
    tri3 = tokin.token + " " + tokin.next + " " + tokin.nextnext
    print(str(biprecount) + " " + str(binextcount))
    if tokin.pre == "" and tokin.next == "":
        return False
    if tokin.pre != "" and tokin.next == "" and biprecount < 50:
        return True
    if tokin.pre == "" and tokin.next != "" and binextcount < 50:
        return True
    if tokin.pre != "" and tokin.next != "" and (biprecount < 50 or binextcount < 50):
        return True
    return False
	
def candidate(tokin):
    context = tokin
    result = []
    candidates_filter = {}
    candidates = {}
    dicCandidateByTransform = {}
	dicCandidateByTransform[context.token] = 0
    change_phuam()
    change_amkep()
    change_dau()
	
    #buoc 1: bien doi tu
    biendoi = dicCandidateByTransform
    candidates = filterCandidate(context, biendoi)
    
    #buoc 2: bien doi + doi dau
    if len(candidates) == 0:
        candidates_filter.clear()
		
        #am kep -> doi dau
        dicCandidateByTransform.clear()
        dicCandidateByTransform[context.token.lower()] = 0
        change_amkep();
        

stringin = "Xin chào tất cả mọi người. Tôi là ai?"
listWord = StrIn(stringin)
print(listWord)
listToken = lstToken(listWord)
print(listToken[2].token)
print(checkerror(listToken[4]))
fixit(listToken)