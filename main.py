import srsly 
import frontmatter
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")
topics_path = Path.cwd() / 'data' / 'topics'

def load_topics():
    topic_files = [(a.stem,frontmatter.load(a)) for a in topics_path.iterdir()]
    topics = []
    for t in topic_files: 
        stem = t[0]
        md = t[1]
        md.stem = stem
        md.content = md.content.replace('\n','<br>')
        topics.append(md)
    return topics

@app.get("/")
def index(request:Request):
    context = {"request": request}
    context['topics'] = load_topics()

    return templates.TemplateResponse("index.html", context)

    

@app.get("/topic/{slug}")
def topics(request:Request, slug:str):
    context = {"request": request}
    try:
        topic_file = [a for a in topics_path.iterdir() if a.stem == slug][0]
        page = frontmatter.load(topic_file) 
        page.content = page.content.replace('\n','<br>')
        context['page'] = page
    except IndexError:
        raise HTTPException(status_code=404, detail="Topic not found")

    return templates.TemplateResponse("topic.html", context)

