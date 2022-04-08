import warnings
from invoke import task
from train import Train
from pretrained import PretrainedModel

warnings.filterwarnings("ignore")


@task
def train(ctx):
    model_config = ctx.model
    dataset_config = ctx.dataset

    model = PretrainedModel(model_config.output_features)
    train_model = Train(model_config, dataset_config, model)

    train_model.sckorh_train()
