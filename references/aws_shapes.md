# AWS4 Shape Style Reference

Verified mxgraph.aws4 style strings for draw.io. All shapes follow this base pattern:
```
shape=mxgraph.aws4.<name>;fillColor=<color>;strokeColor=#ffffff;fontColor=#ffffff;
labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;
sketch=0;aspect=fixed;
```

## Color Reference by Category

| Category | Color | Hex |
|---|---|---|
| Compute | Orange | `#E9822C` |
| Storage | Green | `#7AA116` |
| Database | Red | `#C7131F` |
| Networking | Purple | `#8C4FFF` |
| Security | Dark Red | `#DD3522` |
| Messaging | Pink | `#E7157B` |
| Developer Tools | Red | `#C7131F` |
| AI/ML | Teal | `#01A88D` |
| Management | Pink | `#E7157B` |

---

## Compute

### EC2
```
shape=mxgraph.aws4.ec2;fillColor=#E9822C;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Lambda
```
shape=mxgraph.aws4.lambda;fillColor=#E9822C;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### ECS
```
shape=mxgraph.aws4.ecs;fillColor=#E9822C;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### EKS
```
shape=mxgraph.aws4.eks;fillColor=#E9822C;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Fargate
```
shape=mxgraph.aws4.fargate;fillColor=#E9822C;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

---

## Storage

### S3
```
shape=mxgraph.aws4.s3;fillColor=#7AA116;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### EBS
```
shape=mxgraph.aws4.volume;fillColor=#7AA116;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### EFS
```
shape=mxgraph.aws4.efs;fillColor=#7AA116;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

---

## Database

### RDS
```
shape=mxgraph.aws4.rds;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### DynamoDB
```
shape=mxgraph.aws4.dynamodb;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Redshift
```
shape=mxgraph.aws4.redshift;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### ElastiCache
```
shape=mxgraph.aws4.elasticache;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Aurora
```
shape=mxgraph.aws4.aurora;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### OpenSearch
```
shape=mxgraph.aws4.opensearch_service;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

---

## Networking

### VPC
```
shape=mxgraph.aws4.vpc;fillColor=#8C4FFF;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### ALB (Application Load Balancer)
```
shape=mxgraph.aws4.application_load_balancer;fillColor=#8C4FFF;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### NLB (Network Load Balancer)
```
shape=mxgraph.aws4.network_load_balancer;fillColor=#8C4FFF;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### CloudFront
```
shape=mxgraph.aws4.cloudfront;fillColor=#8C4FFF;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Route53
```
shape=mxgraph.aws4.route_53;fillColor=#8C4FFF;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Transit Gateway
```
shape=mxgraph.aws4.transit_gateway;fillColor=#8C4FFF;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### API Gateway
```
shape=mxgraph.aws4.api_gateway;fillColor=#8C4FFF;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

---

## Security

### WAF
```
shape=mxgraph.aws4.waf;fillColor=#DD3522;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Shield
```
shape=mxgraph.aws4.shield;fillColor=#DD3522;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Cognito
```
shape=mxgraph.aws4.cognito;fillColor=#DD3522;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### IAM
```
shape=mxgraph.aws4.role;fillColor=#DD3522;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### KMS
```
shape=mxgraph.aws4.key_management_service;fillColor=#DD3522;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Secrets Manager
```
shape=mxgraph.aws4.secrets_manager;fillColor=#DD3522;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### GuardDuty
```
shape=mxgraph.aws4.guardduty;fillColor=#DD3522;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Security Hub
```
shape=mxgraph.aws4.security_hub;fillColor=#DD3522;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

---

## Messaging & Integration

### SNS
```
shape=mxgraph.aws4.sns;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### SQS
```
shape=mxgraph.aws4.sqs;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### EventBridge
```
shape=mxgraph.aws4.eventbridge;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Step Functions
```
shape=mxgraph.aws4.step_functions;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Kinesis Data Streams
```
shape=mxgraph.aws4.kinesis_data_streams;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### MSK (Managed Kafka)
```
shape=mxgraph.aws4.managed_streaming_for_apache_kafka;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

---

## Analytics & Data

### Glue
```
shape=mxgraph.aws4.glue;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Athena
```
shape=mxgraph.aws4.athena;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Kinesis Data Firehose
```
shape=mxgraph.aws4.kinesis_data_firehose;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### QuickSight
```
shape=mxgraph.aws4.quicksight;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

---

## Developer Tools

### CodePipeline
```
shape=mxgraph.aws4.codepipeline;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### CodeBuild
```
shape=mxgraph.aws4.codebuild;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### CodeCommit
```
shape=mxgraph.aws4.codecommit;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### CodeDeploy
```
shape=mxgraph.aws4.codedeploy;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### ECR
```
shape=mxgraph.aws4.ecr;fillColor=#E9822C;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

---

## Management & Monitoring

### CloudWatch
```
shape=mxgraph.aws4.cloudwatch;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### CloudWatch Logs
```
shape=mxgraph.aws4.cloudwatch;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### CloudTrail
```
shape=mxgraph.aws4.cloudtrail;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Config
```
shape=mxgraph.aws4.config;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Organizations
```
shape=mxgraph.aws4.organizations;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Control Tower
```
shape=mxgraph.aws4.control_tower;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### AWS App Config
```
shape=mxgraph.aws4.app_config;fillColor=#E7157B;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

---

## AI/ML

### Bedrock
```
shape=mxgraph.aws4.bedrock;fillColor=#01A88D;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### SageMaker
```
shape=mxgraph.aws4.sagemaker;fillColor=#01A88D;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

---

## Internet / Generic

### Internet (external cloud / traffic source)
The generic "Internet" entry point is NOT an AWS service — use the standard cloud shape.
Do NOT use `mxgraph.aws4.internet_gateway` here; that shape is the VPC IGW (a specific AWS resource).
```
shape=cloud;fillColor=#FFFFFF;strokeColor=#232F3E;fontColor=#232F3E;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;
```
Label it `Internet`. Size: `width="78" height="60"`.

### Internet Gateway (VPC IGW)
The actual AWS VPC Internet Gateway resource that lives inside a VPC:
```
shape=mxgraph.aws4.internet_gateway;fillColor=#8C4FFF;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### NAT Gateway
```
shape=mxgraph.aws4.nat_gateway;fillColor=#8C4FFF;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### General User / Client
```
shape=mxgraph.aws4.user;fillColor=#232F3E;strokeColor=#ffffff;fontColor=#232F3E;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Developer Workstation / Laptop
```
shape=mxgraph.aws4.traditional_server;fillColor=#232F3E;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

---

## Shared Services

### Directory Service
```
shape=mxgraph.aws4.directory_service;fillColor=#DD3522;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### Route53 Resolver
```
shape=mxgraph.aws4.route_53_resolver;fillColor=#8C4FFF;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```

### OpenSearch Serverless
```
shape=mxgraph.aws4.opensearch_service;fillColor=#C7131F;strokeColor=#ffffff;fontColor=#ffffff;labelPosition=bottom;verticalLabelPosition=top;verticalAlign=top;align=center;sketch=0;aspect=fixed;
```
