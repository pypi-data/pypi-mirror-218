# Lesaviezvous

Un package Python pour obtenir des informations intéressantes à partir de l'API Lesaviezvous.

## Installation

Installez le package à l'aide de `pip` :

```bash
pip install lesaviezvous
```

## Utilisation
Importez le package dans votre script Python et appelez la fonction get_info() pour obtenir des informations intéressantes :
```bash
from lesaviezvous.api import get_info

info = get_info()
if info:
    print(info)
else:
    print("Impossible de récupérer les informations.")
```

## Exigences
- Python3
- Request

