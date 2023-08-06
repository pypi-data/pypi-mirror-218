import os
from huggingface_hub import snapshot_download


def save_huggingface_model(model_name, path):
    snapshot_download(repo_id=model_name, local_dir=path)