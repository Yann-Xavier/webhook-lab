# Webhook Lab

Laboratório local de idempotência para webhooks. O efeito demonstrado é
a gravação de um evento em SQLite. A chave primária impede duas gravações
com o mesmo identificador, inclusive entre conexões distintas.

## Executar

```sh
python -m pip install -r requirements.txt
python -m uvicorn app:app
```

Em outro terminal, execute duas vezes:

```sh
curl -s http://127.0.0.1:8000/events -H "Content-Type: application/json" -d '{"id":"demo-1","message":"Pedido recebido"}'
```

Com um banco vazio, a primeira entrega retorna `{"accepted":true}`.
O reenvio retorna `{"accepted":false}`. Para usar outro banco, defina
a variável de ambiente `WEBHOOK_DB`.

## Teste

```sh
python -m pytest -q
```

O teste simula a perda da resposta descartando a primeira resposta HTTP
e verifica o efeito diretamente no banco. O laboratório usa dados
sintéticos e foi projetado para execução local.
