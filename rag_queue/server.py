from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queus.worker import process_query

app = FastAPI()


@app.get("/")
def root():
    return {"status": "server is up and running"}


@app.post("/chat")
def chat(
    query: str = Query(
        ...,
        description="The chat query of user"
    )
):
    job = queue.enqueue(process_query, query)

    return {
        "status": "Queued",
        "job_id": job.id
    }
    
@app.get("/job-status")
def get_result(
    job_id:str= Query(...,description="job Id")
):
   job= queue.fetch_job(job_id=job_id)
   
   if job is None:
       return {"status": "Job not found", "result": None}
   
   if job.is_finished:
       return {"status": "finished", "result": job.return_value()}
   elif job.is_failed:
       return {"status": "failed", "error": job.exc_info}
   else:
       return {"status": job.get_status(), "result": None}


