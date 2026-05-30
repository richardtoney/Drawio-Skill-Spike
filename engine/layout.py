#!/usr/bin/env python3
"""
layout.py  —  Recursive layout engine for draw.io diagrams.

Three passes:
  1. Bottom-up sizing:  compute each node's w/h from its children.
  2. Top-down placement: assign child x/y within each container.
  3. Root arrangement:  reflow root-level nodes into column clusters.

Usage:
    python engine/layout.py diagram.drawio [output.drawio]
    Overwrites in-place when output is omitted.
"""

import sys
import xml.etree.ElementTree as ET

# ── constants ─────────────────────────────────────────────────────────────────────────────

ICON_W = 78
ICON_H = 78
LABEL_H = 24
LEAF_W = ICON_W
LEAF_H = ICON_H + LABEL_H

PAD_TOP  = 48   # vertical space for container label
PAD_SIDE = 24   # padding on left/right/bottom inside containers
PAD_GAP  = 20   # gap between siblings

COL_GAP  = 60   # gap between root-level columns
ROW_GAP  = 40   # gap between items in a root-level column

CLUSTER_THRESHOLD = 250  # x-distance that starts a new column

MIN_W = 180
MIN_H = 140

DIRECTION = {
    'group_region':             'H',
    'group_account':            'H',
    'group_vpc':                'VPC',
    'group_availability_zone':  'V',
    'group_subnet':             'H',
    'group_ecs':                'H',
    'group_eks':                'H',
    'group_auto_scaling_group': 'H',
}


# ── helpers ───────────────────────────────────────────────────────────────────────────────

def _gricon(style: str) -> str:
    for part in style.split(';'):
        if part.startswith('grIcon='):
            return part.split('=', 1)[1].split('.')[-1]
    return ''


def _is_group(style: str) -> bool:
    return 'shape=mxgraph.aws4.group' in style


def _geo_float(geo, attr, default=0.0) -> float:
    v = geo.get(attr)
    if v is None:
        return default
    try:
        return float(v)
    except ValueError:
        return default


# ── node model ─────────────────────────────────────────────────────────────────────────────

class Node:
    __slots__ = (
        'id', 'cell', 'geo', 'style', 'is_edge', 'is_vertex', 'parent_id',
        'children', 'is_group', 'gricon_key', 'direction',
        'orig_x', 'orig_y', 'orig_w', 'orig_h', 'w', 'h', 'x', 'y',
    )

    def __init__(self, cell):
        self.id        = cell.get('id', '')
        self.cell      = cell
        self.geo       = cell.find('mxGeometry')
        self.style     = cell.get('style', '')
        self.is_edge   = cell.get('edge') == '1'
        self.is_vertex = cell.get('vertex') == '1'
        self.parent_id = cell.get('parent', '0')
        self.children: list['Node'] = []
        self.is_group  = _is_group(self.style) and self.is_vertex
        self.gricon_key = _gricon(self.style)
        self.direction  = DIRECTION.get(self.gricon_key, 'H')
        g = self.geo
        self.orig_x = _geo_float(g, 'x')          if g is not None else 0.0
        self.orig_y = _geo_float(g, 'y')          if g is not None else 0.0
        self.orig_w = _geo_float(g, 'width',  LEAF_W) if g is not None else LEAF_W
        self.orig_h = _geo_float(g, 'height', LEAF_H) if g is not None else LEAF_H
        self.w = self.orig_w
        self.h = self.orig_h
        self.x = self.orig_x
        self.y = self.orig_y

    def write_geo(self):
        if self.geo is None or self.id in ('0', '1') or self.is_edge:
            return
        self.geo.set('x', f'{self.x:.0f}')
        self.geo.set('y', f'{self.y:.0f}')
        if self.is_group:
            self.geo.set('width',  f'{self.w:.0f}')
            self.geo.set('height', f'{self.h:.0f}')


# ── tree construction ────────────────────────────────────────────────────────────────────

def build_tree(diagram_el):
    nodes: dict[str, Node] = {}
    for cell in diagram_el.findall('.//mxCell'):
        cid = cell.get('id')
        if cid:
            nodes[cid] = Node(cell)

    roots: list[Node] = []
    for nid, node in nodes.items():
        if nid in ('0', '1') or node.is_edge:
            continue
        pid = node.parent_id
        if pid in ('0', '1', None, ''):
            roots.append(node)
        elif pid in nodes:
            nodes[pid].children.append(node)

    return nodes, roots


# ── pass 1: bottom-up sizing ────────────────────────────────────────────────────────────────

