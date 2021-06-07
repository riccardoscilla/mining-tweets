from collections import defaultdict

class Node:
    def __init__(self, itemName, frequency, parentNode):
        self.itemName = itemName
        self.count = frequency
        self.parent = parentNode
        self.children = {}
        self.time = []
        self.next = None

    def increment(self, frequency):
        self.count += frequency

    def display(self, ind=1):
        print('  ' * ind, self.itemName, ' ', self.count, ' ', self.time)
        for child in list(self.children.values()):
            child.display(ind+1)

#########################################################################

def getFrequencyFromList(itemSetList):
    frequency = [1 for i in range(len(itemSetList))]
    return frequency

#########################################################################

def constructTree(data, frequency, min_sup,  min_t_sup, max_t_supp):
    # Counting frequency and create header table
    headerTable = defaultdict(int)
    supportTable = defaultdict(float)
    LSTable = defaultdict(list)

    # Store count of each item and the time it appears
    for idx, itemset in enumerate(data):
        for item in itemset[1]:
            headerTable[item] += frequency[idx]
            LSTable[item].append(itemset[0])

    # Deleting items below minSup and TS or its support
    tmp = headerTable.copy()
    for item in tmp:
        
        LS = max(LSTable[item])-min(LSTable[item])+1
        SP = float(headerTable[item]/LS)

        if LS > max_t_supp or LS < min_t_sup or SP < min_sup:
            del headerTable[item]
            del LSTable[item]
        else:
            supportTable[item] = SP
    
    if len(headerTable) == 0:
        return None, None, None, None

    # HeaderTable column [Item: [frequency, headNode]]
    for item in headerTable:
        headerTable[item] = [headerTable[item], None]

    # Init Null head node
    fpTree = Node('Null', 1, None)
    
    # Update FP tree for each cleaned and sorted itemSet
    for idx, itemset in enumerate(data):
        itemset[1] = [item for item in itemset[1] if item in headerTable] # consider only freq items 
        itemset[1].sort(key=lambda item: (supportTable[item],headerTable[item][0],item), reverse=True) # sort by Supp (decr order)
        
        # update the tree by appending each itemset as a new branch
        currentNode = fpTree
        for item in itemset[1]:  
            currentNode = updateTree(item, currentNode, headerTable, frequency[idx])    
            currentNode.time.append(itemset[0])

    return fpTree, headerTable, supportTable, LSTable


#########################################################################

def updateTree(item, treeNode, headerTable, frequency):
    if item in treeNode.children:
        # If the item already exists, increment its count
        treeNode.children[item].increment(frequency)
    else:
        # Create a new branch
        newItemNode = Node(item, frequency, treeNode)
        treeNode.children[item] = newItemNode
        # Link the new branch to header table
        updateHeaderTable(item, newItemNode, headerTable)

    return treeNode.children[item]

#########################################################################

def updateHeaderTable(item, targetNode, headerTable):
    if(headerTable[item][1] == None):
        headerTable[item][1] = targetNode
    else:
        currentNode = headerTable[item][1]
        # Traverse to the last node then link it to the target
        while currentNode.next != None:
            currentNode = currentNode.next
        currentNode.next = targetNode

#########################################################################

def mineTree(headerTable, supportTable, min_sup, min_t_sup, max_t_supp, preFix, freqItemList):
    # Sort the items with frequency and create a list
    sortedItemList = sorted(list(supportTable), key=lambda item: (supportTable[item],headerTable[item][0],item))

    # Start with the lowest frequency
    for item in sortedItemList:
        
        # Pattern growth is achieved by the concatenation of suffix pattern with frequent patterns generated from conditional FP-tree
        newFreqSet = preFix.copy()
        newFreqSet.add(item)
        if len(newFreqSet)>1:
            freqItemList.append(newFreqSet)
        
        # Find all prefix path, construct conditional pattern base
        conditionalPattBase, frequency = findPrefixPath(item, headerTable)

        # Construct conditonal FP Tree with conditional pattern base
        _, newHeaderTable, newsupportTable, _ = constructTree(conditionalPattBase, frequency, min_sup, min_t_sup, max_t_supp) 

        if newHeaderTable != None:
            # Update global support dict (to compute confidence)
            for i in newsupportTable:
                key = tuple(list(preFix)+[item,i])
                globSup[frozenset(key)] = newsupportTable[i]

            # Mining recursively on the tree
            mineTree(newHeaderTable, newsupportTable, min_sup, min_t_sup, max_t_supp, newFreqSet, freqItemList)

#########################################################################

def findPrefixPath(basePat, headerTable):
    # First node in linked list
    treeNode = headerTable[basePat][1] 
    condPats = []
    frequency = []
    while treeNode != None:
        prefixPath = []
        # From leaf node all the way to root
        ascendFPtree(treeNode, prefixPath)  
        if len(prefixPath) > 1:
            # Storing the prefix path and it's corresponding count
            for t in treeNode.time:
                condPats.append([t, prefixPath[1:]])
                frequency.append(int(treeNode.count/len(treeNode.time)))

        # Go to next node
        treeNode = treeNode.next  

    return condPats, frequency

#########################################################################

def ascendFPtree(node, prefixPath):
    if node.parent != None:
        prefixPath.append(node.itemName)
        ascendFPtree(node.parent, prefixPath)

#########################################################################

def fpgrowth(data, min_sup,  min_t_sup, max_t_supp):
    global globSup
    global globLS

    globSup = defaultdict(float)

    frequency = getFrequencyFromList(data)

    fpTree, headerTable, supportTable, LSTable = constructTree(data, frequency, min_sup, min_t_sup, max_t_supp)    

    if(fpTree == None):
        print('No frequent item set')
        return None, None, None
    else:
        # append global info of 1-frequentset
        globLS = LSTable

        for item in supportTable:
            globSup[frozenset([item])] = supportTable[item]

        freqItemsets = []
        mineTree(headerTable, supportTable, min_sup, min_t_sup, max_t_supp, set(), freqItemsets)

        print("Finished mining")
        print("Number of frequent itemsets: ",len(freqItemsets))
        
        return freqItemsets, globLS, globSup
