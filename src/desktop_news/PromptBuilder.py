from desktop_news.Register import REG_NAMESPACE
import desktop_news.Updaters


class PromptBuilder:
    def __init__(self, conf, args):
        self.header_ = conf["prompt"]["summary"]
        self.updaters_ = [REG_NAMESPACE[u]["instance"]
                          (conf, args) for u in REG_NAMESPACE]

    def _intersection(self, l1, l2):
        return [e for e in l1 if e in l2]

    def build_prompt(self, include_tags=[], exclude_tags=[]):
        ret = self.header_
        for u in self.updaters_:
            tags = REG_NAMESPACE[u.__class__.__name__]["tags"]
            if len(self._intersection(tags, include_tags)) > 0 or (include_tags == [] and len(self._intersection(tags, exclude_tags)) == 0):
                ret += u.update()
                ret += " and "
        return ret[:-5]
