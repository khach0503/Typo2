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

dicCandidateByTransform = {}
def candidate(tokin):
    amtietfile = codecs.open("filteredUni.txt", encoding="utf-8")
    amtiet = amtietfile.read()
    context = tokin
    result = []
    candidates_filter = {}
    candidates = {}
    dicCandidateByTransform.clear()
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
        amkep_dau = change_thaydau(dicCandidateByTransform)
        for i in amkep_dau.keys:
            if i not in candidates_filter:
                candidates_filter[i] = amkep_dau[i]
            else:
                if candidates_filter[i] > amkep_dau[i]:
                    candidates_filter[i] = amkep_dau[i]
                    
        #bien doi xoa
        xoa = change_delete(context.token.lower())
        for i in xoa.keys:
            if i not in candidates_filter:
                candidates_filter[i] = xoa[i]
            else:
                if candidates_filter[i] > xoa[i]:
                    candidates_filter[i] = xoa[i]
                    
        candidates = filterCandidate(context, candidates_filter)
        
    if len(candidates) > 0 and list(candidates.keys)[0] > 0:
        result.append(list(candidates)[0])
    else:
        if len(context.pre) + len(context.next) > 0:
            if countngram(context.token.lower()) == 0:
                result.append("")
    return result
    
    if len(candidates) > 0 and list(candidates.keys)[0] > 0:
        result.append(list(candidates)[0])
    else:
        if countngram(context.token.lower()) == 0:
            result.append("-")
        else:
            result.append("")
    return result
    
def change_phuam()
    lstTransform = []
    candidate = ""
    lstTransform.append("s-x:0.1")
    lstTransform.append("x-s:0.1")
    lstTransform.append("ch-tr:0.1")
    lstTransform.append("tr-ch:0.1")
    lstTransform.append("l-n:0.3")
    lstTransform.append("n-l:0.3")
    lstTransform.append("d-gi:0.2")
    lstTransform.append("gi-d:0.2")
    lstTransform.append("r-d:0.2")
    lstTransform.append("d-r:0.2")
    lstTransform.append("r-gi:0.2")
    lstTransform.append("gi-r:0.2")
    lstTransform.append("dd-đ:0.5")
    lstTransform.append("d-đ:0.8")
    lstTransform.append("i-y:0.1")
    lstTransform.append("y-i:0.1")
    lstTransform.append("ng-ngh:0.3")
    lstTransform.append("ngh-ng:0.3")
    lstTransform.append("k-c:0.5")
    lstTransform.append("o-ô:0.5")
    
    lst = list(dicCandidateByTransform.keys)
    for cand in lst:
        for trans in lstTransform:
            if trans.index("k-c") > -1 and cand.index("kh") > -1:
                continue
            score = float(trans.split(":")[1])
            word = trans.split(":")[0].split("-")
            
            candidate = cand.replace(word[0], word[1])
            if cand != candidate:
                if candidate not in dicCandidateByTransform:
                    dicCandidateByTransform[candidate] = score
                else:
                    dicCandidateByTransform[candidate] += score
                    
def change_amkep():
    lstTransform = []
    candidate = ""
    lstTransform.append("aa-â:0.05")
    lstTransform.append("ee-ê:0.05")
    lstTransform.append("oo-ô:0.05")
    lstTransform.append("aw-ă:0.05")
    lstTransform.append("ow-ơ:0.05")
    lstTransform.append("uw-ư:0.05")
    
    lst = list(dicCandidateByTransform.keys)
    for cand in lst:
        for trans in lstTransform:
            score = float(trans.split(":")[1])
            word = trans.split(":")[0].split("-")
            
            candidate = cand.replace(word[0], word[1])
            if cand != candidate:
                if candidate not in dicCandidateByTransform:
                    dicCandidateByTransform[candidate] = score
                else:
                    dicCandidateByTransform[candidate] += score
                    
