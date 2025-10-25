from datetime import datetime
import os

def get_model_version():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"model_{timestamp}"

def save_model(model, model_dir):
    version = get_model_version()
    model_path = os.path.join(model_dir, version)
    
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    
    # Assuming the model has a method to save itself
    model.save(os.path.join(model_path, "model.pkl"))
    
    return version

def list_model_versions(model_dir):
    return sorted(os.listdir(model_dir))