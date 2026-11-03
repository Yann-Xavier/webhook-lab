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

## Escopo e critérios de aceite

Este laboratório ajuda desenvolvedores a reproduzir entregas duplicadas
com dados sintéticos. Uma entrega nova deve ser aceita. Reenvios, inclusive
concorrentes, devem produzir uma única gravação. O identificador é global
ao banco e a primeira mensagem gravada prevalece.

O escopo é local. Autenticação, fila e política de retries do emissor
ficam fora desta versão. O teste de resposta perdida simula a perspectiva
do emissor descartando a resposta, sem interromper a conexão de rede.

Para repetir a demonstração do zero, aponte `WEBHOOK_DB` para um novo
arquivo. Reverter o código no Git não reverte registros no SQLite.
