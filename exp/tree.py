# Classes implemented according to the Version Detection paper
import time

class Label:
    def __init__(self, _name):
        self.name = _name
        self.dict = {}


class Vertex:
    def __init__(self, name, label={}):
        assert(isinstance(label, dict))
        self.name = str(name)
        self.label = label
        self.children = []
    
    def addc(self, child):
        assert(isinstance(child, Vertex))
        self.children.append(child)

    def __eq__(self, x):
        if not x:
            return False
        assert(isinstance(x, Vertex))
        if self.name == x.name and self.label == x.label:
            return True
        else:
            return False 

class LabeledPath:
    def __init__(self, vertex_names, leaf_label):   # vertex_names - @List<str>
        self.vn = vertex_names[:]   # list copy
        self.label = leaf_label
    
    def __eq__(self, x):
        assert(isinstance(x, LabeledPath))
        if self.vn == x.vn and self.label == x.label:
            return True
        else:
            return False 

class LabeledTree:
    def __init__(self, root=None, name=''):
        self.root = root    # @Vertex
        self.name = name

    def get_metas(self):
        self.fpaths = []
        self.rpaths = []
        self.depth = 0
        self.size = 0
        self.root.par = None
        self.root.depth = 0
        if self.root:
            self.__get_metas__(self.root, 0, [self.root.name])
    
    def __eq__(self, x):
        assert(isinstance(x, LabeledTree))
        if not self.root or not x.root:
            print('Tree is missing.')
            return False
        q1 = []
        q2 = []
        q1.append(self.root)
        q2.append(x.root)
        if self.root != x.root:
            return False

        while len(q1):
            v1 = q1.pop(0)
            v2 = q2.pop(0)
            mask = [1] * len(v2.children)
            for c1 in v1.children:
                found_same_vertex = False
                for c2_i in range(len(v2.children)):
                    c2 = v2.children[c2_i]
                    if c1 == c2:
                        # print(f'x: {c1.name}')
                        mask[c2_i] = 0
                        found_same_vertex = True
                        q1.append(c1)
                        q2.append(c2)
                        break
                if not found_same_vertex:
                    return False
                
            for c2_i in range(len(v2.children)):
                if mask[c2_i] == 0:
                    continue
                c2 = v2.children[c2_i]
                found_same_vertex = False
                for c1 in v1.children:
                    if c1 == c2:
                        # print(f'y: {c1.name}')
                        mask[c2_i] = 0
                        found_same_vertex = True
                        q1.append(c1)
                        q2.append(c2)
                        break
                if not found_same_vertex:
                    return False
        return True

    def __get_metas__(self, par, d, p):
        """
        Generate meta informations for the tree, including tree size, full paths, 
        root paths, vertex depths, tree depth and vertices' parents.

        Parameters:
            par - parent vertex
            d - the depth of par
            p - the path of par (vertex name list)

        Returns:
            self.fpaths - full path set
            self.rpaths - root path set
            self.depth - tree depth
            self.size - vertex number of the tree
            <Vertex>.depth - the depth of each vertex
            <Vertex>.par - the parent of each vertex
            <Vertex>.subtree_size - the size of the subtree rooted from each vertex
        """
        if not par:
            return
        
        rpath = LabeledPath(p, par.label)
        self.rpaths.append(rpath)
        self.size += 1
        par.subtree_size = 1
        if len(par.children) == 0:
            # par is a leaf vertex, record this path
            fpath = LabeledPath(p, par.label)
            self.fpaths.append(fpath)
        else:
            if d + 1 > self.depth:
                self.depth = d + 1
            for c in par.children:
                c.depth = d + 1
                c.par = par
                par.subtree_size += self.__get_metas__(c, d + 1, p + [c.name])
        return par.subtree_size
        
    def min_cover_set(self, usize):
        """
        Find the minimum cover sets.

        Parameters:
            usize - the size of Gamma

        Returns:
            I - the indexes of sets in the collection that cover the universe
        """
        C = set()
        I = set()
        Omega_range = set(range(len(self.Omega)))
        while len(C) < usize - len(self.S):
            max_cover_size = -1
            max_i = -1
            for i in Omega_range - I:
                cover_size = len(C | self.Omega[i])
                if cover_size > max_cover_size:
                    max_cover_size = cover_size
                    max_i = i
            I.add(max_i)
            C |= self.Omega[max_i]
        return I

    def generate_minified_tree(self, I):
        """
        Generate the minified tree based on I.

        Parameters:
            I - index set returned from min_cover_set()

        Returns:
            mroot - the root of the minified tree
        """
        mroot = None
        for i in I:
            p = self.fpaths[i]
            assert(len(p.vn) >= 1)
            if not mroot:
                if len(p.vn) == 1:
                    mroot = Vertex(p.vn[0], p.label)
                else:
                    mroot = Vertex(p.vn[0])
            else:
                assert(mroot.name == p.vn[0])

            v = mroot
            for j in range(1, len(p.vn)):
                v_next = None
                for c in v.children:
                    if c.name == p.vn[j]:
                        v_next = c
                        break
                if not v_next:
                    if j == len(p.vn) - 1:
                        v_next = Vertex(p.vn[j], p.label)
                    else:
                        v_next = Vertex(p.vn[j])
                    v.children.append(v_next)

                v = v_next
        return mroot
                    
                

