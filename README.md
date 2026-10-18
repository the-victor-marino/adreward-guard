# 🚧 WIP — WORK IN PROGRESS 🚧

> [!WARNING]
> **UNDER DEVELOPMENT — NOT PRODUCTION READY.**
> These projects are still being developed and have **not yet been fully reviewed or understood by their author**. Code, documentation, and test coverage remain subject to review. Passing automated checks do not establish production readiness.
>
> **EM DESENVOLVIMENTO:** o autor ainda não revisou nem compreendeu completamente este projeto. Este aviso deve permanecer até que essa revisão e compreensão estejam concluídas.

---

# AdReward Guard

**Mobile game rewarded-ad transaction integrity testing.**

## Why it matters

Rewarded ads must grant the correct reward exactly once—even when callbacks are duplicated, messages arrive late, or connectivity fails.

## MVP scope

An offline, deterministic simulated ad-provider callback workflow and a minimal reward ledger. No live ads or real financial transactions are required.

## Test strategy

This project documents assumptions, positive and negative scenarios, reproducible evidence, and explicit release criteria. The first implementation will be developed on a feature branch and reviewed before merging.

## Status

**In development — initial scaffold.** No passing-test or real-device claims until verified.

## Roadmap

1. Minimal working implementation
2. Automated positive, boundary, and adversarial tests
3. CI reports and reproducible failures
4. Portfolio-quality documentation and demos

## License

License to be chosen before distribution.
