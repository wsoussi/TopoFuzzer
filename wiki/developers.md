# For Developers and Technology Providers

## South Bound Interface and Plugins

Katana Slice Manager is based on a highly modular architecture, built as a group of microservices, each running in a docker container. The southbound components which interact with the Slice Manager are: Virtual Infrastructure Managers (VIMs), Network Function Virtualization Orchestrators (NFVOs) and Network Management Systems (NMS), which include the WAN Infrastructure Manager (WIM), the Element Management System (EMS) and Monitoring Framework. The Adaptation Layer module provides a level of abstraction regarding the lower layer technology, making it feasible for the Slice Manager to operate over any MANO layer component without any modifications to its core functionality, as long as the proper plugin is loaded. The plugins translate the Slice Manager messages and actions that must be performed to type-specific messages and API calls for the south bound components.

| Component | Operation | Phase |
| --- | --- | --- |
| VIM | Create a new Tenant | Slice Creation – Resource Provisioning |
| VIM | Get information about VIM available resources | Slice Creation – Placement |
| VIM | Delete a Tenant | Slice Termination |
| NFVO | Read Network Service Descriptors (NSDs) and Virtual Functions Descriptors (VNFDs) | Slice Creation – Placement |
| NFVO | Add a new VIM account (VIM Tenant) | Slice Creation – Resource Provisioning |
| NFVO | Instantiate a new NS | Slice Creation – Activation |
| NFVO | Read NS Records (NSRs) and VNF Records (VNFRs) | Slice Creation – Activation |
| NFVO | Delete an instantiated NS | Slice Termination |
| NFVO | Delete a VIM account (VIM Tenant) | Slice Termination |
| WIM | Create the transport network graph | Slice Creation – Resource Provisioning |
| WIM | Activate the network traffic steering for a network slice | Slice Creation – Activation |
| WIM | Delete the transport network graph | Slice Termination |
| EMS | Reserve RAN components |Slice Creation – Resource Provisioning |
| EMS | Configure and start RAN services | Slice Creation – Activation |
| EMS | Terminate RAN services | Slice Termination |
| EMS | Release RAN components | Slice Termination |

Most of these actions can be performed with simple API calls to the endpoints that are available by the southbound components. During the slice creation phase, the Slice Manager generates data that will be consumed by the EMS and the WIM in order to instantiate and configure the parts of the slice for which they are responsible. This data is in the form of JSON files, which are defined with the use of [JSON Schemas](https://github.com/medianetlab/katana-slice_manager/tree/master/katana-schemas/sbi-messages). The JSON Schema is a vocabulary that allows to annotate and validate JSON documents. Each plugin must be able to read and translate the data to component-specific messages.

Finally, the plugins must be able to handle the registration of a new southbound component to the Slice Manager. The registration of new components is realized with the use of JSON configuration files, also described with [JSON Schemas](https://github.com/medianetlab/katana-slice_manager/tree/master/katana-schemas/components). The plugin must be able to create a new component object based on these files and store it in the Infrastructure repository.

### Python Plugins

Python modules can be integrated directly within the Slice Manager service stack in order to act as wrapper plugins for any underlying components, in order for them to communicate with the Slice Manager SBI. These modules must introduce methods and functions that will enable the Slice Manager to support the following features:
• Communicate with the underlying component through any available APIs (e.g. REST, ssh, message bus, etc.) and perform the actions that are part of the slice management procedures.
• Receive the messages that the Slice Manager produces for the underlying components and translate them to component-specific messages.
• Create objects for every new component based on the configuration files.

There are two available options for the communication between the python plugins and the slice lifecycle manager: (i) Use direct calls to functions and methods defined and imported by the plugin modules and (ii) create producers and consumer objects that will use the Kafka message bus which is part of the Slice Manager software stack. In both cases, the python module must be saved in the directory “katana-slice_manager/shared_utils/” with a descriptive name following the “<component>Utils.py” format, for example openstackUtils.py.

The plugins define python classes with methods and functions that implement the enlisted features. These classes are imported in the NBI module, as presented below.

```python
from katana.shared_utils.osmUtils import osmUtils
from katana.shared_utils.tango5gUtils import tango5gUtils
from katana.shared_utils.mongoUtils import mongoUtils
```

The NBI module creates a new python object from the imported class for every new southbound component that is registered to the Slice Manager and stores it in the Infrastructure repository. Any time that the plugin must be used for the slice management procedures, the object will be restored from the repository and used by Slicing Lifecycle Manager (SLM) which calls its methods in order to perform the necessary actions.
