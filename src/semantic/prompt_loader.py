from pathlib import Path

class PromptLoader:
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)

    def load(self, name: str) -> str:
        return (self.prompts_dir / name).read_text(encoding="utf-8")
