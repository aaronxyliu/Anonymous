class CreditCalculator:
    # Every time calculate a new tree, should initilaize a new instance

    def __init__(self, trim_depth=5, trim_size=500, total_credit=100):
        self.total_credit = total_credit
        self.depth_subtreesize_index = [0] * (trim_depth + 1)  # the i-th element refers to the subtree size sum of all nodes at depth i
        self.D = 0  # Max depth of the current tree, start from 0
        self.credit_sum = 0     # Used to verify, the sum should equal to self.total_credit
        self.trim_depth = trim_depth
        self.trim_size = trim_size


    def __GetSubtreeSize(self, node, d):
        subtree_size = 1

        for child in node['children']:
            subtree_size += self.__GetSubtreeSize(child, d+1)
        node['subtree_size'] = subtree_size

        return subtree_size
    

    def __GetSubtreeSizeIndex(self, node, d):
        self.depth_subtreesize_index[d] += node['subtree_size']
        for child in node['children']:
            self.__GetSubtreeSizeIndex(child, d+1)
        


    def __CalculateCredit(self, node, d):
        if d == 0:
            node['credit'] = 0
        else:
            current_depth_credit = (2 ** (self.D - d) / (2 ** self.D - 1)) * self.total_credit
            credit = (node['subtree_size'] / self.depth_subtreesize_index[d]) * current_depth_credit
            node['credit'] = round(credit, 3)
        for child in node['children']:
            self.__CalculateCredit(child, d + 1)

    
    # def __CleanMetaInfo(self, node):
    #     if 'depth' in node:
    #         del node['depth']
    #     if 'subtree_size' in node:
    #         del node['subtree_size']
    #     for child in node['children']:
    #         self.__CleanMetaInfo(child)


    def verify (self, node):
        if 'credit' in node:
            self.credit_sum += node['credit']
        for child in node['children']:
            self.verify(child)
    

    def __trim(self, tree):
        node_num = 1
        q = []
        q_depth = [0]
        q.append(tree)
        while len(q):
            node = q.pop(0)
            depth = q_depth.pop(0)
            self.D = depth
            if depth >= self.trim_depth:
                node['children'] = []

            for i in range(len(node['children'])):
                if node_num >= self.trim_size:
                    node['children'] = node['children'][:i]
                    break
                else:
                    q.append(node['children'][i])
                    q_depth.append(depth + 1)
                    node_num += 1
        return node_num, self.D      # Return the size and depth of the tree


    def __findChildByName(self, node, name):
        for i in range(len(node['children'])):
            if node['children'][i]['name'] == name:
                return i
        return -1

    
    def expand(self, tree):
        exp_tree = {'name': 'window', 'dict': {}, 'children': []}
        for node in tree['children']:
            if 'path' not in node.keys():
                print('All child of the root should have the "path" attribute.')
                exit()
                # for i in range(len(node['path'])-1, -1, -1):
                #     # From back to front, insert node in order
                #     new_node = {'name': node['path'][i], 'dict': {'type': 'object'}, 'children': [node], 'credit': 0}
                #     node = new_node
            ptr = exp_tree
            for v_name in node['path']:
                index = self.__findChildByName(ptr, v_name)
                if index != -1:
                    ptr = ptr['children'][index]
                else:
                    new_node = {'name': v_name, 'dict': {'type': 'object'}, 'children': [], 'credit': 0}
                    ptr['children'].append(new_node)
                    ptr = new_node
            ptr['children'].append(node)
        return exp_tree




    def algorithm1(self, tree):
        self.__GetSubtreeSize(tree, 0)
        size, depth = self.__trim(tree)
        self.__GetSubtreeSizeIndex(tree, 0)
        self.__CalculateCredit(tree, 0)
        return size, depth
        # self.__CleanMetaInfo(tree)


    def minifyTreeSpace(self, node):
        # Replace key with shorter name
        if 'name' in node:
            node['n'] = node.pop('name')
        if 'dict' in node:
            node['d'] = node.pop('dict')
            node_dict = node['d']
            if 'type' in node_dict:
                node_dict['t'] = node_dict.pop('type')
                TYPE_OPTIONS = ['undefined', 'null', 'array', 'string', 'object', 'function', 'number', 'boolean']
                for i in range(len(TYPE_OPTIONS)):
                    if node_dict['t'] == TYPE_OPTIONS[i]:
                        node_dict['t'] = i + 1
                        break
                # match node_dict['t']:
                #     case 'undefined':
                #         node_dict['t'] = 1
                #     case 'null':
                #         node_dict['t'] = 2
                #     case 'array':
                #         node_dict['t'] = 3
                #     case 'string':
                #         node_dict['t'] = 4
                #     case 'object':
                #         node_dict['t'] = 5
                #     case 'function':
                #         node_dict['t'] = 6
                #     case 'number':
                #         node_dict['t'] = 7
                #     case 'boolean':
                #         node_dict['t'] = 8
            if 'value' in node_dict:
                node_dict['v'] = node_dict.pop('value')
        if 'children' in node:
            node['c'] = node.pop('children')
        if 'credit' in node:
            node['x'] = node.pop('credit')
        
        # Remove other attributes
        del_attrs = []
        for attr in node:
            if attr != 'n' and attr != 'd' and attr != 'c' and attr != 'x':
                del_attrs.append(attr)
        for attr in del_attrs:
            del node[attr]

        for child in node['c']:
            self.minifyTreeSpace(child)