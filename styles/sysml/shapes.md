# SysML BDD Shape Styles for draw.io

Source-verified from `jgraph/drawio` repository (Sidebar.js, sysml.xml, drawio-diagrams UML templates).

## Block (swimlane with stackLayout)

```
swimllane;fontStyle=0;align=center;verticalAlign=top;
childLayout=stackLayout;horizontal=1;startSize=40;
horizontalStack=0;resizeParent=1;resizeParentMax=0;
resizeLast=1;collapsible=0;marginBottom=0;
fillColor=#dae8fc;strokeColor=#6c8ebf;fontColor=#000000;html=1;
```

**Value** (html=1 required for stereotype rendering):
```html
<b>«block»</b><br><b>BlockName</b>
```
For abstract blocks: use `<i>BlockName</i>` (italic name).

**startSize=40** accommodates the two-line «block» / Name header.

## Compartment Label Row (child of block)

```
text;strokeColor=none;fillColor=#dae8fc;align=left;
verticalAlign=top;spacingLeft=4;overflow=hidden;
rotatable=0;fontStyle=1;
```
- `value`: compartment name (`parts`, `values`, `operations`, `constraints`)
- Height: 14px
- y position: startSize (40) + cumulative height of prior children
- Width: same as parent block

## Compartment Content Row (child of block)

```
text;strokeColor=none;fillColor=none;align=left;
verticalAlign=top;spacingLeft=4;overflow=hidden;rotatable=0;
```
- `value`: newline-separated properties using `&#xa;` in XML
- Each line ~18px tall; set height = lines × 18 + 4
- Width: same as parent block

## Compartment Separator (child of block)

```
line;strokeWidth=1;fillColor=none;rotatable=0;strokeColor=#6c8ebf;
```
- Height: 8px
- Width: same as parent block

## Child Geometry Rules

With `childLayout=stackLayout`, children are stacked automatically when opened in draw.io.
For correct CLI export rendering, set explicit y positions:
- First child: y = startSize (40)
- Each subsequent child: y = previous_y + previous_height

## Block Height Calculation

```
block_height = startSize + sum(child_heights)
```

Example for a block with parts (3 lines) + values (2 lines) + operations (3 lines):
```
40 + 14 + 54 + 8 + 14 + 36 + 8 + 14 + 54 = 242
```

## Diagram Frame

```
shape=mxgraph.sysml.package;html=1;overflow=fill;whiteSpace=wrap;
fillColor=none;gradientColor=none;fontSize=12;fontStyle=1;
align=left;spacingLeft=10;strokeColor=#000000;strokeWidth=2;
verticalAlign=top;spacingTop=6;
```

**Frame label format**: `bdd [Package] ModelElementName [DiagramName]`

## Composition Relationship (filled diamond at owner)

```
startArrow=diamondThin;startFill=1;startSize=20;
endArrow=none;html=1;edgeStyle=orthogonalEdgeStyle;
```
- `source` = composite (owner, diamond end)
- `target` = part
- Add multiplicity as edge `value` label when > 1 (e.g., `[4]`)

## Generalization Relationship (hollow triangle at supertype)

```
endArrow=block;endSize=16;endFill=0;
html=1;edgeStyle=orthogonalEdgeStyle;
```
- `source` = subtype
- `target` = supertype (hollow triangle here)

## Aggregation (hollow diamond)

```
startArrow=diamondThin;startFill=0;startSize=20;
endArrow=none;html=1;edgeStyle=orthogonalEdgeStyle;
```

## Association (plain line with open arrow)

```
endArrow=open;endSize=12;html=1;edgeStyle=orthogonalEdgeStyle;
```

## Canonical Example

See `examples/sysml-vehicle-bdd.drawio` — OMG AutomobileSystem BDD:
- AutomobileSystem → PowerTrain (composition)
- AutomobileSystem → Wheel [4] (composition)
- PowerTrain → Engine (composition)
- PowerTrain → Transmission (composition)
- FourCylinderEngine → Engine (generalization)
- SixCylinderEngine → Engine (generalization)
