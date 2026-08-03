config.json
tokenizer.json

*.gguf

AutoTokenizer.from_pretrained(path)

AutoModelForCausalLM.from_pretrained(path)

FROM D:/AIModels/GGUF/Alibaba/Qwen3-8B/Qwen3.gguf

PARAMETER temperature 0.7
