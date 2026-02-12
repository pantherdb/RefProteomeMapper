# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RefProteomeMapper maps Reference Proteome (UniProt) IDs to PANTHER protein classification IDs. It provides two interfaces: a CLI Perl script (`map_panther.pl`) and a CGI web script (`genericMapping.cgi`).

PANTHER classification data must be downloaded separately from `ftp://ftp.pantherdb.org/generic_mapping/`.

## Setup

```bash
cpanm YAML::XS
cp config.example.yaml config.yaml
# Edit config.yaml to set panther_classification_directory
```

## Running

**CLI:**
```bash
perl map_panther.pl -i <panther_mapping_file> -g <gene_list_file> [-o <output_dir>]
```

**CGI:** Deploy `genericMapping.cgi` on a web server. Accepts `organism` and `fileContents` parameters via GET/POST.

## Architecture

Both scripts share the same core logic:
1. Read a PANTHER classification file into a hash keyed by UniProt ID
2. Iterate through a user-provided gene list (tab-delimited, UniProt ID in first column)
3. Output each gene with its PANTHER ID (or `NOHIT` if not found)
4. Report match/non-match statistics to STDERR (CLI only)

**`map_panther.pl`** — Standalone CLI. Reads files directly. No external config dependency.

**`genericMapping.cgi`** — CGI interface. Reads `config.yaml` (via YAML::XS) to locate the classification data directory. Constructs file path as `<panther_classification_directory>/panther_classification/<organism>`.

**`config.yaml`** — Not committed (in `.gitignore`). Copy from `config.example.yaml`. Single key: `panther_classification_directory`.

## Notes

- No build step, test suite, or linter configured
- Only Perl dependency: `YAML::XS` (used by CGI script only)
- `map_panther.pl` uses `/usr/local/bin/perl` shebang
- Current branch `dustine32-config-yaml` is refactoring hardcoded paths into `config.yaml`
