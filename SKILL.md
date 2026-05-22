---
name: drawio-aws
description: Generate professional, client-ready AWS architecture diagrams as
  draw.io (.drawio) files. Triggers on any request for AWS architecture diagrams,
  system diagrams, cloud architecture diagrams, infrastructure diagrams, AWS
  reference architectures, solution architecture documents, or draw.io files
  involving AWS services. Also triggers when the user says "diagram this
  architecture", "create a drawio", "make an architecture diagram", "draw the
  AWS infrastructure", or describes any multi-service AWS topology. Use this
  skill even if the user only describes the architecture verbally — infer the
  diagram from context. Always use this skill when AWS services and diagramming
  are both implied, even if neither word appears explicitly.
---

# draw.io AWS Architecture Diagram Skill

## What This Skill Does

Generates `.drawio` XML files containing professional AWS architecture diagrams
that open directly in draw.io desktop. The output is always a valid, editable
file — not an image.

## Core Design Principle

Claude is responsible for topology and shape identity. draw.io's layout engine
is responsible for positioning. Never attempt to compute or assign meaningful
x/y coordinates — that is not your job and you will do it badly. Place every
vertex at x="0" y="0" and let postLayout handle everything.

---

## Step 1: Understand the Request

Before generating XML, identify:
1. **Diagram type** — three-tier web app, serverless, EKS-based, data pipeline,
   security architecture, or other
2. **Scope** — single region, multi-region, multi-account, hybrid
3. **Services** — list every AWS service that must appear
4. **Data/traffic flow** — what connects to what, and in which direction
5. **Grouping boundaries** — VPC(s), subnets, availability zones, accounts

If the request is ambiguous on any of these five points, ask before generating.
A clarifying question saves more time than a wrong diagram.

---

## Step 2: Check the Shape Reference

Before writing any XML, read `references/aws_shapes.md` and look up the exact
style string for every AWS service in the diagram. Never guess or approximate a
style string — wrong shapes are the most visible quality failure in a client
deliverable.

If a service is missing from `references/aws_shapes.md`, use this fallback
pattern (replace SERVICE_NAME and COLOR with correct values from the color
reference table in that file):

```
shape=mxgraph.aws4.SERVICE_NAME;fillColor=COLOR;strokeColor=#ffffff;
fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;
verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

---

## Step 3: Plan the Structure Before Writing XML

Write out a plain-text topology plan first:

```
Containers: [list VPCs, subnets, AZs, accounts]
Nodes: [list every service with its container]
Edges: [list every connection as SOURCE → TARGET with label if needed]
Layout direction: [TB for top-down, LR for left-right]
```

This prevents orphaned edge references — the single most common structural error.

---

## Step 4: Generate the XML

### Mandatory structure — no exceptions

Every diagram MUST begin with this exact skeleton:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="" agent="Claude Code drawio-aws skill"
  version="24.0.0" type="device">
  <diagram name="Architecture" id="diagram-1">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10"
      guides="1" tooltips="1" connect="1" arrows="1" fold="1"
      page="0" pageScale="1" pageWidth="1169" pageHeight="827"
      math="0" shadow="0"
      postLayout="LAYOUT_DIRECTIVE">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Replace `LAYOUT_DIRECTIVE` with the appropriate value:

| Diagram type | postLayout value |
|---|---|
| Three-tier web / standard architecture | `verticalHierarchical` |
| Pipeline / data flow (left to right) | `horizontalHierarchical` |
| Org chart / account hierarchy | `tree` |
| Complex mesh with many peers | `stress` |

### Vertex placement rules

- ALL vertices: `x="0" y="0"` — do not change this
- Service icons: `width="78" height="78"` (standard AWS icon size)
- Container cells (VPC, subnet, AZ): `width="400" height="300"` at `x="0" y="0"`
- Labels: use the `value` attribute; keep under 30 characters
- Font: `fontSize=11;fontStyle=1` for primary labels (bold)

### Container cells (VPC, Subnet, AZ, Region)

Copy the appropriate template from `templates/containers.xml`. The container
style strings are the most complex part of draw.io XML — do not write them
from memory.

**VPC:**
```xml
<mxCell id="vpc1" value="VPC (10.0.0.0/16)"
  style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],
    [1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];
    shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;
    strokeColor=#8C4FFF;fillColor=#F4ECFF;verticalAlign=top;align=center;
    spacingTop=25;fontColor=#8C4FFF;dashed=0;fontSize=12;"
  vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="300" as="geometry"/>
