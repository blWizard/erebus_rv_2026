# NOTE(Richo): For this to work you need the obsws-python library, you can
# install it by running 'pip install obsws-python' on the cmd
import obsws_python as obs
import time
import traceback
import json
import os

with open(os.path.join(os.path.dirname(__file__), "scenes.json"), encoding="utf-8") as f:
    SCENES = json.load(f)

class ObsControl:
    def __init__(self, host, port, password):
        self.connected = False
        self.__host = host
        self.__port = port
        self.__password = password
        self.__ws = None

    def connect(self):
        try:
            self.__ws = obs.ReqClient(host=self.__host, port=self.__port, password=self.__password, timeout=3)
            self.connected = True
            self.__ws.set_current_scene_transition_duration(300)
            self.__ws.set_current_scene_transition("Desvanecimiento")
            self.__ws.set_current_program_scene(SCENES["initial_scene"])
        except:
            self.connected = False
            traceback.print_exc()

    def go_to_scene(self, scene_name):
        self.__ws.set_current_program_scene(scene_name)

    def set_text_vars(self, input_name, text):
        if not self.connected: return
        self.__ws.set_input_settings(input_name, {"text": text}, True)

    def start_record(self, name):
        if not self.connected: return
        self.__ws.set_profile_parameter("Output", "FilenameFormatting", name)
        self.__ws.start_record()

    def stop_record(self):
        if not self.connected: return
        self.__ws.stop_record()

    def start_video(self, filename):
        if not self.connected: return
        self.go_to_scene(SCENES["initial_scene"])
        self.start_record(filename)
        time.sleep(2)
        self.go_to_scene(SCENES["presentation_scene"])
        time.sleep(1.5)
        self.go_to_scene(SCENES["competition_scene"])

    def end_video(self):
        if not self.connected: return
        self.go_to_scene(SCENES["end_scene"])
        time.sleep(2)
        self.stop_record()