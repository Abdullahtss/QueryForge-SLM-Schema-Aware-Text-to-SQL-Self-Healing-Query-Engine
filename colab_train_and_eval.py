# ==============================================================================
# QueryForge-SLM: Google Colab QLoRA Fine-Tuning & Held-Out Evaluation Script
# Run on Google Colab with a free T4 GPU:
# !pip install -q -U torch transformers peft accelerate bitsandbytes datasets trl sqlglot pandas
# ==============================================================================

import json
import re
import torch
import sqlglot
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

MODEL_ID = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
OUTPUT_DIR = "./queryforge-qwen-1.5b-qlora"

print("Loading clean Text-to-SQL dataset (b-mc2/sql-create-context)...")
raw_dataset = load_dataset("b-mc2/sql-create-context", split="train")
shuffled = raw_dataset.shuffle(seed=42)
train_data = shuffled.select(range(2000))
test_data = shuffled.select(range(2000, 2150))

SYSTEM_PROMPT = (
    "You are an expert SQL compiler. Given a database DDL schema and a natural language question, "
    "output ONLY a valid, executable SQL query without markdown explanation."
)

def format_chat_prompt(example, include_answer=True):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"### Database Schema:\n{example['context']}\n\n### Question:\n{example['question']}\n\n### SQL Query:",
        },
    ]
    if include_answer:
        messages.append({"role": "assistant", "content": example["answer"]})
    return messages

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

def apply_template(example):
    messages = format_chat_prompt(example, include_answer=True)
    return {"text": tokenizer.apply_chat_template(messages, tokenize=False)}

train_dataset = train_data.map(apply_template)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)

def extract_clean_sql(raw_output: str) -> str:
    cleaned = re.sub(r"```sql|```", "", raw_output, flags=re.IGNORECASE).strip()
    return cleaned.split(";")[0].strip()

def normalize_sql(sql_str: str) -> str:
    try:
        return sqlglot.transpile(sql_str, read="sqlite", write="sqlite")[0].lower().strip()
    except Exception:
        return " ".join(sql_str.lower().split())

def evaluate_model_on_test_set(eval_model, dataset_split, tag="Base Model"):
    eval_model.eval()
    valid_ast_count = 0
    exact_match_count = 0
    clause_hits = 0
    total = len(dataset_split)

    for item in dataset_split:
        messages = format_chat_prompt(item, include_answer=False)
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt").to(eval_model.device)

        with torch.no_grad():
            outputs = eval_model.generate(
                **inputs,
                max_new_tokens=128,
                temperature=0.0,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )

        generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]
        pred_raw = tokenizer.decode(generated_tokens, skip_special_tokens=True)
        pred_sql = extract_clean_sql(pred_raw)
        gold_sql = extract_clean_sql(item["answer"])

        try:
            sqlglot.parse_one(pred_sql, read="sqlite")
            valid_ast_count += 1
        except Exception:
            pass

        if normalize_sql(pred_sql) == normalize_sql(gold_sql):
            exact_match_count += 1

        keywords = ["select", "where", "group by", "order by", "join", "count", "sum", "avg", "max", "min"]
        gold_kw = {k for k in keywords if k in gold_sql.lower()}
        pred_kw = {k for k in keywords if k in pred_sql.lower()}
        if not gold_kw or gold_kw.issubset(pred_kw):
            clause_hits += 1

    metrics = {
        "model_stage": tag,
        "ast_syntax_validity_pct": round((valid_ast_count / total) * 100, 2),
        "normalized_exact_match_pct": round((exact_match_count / total) * 100, 2),
        "structural_clause_accuracy_pct": round((clause_hits / total) * 100, 2),
    }
    print(f"[{tag}] Results:", json.dumps(metrics, indent=2))
    return metrics

base_metrics = evaluate_model_on_test_set(model, test_data, tag="Base Model (Zero-Shot)")

model = prepare_model_for_kbit_training(model)
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
)
model = get_peft_model(model, lora_config)

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    num_train_epochs=1,
    logging_steps=20,
    fp16=True,
    optim="paged_adamw_8bit",
    save_strategy="epoch",
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,
    report_to="none",
)

trainer = SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    dataset_text_field="text",
    max_seq_length=512,
    tokenizer=tokenizer,
    args=training_args,
)

trainer.train()
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

ft_metrics = evaluate_model_on_test_set(model, test_data, tag="QLoRA Fine-Tuned (r=16)")

with open("colab_benchmark_results.json", "w") as f:
    json.dump({"base": base_metrics, "qlora": ft_metrics}, f, indent=2)
