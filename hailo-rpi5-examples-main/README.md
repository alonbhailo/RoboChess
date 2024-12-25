# Hailo Applications Infrastructure

This repository provides the core infrastructure and pipelines required to run Hailo applications. It includes three key application pipelines:
- **Object Detection**
- **Pose Estimation**
- **Instance Segmentation**

Requirements
------------

- hailo_platform==4.19.0
- Pyhailort

## Using the Repository as a Pip Package
-----------------------------
To install the package, ensure you are inside a virtual environment with Pyhailort installed. Then, run the following command:
```shell script
pip install git+https://github.com/giladnah/hailo-apps-infra.git
```
This will install the Hailo Applications Infrastructure package directly from the repository.

For reinstall the package please use:
```shell script
pip install --force-reinstall git+https://github.com/giladnah/hailo-apps-infra.git
```

## Working Locally
To make changes and work with the code locally:
```shell script
git clone https://github.com/giladnah/hailo-apps-infra.git
pip install --force-reinstall -v -e .
```

## Running the Pipelines
--------------------
[Running Hailo Pipelines](https://github.com/giladnah/hailo-rpi5-examples/blob/main/doc/basic-pipelines.md)

## Hailo Raspberry Pi Common Utilities
[Hailo Raspberry Pi Common Utilities](doc/development_guide.md)

License
----------
The infrastructure is released under the MIT license. Please see the [LICENSE](LICENSE) file for more information.


Disclaimer
----------
This code infrastructure is provided by Hailo solely on an “AS IS” basis and “with all faults”. No responsibility or liability is accepted or shall be imposed upon Hailo regarding the accuracy, merchantability, completeness or suitability of the code infrastructure. Hailo shall not have any liability or responsibility for errors or omissions in, or any business decisions made by you in reliance on this code infrastructure or any part of it. If an error occurs when running this infrastructure, please open a ticket in the "Issues" tab.

This infrastructure was tested on specific versions and we can only guarantee the expected results using the exact version mentioned above on the exact environment. The infrastructure might work for other versions, other environment or other HEF file, but there is no guarantee that it will.