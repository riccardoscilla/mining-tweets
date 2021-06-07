
import collections

def flatten(x):
    if isinstance(x, collections.Iterable):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]


class FPTree(object):

    def __init__(self):
        self.root = Node(None, 0, {})
        self.summaries = {}

    def __repr__(self):
        return repr(self.root)

    def add(self, transaction, count):
        time = transaction[0]
        basket = transaction[1]

        print(transaction)

        curr = self.root
        curr.count += count

        for item in basket:
            if item in self.summaries:
                summary = self.summaries.get(item)
            else:
                summary = Summary(0,set())
                self.summaries[item] = summary
            summary.count += count

            if item in curr.children:
                child = curr.children.get(item)
            else:
                child = Node(item, 0, {})
                curr.addChild(child)
            summary.nodes.add(child)
            child.count += count
            child.time.extend([time])
            curr = child
        return self

    def getTransactions(self):
        return [x for x in self.root._getTransactions()]

    def merge(self,tree):
        print(tree.getTransactions())
        for t in tree.getTransactions():
            # print(t)
            self.add(t[0],t[1])
        self.flatTimes(self.root)
        return self

    def flatTimes(self, node):
        node.time = list(set(flatten(node.time)))
        for v in node.children.values():
            self.flatTimes(v)

    def project(self,itemId):
        newTree = FPTree()
        summaryItem = self.summaries.get(itemId)
        if summaryItem:
            for element in summaryItem.nodes:
                t = []
                curr = element.parent
                while curr.parent:
                    t.insert(0,curr.item)
                    curr = curr.parent
                newTree.add(t,element.count)
        return newTree

    def extract(self, minCount, isResponsible = lambda x:True, maxLength=None):
        for item,summary in self.summaries.items():
            if (isResponsible(item) and summary.count >= minCount):
                yield ([item],summary.count)
                for element in self.project(item).extract(minCount, maxLength=maxLength):
                    if maxLength==None or len(element[0])+1<=maxLength:
                        yield ([item]+element[0],element[1])


class Node(object):

    def __init__(self, item, count, children):
        self.item = item
        self.count = count
        self.time = []
        self.children = children #dictionary of children
        self.parent = None

    def __repr__(self):
        return self.toString(0)

    def toString(self, level=0):
        if self.item == None:
            s = "\nRoot("
        else:
            # self.time = list(set(flatten(self.time)))
            s = "(item="+str(self.item)
            s+= ", time="+str(self.time)
            s+= ", count="+str(self.count)
        tabs = "\t".join(['' for i in range(0,level+2)])
        for v in self.children.values():
            s+= tabs+"\n"
            s+= tabs+v.toString(level=level+1)
        s+=")"
        return s

    def addChild(self, node):
        self.children[node.item] = node
        node.parent = self

    def _getTransactions(self):
        count = self.count
        # transactions = []
        for child in self.children.values():
            for t in child._getTransactions():
                # print(t)
                count-=t[1]
                t[0][0].extend(self.time)
                t[0][1].insert(0,child.item)
                yield t
        if (count>0):
            yield ([[],[]],count)

class Summary(object):

    def __init__(self, count, nodes):
        self.count = count
        self.nodes = nodes