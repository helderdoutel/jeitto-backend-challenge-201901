# Desafio Backend do Jeitto


## Pré-requisistos

MongoDB na porta 27017  
Python3

## MongoDB

MongoDB foi escolhido pela facilidade de implementação e escalabilidade.

## Como rodar
Com todos pré-requisitos satisfeitos:

> pip install -r requirements.txt

Com o MongoDB rodando, execute o script principal
> py main.py

## Requests com postman
Utilizei o Postman para simular as requisições da API conforme arquivo "jeitto.postman_collection.json"

#### Consultando URLs via Postman
> POST localhost:50/CompanyProducts

Response
```json
[
    {
        "company_id": "claro_11",
        "products": [
            {
                "id": "claro_10",
                "value": 10.0
            },
            {
                "id": "claro_20",
                "value": 20.0
            }
        ]
    },
    {
        "company_id": "tim_11",
        "products": [
            {
                "id": "tim_10",
                "value": 10.0
            },
            {
                "id": "tim_20",
                "value": 20.0
            }
        ]
    }
]
```

> POST localhost:5000/CompanyProducts?company_id=tim_11

Response
```json
[
    {
        "company_id": "tim_11",
        "products": [
            {
                "id": "tim_10",
                "value": 10.0
            },
            {
                "id": "tim_20",
                "value": 20.0
            }
        ]
    }
]
```

> POST localhost:5000/PhoneRecharges

REQUEST
```json
{
   "company_id": "claro_11",
   "product_id": "claro_10",
   "phone_number": "5511999999999",
   "value": 10.00
}
```

Response
```json
{
    "id": "5edee9d7396f77cdb072f843"
}
```

> GET localhost:5000/PhoneRecharges?phone_number=5511999999999
> GET localhost:5000/PhoneRecharges?id=5edee9d7396f77cdb072f843

Response
```json
[
    {
        "company_id": "claro_11",
        "product_id": "claro_10",
        "phone_number": "5511999999999",
        "value": 10.0,
        "created_at": "09/06/2020, 01:45:59",
        "id": "5edee9d7396f77cdb072f843"
    }
]
```

Perguntas que devem ser respondidas
#### Quais foram os principais desafios durante o desenvolvimento?
Por não ter familiaridade com banco não relacional, tive que estudar como aplicar a solução. Isso tomou boa parte do tempo de desenvolvimento.
#### O que você escolheu como arquitetura/framework/banco e por que?
Utilizei flask por ser intuitivo e fácil de implementar, além de ser voltado para API e como banco escolhi o MongoDB por ser rápido e intuitivo. 
#### O que falta desenvolver / como poderiamos melhorar o que você entregou?
Falta desenvolver os testes unitário e talvez aplicar uma arquitetura mais organizada. Escolhi manter um código mais simples por falta de tempo.
#### Python é a melhor escolha para esta atividade? Por que?
Sim, é muito fácil de subir uma aplicação e conectar com um banco, além da facilidade para tratar os dados e fazer verificações mais complexas nos dados.