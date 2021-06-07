from collections import defaultdict
from itertools import combinations

def getItemsetFromList(data):
    candidate = set()    
    transactions = defaultdict(list)
    for i in range(len(data)):
        itemSet = data[i]
        for item in itemSet[1]:
            candidate.add(frozenset([item]))
            transactions[frozenset([item])].append(i)

    return candidate, transactions
    
def getAboveMinSup(k,min_supp, min_t_supp, max_t_supp, candidate,trans,data,globalItemSetWithSup,globalItemSetWithLS):
    freqItemSet = set()
    localItemSetWithSup = defaultdict(int)
    localItemSetWithLS = defaultdict(list)

    temp = candidate.copy()

    for item in temp:
        for i in trans[item]:
            itemset = data[i]
            if item.issubset(itemset[1]):
                localItemSetWithSup[item] += 1
                globalItemSetWithSup[item] += 1


                localItemSetWithLS[item].append(itemset[0])
                globalItemSetWithLS[item] = localItemSetWithLS[item]


    for item in candidate:

        if len(localItemSetWithLS[item]) > 0:
        
            LS = max(localItemSetWithLS[item])-min(localItemSetWithLS[item])+1
            SP = float(localItemSetWithSup[item]/LS)


            if LS > max_t_supp or LS < min_t_supp or SP < min_supp:
                del globalItemSetWithLS[item]
            else:
                freqItemSet.add(item)

    return freqItemSet

def getUnion(itemSet, trans, length):
    unionSet = set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])
    for item in unionSet:
        for i in item:
            trans[item] = list(set(trans[item]) | set(trans[frozenset({i})]))

    return unionSet, trans

def pruning(candidate, prevFreqSet, length):
    temp = candidate.copy()
    for item in candidate:
        subsets = combinations(item,length)
        for subset in subsets:
            if frozenset(subset) not in prevFreqSet:
                temp.remove(item)
                break

    return temp

def apriori(data, min_supp, min_t_supp, max_t_supp):
    candidate, transactions = getItemsetFromList(data)

    ## Final result global frequent itemset
    freqItemsets = []
    ## Storing global itemset with support count and LS
    globalItemSetWithSup = defaultdict(int)
    globalItemSetWithLS = defaultdict(list)
    globLS = defaultdict(list)
    # print("# single words: "+ str(len(transactions)))
    
    L1ItemSet = getAboveMinSup(1, min_supp, min_t_supp, max_t_supp, candidate,transactions,data,globalItemSetWithSup,globalItemSetWithLS)
    # print("k: 1 # good words: {}".format(str(len(L1ItemSet))))

    for i in globalItemSetWithLS:
        j = ' '.join(ele for ele in list(i))
        globLS[j] = globalItemSetWithLS[i]

    currLSet = L1ItemSet
    k=2
    
    while(currLSet):

        candidate, transactions = getUnion(currLSet,transactions,k)
        candidate = pruning(candidate, currLSet, k-1)

        currLSet = getAboveMinSup(k, min_supp, min_t_supp, max_t_supp, candidate,transactions,data,globalItemSetWithSup,globalItemSetWithLS)
        # print("k: {} # good words: {}".format(k,str(len(currLSet))))
        # print(currLSet)
        if k>1:
            c = [set(i) for i in currLSet]
            freqItemsets.extend(c)
        k+=1

    print("Finished apriori")
    print("Number of frequent itemsets: ",len(freqItemsets))

    return freqItemsets, globLS, globalItemSetWithSup 