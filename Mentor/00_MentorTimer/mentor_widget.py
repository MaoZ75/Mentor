from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.logger import Logger
Builder.load_file('mentor_widget.kv')


class MentorWidget(Screen):  # ToDo: Pulire codice mettendo in kv?

    """def __init__(self):
        the_file = open('mentor_widget.kv')
        file_content = the_file.read()
        the_file.close()
        Builder.load_string(file_content)"""

    def clear_log(self):
        self.ids.log.text = "Cleared"

    def write_something(self, text):
        self.ids.log.text = "{}\n{}".format(text, self.ids.log.text)

    def write_cockpit(self, message, *args):
        #Logger.debug("write_cockpit: {}".format(message[2]))
        partial, total, img, label, other = message[2].split('\t', 4)
        #partial='00.00',total='00.00', label="Some Sequence"):
        self.ids.partial_left.text = partial
        self.ids.total_left.text = total
        #Logger.debug("New Image: {}".format(img))
        if self.ids.img_bk.source != img:
            self.ids.img_bk.source = img
            #self.ids.img_bk.load(img, keep_data=True)
            #self.ids.img_bk.ask_update()
        self.ids.log.text = label
