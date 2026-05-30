#!/usr/bin/env python3
"""
validate_drawio.py
Structural validator for AI-generated .drawio files.
Catches the failure modes LLMs produce most often.
Usage: python validate_drawio.py <path-to-file.drawio>
"""

import sys
import xml.etree.ElementTree as ET
from collections import Counter


def validate_diagram(diagram_el, errors, warnings):
    """Run structural checks scoped to a single <diagram> page."""
    name = diagram_el.get('name', '(unnamed)')
    prefix = f"[page '{name}'] " if diagram_el.get('name') else ""

    cells = diagram_el.findall('.//mxCell')
    ids = {c.get('id') for c in cells if c.get('id')}

    # --- Foundation cells ---
    if '0' not in ids:
        errors.append(f"{prefix}MISSING mxCell id='0' (required foundation cell)")
    if '1' not in ids:
        errors.append(f"{prefix}MISSING mxCell id='1' (required foundation cell)")

    # --- Duplicate IDs ---
    all_ids = [c.get('id') for c in cells if c.get('id')]
    dupes = [cid for cid, count in Counter(all_ids).items() if count > 1]
    for d in dupes:
        errors.append(f"{prefix}DUPLICATE id='{d}'")

    # --- Orphaned references ---
    for c in cells:
        cid = c.get('id', '?')
        parent = c.get('parent')
        if parent and parent not in ids:
            errors.append(f"{prefix}ORPHANED parent='{parent}' on cell id='{cid}'")
        source = c.get('source')
        if source and source not in ids:
            errors.append(f"{prefix}ORPHANED edge source='{source}' on cell id='{cid}'")
        target = c.get('target')
        if target and target not in ids:
            errors.append(f"{prefix}ORPHANED edge target='{target}' on cell id='{cid}'")

    # --- Zero-coordinate check ---
    zero_coord_vertices = []
    placed_vertices = []
    for c in cells:
        if c.get('vertex') == '1' and c.get('id') not in ('0', '1'):
            geo = c.find('mxGeometry')
            if geo is not None:
                x = geo.get('x', '0')
                y = geo.get('y', '0')
                if x in ('0', '0.0', None) and y in ('0', '0.0', None):
                    zero_coord_vertices.append(c.get('id', '?'))
                else:
                    placed_vertices.append(c.get('id', '?'))
    if zero_coord_vertices and not placed_vertices:
        warnings.append(
            f"{prefix}ALL {len(zero_coord_vertices)} vertices are at x=0,y=0 — they will overlap. "
            f"Use the column-grid coordinates from SKILL.md instead."
        )
    elif zero_coord_vertices and len(zero_coord_vertices) > len(placed_vertices):
        warnings.append(
            f"{prefix}{len(zero_coord_vertices)} of "
            f"{len(zero_coord_vertices) + len(placed_vertices)} "
            f"vertices are at x=0,y=0 — they will overlap each other. "
            f"Apply column-grid coordinates to all nodes."
        )

    # --- Large diagram ---
    vertex_count = sum(1 for c in cells
                       if c.get('vertex') == '1' and c.get('id') not in ('0', '1'))
    if vertex_count > 25:
        warnings.append(
            f"{prefix}LARGE DIAGRAM: {vertex_count} vertices. "
            f"Consider splitting into multiple pages for diagrams > 25 nodes."
        )

    # --- AWS4 shape compliance ---
    non_aws4 = []
    for c in cells:
        style = c.get('style', '')
        if c.get('vertex') == '1' and c.get('id') not in ('0', '1'):
            if 'shape=' in style and 'mxgraph.aws4' not in style:
                if 'group' not in style:
                    non_aws4.append(c.get('id', '?'))
    if non_aws4:
        warnings.append(
            f"{prefix}NON-AWS4 shapes found on {len(non_aws4)} vertex/vertices — "
            f"should use mxgraph.aws4 namespace: "
            f"{', '.join(non_aws4[:5])}{'...' if len(non_aws4) > 5 else ''}"
        )

    return sum(1 for c in cells if c.get('vertex') == '1' and c.get('id') not in ('0', '1')), len(cells)


def validate(path: str) -> bool:
    errors = []
    warnings = []

    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        print(f"FATAL: XML parse error — {e}")
        return False

    root = tree.getroot()

    # --- File-level: raw string checks ---
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    if '<!--' in raw:
        errors.append("FORBIDDEN: XML comments found (<!-- -->)")
    if 'Array as="points"' in raw:
        errors.append('FORBIDDEN: <Array as="points"> waypoints found — remove them')
    if '><![CDATA[' in raw:
        errors.append("FORBIDDEN: CDATA (compressed) diagram content found — use raw XML")

    # --- File-level: postLayout warning ---
    for gm in root.findall('.//mxGraphModel'):
        if gm.get('postLayout'):
            warnings.append(
                "postLayout attribute found on mxGraphModel — "
                "draw.io desktop silently ignores this attribute. "
                "Remove it and use explicit x/y coordinates for placement instead."
            )

    # --- Per-diagram structural checks ---
    diagrams = root.findall('diagram')
    if not diagrams:
        # Single-diagram files may omit the <diagram> wrapper; treat root as one page
        diagrams = [root]

    total_cells = 0
    total_vertices = 0
    for diagram in diagrams:
        v, c = validate_diagram(diagram, errors, warnings)
        total_vertices += v
        total_cells += c

    page_count = len(diagrams)

    # --- Report ---
    if errors:
        pages_label = f"{page_count} page(s), " if page_count > 1 else ""
        print(f"VALIDATION FAILED — {len(errors)} error(s), {len(warnings)} warning(s):")
        for e in errors:
            print(f"  ERROR: {e}")
        for w in warnings:
            print(f"  WARN:  {w}")
        print(f"\nDiagram has {pages_label}{total_cells} cells, {total_vertices} vertices")
        return False
    else:
        pages_label = f"{page_count} pages, " if page_count > 1 else ""
        print(f"OK — {pages_label}{total_cells} cells, {total_vertices} vertices, 0 errors")
        if warnings:
            for w in warnings:
                print(f"  WARN: {w}")
        return True


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.drawio>")
        sys.exit(1)
    success = validate(sys.argv[1])
    sys.exit(0 if success else 1)
