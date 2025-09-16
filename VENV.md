Instruções para o ambiente virtual (.venv)

PowerShell (Windows):

1. Criar o venv (se ainda não existir):

   python -m venv .venv

2. Ativar o venv:

   .\.venv\Scripts\Activate.ps1

3. Instalar dependências a partir do requirements:

   pip install -r requirements.txt

4. Para gerar/atualizar o requirements a partir dos pacotes instalados:

   pip freeze > requirements.txt

Observações:
- O projeto já contém um arquivo `requirements.txt` gerado automaticamente.
- O diretório `.venv/` está no `.gitignore`.

Troubleshooting (Windows / PowerShell):

- Se ao rodar `pip` você receber erro do tipo "Fatal error in launcher: Unable to create process...": use o Python do venv para chamar o pip diretamente:

   python -m pip install -r ..\requirements.txt

   ou, para congelar as dependências:

   python -m pip freeze > ..\requirements.txt

- Se o `pip` do sistema estiver conflitando, recrie o venv na pasta do projeto (`EstoqueCdg`) e ative novamente:

   # remover venv antigo (apenas se tiver certeza)
   Remove-Item -Recurse -Force .\.venv

   # criar novamente
   python -m venv .venv

   # ativar
   .\.venv\Scripts\Activate.ps1