def _size(node: Node):
    if node.is_edge:
        return

    for child in node.children:
        _size(child)

    real_kids = [c for c in node.children if not c.is_edge]

    if not node.is_group or not real_kids:
        # Leaf — keep existing size, clamp to at least icon dimensions
        node.w = max(node.w, LEAF_W)
        node.h = max(node.h, LEAF_H)
        return

    d = node.direction
    if d == 'VPC':
        _size_vpc(node, real_kids)
    elif d == 'V':
        _size_v(node, real_kids)
    else:
        _size_h(node, real_kids)


def _size_h(node: Node, kids: list):
    total_w = sum(c.w for c in kids) + PAD_GAP * max(0, len(kids) - 1)
    max_h   = max(c.h for c in kids)
    node.w  = max(MIN_W, total_w + PAD_SIDE * 2)
    node.h  = max(MIN_H, PAD_TOP + max_h + PAD_SIDE)


def _size_v(node: Node, kids: list):
    max_w   = max(c.w for c in kids)
    total_h = sum(c.h for c in kids) + PAD_GAP * max(0, len(kids) - 1)
    node.w  = max(MIN_W, max_w + PAD_SIDE * 2)
    node.h  = max(MIN_H, PAD_TOP + total_h + PAD_SIDE)


def _size_vpc(node: Node, kids: list):
    azs      = [c for c in kids if c.gricon_key == 'group_availability_zone']
    cross_az = [c for c in kids if c.gricon_key != 'group_availability_zone']

    az_w  = sum(c.w for c in azs) + PAD_GAP * max(0, len(azs) - 1) if azs else 0
    az_h  = max((c.h for c in azs), default=0)

    cx_w  = sum(c.w for c in cross_az) + PAD_GAP * max(0, len(cross_az) - 1) if cross_az else 0
    cx_h  = (max((c.h for c in cross_az), default=0) + PAD_GAP) if cross_az else 0

    content_w = max(az_w, cx_w)
    node.w = max(MIN_W, content_w + PAD_SIDE * 2)
    node.h = max(MIN_H, PAD_TOP + cx_h + az_h + PAD_SIDE)


# ── pass 2: top-down placement ────────────────────────────────────────────────────────────────

def _place(node: Node):
    if node.is_edge:
        return

    real_kids = [c for c in node.children if not c.is_edge]
    if not real_kids:
        return

    d = node.direction
    if d == 'VPC':
        _place_vpc(node, real_kids)
    elif d == 'V':
        _place_v(node, real_kids)
    else:
        _place_h(node, real_kids)

    for child in real_kids:
        _place(child)


def _place_h(node: Node, kids: list):
    max_h = max(c.h for c in kids)
    x = PAD_SIDE
    for kid in kids:
        kid.x = x
        kid.y = PAD_TOP + (max_h - kid.h) / 2
        x += kid.w + PAD_GAP


def _place_v(node: Node, kids: list):
    max_w = max(c.w for c in kids)
    y = PAD_TOP
    for kid in kids:
        kid.x = PAD_SIDE + (max_w - kid.w) / 2
        kid.y = y
        y += kid.h + PAD_GAP


def _place_vpc(node: Node, kids: list):
    azs      = [c for c in kids if c.gricon_key == 'group_availability_zone']
    cross_az = [c for c in kids if c.gricon_key != 'group_availability_zone']

    cx_h = (max((c.h for c in cross_az), default=0) + PAD_GAP) if cross_az else 0
    az_y = PAD_TOP + cx_h

    # Cross-AZ icons: centred row above AZs
    if cross_az:
        row_w = sum(c.w for c in cross_az) + PAD_GAP * max(0, len(cross_az) - 1)
        cx = max(PAD_SIDE, (node.w - row_w) / 2)
        icon_y = PAD_TOP + (cx_h - PAD_GAP - max(c.h for c in cross_az)) / 2
        for icon in cross_az:
            icon.x = cx
            icon.y = max(PAD_TOP, icon_y)
            cx += icon.w + PAD_GAP

    # AZs: side by side
    if azs:
        az_total_w = sum(c.w for c in azs) + PAD_GAP * max(0, len(azs) - 1)
        ax = max(PAD_SIDE, (node.w - az_total_w) / 2)
        for az in azs:
            az.x = ax
            az.y = az_y
            ax += az.w + PAD_GAP


# ── pass 3: root-level arrangement ──────────────────────────────────────────────────────────────────

