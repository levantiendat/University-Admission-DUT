from transformers import AutoModel, AutoTokenizer

model_name = "vinai/phobert-base"
save_path = "./models/phobert"

print(f"Tải mô hình {model_name}...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)

print(f"✅ Đã lưu tại {save_path}")
