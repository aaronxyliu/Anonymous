function createObjectTree(depth_limit = 5, node_limit = 50, debug = false, bl = []) {  //bl: optional blacklist

    class TreeNode {
        constructor(_name) {
            this.name = _name
            this.dict = {}
            this.children = []
        }
    }

    function isArraySetMap(v) {
        if (Array.isArray(v))   return true;
        if (Object.getPrototypeOf(v) === Set.prototype)   return true;
        if (Object.getPrototypeOf(v) === Map.prototype)   return true;
        return false;
    }
    
    function analyzeVariable(v) {
        let v_info = {}
        if (v == undefined) {
            v_info = { dict: { 'type': 'undefined' }, 'children': [] }
        }
        else if (v == null) {
            v_info = { dict: { 'type': 'null' }, 'children': [] }
        }
        else if (isArraySetMap(v)) {
            value = 0
            try{
                value = CryptoJS.MD5(JSON.stringify(v)).toString()
            } catch (e) {
                value = v.length
            }
            v_info = { dict: { 'type': 'array', 'value': value }, 'children': [] }
        }
        else if (typeof (v) == 'string') {
            v_info = { dict: { 'type': 'string', 'value': v.slice(0, 24) }, 'children': [] }
        }
        else if (typeof (v) == 'object') {
            let vlist = Object.getOwnPropertyNames(v)
            vlist = vlist.filter(val => !["prototype"].includes(val));  // Remove name "prototype"
            v_info = { dict: { 'type': 'object' }, 'children': vlist }
        }
        else if (typeof (v) == 'function') {
            let vlist = Object.getOwnPropertyNames(v)
            vlist = vlist.filter(val => !["prototype", "length", "name"].includes(val));
            v_info = { dict: { 'type': 'function' }, 'children': vlist }
        }
        else if (typeof (v) == 'number') {
            v_info = { dict: { 'type': 'number', 'value': v.toFixed(2)}, 'children': [] }
        }
        else {
            v_info = { dict: { 'type': typeof (v), 'value': v }, 'children': [] }
        }
        return v_info
    }


    function hasCircle(v_path) {
        // Prevent loop in the object tree
        // Check whether v points to some parent variable
        if (v_path.length < 1) 
            return false

        cur_v = 'window'
        for (let v of v_path) {
            cur_v += `["${v}"]`
        }
        try{
            if (eval(`typeof (${cur_v}) != 'object' && typeof (${cur_v}) != 'function'`)) 
                return false
        }
        catch{
            return false
        }

        ancient_v = 'window'
        if (eval(`${ancient_v} == ${cur_v}`))
            return true
        for (let i = 0; i < v_path.length - 1; i += 1) {
            ancient_v += `["${v_path[i]}"]`
            try {
                if (eval(`typeof (${ancient_v}) == 'object' || typeof (${ancient_v}) == 'function'`))
                    if (eval(`${ancient_v} == ${cur_v}`))
                        return true
            }
            catch {
                continue
            }
        }

        return false
    }

    // Check whether the property name meet the standard
    function Sanitazer(str) {
        if (str.includes('"'))
            return false
        if (str.length > 24)
            return false
        return true
    }
    

    function genPTree(node_limit, depth_limit, blacklist) {
        // BFS
        let circle_num = 0
        let node_num = 1
        var root = new TreeNode('window')
        let q = []      // Property Path Queue
        let qc = []     // Generated Property Tree Queue
        q.push([])
        qc.push(root)

        while (q.length) {
            let v_path = q.shift()
            let cur_node = qc.shift()

            if (hasCircle(v_path)) {
                circle_num += 1
                continue
            }

            let v_str = 'window'
            for (let v of v_path) {
                if (v == '"') {
                    v_str += `['${v}']`
                }
                else {
                    v_str += `["${v}"]`
                }
            }
            
            if (debug)
                console.log(`${v_str}   depth: ${v_path.length}`)
            
            let v_info = {}
            eval(`v_info = analyzeVariable(${v_str});`)
            if (v_path.length > 0 && cur_node.name != v_path[v_path.length - 1]) {
                console.log('ERROR: UNMATACHED NODES.')
            }

            cur_node.dict = v_info.dict

            // Remove global variables in blacklist
            if (v_path.length == 0) {
                v_info['children'] = v_info['children'].filter(val => !blacklist.includes(val));
            }
            
            if (v_path.length < depth_limit) {
                for (let child of v_info['children']) {
                    if (node_num >= node_limit)
                        break
                    if (!Sanitazer(child))
                        continue    
                    let c_node = new TreeNode(child)
                    cur_node.children.push(c_node)
                    q.push([...v_path])              // shallow copy
                    q[q.length - 1].push(child)
                    qc.push(c_node)
                    node_num += 1
                }
            }
            
        }
        return [root, node_num, circle_num]
    }


    this.fetch(`../../static/blacklist.json`, {
        cache: 'no-store'
    })
        .then((response) => response.json())
        .then((origin_vlist) => {
            let tree_info = genPTree(node_limit, depth_limit, [...origin_vlist, ...bl])
            let tree = tree_info[0]

            if (debug) {
                console.log(`Node number: ${tree_info[1]}   Circle number: ${tree_info[2]}`)
                console.log(tree)
            }
            let tree_size_div = document.getElementById('tree-size');
            tree_size_div.innerHTML = tree_info[1];

            let circle_num_div = document.getElementById('circle-num');
            circle_num_div.innerHTML = tree_info[2];

            let json_str = JSON.stringify(tree);
            let display_div = document.getElementById('obj-tree');
            display_div.innerHTML = json_str.replace(/<|>/g, '_');
        })
}


function getGlobalV() {
    var vlist = Object.getOwnPropertyNames(window)


    this.fetch(`../../static/blacklist.json`, {
        cache: 'no-store'
    })
        .then((response) => response.json())
        .then((origin_vlist) => {
            vlist = vlist.filter(val => !origin_vlist.includes(val));
            let json_str = JSON.stringify(vlist);
            let display_div = document.getElementById('gloabl-v');

            // Replace '<' and '>' with '_' to prevent the conflict with web tag
            display_div.innerHTML = json_str.replace(/<|>/g, '_')
        })
}