def _arrange_roots(roots: list):
    """
    Anchor-based root layout:
      1. Find the main container (region/account, or the largest group).
      2. Classify other root nodes as top / right / bottom / left
         relative to the main container's ORIGINAL bounding box.
      3. Place main, then position each zone around it.
         - top:    centred above main
         - right:  stacked vertically to the right of main
         - bottom: shifted en-bloc below main, preserving relative x/y
         - left:   stacked vertically to the left of main
    """
    if not roots:
        return

    # Identify main container
    main = next(
        (n for n in roots if n.gricon_key in ('group_region', 'group_account')),
        None,
    )
    if main is None:
        main = max(
            (n for n in roots if n.is_group),
            key=lambda n: n.orig_w * n.orig_h,
            default=None,
        )

    if main is None:
        # No containers — simple left-to-right flow
        x = 0
        for n in sorted(roots, key=lambda n: n.orig_x):
            n.x, n.y = x, 0
            x += n.w + COL_GAP
        return

    # Classify non-main roots using original bounding box of main
    mx, my  = main.orig_x, main.orig_y
    mw, mh  = main.orig_w, main.orig_h

    top_nodes: list[Node]    = []
    right_nodes: list[Node]  = []
    bottom_nodes: list[Node] = []
    left_nodes: list[Node]   = []

    for n in roots:
        if n is main:
            continue
        nx, ny = n.orig_x, n.orig_y
        if nx > mx + mw * 0.75:
            right_nodes.append(n)
        elif ny > my + mh * 0.75:
            bottom_nodes.append(n)
        elif ny < my + mh * 0.15:
            top_nodes.append(n)
        else:
            left_nodes.append(n)

    # Reserve space for left column
    left_w = (max(n.w for n in left_nodes) + COL_GAP) if left_nodes else 0

    # Place main
    main.x = left_w
    main.y = 0

    # Top nodes: centred horizontally above main
    if top_nodes:
        top_sorted = sorted(top_nodes, key=lambda n: n.orig_x)
        total_w = sum(n.w for n in top_sorted) + COL_GAP * (len(top_sorted) - 1)
        tx = main.x + max(0, (main.w - total_w) / 2)
        ty = -(max(n.h for n in top_sorted) + ROW_GAP)
        for n in top_sorted:
            n.x = tx
            n.y = ty
            tx += n.w + COL_GAP

    # Right nodes: stacked vertically right of main
    if right_nodes:
        rx = main.x + main.w + COL_GAP
        ry = main.y
        for n in sorted(right_nodes, key=lambda n: n.orig_y):
            n.x = rx
            n.y = ry
            ry += n.h + ROW_GAP

    # Bottom nodes: shifted en-bloc below main, preserving relative layout
    if bottom_nodes:
        min_orig_y = min(n.orig_y for n in bottom_nodes)
        min_orig_x = min(n.orig_x for n in bottom_nodes)
        new_top_y  = main.y + main.h + ROW_GAP * 2
        shift_y    = new_top_y - min_orig_y
        shift_x    = main.x - min_orig_x
        for n in bottom_nodes:
            n.x = n.orig_x + shift_x
            n.y = n.orig_y + shift_y

    # Left nodes: stacked vertically left of main
    if left_nodes:
        ly = main.y
        for n in sorted(left_nodes, key=lambda n: n.orig_y):
            n.x = 0
            n.y = ly
            ly += n.h + ROW_GAP


# ── main entry point ─────────────────────────────────────────────────────────────────────────────

def layout_diagram(diagram_el) -> tuple[int, int]:
    """Apply layout to a single diagram page. Returns (containers_resized, nodes_placed)."""
    nodes, roots = build_tree(diagram_el)

    containers_resized = 0
    nodes_placed = 0

    for root in roots:
        _size(root)

    for root in roots:
        _place(root)
        containers_resized += sum(1 for n in _walk(root) if n.is_group)
        nodes_placed += sum(1 for n in _walk(root))

    _arrange_roots(roots)

    for node in nodes.values():
        node.write_geo()

    return containers_resized, nodes_placed


def _walk(node: Node):
    yield node
    for child in node.children:
        yield from _walk(child)


def layout_file(src: str, dst: str):
    ET.register_namespace('', '')
    tree = ET.parse(src)
    root = tree.getroot()

    total_containers = 0
    total_nodes = 0

    for diagram in root.findall('diagram'):
        c, n = layout_diagram(diagram)
        total_containers += c
        total_nodes += n

    tree.write(dst, encoding='unicode', xml_declaration=True)
    print(f'Layout applied: {total_containers} containers resized, '
          f'{total_nodes} nodes repositioned → {dst}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} diagram.drawio [output.drawio]')
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else src
    layout_file(src, dst)
