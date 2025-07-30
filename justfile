set windows-shell := ["nu.exe", "-c"]
set shell := ["nu", "-c"]

root := absolute_path('')

default:
    @just --choose

format:
    cd '{{ root }}'; just --unstable --fmt
    nixpkgs-fmt '{{ root }}'
    prettier --write '{{ root }}'
    ruff check --fix '{{ root }}'
    ruff format '{{ root }}'

schema:
    truffle-cli --schema | save -f '{{ root }}/docs/src/schema.json'

lint:
    cd '{{ root }}'; just --unstable --fmt --check
    nixpkgs-fmt '{{ root }}' --check
    prettier --check '{{ root }}'
    cspell lint '{{ root }}' --no-progress
    markdownlint --ignore-path .gitignore '{{ root }}'
    if (markdown-link-check \
      --config '{{ root }}/.markdown-link-check.json' \
      ...(fd '^.*.md$' '{{ root }}' | lines) \
      | rg -q error \
      | complete \
      | get exit_code) == 0 { exit 1 }
    ruff check '{{ root }}'
    pyright '{{ root }}'

test *args:
    pytest '{{ root }}' {{ args }}

docs:
    rm -rf '{{ root }}/artifacts'
    cd '{{ root }}/docs'; mdbook build
    mv '{{ root }}/docs/book' '{{ root }}/artifacts'

build-cli:
    rm -rf '{{ root }}/artifacts'
    nuitka \
      --company-name='haras-unicorn' \
      --product-name='Truffle CLI' \
      --product-version='0.1.0' \
      $"--file-description=(open '{{ root }}/README.md' \
        | lines \
        | skip 2 \
        | take 2 \
        | str join ' ')" \
      --copyright='haras-unicorn' \
      --macos-create-app-bundle \
      --macos-app-name='Truffle CLI' \
      --macos-app-version='0.1.0' \
      --macos-app-mode='background' \
      --windows-console-mode='force' \
      --output-dir='{{ root }}/artifacts' \
      --output-filename='truffle-cli' \
      --standalone \
      --onefile \
      '{{ root }}/src/cli/src/truffle_cli/__init__.py'
