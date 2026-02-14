class Actor:
    def __init__(self, name):
        self.name = name
        self.last_line = None


class Play:
    def __init__(self, title):
        self.title = title


class Rehearser:
    def __init__(self, play_title, user_character):
        self.play = Play(play_title)
        self.user = Actor(user_character)
        # self.ai = Actor(ai_character)
        self.history = []  # list of (actor, line)

    def record_line(self, actor_name, line):
        self.history.append((actor_name, line))
        if actor_name == self.user.name:
            self.user.last_line = line
        else:
            # self.ai.last_line = line
            pass

    def get_context_prompt(self):
        last_user_line = self.user.last_line or ""
        return f"""
        The user is {self.user.name} in the play {self.play.title}.
        You play all other characters.
        The user's last line was: "{last_user_line}"
        Respond with the next line of your character, keeping the scene flowing naturally.
        """
