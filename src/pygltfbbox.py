import argparse
import numpy as np
from pygltflib import GLTF2
from typing import List
import sys
from dataclasses import dataclass

@dataclass
class Point:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

@dataclass
class Node:
    bmin: Point # min
    bmax: Point # max
    # transformation in form of matrix
    transMat = [0] * 16

def union(p1: Point, p2: Point, compare) -> Point:
    ret = Point()
    ret.x = compare(p1.x, p2.x)
    ret.y = compare(p1.y, p2.y)
    ret.z = compare(p1.z, p2.z)
    return ret

# we make the node relation into list of list of int
# while just create an array of structure that has each node mesh info.
def extract_nodes_hirachy(gltf:GLTF2):
    index_tree = []
    nodes_list = []
    for node in gltf.nodes:
        bmin = None
        bmax = None
        if not node.mesh is None:
            bmin = Point(sys.float_info.max, sys.float_info.max, sys.float_info.max)
            bmax = Point(-sys.float_info.max, -sys.float_info.max, -sys.float_info.max)
            curMesh = gltf.meshes[node.mesh]
            for primitive in curMesh.primitives:
                curPositionAccessor = gltf.accessors[primitive.attributes.POSITION]
                cmin = Point(curPositionAccessor.min[0], curPositionAccessor.min[1], curPositionAccessor.min[2])
                cmax = Point(curPositionAccessor.max[0], curPositionAccessor.max[1], curPositionAccessor.max[2])
                bmin = union(cmin, bmin, min)
                bmax = union(cmax, bmax, max)
        ele = Node(bmin, bmax)
        nodes_list.append(ele)
        index_tree.append(node.children)
    return index_tree, nodes_list
        



if __name__=='__main__':
    parser = argparse.ArgumentParser("Script to obtain a gltf global bbox as min, max")
    parser.add_argument("-i", "--input", help="the input glb/gltf path")
    
    args = parser.parse_args()
    gltf = GLTF2().load(args.input)
    index_tree, nodes_list = extract_nodes_hirachy(gltf)
    # now we have a general node tree structure to work with.
    print(nodes_list)
    