</mxCell>
```

**Public Subnet:**
```xml
<mxCell id="subnet-pub1" value="Public Subnet"
  style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],
    [1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];
    shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_public_subnet;
    strokeColor=#147EBA;fillColor=#E6F2F8;verticalAlign=top;align=center;
    spacingTop=25;fontColor=#147EBA;dashed=0;fontSize=11;"
  vertex="1" parent="vpc1">
  <mxGeometry x="0" y="0" width="180" height="150" as="geometry"/>
</mxCell>
```

**Private Subnet:**
```xml
<mxCell id="subnet-prv1" value="Private Subnet"
  style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],
    [1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];
    shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_private_subnet;
    strokeColor=#147EBA;fillColor=#EBF5FB;verticalAlign=top;align=center;
    spacingTop=25;fontColor=#147EBA;dashed=0;fontSize=11;"
  vertex="1" parent="vpc1">
  <mxGeometry x="0" y="0" width="180" height="150" as="geometry"/>
</mxCell>
```

**Availability Zone:**
```xml
<mxCell id="az1" value="Availability Zone 1"
  style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],
    [1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];
    shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_availability_zone;
    strokeColor=#147EBA;fillColor=none;verticalAlign=top;align=center;
    spacingTop=25;fontColor=#147EBA;dashed=1;fontSize=11;"
  vertex="1" parent="vpc1">
  <mxGeometry x="0" y="0" width="350" height="250" as="geometry"/>
</mxCell>
```

**AWS Account / Region boundary:**
```xml
<mxCell id="region1" value="us-east-1"
  style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],
    [1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];
    shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;
    strokeColor=#232F3E;fillColor=#FAFAFA;verticalAlign=top;align=center;
    spacingTop=25;fontColor=#232F3E;dashed=1;fontSize=12;"
  vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="700" height="500" as="geometry"/>
</mxCell>
```

### Edge rules

- Every edge must reference `source` and `target` IDs that already exist in the XML
- Use `parent="1"` for all edges (not a container ID — edges belong to the root layer)
- Standard edge style for data flow:

```xml
<mxCell id="edge1" value="HTTPS" edge="1" source="alb1" target="ec2-1" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

- Directional arrows (when flow direction matters):
  ```
  style="rounded=0;orthogonalLoop=1;jettySize=auto;exitX=1;exitY=0.5;
    exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;endArrow=block;"
  ```
- NEVER add `<Array as="points">` waypoints. postLayout routes edges automatically.

### ID assignment rules

- `id="0"` and `id="1"` are reserved — do not use for anything else
- Use descriptive IDs: `vpc1`, `subnet-pub1`, `ec2-app1`, `rds-primary`, `edge-alb-ec2`
- IDs must be unique across the entire file
- Assign IDs sequentially (containers first, then services, then edges) so every
  `source`/`target` reference points to a cell that already appears earlier in the XML

### Absolute prohibitions

The following will cause the file to fail or look broken:

- XML comments (`<!-- -->`) — forbidden entirely; they waste tokens and can cause parse errors
- Coordinates other than `x="0" y="0"` for vertices
- `<Array as="points">` waypoints on edges
- `id="0"` or `id="1"` used for anything other than the two foundation cells
- Any `mxCell` without a `parent` attribute
- Duplicate IDs anywhere in the file
- Base64-compressed diagram content — use raw XML only

---

## Step 5: Validate Before Delivering

After generating the XML, run the validation script:

```bash
python ~/.claude/skills/drawio-aws/scripts/validate_drawio.py output.drawio
```

If validation fails, read the error output and correct the XML before delivering
the file to the user. Self-correction is expected — do not deliver an invalid file.

---

## Step 6: Deliver

Save the file as `<diagram-name>.drawio` in the user's working directory or
wherever they specify. Tell the user:
- File name and location
- How many nodes/containers the diagram contains
- Any services you assumed or inferred (so they can correct them)
- draw.io will run auto-layout on first open — this is expected and correct

---

## Multi-Page Diagrams

If the architecture has more than 25 service nodes, split it into multiple logical
pages rather than crowding one canvas. Each page gets its own `<diagram>` element:

```xml
<mxfile ...>
  <diagram name="Overview" id="page-overview">
    <!-- high-level architecture -->
  </diagram>
  <diagram name="Network Detail" id="page-network">
    <!-- VPC and subnet detail -->
  </diagram>
  <diagram name="Data Tier" id="page-data">
    <!-- databases, caches, storage -->
  </diagram>
</mxfile>
```

This mirrors how AWS reference architecture PDFs are structured and makes the
diagrams more usable in client presentations.
