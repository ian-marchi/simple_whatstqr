# whatstqr

Gere QR Codes de WhatsApp com uma linha de Python.

`whatstqr` é uma biblioteca Python pequena e direta para criar QR Codes em PNG que abrem uma conversa no WhatsApp, com ou sem mensagem pré-preenchida.

## Por que usar?

- API simples: uma função para gerar o QR Code
- Funciona localmente: salva o PNG direto na sua máquina
- Pronto para WhatsApp: monta links `wa.me` corretamente
- Boas configurações padrão: adiciona `55` em números brasileiros sem DDI
- Saída flexível: você escolhe pasta e nome do arquivo

## Instalação

### Instalação local para desenvolvimento

Na raiz do projeto:

```bash
pip install -e .
```

Se você usa um executável específico do Python, faça a instalação com o mesmo interpretador que vai executar o seu script:

```powershell
& C:\caminho\para\python.exe -m pip install -e .
```

Isso é importante no Windows quando existem várias instalações do Python na mesma máquina.

## Início rápido

```python
from whatstqr import create_whatsapp_qr

qr_path = create_whatsapp_qr(
    phone_number="(11) 99999-9999",
    contact_name="Joao Silva",
    include_message=True,
    message_text="Ola! Vim pelo QR Code.",
)

print(qr_path)
```

Exemplo de saída:

```text
C:\sua-pasta\joao_silva_5511999999999.png
```

## Exemplos de uso

### Criar um QR Code sem mensagem

```python
from whatstqr import create_whatsapp_qr

create_whatsapp_qr(
    phone_number="(11) 98888-7777",
    contact_name="Maria",
)
```

Esse exemplo gera um QR Code que abre apenas a conversa no WhatsApp.

### Criar um QR Code com mensagem pré-preenchida

```python
from whatstqr import create_whatsapp_qr

create_whatsapp_qr(
    phone_number="(11) 98888-7777",
    contact_name="Maria",
    include_message=True,
    message_text="Oi Maria, tudo bem?",
)
```

Esse exemplo gera um QR Code que abre a conversa com a mensagem já preenchida.

### Salvar o arquivo em outra pasta

```python
from whatstqr import create_whatsapp_qr

create_whatsapp_qr(
    phone_number="(11) 98888-7777",
    contact_name="Maria",
    output_dir="output",
)
```

### Usar um nome de arquivo personalizado

```python
from whatstqr import create_whatsapp_qr

create_whatsapp_qr(
    phone_number="(11) 98888-7777",
    contact_name="Maria",
    file_name="qr_maria_final",
)
```

A biblioteca salvará o arquivo como `qr_maria_final.png`.

## API

```python
create_whatsapp_qr(
    phone_number: str,
    contact_name: str,
    include_message: bool = False,
    message_text: str | None = None,
    output_dir: str | Path = ".",
    file_name: str | None = None,
) -> Path
```

### Parâmetros

- `phone_number`: número de WhatsApp usado no QR Code
- `contact_name`: nome do contato usado para montar o nome do arquivo
- `include_message`: se `True`, adiciona uma mensagem pré-preenchida ao link do WhatsApp
- `message_text`: conteúdo da mensagem usado quando `include_message=True`
- `output_dir`: pasta onde o PNG será salvo
- `file_name`: nome personalizado para o arquivo gerado

### Retorno

- Retorna um `Path` apontando para o arquivo PNG gerado

## Comportamento do número

A biblioteca normaliza o número antes de gerar a URL:

- Remove espaços, `+`, parênteses e hífens
- Se o número tiver 10 ou 11 dígitos, assume Brasil e adiciona `55`
- Se o número já vier com DDI, preserva o valor informado
- Rejeita números inválidos ou curtos demais

## Comportamento do nome do arquivo

Por padrão, o nome do arquivo é montado assim:

```text
{nome_sanitizado}_{numero_normalizado}.png
```

Exemplo:

```text
joao_silva_5511999999999.png
```

Caracteres inválidos são sanitizados automaticamente para manter o nome do arquivo seguro no Windows.

## Rodando os testes

Na raiz do projeto:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Estrutura do projeto

```text
simple_whatstqr/
├── src/
│   └── whatstqr/
│       ├── __init__.py
│       └── core.py
├── tests/
├── LICENSE
├── pyproject.toml
└── README.md
```

## Antes de publicar no GitHub

Antes de publicar este repositório, vale fazer estes ajustes:

1. Trocar as URLs de exemplo em `pyproject.toml` pelas URLs reais do seu GitHub
2. Atualizar a linha de copyright no `LICENSE`, se quiser
3. Criar o repositório no GitHub e subir o projeto

## Licença

MIT
