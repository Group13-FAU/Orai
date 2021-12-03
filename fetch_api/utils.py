from typing import Sized

from .models import Story


class Sprint(Sized):

    def __init__(self, name: str) -> None:
        self.stories = []
        self.name = name

    def __len__(self) -> int:
        return len(self.stories)

    def append(self, story: Story):
        self.stories.append(story)

    def __str__(self) -> str:
        return f"Sprint(name: {self.name}, total_complexity: {self.total_complexity()}, stories: {self.stories}"

    def total_complexity(self) -> int:
        if len(self.stories) > 0:
            return sum(map(lambda story: story.complexity, self.stories))
        else:
            return 0
