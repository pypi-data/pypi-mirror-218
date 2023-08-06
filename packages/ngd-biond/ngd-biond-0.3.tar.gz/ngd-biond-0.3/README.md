# Python client for NGD Backend 

A Python client package to operate with NGD-Backend

NGD Backend purpose is to manage and process Bar Code of Life information, applied to decision-making in conservation of biodiversity. 
It is a software system (a set of software components) developed as part of project "NEXTGENDEM" activities. 
BCS-Backend is the main component, an engine capable of managing bioinformatic information 
(import, export, visualization) and providing easy access to bioinformatic processes by filling parameters and submitting to available compute resources.

## Getting started

### Prerequisites

* Python >= 3.8
* An NGD backend instance has to be running and accessible. The URL of the API endpoint is the required parameter for the construction of the client. See the example in "Basic Usage" section below.
* An API Key to authenticate into the NGD Backend instance (go to the GUI of NGD and request and download an API Key file)

### Installing 
```bash
pip install ngd-biond
```

### Basic Usage

```python
from biond import Client

# Use "http://dev_balder_2_app_1/" as URL if from Jupyter Notebook at jupyter.nextgendem.eu
c = Client("http://localhost:5000/")  # Construct client
c.check_backend_available()
c.login(
    "api_key_file.txt")  # Login, using API Key in a file (direct API key not supported to avoid unintended upload of API keys)
c.logout()
```

## Package authors

* **Rafael Nebot Medina**. ITC-DCCT (Instituto Tecnológico de Canarias, SA - Departamento de Computación)
* **Daniel Reyes Parrilla**. ITC-DCCT

## Nextgendem Platform

* **Alejandro Curbelo Fontelos**. ITC-DCCT
* **Juli Caujapé Castells**. JBCVC-UACSIC (Jardín Botánico Canario "Viera y Clavijo", Unidad asociada CSIC)
* **Ruth Jaén Molina**. JBCVC-UACSIC
* **Antonio Díaz Pérez**. Gesplan (Gestión y Planeamiento del territorio, SA)
* **Isabel Saro Hernández**. JBCVC-UACSIC
* **Carlos Caraballo**. ITC-DCCT


## License

This project is licensed under the BSD-3 License - see the [LICENSE](LICENSE) file for details

## Acknowledgements

The development of this software was carried out under project NEXTGENDEM (https://www.nextgendem.eu), funded by the Interreg MAC 2014-2020 Cooperation Programme with project code "MAC2/4.6d/236". 
This work reflects the authors' view only; the funding agencies are not responsible for any use that may be made of the information it contains.
