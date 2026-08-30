import torch

from config import MODEL_SCRIPT_PATH, MODEL_WEIGHTS_PATH
from model import Model


def main():
    model = Model()
    try:
        model.load_state_dict(torch.load(MODEL_WEIGHTS_PATH))
    except (FileNotFoundError):
        print("Run train.py first")
        return
    model.eval()
    script_model = torch.jit.script(model)
    script_model.save(MODEL_SCRIPT_PATH)

    print(f"Exported to {MODEL_SCRIPT_PATH}")


if __name__ == "__main__":
    main()
