# Contributing

## Adding an example

1. Create a folder `examples/<language>/<short-name>/`.
2. Make it self-contained: `README.md`, dependency file (`requirements.txt`, `package.json`, ...) and `.env.example`.
3. Never include real keys, tokens or hostnames. Use placeholders.
4. Link it from the root [README](README.md) and from the relevant doc page.
5. Code, comments and example READMEs are written in English only.

## Documentation and translations

- `docs/en/` is the source of truth. Write and change docs there first.
- `docs/pt-br/` and `docs/es/` mirror it with **identical file names**.
- When you change an English page, update the translations in the same pull request, or open an issue listing the pages that are out of date.
- Keep code blocks, endpoint paths, field names and `error_code` values untranslated.
- To add a language, copy `docs/en/` to `docs/<code>/`, translate it and add the language to the language line in every `index.md` and in the root README.
