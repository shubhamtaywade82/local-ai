# Local AI: Open WebUI + OpenUI + Ollama

Deterministic end-to-end setup integrating native host **Ollama**, containerized **Open WebUI**, and the **OpenUI Generative UI Tool** with an offline local asset server.

---

## 1. Architectural Model & Boundary Separation

```text
                     HOST MACHINE
                          │
            ┌─────────────┴─────────────┐
            │                           │
            ▼                           ▼
     Ollama (:11434)             Docker Compose
     Native + RTX 4060           │
            │                    ├── Open WebUI (:3002 -> :8080)
            │                    │     Chat / Tools / MCP / RAG
            │                    │
            │                    └── Nginx Asset Server (:8081)
            │                          Serves @openuidev/browser-bundle
            │
            └──────────────┐
                           │ (host.docker.internal)
                           ▼
                     Open WebUI
                           │
                           │ render_openui() tool call
                           ▼
                      OpenUI Lang
                           │
                           ▼
                    Browser Client
                           │
                           ├── Fetches bundle: http://localhost:8081
                           ▼
                    OpenUI Renderer
                           │
                           │ User interaction: sendPrompt()
                           ▼
                     Open WebUI
                           │
                           ▼
                         Ollama
```

### Core Architectural Rules

1. **Ollama is Native, Not Containerized:** This Compose setup contains no Ollama container or model storage volumes. Ollama lives on the host system (`~/.ollama/models/`), keeping GPU access direct and model storage isolated.
2. **Assets Served to Browser via `localhost:8081`:** While `openui-assets:80` is an internal Docker network DNS name, the browser client runs outside Docker on the host. Therefore, `cdn_base_url` must point to `http://localhost:8081`.
3. **No Direct Renderer-to-Ollama Connection:** The OpenUI component renderer inside the iframe never queries Ollama directly. UI events dispatch `sendPrompt()` back to Open WebUI, preserving the conversation history and multi-turn agentic loop.

---

## 2. Port Map

| Component | Host Port | Role | Endpoint Verification |
| :--- | :--- | :--- | :--- |
| **Ollama** | `11434` | Native Host LLM Engine | `http://localhost:11434/api/tags` |
| **Open WebUI** | `3002` | Main Chat & Tool Orchestration | `http://localhost:3002/health` |
| **OpenUI Assets** | `8081` | Self-Hosted OpenUI Runtime | `http://localhost:8081/dist/openui-bundle.min.js` |

*Note: Port 3002 is assigned because ports 3000 and 3001 are occupied on this host machine.*

---

## 3. Directory Layout

```text
/home/nemesis/projects/local-ai/ (symlinked at ~/local-ai/openwebui-openui)
├── .env                           # Local runtime environment (ports, secrets)
├── .env.example                   # Template environment configuration
├── .gitignore                     # Ignores .env, logs, and volume backups
├── docker-compose.yml             # Orchestration for Open WebUI and Nginx assets
├── README.md                      # Architecture guide & verification workflow
├── openui-assets/                 # Self-hosted OpenUI bundle (@openuidev/browser-bundle)
│   ├── nginx.conf                 # Dual-stack server configuration with CORS headers
│   └── dist/
│       ├── openui-bundle.min.js   # OpenUI React bundle & renderer (3.6 MB)
│       └── openui-styles.css      # Component stylesheet (317 KB)
└── scripts/
    ├── fetch-openui-bundle.sh     # Automates npm pack & version-pinned extraction
    └── backup-volumes.sh          # Volume snapshot backup script
```

---

## 4. Operational Guide

### Start Services

```bash
docker compose up -d
docker compose ps
```

### Install the OpenUI Tool in Open WebUI

1. Navigate to [http://localhost:3002](http://localhost:3002) (first created user becomes Admin).
2. Go to **Workspace** $\rightarrow$ **Tools** (or **Admin Panel** $\rightarrow$ **Tools**).
3. Click **+** (Add New Tool).
4. Fetch the official tool implementation:
   ```bash
   curl -s https://raw.githubusercontent.com/thesysdev/openwebui-plugin/main/tool.py
   ```
5. Paste the Python code into the editor and click **Save**.
6. Click the gear/settings icon (**Valves**) for the OpenUI tool.
7. Set `cdn_base_url` to:
   ```text
   http://localhost:8081
   ```
8. Save the valve setting.

---

## 5. Verification Prompts

Open a new chat at [http://localhost:3002](http://localhost:3002), select a tool-calling model, and toggle on **OpenUI - Generative UI**:

- **Table:**
  > *"Create a comparison table of Ruby, TypeScript, Python, and Go showing typing, backend ecosystems, and concurrency models."*
- **Chart:**
  > *"Create a bar chart comparing performance benchmarks: Ruby 80, TypeScript 95, Python 90, Go 115, Rust 130."*
- **Interactive Form:**
  > *"Create an interactive contact form with Name, Email, and Message with a submit button."*

---

## 6. Utilities

- **Refresh / Re-pin Bundle Version:**
  ```bash
  OPENUI_BROWSER_BUNDLE_VERSION=0.1.4 ./scripts/fetch-openui-bundle.sh
  docker compose restart openui-assets
  ```
- **Backup Persistent Volumes:**
  ```bash
  ./scripts/backup-volumes.sh local-ai_open-webui-data
  ```
