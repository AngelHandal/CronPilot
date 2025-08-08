# CronPilot 🛠️

A lightweight DevOps tool to **view, create, and deploy cron jobs** on a Unix-like system.  
Built with **FastAPI** + **Jinja2 (Bootstrap)**. It provides:

- A clean dashboard to list current cron jobs
- Human-readable descriptions of cron expressions
- Next run preview (using `croniter`)
- Create jobs via form (UI) or JSON (API)
- One-click **Deploy** to apply jobs to the system `crontab`

> ⚠️ Requires macOS/Linux (or WSL). Windows `crontab` is not available natively.

---

## Features

- **UI Dashboard** (Jinja2 + Bootstrap)
- **API Endpoints** (FastAPI)
- **Translate cron** expressions (cron-descriptor)
- **Next execution** calculation (croniter)
- **Deploy** saved jobs to system `crontab`
- Minimal dependencies & easy setup

---

## Tech Stack

- Backend: FastAPI
- Templating: Jinja2 (Bootstrap 5)
- Scheduling helpers: cron-descriptor, croniter
- Runtime: Uvicorn

---

## Getting Started

### 1) Clone & install

```bash
git clone https://github.com/<your-user>/CronPilot.git
cd CronPilot
python -m venv env
source env/bin/activate        # on Windows: .\env\Scripts\activate
pip install -r requirements.txt
