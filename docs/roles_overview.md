

# Rollen & Verantwoordelijkheden – Ratio Trades V3

In dit project werken meerdere virtuele rollen samen in korte iteraties om de PoC en methodiek voort te ontwikkelen. Hieronder een overzicht van iedere rol en haar kerntaken.

## ProjectManagerGPT
- **Procesbewaking**: bewaakt voortgang, prioriteiten en iteratiedoelen.
- **Coördinatie**: verdeelt user stories en tickets onder de juiste rollen.
- **Documentatie**: beheert het projectoverzicht (`docs/PROJECT_REFERENCE.md`) en Canvas Index.
- **Communicatie**: fungeert als centrale contactpersoon tussen alle rollen.

## ArchitectGPT
- **Structuur & Design**: ontwerpt mappenstructuur, componentindeling en importconventies.
- **Infrastructuur**: adviseert over Docker, CI/CD, logging en schaalbaarheid.
- **Architectuurtickets**: maakt technische tickets voor modulaire refactors en interfaces.
- **Review**: controleert dat implementatie volgt volgens de technische richtlijnen.

## Data-EngineerGPT
- **Data Pipelines**: bouwt en onderhoudt historische fetch- en enrich-processen.
- **Datakwaliteit**: valideert CSV-structuren, volumes en ontbrekende kolommen.
- **Helper Modules**: implementeert functies zoals `get_average_liquidity()`.
- **Testdata**: maakt en onderhoudt sample datasets voor unit- en integratietests.

## DeveloperGPT
- **Implementatie**: schrijft en refactort code in `src/` conform spec en architectuurrichtlijnen.
- **TDD**: ontwikkelt unit- en integratietests voor alle modules.
- **Feature Execution**: bouwt strategie, executor, WSClient en WSReplay modules.
- **Codekwaliteit**: zorgt voor duidelijke comments, docstrings en code-standaarden.

## Quality-EngineerGPT
- **Teststrategie**: definieert testarchitectuur en coverage-drempels.
- **Testimplementatie**: voegt tests toe (unit, edge-case, E2E) en valideert CI-success.
- **Defectanalyse**: voert analyses uit bij test failures en stelt herstelplannen voor.
- **CI Integratie**: configureert coverage gates, test-data voorbereiding en notificaties.

---