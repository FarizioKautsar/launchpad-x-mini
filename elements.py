#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_Mini_MK3/elements.py
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import depends
from ableton.v2.control_surface.elements import ButtonMatrixElement, ColorSysexElement, SysexElement
from novation import sysex
from novation.launchpad_elements import create_button, create_slider, LaunchpadElements, SESSION_WIDTH, BUTTON_FADER_COLOR_CHANNEL
from . import sysex_ids as ids

class Elements(LaunchpadElements):
    model_id = ids.LP_MINI_MK3_ID
    default_layout = sysex.KEYS_LAYOUT_BYTE
    button_fader_cc_offset = 21

    @depends(skin=None)
    def __init__(self, skin = None, *a, **k):
        (super(Elements, self).__init__)(*a, **k)
        self.drums_mode_button = create_button(96, u'Drums_Mode_Button')
        self.keys_mode_button = create_button(97, u'Keys_Mode_Button')
        self.user_mode_button = create_button(98, u'User_Mode_Button')
        self.button_faders = ButtonMatrixElement(rows=[
            [create_slider(index + self.button_fader_cc_offset, 'Button_Fader_{}'.format(index)) for index in range(SESSION_WIDTH)]],
        name='Button_Faders')
        self.button_fader_color_elements_raw = [create_button(index + self.button_fader_cc_offset, u'Button_Fader_Color_Element_{}'.format(index), channel=BUTTON_FADER_COLOR_CHANNEL) for index in range(SESSION_WIDTH)]
        self.button_fader_color_elements = ButtonMatrixElement(rows=[self.button_fader_color_elements_raw], name=u'Button_Fader_Color_Elements')
        session_button_color_identifier = sysex.STD_MSG_HEADER + (ids.LP_MINI_MK3_ID, 20)
        self.session_button_color_element = ColorSysexElement(name=u'Session_Button_Color_Element', sysex_identifier=session_button_color_identifier, send_message_generator=lambda v: session_button_color_identifier + v + (sysex.SYSEX_END_BYTE,), skin=skin)
        self.button_fader_setup_element = SysexElement(name=u'Button_Fader_Setup_Element', send_message_generator=partial(self._fader_setup_message_generator, 0))