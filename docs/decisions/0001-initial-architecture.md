# ADR 0001 — Initial Architecture

**Status:** Accepted  
**Date:** 2026-10-07  
**Phase:** PHASE_0

## Context

VYRA GEOCORE must be rebuilt from zero as a recoverable, auditable geospatial-computing infrastructure. Previous attempts were lost due to ephemeral Colab sessions and lack of formal checkpoints.

## Decision

Adopt a strict layered architecture with:

- GitHub as logical source of truth
- Object storage for heavy artifacts
- Immutable checkpoints after every gate
- Dual identity (file SHA256 + semantic fingerprint)
- Explicit gate machine (`PASS` / `FAIL` / `BLOCKED` / `NOT_EXECUTED` / `WARNING`)
- Configuration externalised to versioned YAML
- Recovery script as a first-class citizen

## Consequences

- No heavy processing before foundation is committed and verified via clean clone.
- Training is gated behind seven preceding data gates.
- Legacy hashes are preserved only as references, never as automatic PASS criteria.
