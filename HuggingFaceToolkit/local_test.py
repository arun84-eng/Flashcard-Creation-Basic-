from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Example educational prompt
input_text = "Explain the process of photosynthesis in simple terms."
input_ids = tokenizer(input_text, return_tensors="pt").input_ids

output_ids = model.generate(input_ids, max_length=100, num_return_sequences=1)
answer = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print("Generated Answer:")
print(answer)
