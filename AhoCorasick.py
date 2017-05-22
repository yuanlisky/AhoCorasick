# -*- coding: utf-8 -*-
"""
AC自动机
"""
__all__ = ['Ahocorasick', ]


class Node(object):
    def __init__(self):
        self.next = {}
        self.fail = None  # 失败指针
        self.isWord = False


class Ahocorasick(object):
    def __init__(self):
        self.__root = Node()

    def addWord(self, word):
        tmp = self.__root
        for char in word:
            tmp = tmp.next.setdefault(char, Node())
        tmp.isWord = True

    def make(self):
        """
        构建失败路径
        """
        tmpQueue = list()
        tmpQueue.append(self.__root)
        while len(tmpQueue) > 0:
            temp = tmpQueue.pop()
            p = None
            for k, v in temp.next.items():
                if temp == self.__root:
                    temp.next[k].fail = self.__root
                else:
                    p = temp.fail
                    while p is not None:
                        if k in p.next:
                            temp.next[k].fail = p.next[k]
                            break
                        p = p.fail
                    if p is None:
                        temp.next[k].fail = self.__root
                tmpQueue.append(temp.next[k])

    def search(self, content):
        """
        返回列表，每个元素为匹配的模式串在句中的起止位置
        """
        result = []
        startWordIndex = 0
        for currentPosition in range(len(content)):
            word = content[currentPosition]
            endWordIndex = currentPosition
            p = self.__root
            while word in p.next:
                if p == self.__root:
                    startWordIndex = currentPosition
                p = p.next[word]
                if p.isWord:
                    result.append((startWordIndex, endWordIndex))
                if p.next and endWordIndex+1 < len(content):
                    endWordIndex += 1
                    word = content[endWordIndex]
                else:
                    break
                while (word not in p.next) and (p != self.__root):
                    p = p.fail
                    startWordIndex += 1
                if p == self.__root:
                    break
        return result

    def replace(self, content):
        """
        匹配到的字符串以'*'号表示
        """
        replacepos = self.search(content)
        result = content
        for posindex in replacepos:
            result = result[0:posindex[0]] + (posindex[1] - posindex[0] + 1) * '*' + content[posindex[1] + 1:]
        return result


if __name__ == '__main__':
    import time
    ah = Ahocorasick()
    x = ["CD", "CDH", "CCDH", "HY", 'DH', 'CCD']
    for i in x:
        ah.addWord(i)
    ah.make()
    text = ['G', 'G', 'C', 'D', 'H', 'C', 'C', 'D', 'H', 'Y']
    # 可以是字符串，也可以是列表
    start = time.clock()
    res = ah.search(text)
    end = time.clock()
    print(res)
    print(end - start)
