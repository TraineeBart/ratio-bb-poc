


# 🗂️ Git Workflow – Ratio-BB-POC

## Branchstructuur

- **main**  
  - Bevat stabiele, release-waardige code.
  - Gebruik voor snapshots, demo’s en milestones.

- **develop**  
  - Actieve ontwikkelbranch voor nieuwe features.
  - Alles wordt hier eerst geïntegreerd voordat het naar `main` gaat.

## Werkwijze

1. **Start vanaf develop**

```bash
git checkout develop
```

2. **Maak een feature-branch**

```bash
git checkout -b feature/naam-van-feature
```

3. **Voer je werk uit en commit**

```bash
git add .
git commit -m "Feature: korte omschrijving"
```

4. **Push de feature-branch**

```bash
git push origin feature/naam-van-feature
```

5. **Open Pull Request naar develop**

- Doe code review en merge naar `develop`

6. **Regelmatig `develop` naar `main` mergen**

- Alleen na afronding van een stabiele fase of POC snapshot

## Naming Conventions

- `feature/xyz` – Voor nieuwe features of refactors
- `bugfix/xyz` – Voor het oplossen van bugs
- `hotfix/xyz` – Voor dringende fixes op `main`

## Releases

- Gebruik tags voor milestones:

```bash
git tag v0.4.0
git push origin v0.4.0
```

---

## Samenvatting

| Branch | Doel |
|---------|------|
| `main`  | Stabiel, release |
| `develop` | Actief ontwikkelwerk |
| `feature/*` | Afgebakende features of taken |
