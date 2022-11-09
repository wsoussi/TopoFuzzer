# Katana CLI Tool

Alongside Katana Slice Manager, a CLI tool is installed that consumes Katana's REST APIs described in [NBI page](nbi)

## Command Structure

The structure of each command is `katana <target_component> <action> [argument] [options]`
> You can use the `--help` option for the manual

```bash
Usage: katana [OPTIONS] COMMAND [ARGS]...

  katana-cli is a command-line tool that interacts with the katana slice
  manager

Options:
  --help  Show this message and exit.

Commands:
  base_slice_des  Query Slice Descriptors
  bootstrap       Bootstrap Katana
  ems             Manage EMS
  function        Manage supported Network Functions
  gst             Query added GSTs
  location        Manage Platform Location
  nfvo            Manage NFVOs
  ns              Query Network Service Descriptors
  policy          Manage Policy Engine
  resources       Query Resources
  slice           Manage slices
  vim             Manage VIMs
  wim             Manage WIM
```

## Target Components

| target | description | actions |
| ------ | ------ | ------ |
| slice | deployed slices | ls, inspect, add, rm |
| function | supported network functions by the underlying platform | ls, inspect, add, update, rm |
| nfvo | registered NFVO instances | ls, inspect, add, update, rm |
| wim | registered WIM instances | ls, inspect, add, update, rm |
| vim | registered VIM instances | ls, inspect, add, update, rm |
| ems | registered EMS instances | ls, inspect, add, update, rm |
| gst | received GSTs | ls, inspect |
| base_slice_des | descriptors of the core slice that can be referenced by the GST | ls, inspect, add, update, rm |
| resources | available platform resources | ls, inspect, add, update, rm |
| location | available platform locations | ls, inspect, add, update, rm |
| policy | registered platform policy engines | ls, inspect, add, update, rm |

## Actions

| action | description |
| ------ | ------ |
| ls | Return a list of the defined target |
| inspect <id\> | Return details for the id of the defined target |
| add -f <config-file\> | Add a new instance of the defined target |
| rm <id\> | Remove an instance of the defined target |
| update <id\> | Update an instance of the defined target |

## Arguments & Options

* Arguments are the id of the target component
* Options: -f file for add or update actions

## Examples

```bash
katana vim ls

VIM_ID                                  CREATED AT               TYPE                
c74dbbb7-c092-487c-9fbc-87b3cc96d86e    2019-06-06 10:55:53      openstack  
```

```bash
katana nfvo add -f nfvo.json

9f1b606d-fd72-4a2a-96e9-8c2a63cd8cb4
```

```bash
katana wim inspect b655bb43-bafc-4271-b3f4-9265f3d89711

{
  "_id": "b655bb43-bafc-4271-b3f4-9265f3d89711",
  "name": "tnm-wim",
  "description": "Athens Platform WIM",
  "url": "http://10.30.0.190:8000",
  "created_at": 1559818349.5475748
}
```
