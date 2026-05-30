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

Claude is responsible for topology, shape identity, and rough placement. Assign
non-overlapping x/y coordinates using the column-grid in Step 4. Never place all
vertices at x="0" y="0" — they will stack on top of each other and render as an
unreadable pile. draw.io's **Arrange → Layout** function refines exact positioning
after the file opens.

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

Write this topology plan in your response before generating any XML.
This is required — do not skip it or generate XML without writing the plan first:

```
Containers: [list VPCs, subnets, AZs, accounts]
Nodes: [list every service with its container]
Edges: [list every connection as SOURCE → TARGET with label if needed]
Layout direction: [TB for top-down, LR for left-right]
```

This prevents orphaned edge references — the single most common structural error.

Only begin generating XML after the topology plan is written out above.

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
      math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Minimal reference example

A correct 3-node diagram to use as a structural reference. Every real diagram
follows this same pattern — more nodes, same structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="" agent="Claude Code drawio-aws skill"
  version="24.0.0" type="device">
  <diagram name="Architecture" id="diagram-1">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10"
      guides="1" tooltips="1" connect="1" arrows="1" fold="1"
      page="0" pageScale="1" pageWidth="1169" pageHeight="827"
      math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="cf1" value="CloudFront"
          style="shape=mxgraph.aws4.cloudfront;fillColor=#8C4FFF;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;"
          vertex="1" parent="1">
          <mxGeometry x="100" y="120" width="78" height="78" as="geometry"/>
        </mxCell>
        <mxCell id="alb1" value="ALB"
          style="shape=mxgraph.aws4.application_load_balancer;fillColor=#8C4FFF;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;"
          vertex="1" parent="1">
          <mxGeometry x="350" y="120" width="78" height="78" as="geometry"/>
        </mxCell>
        <mxCell id="ec2-1" value="EC2 App"
          style="shape=mxgraph.aws4.ec2;fillColor=#E9822C;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;"
          vertex="1" parent="1">
          <mxGeometry x="600" y="120" width="78" height="78" as="geometry"/>
        </mxCell>
        <mxCell id="edge-cf-alb" value="HTTPS" edge="1" source="cf1" target="alb1" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="edge-alb-ec2" value="HTTP" edge="1" source="alb1" target="ec2-1" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Key patterns to note: containers before service nodes before edges; descriptive
IDs; column-grid x coordinates (100 → 350 → 600); uniform 78×78 icon size;
`parent="1"` on all root-level cells including edges.

### Column-grid coordinate reference

Assign x/y from this grid. Tiers run left-to-right; services stack top-to-bottom
within each tier. Adjust column spacing if the diagram is wider than average.

| Tier | x |
|---|---|
| External / Internet / Users | 100 |
| Entry (IGW, ALB, CloudFront, API GW) | 350 |
| App / Compute (EC2, Lambda, ECS, EKS) | 600 |
| Data (RDS, DynamoDB, ElastiCache, S3) | 850 |
| Auxiliary (SQS, SNS, Secrets Manager, etc.) | 1100 |

**Row spacing:** first service in a tier at y=120; increment y by 150 for each
additional service in the same tier.

**Children inside containers** (icons inside a VPC, subnet, or AZ) use coordinates
relative to the container, not the canvas. Place the first child at x=40, y=60
and increment by 110 horizontally or 120 vertically within the container.

**Container sizing:** size each container to encompass all its children plus 40px
padding on every side. Containers at the root level use absolute x/y from the
grid; nested containers use parent-relative coordinates.

### Vertex placement rules

- Service icons: `width="78" height="78"` (standard AWS icon size)
- Container cells (VPC, subnet, AZ): size to frame their children with 40px padding
- Use the column-grid above for x/y — coordinates must be non-overlapping
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
  <mxGeometry x="200" y="50" width="700" height="500" as="geometry"/>
</mxCell>
```

**Public Subnet:**
```xml
<mxCell id="subnet-pub1" value="Public Subnet"
  style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],
    [1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];
    shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_subnet;
    strokeColor=#147EBA;fillColor=#E6F2F8;verticalAlign=top;align=center;
    spacingTop=25;fontColor=#147EBA;dashed=0;fontSize=11;"
  vertex="1" parent="vpc1">
  <mxGeometry x="40" y="60" width="280" height="380" as="geometry"/>
</mxCell>
```

**Private Subnet:**
```xml
<mxCell id="subnet-prv1" value="Private Subnet"
  style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],
    [1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];
    shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_subnet;
    strokeColor=#147EBA;fillColor=#EBF5FB;verticalAlign=top;align=center;
    spacingTop=25;fontColor=#147EBA;dashed=0;fontSize=11;"
  vertex="1" parent="vpc1">
  <mxGeometry x="380" y="60" width="280" height="380" as="geometry"/>
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
  <mxGeometry x="40" y="60" width="620" height="380" as="geometry"/>
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
  <mxGeometry x="150" y="30" width="900" height="650" as="geometry"/>
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
- Avoid `<Array as="points">` waypoints — manual routing is rarely needed and clutters the XML.

### ID assignment rules

- `id="0"` and `id="1"` are reserved — do not use for anything else
- Use descriptive IDs: `vpc1`, `subnet-pub1`, `ec2-app1`, `rds-primary`, `edge-alb-ec2`
- IDs must be unique across the entire file
- Assign IDs sequentially (containers first, then services, then edges) so every
  `source`/`target` reference points to a cell that already appears earlier in the XML

### Absolute prohibitions

The following will cause the file to fail or look broken:

- XML comments (`<!-- -->`) — forbidden entirely; they waste tokens and can cause parse errors
- `<Array as="points">` waypoints on edges
- `id="0"` or `id="1"` used for anything other than the two foundation cells
- Any `mxCell` without a `parent` attribute
- Duplicate IDs anywhere in the file
- Base64-compressed diagram content — use raw XML only
- `postLayout` attribute on `mxGraphModel` — draw.io desktop silently ignores it; use explicit x/y coordinates instead

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
- To refine positioning: open in draw.io, then use **Arrange → Layout** for a cleaner result

---

## Multi-Page Diagrams

If the architecture has more than 25 service nodes, split it into multiple logical
pages rather than crowding one canvas. Each page gets its own `<diagram>` element:

```xml
<mxfile host="app.diagrams.net" modified="" agent="Claude Code drawio-aws skill"
  version="24.0.0" type="device">
  <diagram name="Overview" id="page-overview">
    <mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/></root></mxGraphModel>
  </diagram>
  <diagram name="Network Detail" id="page-network">
    <mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/></root></mxGraphModel>
  </diagram>
  <diagram name="Data Tier" id="page-data">
    <mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/></root></mxGraphModel>
  </diagram>
</mxfile>
```

This mirrors how AWS reference architecture PDFs are structured and makes the
diagrams more usable in client presentations.
