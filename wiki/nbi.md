# North Bound Interface REST APIs

You can reach Katana Slice Manager at **[http://<katana_ip>:8000](http://<katana_ip>:8000)** using the REST APIs listed below:
> Each data file is a link to a demo file

## Network Slice

### Available APIs

| Method | URI | Data | Description |
| ------ | ------ | ------ | ------ |
| GET | /api/slice | - | Returns a list of slices and their details |
| GET | /api/slice/<slice_id\> | - | Returns the details of specific slice |
| POST| /api/slice | [GST Example](https://github.com/medianetlab/katana-slice_manager/blob/master/katana-schemas/gst_model.json) | Adds a new network slice |
| GET | /api/slice/<slice_id\>/time | - | Returns Deployment time report |

### Examples

``` bash
echo $(curl -X POST -H "Content-Type: application/json" -d @slice_example.json http://10.100.129.104:8000/api/slice)

b8a8465d-3499-458c-bfda-5610e5dab8f1
```

## Supported Network Functions by the Platform Infrastructure

### Functions Available APIs

| Method | URI | Data | Description |
| ------ | ------ | ------ | ------ |
| GET | /api/function | - | Returns a list of supported network function and their details |
| GET | /api/function/<function_id\> | - | Returns the details of specific network function |
| POST| /api/function | [function Config file](https://github.com/medianetlab/katana-slice_manager/tree/master/example_config_files/Functions) | Add a new supported network function |
| DELETE | /api/function/<function_id\> | - | Removes a supported network function |
| PUT | /api/function/<function_id\> | [Netwotk Function Config file](https://github.com/medianetlab/katana-slice_manager/tree/master/example_config_files/Functions) | Updates a registered Network Function |

### Functions Examples

``` bash
echo $(curl -X POST -H "Content-Type: application/json" -d @function.json http://10.100.129.104:8000/api/function)

16600f0e-1120-496d-8053-51fc82fe3b72
```

``` bash
curl -XGET  http://10.100.129.104:8000/api/function | python -m json.tool

[
    {
        "_id": "16600f0e-1120-496d-8053-51fc82fe3b72",
        "created_at": 1582114017.0287354,
        "func": "Core",
        "func_id": "O5GCore_Core",
        "gen": "5G",
        "loc": "Core",
        "type": "Virtual"
    }
]

```

``` bash
curl -XGET  http://10.100.129.104:8000/api/function/16600f0e-1120-496d-8053-51fc82fe3b72 | python -m json.tool

{
    "_id": "16600f0e-1120-496d-8053-51fc82fe3b72",
    "created_at": 1582114017.0287354,
    "ems-id": "test-ems",
    "func": 0,
    "gen": 5,
    "id": "O5GCore_Core",
    "location": "Core",
    "name": "O5GCore_Core",
    "ns_list": [
        {
            "nfvo-id": "OSM5",
            "ns-name": "5GCore_GW_nsd",
            "nsd-id": "f27602a7-173d-4ead-ac7e-79bfbdfdaf44",
            "optional": false,
            "placement": 0
        },
        {
            "nfvo-id": "OSM5",
            "ns-name": "5GCore_MME-HSS_nsd",
            "nsd-id": "91e16ae4-d9f9-4787-aebf-e058dcf9d05f",
            "optional": false,
            "placement": 0
        },
        {
            "nfvo-id": "OSM5",
            "ns-name": "5GCore_PCRF_nsd",
            "nsd-id": "551b27ec-4903-4877-ac46-96e91a1e0d7a",
            "optional": true,
            "placement": 0
        },
        {
            "nfvo-id": "OSM5",
            "ns-name": "dummy_ns",
            "nsd-id": "65373e5a-679d-46b7-898a-e304652e5102",
            "optional": true,
            "placement": 0
        }
    ],
    "shared": {
        "availability": true
    },
    "tenants": [],
    "type": 0
}
```

## NFVO

### NFVO Available APIs

| Method | URI | Data | Description |
| ------ | ------ | ------ | ------ |
| GET | /api/nfvo | - | Returns a list of NFVO and their details |
| GET | /api/nfvo/<nfvo_id\> | - | Returns the details of specific NFVO |
| POST| /api/nfvo | [NFVO Config file](https://github.com/medianetlab/katana-slice_manager/blob/master/katana-schemas/components/nfvo_model.json) | Add a new NFVO instance |
| DELETE | /api/nfvo/<nfvo_id\> | - | Removes an NFVO instance |
| PUT | /api/nfvo/<nfvo_id\> | [NFVO Config file](https://github.com/medianetlab/katana-slice_manager/blob/master/katana-schemas/components/nfvo_model.json) | Updates a registered NFVO info |

### NFVO Examples

``` bash
echo $(curl -X POST -H "Content-Type: application/json" -d @nfvo.json http://10.100.129.104:8000/api/nfvo)

1280229b-c25d-4fa6-b420-5eafb46cd347
```

``` bash
curl -XGET  http://10.100.129.104:8000/api/nfvo | python -m json.tool

[
    {
        "_id": "ad7699c0-a7c0-4f88-9c19-7f6c87f71d20",
        "created_at": 1577724536.1213048,
        "nfvo_id": "OSM5",
        "type": "OSM"
    },
    {
        "_id": "1280229b-c25d-4fa6-b420-5eafb46cd347",
        "created_at": 1577724540.9773626,
        "nfvo_id": "OSM6",
        "type": "OSM"
    }
]

```

``` bash
curl -XGET  http://10.100.129.104:8000/api/nfvo/1280229b-c25d-4fa6-b420-5eafb46cd347 | python -m json.tool

{
    "_id": "1280229b-c25d-4fa6-b420-5eafb46cd347",
    "config": {},
    "created_at": 1577724540.9773626,
    "description": "NCSRD OSM Release 6",
    "id": "OSM6",
    "name": "Athens OSM6",
    "nfvoip": "10.200.64.53",
    "nfvopassword": "admin",
    "nfvousername": "admin",
    "tenantname": "admin",
    "tenants": {},
    "type": "OSM",
    "version": "6"
}

```

## WIM

### WIM Available APIs

| Method | URI | Data | Description |
| ------ | ------ | ------ | ------ |
| GET | /api/wim | - | Returns a list of WIM and their details |
| GET | /api/wim/<wim_id\> | - | Returns the details of specific WIM |
| POST| /api/wim | [WIM Config file](https://github.com/medianetlab/katana-slice_manager/blob/master/katana-schemas/components/wim_model.json) | Add a new WIM instance |
| DELETE | /api/wim/<wim_id\> | - | Removes a WIM instance |
| PUT | /api/wim/<wim_id\> | [WIM Config file](https://github.com/medianetlab/katana-slice_manager/blob/master/katana-schemas/components/wim_model.json) | Updates a registered WIM info |

### WIM Examples

```bash
echo $(curl -X POST -H "Content-Type: application/json" -d @wim.json http://10.100.129.104:8000/api/wim)

6ee47f45-51cb-46e9-a4bf-60a11f86f611
```

```bash
curl -XGET  http://10.100.129.104:8000/api/wim | python -m json.tool

[
    {
        "_id": "6ee47f45-51cb-46e9-a4bf-60a11f86f611",
        "created_at": 1577722847.5991163,
        "wim_id": "test-wim"
    }
]
```

```bash
curl -XGET  http://10.100.129.104:8000/api/wim/6ee47f45-51cb-46e9-a4bf-60a11f86f611 | python -m json.tool

{
    "_id": "6ee47f45-51cb-46e9-a4bf-60a11f86f611",
    "created_at": 1577722847.5991163,
    "description": "Test Katana WIM",
    "id": "test-wim",
    "name": "test-wim",
    "slices": {},
    "type": "odl-wim",
    "url": "https://jsonplaceholder.typicode.com"
}
```

## VIM

### VIM Available APIs

| Method | URI | Data | Description |
| ------ | ------ | ------ | ------ |
| GET | /api/vim | - | Returns a list of VIM and their details |
| GET | /api/vim/<vim_id\> | - | Returns the details of specific VIM |
| POST| /api/vim | [VIM Config file](https://github.com/medianetlab/katana-slice_manager/blob/master/katana-schemas/components/vim_model.json) | Add a new VIM instance |
| DELETE | /api/vim/<vim_id\> | - | Removes a VIM instance |
| PUT | /api/vim/<vim_id\> | [VIM Config file](https://github.com/medianetlab/katana-slice_manager/blob/master/katana-schemas/components/vim_model.json) | Updates a registered VIM info |

### VIM Examples

```bash
echo $(curl -X POST -H "Content-Type: application/json" -d @vim.json http://10.100.129.104:8000/api/vim)

391b1daa-4b99-4006-b9af-b242eb46abef
```

```bash
curl -XGET  http://10.100.129.104:8000/api/vim | python -m json.tool

[
    {
        "_id": "8b96c8b8-3861-4cdb-b506-bae9daa21953",
        "created_at": 1577723214.5738564,
        "type": "openstack",
        "vim_id": "mnl_cloud"
    },
    {
        "_id": "391b1daa-4b99-4006-b9af-b242eb46abef",
        "created_at": 1577723219.312977,
        "type": "openstack",
        "vim_id": "minilab_vim"
    }
]
```

```bash
curl -XGET  http://10.100.129.104:8000/api/vim/391b1daa-4b99-4006-b9af-b242eb46abef | python -m json.tool

{
    "_id": "391b1daa-4b99-4006-b9af-b242eb46abef",
    "admin_project_name": "admin",
    "auth_url": "http://10.100.128.2:5000/v3/",
    "config": {
        "security_groups": "TBD"
    },
    "created_at": 1577723219.312977,
    "description": "Edge VIM - IoRL/Minilab",
    "id": "minilab_vim",
    "location": "minilab",
    "name": "minilab_vim",
    "password": "ii70mseq",
    "tenants": {},
    "type": "openstack",
    "username": "admin",
    "version": "Queens"
}

```

## EMS

### EMS Available APIs

| Method | URI | Data | Description |
| ------ | ------ | ------ | ------ |
| GET | /api/ems | - | Returns a list of EMS and their details |
| GET | /api/ems/<ems_id\> | - | Returns the details of specific EMS |
| POST| /api/ems | [EMS Config file](https://github.com/medianetlab/katana-slice_manager/blob/master/katana-schemas/components/ems_model.json) | Add a new EMS instance |
| DELETE | /api/ems/<ems_id\> | - | Removes a EMS instance |
| PUT | /api/ems/<ems_id\> | [EMS Config file](https://github.com/medianetlab/katana-slice_manager/blob/master/katana-schemas/components/ems_model.json) | Updates a registered EMS info |

### EMS Examples

```bash
echo $(curl -X POST -H "Content-Type: application/json" -d @ems.json http://10.100.129.104:8000/api/ems)

7264a56d-e419-4731-b3f9-78976dc80bdd
```

```bash
curl -XGET  http://10.100.129.104:8000/api/ems | python -m json.tool

[
    {
        "_id": "9e78d91f-5425-4c04-a8c6-c6eb80451a59",
        "created_at": 1577724562.6716278,
        "ems_id": "test_ems"
    },
    {
        "_id": "7264a56d-e419-4731-b3f9-78976dc80bdd",
        "created_at": 1577724567.1723485,
        "ems_id": "Amarisoft_EMS"
    }
]

```

```bash
curl -XGET  http://10.100.129.104:8000/api/ems/7264a56d-e419-4731-b3f9-78976dc80bdd | python -m json.tool

{
    "_id": "7264a56d-e419-4731-b3f9-78976dc80bdd",
    "created_at": 1577724567.1723485,
    "description": "Athens Platform EMS",
    "id": "Amarisoft_EMS",
    "name": "athens_ems",
    "type": "Amarisoft_EMS",
    "url": "https://jsonplaceholder.typicode.com"
}

```

## PDU

### Available APIs

| Method | URI | Data | Description |
| ------ | ------ | ------ | ------ |
| GET | /api/pdu | - | Returns a list of PDUs and their details |
| GET | /api/pdu/<pdu_id\> | - | Returns the details of specific PDU |
| POST| /api/pdu | [PDU Config file](https://github.com/medianetlab/katana-slice_manager/blob/master/katana-schemas/components/pdu_model.json) | Add a new PDU instance |
| DELETE | /api/pdu/<pdu_id\> | - | Removes a PDU instance |
| PUT | /api/pdu/<pdu_id\> | [PDU Config file](https://github.com/medianetlab/katana-slice_manager/blob/master/katana-schemas/components/pdu_model.json) | Updates a registered PDU info |

### Examples

```
echo $(curl -X POST -H "Content-Type: application/json" -d @pdu.json http://10.100.129.104:8000/api/pdu)

e189a253-4c9b-4b5b-a66b-8c1d3229d819
```

```
curl -XGET  http://10.100.129.104:8000/api/pdu | python -m json.tool

[
    {
        "_id": "e189a253-4c9b-4b5b-a66b-8c1d3229d819",
        "created_at": 1578403792.045132,
        "location": "Minilab",
        "pdu_id": "AmarisoftENB"
    }
]

```

```
curl -XGET  http://10.100.129.104:8000/api/pdu/e189a253-4c9b-4b5b-a66b-8c1d3229d819 | python -m json.tool

{
    "_id": "e189a253-4c9b-4b5b-a66b-8c1d3229d819",
    "created_at": 1578403792.045132,
    "description": "Amarisoft Minilab ENB",
    "id": "AmarisoftENB",
    "ip": "10.2.1.11",
    "location": "Minilab",
    "name": "AmarisoftENB",
    "tenants": []
}

```

## GST

> GSTs are stored with each slice creation request

### Available APIs

| Method | URI | Data | Description |
| ------ | ------ | ------ | ------ |
| GET | /api/gst | - | Returns a list of GSTs and their details |
| GET | /api/gst/<gst_id\> | - | Returns the details of specific GST |

### Examples

```
curl -XGET  http://10.100.129.104:8000/api/gst | python -m json.tool

[
    {
        "_id": "f70fc0e5-c19b-4096-80f1-c53974510bbb"
    }
]

```

```
curl -XGET  http://10.100.129.104:8000/api/gst/f70fc0e5-c19b-4096-80f1-c53974510bbb | python -m json.tool

{
    "_id": "f70fc0e5-c19b-4096-80f1-c53974510bbb",
    "base_slice_descriptor": {
        "base_slice_des_id": "5GCore_embb",
        "base_slice_des_ref": null,
        "coverage": [],
        "delay_tolerance": true,
        "deterministic_communication": null,
        "device_velocity": null,
        "group_communication_support": null,
        "isolation_level": null,
        "mission_critical_support": null,
        "mmtel_support": null,
        "mtu": null,
        "nb_iot": null,
        "network_DL_throughput": null,
        "network_UL_throughput": null,
        "nonIP_traffic": null,
        "number_of_connections": null,
        "number_of_terminals": null,
        "positional_support": null,
        "qos": [],
        "radio_spectrum": [],
        "simultaneous_nsi": null,
        "terminal_density": null,
        "ue_DL_throughput": null,
        "ue_UL_throughput": null
    },
    "service_descriptor": {
        "ns_list": [
            {
                "nfvo-id": "OSM5",
                "ns-name": "Amarisoft_vEPC",
                "nsd-id": "a9ac7f6e-9b44-4f99-860b-db4c94794b4d",
                "optional": false,
                "placement": 0
            }
        ]
    },
    "test_descriptor": null
}

```

## Core Slice Descriptor

> Is used by the GST in order to describe the core slice functions and parameters. Slice Descriptors are also stored from the GST when a new slice is created.

### Available APIs

| Method | URI | Data | Description |
| ------ | ------ | ------ | ------ |
| GET | /api/slice_des | - | Returns a list of Core Slice Descriptors and their details |
| GET | /api/slice_des/<slice_des_id\> | - | Returns the details of specific Core Slice Descriptor |
| POST| /api/slice_des | Core Slice Descriptor Config file | Add a new Core Slice Descriptor instance |
| DELETE | /api/slice_des/<slice_des_id\> | - | Removes a Core Slice Descriptor instance |
| PUT | /api/slice_des/<slice_des_id\> | [Core Slice Descriptor Config file]() | Updates a Core Slice Descriptor info |

### Examples

```
echo $(curl -X POST -H "Content-Type: application/json" -d @slice_des.json http://10.100.129.104:8000/api/slice_des)

fb419cb5-e317-4f8f-be9c-a8e7c91495d1
```

```
curl -XGET  http://10.100.129.104:8000/api/slice_des | python -m json.tool

[
    {
        "_id": "fb419cb5-e317-4f8f-be9c-a8e7c91495d1",
        "base_slice_des_id": "5GCore_embb"
    }
]


```

```
curl -XGET  http://10.100.129.104:8000/api/slice_des/fb419cb5-e317-4f8f-be9c-a8e7c91495d1 | python -m json.tool

{
    "_id": "fb419cb5-e317-4f8f-be9c-a8e7c91495d1",
    "base_slice_des_id": "5GCore_embb",
    "base_slice_des_ref": null,
    "coverage": [],
    "delay_tolerance": true,
    "deterministic_communication": null,
    "device_velocity": null,
    "group_communication_support": null,
    "isolation_level": null,
    "mission_critical_support": null,
    "mmtel_support": null,
    "mtu": null,
    "nb_iot": null,
    "network_DL_throughput": null,
    "network_UL_throughput": null,
    "nonIP_traffic": null,
    "number_of_connections": null,
    "number_of_terminals": null,
    "positional_support": null,
    "qos": [],
    "radio_spectrum": [],
    "simultaneous_nsi": null,
    "terminal_density": null,
    "ue_DL_throughput": null,
    "ue_UL_throughput": null
}

```

## Resources

### Available APIs

| Method | URI | Data | Description |
| ------ | ------ | ------ | ------ |
| GET | /api/resources | - | Returns a list of the platform available resources |
| GET | /api/resources/<location\> | - | Returns a list of the platform available resources for a specific location |

### Examples

```
curl -XGET  http://10.100.129.104:8000/api/resources | python -m json.tool

{
    "PDUs": [
        {
            "id": "AmarisoftENB",
            "location": "Minilab",
            "name": "AmarisoftENB",
            "tenants": []
        }
    ],
    "VIMs": [
        {
            "avail_resources": null,
            "id": "mnl_cloud",
            "location": "core",
            "max_resources": null,
            "name": "core_vim",
            "tenants": {},
            "type": "openstack"
        },
        {
            "avail_resources": null,
            "id": "minilab_vim",
            "location": "minilab",
            "max_resources": null,
            "name": "minilab_vim",
            "tenants": {},
            "type": "openstack"
        }
    ]
}

```

```
curl -XGET  http://10.100.129.104:8000/api/resources/minilab | python -m json.tool

{
    "PDUs": [],
    "VIMs": [
        {
            "avail_resources": null,
            "id": "minilab_vim",
            "location": "minilab",
            "max_resources": null,
            "name": "minilab_vim",
            "tenants": {},
            "type": "openstack"
        }
    ]
}

```
