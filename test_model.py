from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_path = "toxic_model"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

model.to(device)
model.eval()

def predict(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    """
    De esta forma nos da la el porcentaje entre 0 y 1 de ser toxico, ya veremos que umbral ponemos,
    si solo quieres que prediga 0 o 1 cambia las 3 lineas siguiebtes por esto
        logits = outputs.logits
        pred = logits.argmax(dim=1).item()

        return pred
    """
    probs = torch.softmax(outputs.logits, dim=1)
    toxic_score = probs[0][1].item()
 
    return toxic_score

print(predict("eres un idiota"))
print(predict("hola, que tal"))