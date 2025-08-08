from fastapi import APIRouter,HTTPException
import subprocess
from app.utils import translate_cron, get_next_execution
from app.schemas import CronJobCreate
from datetime import datetime
from croniter import croniter
import os 

router = APIRouter()

@router.get("/cronjobs", summary="List of current cron jobs")
def list_cronjobs():
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT)
        lines = output.decode().splitlines()
        jobs = []

        for line in lines:
            if line.strip() == "" or line.startswith("#"):
                continue  # skip empty lines or comments

            parts = line.split(maxsplit=5)
            if len(parts) < 6:
                continue  # invalid line

            expression = " ".join(parts[:5])
            command = parts[5]
            description = translate_cron(expression)
            next_run = get_next_execution(expression)

            jobs.append({
                "raw": line,
                "expression": expression,
                "command": command,
                "description": description,
                "next_run": next_run
            })

        return {"cronjobs": jobs}
    except subprocess.CalledProcessError:
        return {"cronjobs": [], "message": "No cron jobs found or crontab is not configured."}


@router.post("/cronjobs", summary="Create a new cron job")
def create_cronjob(job: CronJobCreate):
    try:
        if not croniter.is_valid(job.expression):
            raise HTTPException(status_code=400, detail="Invalid cron expression.")

        line = f"{job.expression} {job.command}"

        with open("saved_cronjobs.txt", "a") as f:
            f.write(line + "\n")

        return {
            "message": "Cron job saved successfully.",
            "raw": line,
            "next_run": get_next_execution(job.expression),
            "description": translate_cron(job.expression)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/cronjobs/deploy", summary="Apply saved cron jobs to system")
def deploy_cronjobs():
    try:
        if not os.path.exists("saved_cronjobs.txt"):
            raise HTTPException(status_code=404, detail="No saved cron jobs found.")

        subprocess.run(["crontab", "saved_cronjobs.txt"], check=True)

        return {"message": "Cron jobs deployed successfully."}
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Failed to apply cron jobs.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))