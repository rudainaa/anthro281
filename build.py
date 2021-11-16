import time 
from fastapi import Request
from main import index, topics
import shutil
from pathlib import Path 

def build_home():
    page = index(Request)
    (site_path / 'index.html').write_bytes(page.body)

def topic_pages():
    if not (site_path / 'topic' ).exists():
        (site_path / 'topic' ).mkdir(parents=True, exist_ok=True)    
        
    topics_path = Path.cwd() / 'data' / 'topics'
    topic_files = [a.stem for a in topics_path.iterdir()]
    
    for topic in topic_files:
        page = topics(Request, topic)
        (site_path / 'topic' / f'{topic}.html').write_bytes(page.body)

if __name__ == '__main__':
    start_time = time.time()
    # Create site directory
    site_path = Path.cwd() / 'site'
    if not site_path.exists():
        site_path.mkdir(parents=True, exist_ok=True)

    # Copy assets to site directory
    if not (site_path / 'assets').exists():
        shutil.copytree((Path.cwd() / 'assets'), (site_path / 'assets')) 
    else:
        shutil.rmtree((site_path / 'assets'))
        shutil.copytree((Path.cwd() / 'assets'), (site_path / 'assets')) 

    build_home()
    topic_pages()
    print(f"--- {time.time() - start_time} seconds ---")
