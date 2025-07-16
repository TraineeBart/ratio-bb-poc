#!/bin/bash

ZIPNAME="ratio-bb-poc-review.zip"

# Verwijder oude zip als die bestaat
rm -f $ZIPNAME

# Voeg toe: src mappen en bestanden
zip -r $ZIPNAME src/batching src/core src/executor src/infra src/webhook_service src/Orchestration src/utils src/experimental src/backtester.py

# Voeg toe: docs mappen en bestanden
zip -r $ZIPNAME docs/architecture/datamodel-live-pipeline.md docs/architecture docs/dev/modules.md docs/project-taskboard.md docs/reviews docs/tests

# Voeg toe: tests mappen en bestanden
zip -r $ZIPNAME tests/integration tests/unit tests/live tests/data tests/helpers.py

# Voeg toe: configuratiebestanden
zip $ZIPNAME .env pytest.ini .github/workflows/ci.yml requirements.txt requirements-dev.txt

echo "Archief $ZIPNAME is klaar."
