from pathlib import Path
from get_problems import create_math_prompt_template_2, get_json_schema, get_objective

prompt_template = create_math_prompt_template_2()
objectives = get_objective(-1)
schema = get_json_schema(False)

prompts_dir = Path("prompts")
prompts_dir.mkdir(exist_ok=True)

for objective in objectives:
    objective_num = objective["objective"]
    count = objective["count"] 
    text = objective["text"]
    formatted_text = prompt_template.format(count=count, objective=text, schema=schema)
    prompt_filename = f"prompt-{objective_num}.txt"
    prompt_file_path = prompts_dir / prompt_filename
    prompt_file_path.write_text(formatted_text, encoding="utf-8")

print("done.")
