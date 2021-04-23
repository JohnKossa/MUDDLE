from __future__ import annotations
from typing import Optional, List


class Conversation:
    """Tracks a conversation between a player and an NPC.
    When a player uses the !say command, it changes the conversation node here.
    If the player or the NPC leaves the room, the conversation ends and is cleaned up.
    This object will also contain helper functions that pass context to the dialog trees if required."""
    def __init__(self):
        self.npc = None
        self.character = None
        self.dialog_dict = None
        self.conversation_node = None
        self.room = None
        self.possible_responses = []
        self.active_triggers = []

    def init_conversation(self, game, source_dict):
        self.dialog_dict = source_dict
        for possible_init in self.dialog_dict["init"]:
            if possible_init.get("condition") is not None:
                if eval(possible_init, {}, {"game": game, "npc": self.npc, "character": self.character}):
                    self.conversation_node = possible_init["dialog"]
        if self.conversation_node is None:
            raise Exception("Unable to start dialog.")
        else:
            self.say_node(game)
        from utils.TriggerFunc import TriggerFunc
        leave_room_trigger = TriggerFunc(self.cleanup_on_leave_room)
        self.active_triggers.append(leave_room_trigger)
        game.once("leave_room", leave_room_trigger)

    def cleanup_on_leave_room(self, source_player=None, game=None, **kwargs):
        if source_player == self.character:
            self.cleanup(game)

    def say_node(self, game):
        npc_text = format(self.dialog_dict["dialogs"][self.conversation_node]["text"],
                          **{"game": game, "npc": self.npc, "character": self.character})
        response_ids = self.dialog_dict["dialogs"][self.conversation_node]["responses"]
        if response_ids is None:
            self.cleanup(game)
            return
        response_objects = [*map(lambda x: self.dialog_dict["responses"][x], response_ids)]
        filtered_response_objects = [x for x in response_objects if x.get("condition", True)]
        if len(filtered_response_objects) == 0:
            self.cleanup(game)
            return
        self.possible_responses = filtered_response_objects
        response_texts = ""
        for i in range(len(self.possible_responses)):
            response = self.possible_responses[i]
            response_texts = response_texts + f"\n{i+1}." + format(response["text"], **{"game": game, "npc": self.npc, "character": self.character})
        game.discord_connection.send_game_chat_sync(npc_text+response_texts, [self.character.discord_user])

    def handle_response(self, game, response):
        try:
            resp_num = int(response)
        except ValueError:
            game.discord_connection.send_game_chat_sync("Response not recognized", [self.character.discord_user])
            return
        try:
            matched_response = self.possible_responses[resp_num-1]
        except IndexError:
            game.discord_connection.send_game_chat_sync("Response not recognized", [self.character.discord_user])
            return
        response_effect = matched_response.get("effect", None)
        if response_effect is not None:
            eval(response_effect, {}, {"game": game, "npc": self.npc, "character": self.character})
        self.conversation_node = matched_response["dialog"]
        self.say_node(game)

    def cleanup(self, game):
        self.room.conversations.remove(self)
        self.npc = None
        self.character = None
        self.dialog_dict = None
        self.conversation_node = None
        self.room = None
        self.possible_responses = []
        for trigger in self.active_triggers:
            game.off("leave_room", trigger)
