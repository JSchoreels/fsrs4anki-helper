# Packaging Data

`package.sh` creates `dist/fsrs4anki-helper.ankiaddon` by reading the add-on
source files from the repository root and writing a fresh package archive. If an
older archive exists at the target path, it is deleted before the new archive is
created.

After creating the archive, the script runs `scripts/validate_anki_addon.py`.
Validation reads the archive, checks that required runtime files and docs are
present, and rejects cache/build files that should not ship.

The generated archive is ignored by git because it is build output.
