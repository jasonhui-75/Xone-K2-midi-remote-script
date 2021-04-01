from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.Control import ButtonControl
from _Framework.SubjectSlot import subject_slot
from _Framework.ButtonElement import ButtonElement
from _Framework.TransportComponent import TransportComponent 
from _Framework.Util import clamp

class MyTransportComponent(TransportComponent):
    shift_button = ButtonControl()

    def __init__(self, *a, **k):

        def play_toggle_model_transform(val):
            if self.shift_button.is_pressed:
                return False
            return val

        k[u'play_toggle_model_transform'] = play_toggle_model_transform
        super(MyTransportComponent, self).__init__(*a, **k)
        self._coarse_tempo_encoder_control = None
        self._fine_tempo_encoder_control = None
   
    
    def set_coarse_tempo_encoder(self, control):
        assert not control or control.message_map_mode() in (Live.MidiMap.MapMode.relative_smooth_two_compliment, Live.MidiMap.MapMode.relative_two_compliment)
        if control != self._coarse_tempo_encoder_control:
            self._coarse_tempo_encoder_control = control
            self._coarse_tempo_encoder_value.subject = control
            self.update()

    @subject_slot(u'value')
    def _coarse_tempo_encoder_value(self, value):
        step = 1.0 
        amount = value - 128 if value >= 64 else value
        self.song().tempo = clamp(self.song().tempo + amount * step, 50, 200)

    def set_fine_tempo_encoder(self, control):
        assert not control or control.message_map_mode() in (Live.MidiMap.MapMode.relative_smooth_two_compliment, Live.MidiMap.MapMode.relative_two_compliment)
        if control != self._coarse_tempo_encoder_control:
            self._fine_tempo_encoder_control = control
            self._fine_tempo_encoder_value.subject = control
            self.update()

    @subject_slot(u'value')
    def _fine_tempo_encoder_value(self, value):
        step = 0.1 
        amount = value - 128 if value >= 64 else value
        self.song().tempo = clamp(self.song().tempo + amount * step, 50, 200)