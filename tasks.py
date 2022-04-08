import uvicorn
import warnings
from invoke import task
from main import app, img

warnings.filterwarnings("ignore")

@task
def start(ctx):
    config = ctx.model
    img.read_config(config)
    uvicorn.run(app)
