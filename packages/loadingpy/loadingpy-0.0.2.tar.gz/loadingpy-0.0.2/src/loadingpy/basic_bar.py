import os
import time
from typing import Any, Iterable


class ProgressBar:
    def __init__(
        self,
        iterable: Iterable,
        total_steps: int = -1,
        base_str: str = "loop",
    ) -> None:
        self.iterable = iter(iterable)
        self.total_steps = len(iterable) if total_steps < 0 else total_steps
        self.base_str = base_str
        self.progress_bar_size = self.get_size() - (36 - (21 - len(self.base_str)))
        self.current_progression = 0
        self.suffix_length = 11
        self.start_time = time.time()

    def __len__(self) -> int:
        return self.total_steps

    def get_size(self):
        try:
            width = os.get_terminal_size().columns
        except:
            width = 80
        return width

    def get_remaining_time(self) -> str:
        one_step_duration = (time.time() - self.start_time) / (
            self.current_progression + 1
        )
        remaining_steps = self.total_steps - (self.current_progression + 1)
        remaining_time = one_step_duration * remaining_steps
        return time.strftime("%H:%M:%S", time.gmtime(remaining_time))

    def runtime(self) -> str:
        duration = time.time() - self.start_time
        return time.strftime("%H:%M:%S", time.gmtime(duration))

    def update_bar_size(self) -> None:
        if (
            self.get_size() - (3 + len(self.base_str) + self.suffix_length)
            != self.progress_bar_size
        ):
            self.progress_bar_size = self.get_size() - (
                3 + len(self.base_str) + self.suffix_length
            )

    def build_prefix(self) -> str:
        base_string = f"\r[{self.base_str}]"
        return base_string

    def build_bar(self, progression_complete: bool) -> str:
        if progression_complete:
            bar = f"|" + "█" * self.progress_bar_size + "|"
        else:
            percentage = int(
                self.progress_bar_size * self.current_progression / self.total_steps
            )
            bar = (
                f"|"
                + "█" * percentage
                + " " * (self.progress_bar_size - percentage)
                + "|"
            )
        return bar

    def build_suffix(self, progression_complete: bool) -> str:
        if progression_complete:
            return self.runtime()
        else:
            return self.get_remaining_time()

    def __iter__(self):
        return self

    def __next__(self, *args: Any, **kwds: Any) -> Any:
        progression_complete = self.current_progression == self.total_steps
        base_string = self.build_prefix()
        suffix = self.build_suffix(progression_complete=progression_complete)
        self.update_bar_size()
        bar = self.build_bar(progression_complete=progression_complete)
        print(
            f"\r{base_string} {bar} {suffix}",
            end="" if not progression_complete else "\n",
        )
        if progression_complete:
            raise StopIteration
        output = next(self.iterable)
        self.current_progression += 1
        return output


if __name__ == "__main__":
    a = list(range(15))
    for i in ProgressBar(a):
        pass
    print("last value", i)
    print("---")
    for i in ProgressBar(a, total_steps=10):
        pass
    print("last value", i)

# python -m src.loadingpy.basic_bar
