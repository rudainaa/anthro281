import srsly 
import frontmatter
import markdown
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")
topics_path = Path.cwd() / 'data' / 'topics'

def load_topics(stem=None):
    if stem:
        try:
            topic_files = [(a.stem,frontmatter.load(a)) for a in topics_path.iterdir() if a.stem == stem]
        except IndexError:
            raise HTTPException(status_code=404, detail="Topic not found")
    else:    
        topic_files = [(a.stem,frontmatter.load(a)) for a in topics_path.iterdir()]
    topics = []
    for t in topic_files: 
        stem = t[0]
        md = t[1]
        md.stem = stem
        md.content = markdown.markdown(md.content)
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
    context['topics'] = load_topics()
    context['page'] = load_topics(stem=slug)[0]
    
    return templates.TemplateResponse("topic.html", context)

