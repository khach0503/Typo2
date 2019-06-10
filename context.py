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
"""    
def fixit(tokenin)
    tokentmp = tokenin
    for x in range(len(tokentmp)):
        if tokentmp[x].token not in amtiet:
            if tokentmp[x].token not in dtr and tokentmp[x].token not in tdb:
                if 2 gram viet hoa:
                else:
                    candi = candidate(tokentmp[x].token)
                    if len(candi) > 0 and candi[0] != tokentmp[x].token:
                        tokentmp[x].token = candi[0]
        else:
            if checkerror(tokentmp[x]) == true:
                candi = candidate(tokentmp[x].token)
                if len(candi) > 0 and candi[0] != tokentmp[x].token:
                    tokentmp[x].token = candi[0]
    return tokentmp"""

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
    with open("bigram_word.txt") as file:
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

strin = "Xin chào a bank tất cả mọi người. Tôi là ai?"
listWord = StrIn(strin)
print(listWord)
listToken = lstToken(listWord)
print(listToken[2].token)
print(checkerror(listToken[5]))