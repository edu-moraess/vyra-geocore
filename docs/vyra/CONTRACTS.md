# CONTRACTS — schema 0.1.0

Fonte de verdade: `src/vyra/domain/contracts.py`. Imutáveis (`frozen`, `slots`); validam na construção
e lançam `ContractError`. Coleções são `tuple`. Pixels nunca entram no domínio.

## Tipos de valor (`ValueKind`)
`MEASURED` (sensor/modelo) · `EXTERNAL` (fornecido de fora) · `INFERRED` (modelo/regra sobre dados)
· `DERIVED` (cálculo determinístico) · `PREDICTED` (extrapolação) · `HYPOTHETICAL` (suposição).

## Contratos e invariantes
| Contrato | Papel | Invariantes principais |
|---|---|---|
| `Quantity` | valor com unidade, ou indisponível | exatamente um entre `value` e `unavailable_reason`; valor finito exige `kind` |
| `Provenance` | componente, versão, configuração | digest SHA-256 determinístico, independente da ordem dos parâmetros |
| `Stamp` | fonte + frame + tempo + relógio | `frame_index >= 0`, tempo finito `>= 0`, domínio de relógio explícito |
| `Origin` | descrição da fonte | `width/height >= 1`; `nominal_fps` é `None` (desconhecido) ou `> 0` |
| `FrameRecord` | metadados do frame | `INVALID` exige `note`; frames inválidos não são descartados em silêncio |
| `Detection` | observação instantânea | `score` em [0,1] (confiança bruta, **não calibrada**); `index` único no frame |
| `Track` | identidade temporal | ID do tracker; **não** é identidade física permanente |
| `TrackState` | estado do track num instante | observado ⇒ `bbox` MEASURED + `detection_index`, 0 misses, não LOST/TERMINATED; bbox sem detecção ⇒ PREDICTED; TERMINATED sem posição |
| `SceneSnapshot` | estado da cena num `Stamp` | todos os itens com o mesmo `Stamp`; sem `index`/`track_id` duplicados; referências existentes; 1 detecção sustenta no máximo 1 track; contagens **derivadas** das detecções do frame |
| `EvidenceRef` | ponteiro de evidência | `track_id` e/ou `detection_index` |
| `Event` | evento temporal | mesma fonte e relógio; intervalo não invertido; `DETECTED`/`HYPOTHESIS` exigem evidências dentro do intervalo; `INDETERMINATE` exige `limitations` |
| `PipelineMetrics` | métricas de execução | `ok + invalid == total`; unidades fixas; só `MEASURED`/`DERIVED`; indisponível é explícito |

## Serialização
`vyra.domain.serialization.to_json_line(obj)` → JSONL determinístico (`sort_keys`, compacto,
`allow_nan=False`) com envelope `{schema_version, type, data}`. Enums viram seu valor; tuplas viram listas.
**Pendente:** `from_dict` (replay) — Fase 1.

## Compatibilidade
SemVer do schema: campo novo opcional = minor; remoção/renomeação/mudança de invariante = major.