class Gamma:
    def __init__(self):
        self.trees = []    # @List<LabeledTree>
    
    def addt(self, t):
        assert(isinstance(t, LabeledTree))
        self.trees.append(t)
    
    def get_trees_metas(self):
        for t in self.trees:
            t.get_metas()
    
    def get_mtrees_metas(self):
        for t in self.mtrees:
            t.get_metas()

    def get_equivalence(self):
        """
        Generate the equivalence class for every tree in Gamma.
        Reference: Thesis: Sorting and Selection with Equality Comparisons. (2015) Theorem 1.

        Required:
            self.trees
            <LabeledTree>.fpaths

        Update:
            self.trees
        """
        T1 = time.time()
        r = 0
        eq = []    # eq[i] = {1, 3, 5} means 1, 3, 5 belong to a equivalence class
        n = len(self.trees)
        for i in range(n):
            eq.append({i})
        max_eq_size = 1
        neq = [set()] * n
        U = set(range(n))
        while True:
            r += 1
            for i in range(n):
                # Find the next j if any, starting from i + 1, wrapped around after n if necessary, such that j /∈ eq(i) ∪ neq(i).
                jRange = U - (eq[i] | neq[i])
                for j in jRange:
                    if self.trees[i] == self.trees[j]:
                        xRange = eq[i] | eq[j]
                        for x in xRange:
                            eq[x] = eq[i] | eq[j]
                            neq[x] = neq[i] | neq[j]
                            if len(eq[x]) > max_eq_size:
                                max_eq_size = len(eq[x])
                    else:
                        for x in eq[i]:
                            neq[x] = neq[x] | eq[j]
                        for y in eq[j]:
                            neq[y] = neq[y] | eq[i]
            if max_eq_size >= (n - 1) / r:
                break

        new_trees = []
        while len(U):
            i = U.pop()
            U -= eq[i]
            eq_list = sorted(list(eq[i]))
            new_name = ''
            sec_start = -1
            eq_name_list = []    # Equivalence Class Tree Names List

            for j in range(len(eq_list)):
                eq_name_list.append(self.trees[eq_list[j]].name)
                if sec_start == -1: 
                    # start a new section
                    sec_start = eq_list[j]
                    if j == 0:
                        new_name += self.trees[eq_list[j]].name
                    else:
                        new_name += ', ' + self.trees[eq_list[j]].name
                if j == len(eq_list) - 1 or eq_list[j+1] - eq_list[j] > 1:
                    # end the section
                    if eq_list[j] - sec_start == 1:
                        new_name += ', ' + self.trees[eq_list[j]].name
                    elif eq_list[j] - sec_start > 1:
                        new_name += ' ~ ' + self.trees[eq_list[j]].name
                    sec_start = -1

            self.trees[i].name = new_name
            self.trees[i].eq_name_list = eq_name_list

            new_trees.append(self.trees[i])
        self.trees = new_trees

        T2 = time.time()
        return [T2 - T1]


    def path_in_tree(self, fpath, tree):
        """
        Check whether fpath is a root path in tree. 

        Parameters:
            fpath - full path
            tree - <LabeledTree> 

        Return:
            True or False
        """
        
        assert(isinstance(fpath, LabeledPath))
        assert(isinstance(tree, LabeledTree))
        path_len = len(fpath.vn)
        assert(path_len > 0)

        v = tree.root
        if fpath.vn[0] != v.name:
            return False
        
        for i in range(1, path_len):
            found_child = False
            for c in v.children:
                if c.name == fpath.vn[i]:
                    v = c
                    found_child = True
                    break
            if not found_child:
                return False
            
        if v.label != fpath.label:
                return False
        return True




    def tree_size_reduction(self):
        """
        Tree size reduction. 

        Parameters:
            None

        Returns:
            <LabeledTree>.Omega - the path coloring collection for each tree
            <LabeledTree>.S - the supertree set of each tree
            time log - an array of time records for each stage in the algorithm
        """
        self.mtrees = []
        time_log = [0] * 4
        timestamp = [0] * 5
        for t in self.trees:
            # Generate the coloring set gamma for each path in t.
            timestamp[0] = time.time()
            t.Omega = []
            for i in range(len(t.fpaths)):
                p = t.fpaths[i]
                omega = set()  # the coloring set of p
                for j in range(len(self.trees)):
                    if self.path_in_tree(p, self.trees[j]):
                    # if p in self.trees[j].rpaths:
                        omega.add(j)
                t.Omega.append(omega)
            timestamp[1] = time.time()
            
            # Generate the supertree set of t.
            U = set(range(len(self.trees))) # Full set
            t.S = U.copy()
            for omega in t.Omega:
                t.S &= omega
            
            for i in range(len(t.Omega)):
                t.Omega[i] = U - t.Omega[i]
            timestamp[2] = time.time()

            # Find the minimum cover sets of the coloring collection
            I = t.min_cover_set(len(U))
            timestamp[3] = time.time()

            # Generate minified tree
            mtree = LabeledTree(t.generate_minified_tree(I), t.name)
            self.mtrees.append(mtree)
            timestamp[4] = time.time()
        
            # Record the time spent on each stage
            for i in range(len(time_log)):
                time_log[i] += timestamp[i + 1] - timestamp[i]
        
        return time_log
    
        
    def strict_supertree_set_minify(self):
        """
        Strict supertree set minify. 

        Required:
            <LabeledTree>.S - supertree set of each tree

        Returns:
            <LabeledTree>.Sm - minified strict supertree set of each tree
        """
        T1 = time.time()
        # Generate the equavalence class of each tree
        for i in range(len(self.trees)):
            t = self.trees[i]
        
            S_st = t.S - {i}
            t.Sm = set()
            while len(S_st):
                max_S = -1
                max_k = -1
                for k in S_st:
                    if len(self.trees[k].S) > max_S:
                        max_S = len(self.trees[k].S)
                        max_k = k
                S_st -= self.trees[max_k].S
                t.Sm.add(max_k)

        T2 = time.time()
        return [T2 - T1]
    

    def max_freq_subtree(self):
        """
        Generate the maximum frequent subtree in Gamma.

        Required:
            self.trees

        Return:
            freqT - the maximum frequent subtree
        """

        n = len(self.trees)
        if n < 1:
            return None
        
        queues = [[]] * n
        for i in range(n):
            if  self.trees[i].root == None:
                return None
            queues[i].append(self.trees[i].root)
        
        freqT = LabeledTree(Vertex('window'), 'max freq subtree')
        queue_f = [freqT.root]

        while len(queues[0]):
            ptr_f = queue_f.pop(0)
            ptrs = [None] * n
            for i in range(n):
                ptrs[i] = queues[i].pop(0)

            for c in ptrs[0].children:
                # print(c.name)
                clist = self.__child_with_given_name(c.name, ptrs[1:])
                # print(clist)
                if None in clist:
                    # if one vertex doesn't have a child with the name same as the first tree's child
                    continue

                queues[0].append(c)
                for i in range(1, n):
                    queues[i].append(clist[i - 1])
                new_vertex = Vertex(c.name)
                queue_f.append(new_vertex)
                ptr_f.addc(new_vertex)

        return freqT



    def __child_with_given_name(self, name, vertex_list):
        """
        Find the child of each vertex with the given name. If no such child, return None.

        Required:
            name <string>
            vertex_list = [v1, v2, ..., vn]

        Return:
            child_list = [ptr1, ptr2, ..., ptrn]
        """
        n = len(vertex_list)
        child_list = [None] * n
        for i in range(n):
            v = vertex_list[i]
            assert(v != None)
            for c in v.children:
                if c.name == name:
                    child_list[i] = c
                    break
        return child_list




        
        


            

    