def change_dau():
    lstTransform = []
    candidate = ""
    lstTransform.append("as-á:0.2")
    lstTransform.append("af-à:0.2")
    lstTransform.append("ar-ả:0.2")
    lstTransform.append("ax-ã:0.2")
    lstTransform.append("aj-ạ:0.2")

    lstTransform.append("ăs-ắ:0.2")
    lstTransform.append("ăf-ằ:0.2")
    lstTransform.append("ăr-ẳ:0.2")
    lstTransform.append("ăx-ẵ:0.2")
    lstTransform.append("ăj-ặ:0.2")

    lstTransform.append("âs-ấ:0.2")
    lstTransform.append("âf-ầ:0.2")
    lstTransform.append("âr-ẩ:0.2")
    lstTransform.append("âx-ẫ:0.2")
    lstTransform.append("âj-ậ:0.2")

    lstTransform.append("is-í:0.2")
    lstTransform.append("if-ì:0.2")
    lstTransform.append("ir-ỉ:0.2")
    lstTransform.append("ix-ĩ:0.2")
    lstTransform.append("ij-ị:0.2")

    lstTransform.append("es-é:0.2")
    lstTransform.append("ef-è:0.2")
    lstTransform.append("er-ẻ:0.2")
    lstTransform.append("ex-ẽ:0.2")
    lstTransform.append("ej-ẹ:0.2")

    lstTransform.append("ês-ế:0.2")
    lstTransform.append("êf-ề:0.2")
    lstTransform.append("êr-ể:0.2")
    lstTransform.append("êx-ễ:0.2")
    lstTransform.append("êj-ệ:0.2")

    lstTransform.append("os-ó:0.2")
    lstTransform.append("of-ò:0.2")
    lstTransform.append("or-ỏ:0.2")
    lstTransform.append("ox-õ:0.2")
    lstTransform.append("oj-ọ:0.2")

    lstTransform.append("ôs-ố:0.2")
    lstTransform.append("ôf-ồ:0.2")
    lstTransform.append("ôr-ổ:0.2")
    lstTransform.append("ôx-ỗ:0.2")
    lstTransform.append("ôj-ộ:0.2")

    lstTransform.append("ơs-ớ:0.2")
    lstTransform.append("ơf-ờ:0.2")
    lstTransform.append("ơr-ở:0.2")
    lstTransform.append("ơx-ỡ:0.2")
    lstTransform.append("ơj-ợ:0.2")

    lstTransform.append("us-ú:0.2")
    lstTransform.append("uf-ù:0.2")
    lstTransform.append("ur-ủ:0.2")
    lstTransform.append("ux-ũ:0.2")
    lstTransform.append("uj-ụ:0.2")

    lstTransform.append("ưs-ứ:0.2")
    lstTransform.append("ưf-ừ:0.2")
    lstTransform.append("ưr-ử:0.2")
    lstTransform.append("ưx-ữ:0.2")
    lstTransform.append("ưj-ự:0.2")
    
    lst = list(dicCandidateByTransform.keys)
    for cand in lst:
        for trans in lstTransform:
            score = float(trans.split(":")[1])
            word = trans.split(":")[0].split("-")
            
            candidate = cand.replace(word[0], word[1])
            if cand != candidate:
                if candidate not in dicCandidateByTransform:
                    dicCandidateByTransform[candidate] = score
                else:
                    dicCandidateByTransform[candidate] += score
                    
def filterCandidate(context, lstCandidates):

                
    
def countngram(stin):
    so = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    amtietfile = codecs.open("filteredUni.txt", encoding="utf-8")
    amtiet = amtietfile.read()
    index = amtiet.index(stin) + len(stin) + 1
    ret = amtiet(index)
    i = index + 1
    while amtiet[i] in so:
        ret = ret + amtiet[i]
        i += 1
    return int(ret)

stringin = "Xin chào tất cả mọi người. Tôi là ai?"
listWord = StrIn(stringin)
print(listWord)
listToken = lstToken(listWord)
print(listToken[2].token)
print(checkerror(listToken[4]))
fixit(listToken)