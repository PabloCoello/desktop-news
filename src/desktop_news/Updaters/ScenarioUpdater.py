from desktop_news.Register import Register
from desktop_news.IUpdater import IUpdater


@Register("Update prompt with user defined scenario", tags=["literal", "scenario"])
class ScenarioUpdater(IUpdater):
    def __init__(self, conf, args):
        self.args_ = args

    def update(self) -> str:
        return f" Create the image like everything is happening in the following environment/universe/scenario: {self.args_.scenario}."
