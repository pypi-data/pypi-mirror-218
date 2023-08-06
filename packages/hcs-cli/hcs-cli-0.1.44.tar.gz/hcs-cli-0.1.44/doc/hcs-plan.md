# HCS Plan

HCS Plan is the deployment engine to manage HCS resources in a declarative way.

## File Types

### Blueprint
A file that consists of the resources to be deployed, normally with varieties of variables.

### Variable File
A file that contains all the variables that required by a blueprint file.

### Plan File
- Plan file is the simple composition of blueprint file and the related variable file.
- Plan file is the deployment input of HCS plan engine.

### State File
- The deployment related states of a plan.

## Principles
### Provider
- Each provider should focus on a single API
- Resources should represent a single API object
- Resource and attribute schema should closely match the underlying API


## Syntax
### Sections
#### deploymentId
The unique deployment ID to distinguish one deployment from another. Resources will be tagged based on the deploymentId if possible, and smart refresh should also consider deploymentId to identify related resource, upon missing previous state.

#### vars
The input of the blueprint. All top-level variables are specified here.

#### defaults
A section to help deduplicate common variables.

#### resources
The resources to be created. A map from unique resource name to resource definition.

### Repeated Items
Example:
```
vars:
  tenantId: <the-tenant-id>
  userEmails:
  - u1@mydomain.com
  - u2@mydomain.com
resources:
  myAADGroup:
    kind: azure/aad-group
    data:
        tenant: ${vars.tenantId}
  myAADUsers:
    kind: azure/aad-user
    for: email in vars.userEmails
    data:
      group: ${myAADGroup.id}
```

In azure/aad-user resource handler, the received data object will have 'email' added, as declared in the 'for' statement:
```
    {
        'group': '<group-id>'
        'email': '<one-of-the-emails>
    }
```

### Map list to a new list
```
vars:
  tenantId: <the-tenant-id>
  userEmails:
  - u1@mydomain.com
  - u2@mydomain.com
resources:
  myAADGroup:
    kind: azure/aad-group
    data:
        tenant: ${vars.tenantId}
  myAADUsers:
    kind: azure/aad-user
    for: email in vars.userEmails
    data:
      group: ${myAADGroup.id}
  myEntitlement:
    kind: hcs/entitlement
    data:
      orgId: ${vars.orgId}
      poolIds:
      - ${myPoolGroup.id}
      resourceDetails:
      - poolId: ${myPoolGroup.id}
      userIds: ${[for u in myAADUser: u.id]}
```

The resource myEntitlement will receive data object with field 'userIds' as an string array:
```
{
  ...
  'userIds': [ 'user-id1', 'user-id2' ]
}
```
### Referencing profile value
```
resources:
  myLaunchItem:
    kind: hcs/launch-item
    data:
      users: ...
      entitlementId: ...
      domainName: ...
      stackUrl: ${profile.hcs.url}
```


## Cheatsheet
| Command | Description |
| ------- | ----------- |
| hcs plan deploy -f \<filename\> --sequential | Deploy resources sequentially, for debugging |
| hcs play deploy -f \<filename\> --resource \<resource-id\> | Deploy only the specified resource (and dependencies). |