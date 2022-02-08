'''
    单链表 crud
'''


# 构建单链表
class Node(object):
    def __init__(self, val):
        self.value = val
        self.next = None


class SingleLinkList(object):
    def __init__(self, node=None):
        # 头节点默认置空，如果传值则头节点设置为该值
        self.__head = Node(node) if node else None

    def __len__(self):
        length = 0
        current = self.__head
        while current is not None:
            # while current:
            current = current.next
            length += 1
        return length

    def is_empty(self):
        current = self.__head
        if not current:
            return True
        else:
            return False

    # 头插法
    def add(self, value):
        if value:
            node = Node(value)
            current = self.__head
            # 如果头节点为空 直接将当前节点置为头节点 并结束添加
            if current is None:
                self.__head = node
                return
            # 新节点的next指向头节点
            node.next = current
            # 把新节点 置为头节点
            self.__head = node
        # return current

    # 尾插法
    def append(self, value):
        # 待插入节点非空
        if value:
            # 获取待插入节点
            node = Node(value)
            # 获取头节点
            current = self.__head
            # 头节点非空 才能有next　
            if current:
                # 　节点的节点的next非空 则继续遍历
                while current.next:
                    current = current.next
                # 节点的next为空 则说明该节点就是最后一个节点 其next后插入新节点
                current.next = node
            else:
                # 否则 头节点为空则当前节点置为头节点
                self.__head = node

    # 指定索引位置插入
    def insert(self, pos, value):
        if pos <= 0:
            self.add(value)
        elif pos >= self.__len__() - 1:
            self.append(value)
        else:
            node = Node(value)
            current = self.__head
            # 当前节点索引
            index = 0
            if value:
                # 第n个节点从1开始计算 而 链表索引实际从0 开始 故 删除第2个节点 实际上对应链表的 索引  1
                # 取小于而不是小于等于 是为了获取待插入节点的前一个节点
                while index < pos - 1:
                    index += 1
                    current = current.next

                # 0 -> 1 ->2 ->3
                # 假设 pos = 1 则遍历结束 current = 0
                # 此时 value应该插入 0 和 1 之间 结果如此： 0 -> value -> 1 -> 2
                # 故 value的next即为 0的next 0 的next即为value 此时即形成新的链表 二者顺序不可变
                node.next = current.next
                current.next = node
            else:
                raise Exception(f"插入节点为空")

    # 遍历单链表
    def travel(self):
        current = self.__head
        while current.next:
            # 打印节点
            print(current.value)
            current = current.next
        # 打印最后的节点
        print(current.value)

    # 清空单链表
    def clear(self):
        self.__head = None

    # 根据索引删除节点 pos:0,1,2...
    def remove(self, pos):
        if pos > self.__len__() - 1 or pos < 0:
            raise Exception("索引节点不存在")

        # 删除头节点 特殊处理
        if pos == 0:
            self.__head = self.__head.next

        index = 0
        current = self.__head
        while index < pos - 1:
            index += 1
            current = current.next
        # 待删除节点
        del_node = current.next
        # 当前节点指向待删除节点的next
        current.next = del_node.next

    # 根据值删除节点
    def remove_value(self, value):
        if value:
            current = self.__head
            node = Node(value)
            # 删除头节点
            if current == node:
                self.__head = self.__head.next

            # 遍历寻值
            while current and current.next.value != node.value:
                current = current.next

            # 遍历结束 找到待删除节点则 判断为True 否则就是没找到
            if current.next.value != node.value:
                raise Exception(f"待删除节点{value}不存在")

            # 待删除节点
            del_node = current.next
            # 当前节点指向待删除节点的next
            current.next = del_node.next
        else:
            raise Exception("删除节点不能为空")

    # 逆序遍历单链表
    def reverse_travel(self):
        node = self.__head

        def loop(node):
            if node:
                cur = node
                node = node.next
                loop(node)
                print(cur.value)

        loop(node)


# 翻转单链表
def reverse_single_link_list(head):
    cur = None
    node = head

    def loop(node, cur=cur):
        if node:
            now = node
            node = now.next
            loop(node)
            if cur is None:
                cur = node
            else:
                cur.next = node

    return loop(node)

    


if __name__ == '__main__':
    # node = Node(val=None)
    sl = SingleLinkList()
    print(sl.is_empty())
    print(sl.__len__())
    sl.add('200')
    sl.append('1')
    sl.append('2')
    sl.append('3')
    sl.insert(1, '100')
    print(sl.__len__())
    print(sl.is_empty())
    sl.travel()
    sl.remove(0)
    print('-' * 30)
    sl.travel()
    # sl.remove_value('1')
    print('-' * 30)
    # sl.travel()
    # sl.reverse_travel()

    kk = reverse_single_link_list(sl)

