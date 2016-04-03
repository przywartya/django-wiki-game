from WikiLogic.wiki import *
from threading import Thread

class wikiPage:
    def __init__(self, state, parent):
        # Use page link as state.
        self.state = state
        self.parent = parent

    def get_children(self):
        children = list(get_relevant_links(self.state).values())
        result = []
        for i in children:
            link = wikiPage(i, self)
            result.append(link)
        return result

    def get_path(self):
        path = []
        current = self
        while current is not None:
            path = [current.state] + path
            current = current.parent
        return path

def win_wiki_game(start, goal):
    if goal == start.state:
        return [start.state]
    queue = [start]
    visited = {start.state}
    while queue:
        vertex = queue.pop(0)
        for child in vertex.get_children():
            if goal == child.state:
                return child.get_path()
            elif child.state not in visited:
                visited.add(child.state)
                queue.append(child)
    return None

start = wikiPage("Poland", None)
print (win_wiki_game(start, "Kutno"))
