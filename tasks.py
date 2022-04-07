import warnings
from invoke import task
from train import Train
from pretrained import PretrainedModel

warnings.filterwarnings("ignore")

@task
def train(ctx):

    config = ctx.model
    model = PretrainedModel(config.output_features)
    train_model = Train(config, model)
    train_model.sckorh_train()
    
    




    


