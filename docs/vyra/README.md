# VYRA — Visual Intelligence and Perception Engine (nome provisório)

Motor modular de percepção visual. **Estado: Fase 0** (fundação: contratos, testes, fronteiras).
Ainda não há leitura de vídeo, YOLO, tracking nem HUD. Ver `ARCHITECTURE.md` e `CONTRACTS.md`.

## Local
```bash
python -m venv .venv && source .venv/bin/activate   # Python >= 3.11
pip install -e ".[test,lint]"
pytest -q
ruff check .
python -m vyra.env          # diagnóstico do ambiente (use --gpu para sondar CUDA)
```

## Google Colab
```python
from google.colab import files
files.upload()                      # envie vyra.zip
!unzip -q -o vyra.zip
%cd vyra
!pip install -q -e ".[test]"
!pytest -q
!python -m vyra.env --gpu
```

O núcleo não tem dependências de runtime. Extras opcionais: `numeric`, `video`, `yolo`.
