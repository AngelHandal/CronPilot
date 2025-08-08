from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.routes import router
from app.utils import translate_cron, get_next_execution
from croniter import croniter
import subprocess, os


app = FastAPI(title="CronPilot")

# Static & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# JSON API routes
app.include_router(router)


@app.get("/", summary="UI: Cron job dashboard")
def show_dashboard(request: Request):
    from subprocess import check_output, CalledProcessError

    status = request.query_params.get("status")
    message, alert_class = None, "info"
    if status == "created":
        message, alert_class = "Cron job saved. Click Deploy to apply it to the system.", "primary"
    elif status == "deployed":
        message, alert_class = "Cron jobs deployed successfully.", "success"
    elif status == "no_saved":
        message, alert_class = "No saved cron jobs found to deploy.", "warning"
    elif status == "invalid":
        message, alert_class = "Invalid cron expression.", "danger"
    elif status == "fail":
        message, alert_class = "Operation failed.", "danger"

    jobs = []
    try:
        output = check_output(["crontab", "-l"])
        lines = output.decode().splitlines()
        for line in lines:
            if line.strip() == "" or line.startswith("#"):
                continue
            parts = line.split(maxsplit=5)
            if len(parts) < 6:
                continue
            expr = " ".join(parts[:5])
            cmd = parts[5]
            jobs.append({
                "expression": expr,
                "command": cmd,
                "description": translate_cron(expr),
                "next_run": get_next_execution(expr),
            })
    except CalledProcessError:
        pass

    return templates.TemplateResponse(
        "cronjobs.html",
        {
            "request": request,
            "jobs": jobs,
            "message": message,
            "alert_class": alert_class,
        },
    )


@app.post("/create-cron")
def create_cron(expression: str = Form(...), command: str = Form(...)):
    if not croniter.is_valid(expression):
        return RedirectResponse(url="/?status=invalid", status_code=303)

    line = f"{expression} {command}"
    with open("saved_cronjobs.txt", "a") as f:
        f.write(line + "\n")

    return RedirectResponse(url="/?status=created", status_code=303)


# UI: Deploy button
@app.post("/deploy-cron")
def deploy_cron():
    if not os.path.exists("saved_cronjobs.txt"):
        return RedirectResponse(url="/?status=no_saved", status_code=303)
    try:
        subprocess.run(["crontab", "saved_cronjobs.txt"], check=True)
        return RedirectResponse(url="/?status=deployed", status_code=303)
    except Exception:
        return RedirectResponse(url="/?status=fail", status_code=303)
