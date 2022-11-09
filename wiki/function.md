# Supported Network Functions

## Introduction

Katana Slice Manager keeps a repository with all the Network Functions that are supported by the underlying platform infrastructure. The Network Functions are selected by the Katana Slice Mapping module when the slice sst is defined. Then, they are used for the actual deployment of the Slice by Katana LCM module, after the placement process is completed.

## Use

Before the slice creation phase, Katana admin must add the supported Network Functions by the underlying platform. There are three ways to do that:

* Use the REST API at <<http://<katana_IP>:8001/api/function>>. Refer [NBI REST API docs](nbi) to for more information regarding this API.
* Use the `katana function <action> [id] [-f file]` command. Refer to [katana cli tool docs](cli) for more information regarding this command.

> Example [supported Network Functions](https://github.com/medianetlab/katana-slice_manager/tree/master/example_config_files/Functions)

## The JSON Schema model for the supported Network Functions

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",

  "definitions": {
    "ns": {
      "type": "object",
      "description": "A Network Service",
      "properties":{
        "nfvo-id":{
          "type": "string",
          "description": "The NFVO that will manage the life cycle of the NS"
        },
        "nsd-id": {
          "type": "string",
          "description": "The NSD id as defined on the NFVO"
        },
        "ns-name": {
          "type": "string",
          "description": "The name of the NS"
        },
        "placement": {
          "type": "number",
          "enum": [0, 1],
          "description": "1: Core, 2: Edge"
        },
        "optional":{
          "type": "boolean"
        }
      }
    },
    "pnf": {
      "type": "object",
      "description": "A Physical Network Service",
      "properties": {
        "pnf-id": {
          "type": "string",
          "description": "A Unique ID of the pnf"
        },
        "pnf-name": {
          "type": "string",
          "description": "The name of the PNF"
        },
        "description": {
          "type": "string"
        },
        "ip": {
          "type": "string",
          "description": "The management IP of the PNF"
        },
        "location": {
          "type": "string",
          "description": "The location of the PNF"
        },
        "optional":{
          "type": "boolean"
        }
      }
    }
  },

  "type": "object",
  "description": "A core slice network function",
  "properties": {
    "id": {
      "type": "string",
      "description": "A unique ID for this network function"
    },
    "name": {
      "type": "string",
      "description": "Optional name for the network function"
    },
    "gen": {
      "type": "number",
      "enum": [4, 5],
      "description" : "Type of the network function - 4: 4G, 5: 5G"
    },
    "func":{
      "type": "number",
      "enum": [0, 1],
      "description": "0: Core, 1: Radio"
    },
    "shared": {
      "type": "object",
      "description": "Defines if the function can be shared between different slices",
      "properties": {
        "availability": {
          "type": "boolean",
          "description": "true: shared, false: no shared"
        },
        "max_shared": {
          "type": "number",
          "description": "Max number of slices - If availability is true and max_shared not defined, it will be assumed unlimited availability"
        }
      },
      "required": ["availability"]
    },
    "type": {
      "type": "number",
      "enum": [0, 1],
      "description": "0: Virtual, 1: Physical"
    },
    "location": {
      "type": "string",
      "description": "Supported location"
    },
    "ns_list": {
      "type": "array",
      "description": "Conditional - If type == Virtual - A list of the NSs that will be part of the slice",
      "items": {
        "$ref": "#/definitions/ns"
      }
    },
    "pnf_list": {
      "type": "array",
      "description": "Conditional - If type == Physical - A list of the PNFs that will be part of the slice",
      "items": {
        "$ref": "#/definitions/pnf"
      }
    },
    "ems-id": {
      "type": "string",
      "description": "Optional - Defines the EMS that is responsible for D1&2 configuration"
    },
    "other_required_functions":{
      "type": "array",
      "description": "A list with the IDs of other functions that are required to be deployed along with this",
      "items": {
        "type": "string",
        "description": "ID of a network function"
      }
    },
    "other_supported_functions":{
      "type": "array",
      "description": "A list with the IDs of other functions that can be deployed along with this",
      "items": {
        "type": "string",
        "description": "ID of a network function"
      }
    }
  },
  "required": ["id", "gen", "func", "shared", "type", "location"]
}
```
