from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class Toxic:

    model_path = "toxic_model"

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


        self.tokenizer = AutoTokenizer.from_pretrained(Toxic.model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(Toxic.model_path)

        self.model.to(self.device)
        self.model.eval()

    def predict(self,text):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)

        """
        De esta forma nos da la el porcentaje entre 0 y 1 de ser toxico, ya veremos que umbral ponemos,
        si solo quieres que prediga 0 o 1 cambia las 3 lineas siguiebtes por esto
            logits = outputs.logits
            pred = logits.argmax(dim=1).item()

            return pred
        """
        probs = torch.softmax(outputs.logits, dim=1)
        toxic_score = probs[0][1].item()

        if(toxic_score>=0.8):
            return True
        else:
            return False
        