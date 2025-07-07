// infrastructure/bin/app.ts
import * as cdk from 'aws-cdk-lib';
import { NetworkingStack } from '../lib/networking-stack';
import { DatabaseStack } from '../lib/database-stack';
import { SecurityStack } from '../lib/security-stack';
import { ComputeStack } from '../lib/compute-stack';
import { ApiStack } from '../lib/api-stack';
import { MonitoringStack } from '../lib/monitoring-stack';

const app = new cdk.App();

// Get environment and region from context
const environment = app.node.tryGetContext('environment') || 'development';
const region = app.node.tryGetContext('region') || 'us-east-1';

const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT,
  region: region
};

// Stack naming convention
const stackPrefix = `uptime-monitor-${environment}`;

// Create stacks with dependencies
const networkingStack = new NetworkingStack(app, `${stackPrefix}-networking`, {
  env,
  environment,
  description: 'Networking infrastructure for API Uptime Monitor'
});

const securityStack = new SecurityStack(app, `${stackPrefix}-security`, {
  env,
  environment,
  vpc: networkingStack.vpc,
  description: 'Security resources for API Uptime Monitor'
});

const databaseStack = new DatabaseStack(app, `${stackPrefix}-database`, {
  env,
  environment,
  vpc: networkingStack.vpc,
  securityGroup: securityStack.databaseSecurityGroup,
  description: 'Database resources for API Uptime Monitor'
});

const computeStack = new ComputeStack(app, `${stackPrefix}-compute`, {
  env,
  environment,
  vpc: networkingStack.vpc,
  database: databaseStack.database,
  securityGroup: securityStack.lambdaSecurityGroup,
  description: 'Lambda functions for API Uptime Monitor'
});

const apiStack = new ApiStack(app, `${stackPrefix}-api`, {
  env,
  environment,
  lambdaFunctions: computeStack.lambdaFunctions,
  description: 'API Gateway and CloudFront for API Uptime Monitor'
});

const monitoringStack = new MonitoringStack(app, `${stackPrefix}-monitoring`, {
  env,
  environment,
  lambdaFunctions: computeStack.lambdaFunctions,
  database: databaseStack.database,
  description: 'Monitoring and alerting for API Uptime Monitor'
});

// Add stack dependencies
databaseStack.addDependency(networkingStack);
databaseStack.addDependency(securityStack);
computeStack.addDependency(databaseStack);
apiStack.addDependency(computeStack);
monitoringStack.addDependency(computeStack);

// Tags for all stacks
const tags = {
  Project: 'api-uptime-monitor',
  Environment: environment,
  ManagedBy: 'CDK'
};

Object.entries(tags).forEach(([key, value]) => {
  cdk.Tags.of(app).add(key, value);
});

app.synth();