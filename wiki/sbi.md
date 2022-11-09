# South Bound Interface

## South Bound Components

- **VIMs:** Register the VIMs in each location of the platform that will be used in each location for hosting network services as part of network slices
- **NFVOs:** Register the NFVOs in the platform that will be responsible for the management of the network services
- **WIM (Optional)**: Register the WIM in the platform that will be responsible for managing the Transport Network part of the Slice. If no WIM is added during a slice creation phase, the slice will still be created, but the Transport Network will not be configured
- **EMS (Optional)**: Register the EMSs that will be responsible for configuring the RAN functions that will be part of the Slice. If no EMS is added during a slice creation phase, the slice will still be created, but the RAN functions will not be configured
- **Policy Engines**: Register the Policy Engines/Systems that will interact with Katana

## Supported Components

Current version of the Slice Manager supports the following components:

| VIM | NFVO | WIM | EMS | Policy |
| ------ | ------ | ------ | ------ | ------ |
| OpenStack (Queens, Rocky & Stein)| OSM (5 - 9) | Athens Platform ODL WIM | Amarisoft EMS | NEAT |
| OpenNebula | | | | APEX |

> Katana Slice Manager communicates with these components via REST APIs or the Kafka message bus.

## Component Configuration Files

- [JSON Model](https://github.com/medianetlab/katana-slice_manager/tree/master/templates/components)
- [Examples](https://github.com/medianetlab/katana-slice_manager/tree/master/templates/example_config_files/SB_components)
