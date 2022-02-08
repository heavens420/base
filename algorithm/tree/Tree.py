'''
    二叉树crud
'''


class Node(object):
    def __init__(self, value=None):
        self.left = None
        self.right = None
        self.value = value


class Tree(object):
    def __init__(self, root=None):
        self.root = Node(root) if root else None

    def add(self, value):
        current = self.root

        # 待插入节点非空
        if value:
            node = Node(value)
            # 根节点非空
            if current:
                while True:
                    # 左子叶非空 左移
                    if current.left:
                        current = current.left
                    else:  # 左子叶为空 新值插入左子叶
                        current.left = node
                        break

                    if current.right:
                        current = current.right
                    else:
                        current.right = node
                        break
            else:  # 根节点为空
                # 插入的节点置为根节点
                self.root = node

        else:  # 待插入节点为空
            raise Exception("插入节点为空")
