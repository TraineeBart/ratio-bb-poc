

# Context & Achtergrond – Ratio Trades V3

In dit project ontwikkelen we een AI-gedreven tradingbot Proof of Concept (PoC) voor het handelen in crypto-paren (TFUEL-USDT en THETA-USDT) met de Ratio-Bollinger Band strategie. Belangrijke uitgangspunten:

- **Iteratief werken:** korte sprints van maximaal 2 uur, met dagelijkse rapportages per virtuele rol.
- **Virtuele rollen:** ProjectManagerGPT, ArchitectGPT, DeveloperGPT, Data-EngineerGPT en Quality-EngineerGPT werken gestructureerd samen.
- **Single source of truth:** alle documentatie en canvassen worden beheerd in de `docs/`-map in Git.
- **Testbare PoC:** beide flows (historische backtest en live trading) moeten volledig geautomatiseerd en getest zijn.
- **Limit-order focus:** we gebruiken uitsluitend limit-orders met batching op basis van orderboek-liquiditeit.
- **Golden files:** referentiebestanden voor expected output in `acceptance/`-map.

Zie voor detail:
- Rollen: `docs/roles_overview.md`
- Project specificatie: `docs/PROJECT_SPEC.md`
- Canvas overzicht: Open het Canvas Index