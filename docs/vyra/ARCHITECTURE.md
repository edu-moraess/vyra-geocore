# ARCHITECTURE — VYRA (Fase 0)

## 1. Definição técnica
VYRA é um motor de percepção visual: recebe frames, produz detecções, associa-as no tempo (tracks),
mantém um estado estruturado da cena e emite eventos com evidências. Caso de uso inicial: tráfego.
Não é: um script YOLO com caixas; um sistema que entende intenções, prevê acidentes ou mede velocidade
física sem calibração validada. Nome ("Visual Intelligence and Perception Engine") provisório.

## 2. Camadas
```
Sensor → Ingestion → Perception → Geometry → Association → Tracking → Temporal → Scene State → Event Engine → Output
                                                                                         │
                                                                                         └──► HUD (somente consome Scene/Event/Metrics)
```
| Camada | Responsabilidade | Fase |
|---|---|---|
| domain | contratos imutáveis, geometria de imagem, serialização, checks | 0 |
| adapters | YOLO, OpenCV, trackers externos | 2–4 |
| Association | associação, ciclo de vida, `TrackState`; algoritmo trocável | 4 |
| Temporal | histórico, gaps, movimento em px/s | 6 |
| Scene State | `SceneSnapshot` por `Stamp` | 1 |
| Event Engine | regras verificáveis → `Event` | 6 |
| Output | memória, JSONL, métricas | 1 |
| HUD | apresentação; nunca recalcula nem controla o pipeline | 5 |

**Regras de dependência:** `domain` importa só a stdlib; camadas dependem apenas das anteriores e de
`domain`; bibliotecas pesadas (numpy, cv2, torch, ultralytics) só em `adapters`/ingestion de vídeo; o HUD
não é importado pelo núcleo. Impostas por `tests/unit/test_import_boundary.py`.

## 3. Estrutura (somente o que existe na Fase 0)
`src/vyra/domain/{checks,geometry,contracts,serialization}.py`, `src/vyra/env.py`, `tests/{contract,unit}`.
Diretórios das fases seguintes só serão criados quando houver código (sem módulos vazios).

## 4. Estratégia de testes
- **contract:** cada contrato com caso válido e casos inválidos por invariante; serialização determinística.
- **unit:** fronteiras de import (AST + subprocesso), diagnóstico de ambiente.
- **integration (Fase 1+):** pipeline sintético, sem baixar modelos; determinismo e ordem temporal.
- Nada de rede/GPU/pesos nos testes padrão; testes que exijam FFmpeg/OpenCV/YOLO serão marcados e pulados se ausentes.

## 5. Aceitação da Fase 0
1. `pip install -e ".[test]"` funciona em Python ≥ 3.11 sem dependências de runtime.
2. `pytest -q` verde. 3. `import vyra` e contratos não carregam numpy/cv2/torch/ultralytics.
4. `domain` só importa stdlib. 5. Cada contrato tem teste negativo. 6. JSONL determinístico, sem NaN.
7. `python -m vyra.env` roda sem extras. 8. `ruff check .` sem erros. 9. Docs coerentes com o código.

## 6. Riscos e decisões pendentes
- **Tracker:** implementação própria vs. ByteTrack de biblioteca; `model.track()` do Ultralytics acopla
  detector e tracker e fere a separação — decidir na Fase 4.
- **Tempo:** timestamps do OpenCV em vídeo de FPS variável podem ser imprecisos; `ClockDomain` registra a origem.
- **Licença:** Ultralytics é AGPL-3.0; manter como extra opcional e avaliar antes de distribuir.
- **Vocabulário:** classes COCO do YOLO ≠ classes desejadas; mapeamento explícito no adaptador.
- **Replay:** `from_dict` pendente; define compatibilidade real do schema.
- **HUD:** sobreposição OpenCV vs. interface web — decidir na Fase 5 conforme o ambiente.
- **Relação com o repositório MPE:** este pacote é independente; contratos de nome igual **não** foram importados.
