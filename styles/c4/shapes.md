# C4 Model Shape Styles for draw.io

Source-verified from `jgraph/drawio` repository (c4.js) and real C4 diagram files.

## Colors

| Element | fillColor | strokeColor | fontColor |
|---|---|---|---|
| Internal Person | `#08427b` | `#3c7fc0` | `#ffffff` |
| Internal Software System | `#1168bd` | `#0f5eaa` | `#ffffff` |
| Internal Container | `#438dd5` | `#3c7fc0` | `#ffffff` |
| Internal Component | `#85bbf0` | `#78a8d8` | `#000000` |
| External Person | `#686868` | `#8a8a8a` | `#ffffff` |
| External System/Container | `#999999` | `#8a8a8a` | `#ffffff` |

## Person

```
shape=mxgraph.c4.person;fillColor=#08427b;fontColor=#ffffff;strokeColor=#3c7fc0;
whiteSpace=wrap;html=1;align=center;spacingTop=0;fontSize=12;
```
- Width: 160, Height: 180
- External person: use fillColor=#686868;strokeColor=#8a8a8a

## Software System (internal)

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#1168bd;fontColor=#ffffff;
strokeColor=#0f5eaa;arcSize=7;fontSize=12;align=center;
```
- Width: 220, Height: 150

## Software System (external)

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#999999;fontColor=#ffffff;
strokeColor=#8a8a8a;arcSize=7;fontSize=12;align=center;
```

## Container (rectangle)

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#438dd5;fontColor=#ffffff;
strokeColor=#3c7fc0;arcSize=6;fontSize=12;align=center;
```
- Width: 210, Height: 150

## Container (database / cylinder)

```
shape=cylinder;whiteSpace=wrap;html=1;boundedLbl=1;rounded=0;
fillColor=#438dd5;fontColor=#ffffff;strokeColor=#3c7fc0;
fontSize=12;align=center;verticalAlign=top;spacingTop=4;
```
- Width: 200, Height: 170

## System Boundary

```
rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#cccccc;
strokeWidth=2;dashed=1;verticalAlign=top;fontSize=14;fontStyle=1;
fontColor=#555555;arcSize=2;align=center;
```

## Relationship Edges

All edges use `parent="1"` (root layer).

```
edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;strokeColor=#707070;
strokeWidth=2;fontColor=#707070;fontSize=11;
```

For dashed relationships (e.g., async or reply): add `dashed=1;`

## Label Format (HTML, html=1 required)

```html
<b>Element Name</b><br>
<font style="font-size:10px;">[Type]</font><br>
<font style="font-size:11px;font-style:italic;">Description text here.</font>
```

## Multi-Page Conventions

- Page 1: System Context (`1 - System Context`)
- Page 2: Containers (`2 - Containers`)
- Page 3: Components (`3 - Components`)
- draw.io CLI: `--page-index 1` for first page, `--page-index 2` for second
