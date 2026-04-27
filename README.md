# HEASARC MCP Server

An MCP (Model Context Protocol) server that connects Claude AI to NASA's HEASARC archive, enabling natural language search, download, and management of X-ray astronomy observations.

> Built as part of learning MCP development, with a focus on real scientific workflows.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![MCP](https://img.shields.io/badge/MCP-compatible-purple)
![License](https://img.shields.io/badge/license-MIT-green)
![Missions](https://img.shields.io/badge/missions-XMM%20%7C%20Chandra%20%7C%20NuSTAR%20%7C%20NICER-orange)

---

## What it does

Instead of navigating HEASARC's web interface or writing `astroquery` scripts manually, you can talk to Claude:

```
You:    "Search for XMM-Newton observations of Cas A longer than 50ks"
Claude: Found 4 observations:
        - 0110010101 | 98.3 ks
        - 0650450201 | 117.9 ks
        - 0650450301 | 115.3 ks
        - 0650450401 | 121.9 ks

You:    "Download the first two"
Claude: Downloading with wget (resume enabled)...
        ✓ 0110010101 complete
        ✓ 0650450201 complete

You:    "What NICER observations of Cas A did I have pending?"
Claude: From your notes: NICER observations from 2023 were marked as pending.
        Want me to search and download them now?
```

---

## Motivation

Downloading observations from HEASARC is one of the most time-consuming and error-prone steps in X-ray astronomy workflows. Between navigating the web interface, constructing `wget` commands, managing interrupted downloads, and keeping track of what's already local — it's a lot of "dead time" that has nothing to do with the actual science.

This project automates exactly that part, **without touching the analysis workflow**. XSPEC, SAS, HEASoft — all of that stays exactly as it is.

---

## Supported Missions

| Mission | HEASARC Table | Notes |
|---|---|---|
| XMM-Newton | `xmmmaster` | Full ODF structure |
| Chandra | `chanmaster` | evt2 + ancillary files |
| NuSTAR | `numaster` | FPMA/FPMB event files |
| NICER | `nicermastr` | Lightweight, many short obs |

---

## Architecture

```
You (any Linux machine)
        │
        ▼
  Python client          ← client.py
        │
   MCP protocol
        │
        ▼
   MCP server            ← server/main.py
        │
   ┌────┴────┐
   ▼         ▼
HEASARC   Local filesystem
SIMBAD    ~/astro_data/
```

---

## Available Tools

### Search & Discovery
| Tool | Description |
|---|---|
| `tool_resolve_object` | Resolve object name to RA/Dec via SIMBAD |
| `tool_search_observations` | Search HEASARC by object, mission, min exposure |

### Local Data Management *(coming soon)*
| Tool | Description |
|---|---|
| `tool_download_observations` | Download via wget with resume support |
| `tool_check_download_status` | Verify downloaded files |
| `tool_list_local_data` | Show what's already downloaded for an object |
| `tool_create_object_workspace` | Create standard folder structure |
| `tool_read_object_notes` | Read scientific notes for an object |
| `tool_update_object_notes` | Add entries to an object's notes |

---

## Installation

### Requirements

- Python 3.10+
- `wget` available in PATH
- `git`

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/heasarc-mcp-server
cd heasarc-mcp-server

# Create a virtual environment (keeps your astro environment clean)
python3 -m venv ~/.venv/mcp-env
source ~/.venv/mcp-env/bin/activate

pip install -r requirements.txt
```

---

## Usage

```bash
# Activate the environment
source ~/.venv/mcp-env/bin/activate
cd heasarc-mcp-server

# Resolve an object name to coordinates
python client.py resolve "Cas A"

# Search all missions
python client.py search "Cas A"

# Search a specific mission
python client.py search "Cas A" XMM

# Filter by minimum exposure (in ks)
python client.py search "Cas A" XMM 50

# Works with INTEGRAL/IBIS source names too
python client.py search "IGR J16320-4751" NICER 0
```

---

## Local Folder Structure

The server organizes data **by object**, which reflects how astronomers actually work:

```
~/astro_data/
├── Cas_A/
│   ├── obsid/
│   │   ├── XMM_0110010101/
│   │   ├── Chandra_21090/
│   │   └── NuSTAR_60001110002/
│   ├── scripts/
│   ├── plots/
│   └── notes.md          ← scientific diary, readable by Claude
│
├── IGR_J16320-4751/
│   ├── obsid/
│   │   └── NICER_8586011001/
│   ├── scripts/
│   ├── plots/
│   └── notes.md
```

---

## Project Structure

```
heasarc-mcp-server/
│
├── README.md
├── requirements.txt
│
├── server/
│   ├── main.py              ← MCP server entry point
│   │
│   ├── tools/
│   │   ├── search.py        ← astroquery-based search
│   │   ├── download.py      ← wget download manager (coming soon)
│   │   └── verify.py        ← checksum & integrity (coming soon)
│   │
│   └── utils/
│       ├── missions.py      ← per-mission configuration
│       ├── formatter.py     ← format tables for Claude
│       └── config.py        ← paths and settings
│
├── examples/
│   └── demo_cas_a.md        ← real session demo (coming soon)
│
└── tests/
    └── test_search.py
```

---

## Dependencies

- [astroquery](https://astroquery.readthedocs.io/) — HEASARC search via VO/TAP
- [mcp](https://github.com/anthropics/mcp) — Model Context Protocol SDK
- `wget` — robust download with resume support

---

## Roadmap

- [ x ] Object name resolution via SIMBAD
- [ x ] Multi-mission observation search
- [ x ] Exposure time filtering
- [ x ] NICER observation type and processing status
- [ ] `wget`-based download with resume
- [ ] Download verification (checksums)
- [ ] Local data management tools
- [ ] Scientific notes per object
- [ ] Demo with real session

---

## License

MIT

---

*Built while learning MCP development. Feedback welcome from the X-ray astronomy community!*

An MCP (Model Context Protocol) server that connects Claude AI to NASA's HEASARC archive, enabling natural language search, download, and management of X-ray astronomy observations.

> Built as part of learning MCP development, with a focus on real scientific workflows.
