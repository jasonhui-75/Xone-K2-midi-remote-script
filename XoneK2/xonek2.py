from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
from _Framework.SliderElement import SliderElement
from _Framework.TransportComponent import TransportComponent 
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SessionComponent import SessionComponent
from _Framework.EncoderElement import *

from Launchpad.ConfigurableButtonElement import ConfigurableButtonElement
from .MyTransportComponent import MyTransportComponent

NUM_TRACKS = 4
NUM_RETURNS = 4
NUM_SCENES = 7

def new(transport, fine_control):
	if transport._tempo_fine_control != fine_control:
		transport._tempo_fine_control = fine_control
		transport._tempo_fine_value.subject = fine_control
		transport._fine_tempo_needs_pickup = True
		transport._prior_fine_tempo_value = -1
	
class xonek2(ControlSurface):

	def __init__(self, c_instance):
		super(xonek2, self).__init__(c_instance)
		with self.component_guard():
			global _map_modes
			_map_modes = Live.MidiMap.MapMode
			# mixer
			global mixer
			NUM_TRACKS = 4
			NUM_RETURNS = 4
			self.mixer = MixerComponent(NUM_TRACKS, NUM_RETURNS)
		
			self._create_components()
			self.show_message("Powered by Jason")

	def _create_components(self):
		self._create_mixer()
		self._create_transport()
	

	def _create_mixer(self):
		for i in range(NUM_TRACKS):
			self.mixer.channel_strip(i).set_volume_control(SliderElement(MIDI_CC_TYPE, 14, 16 + i))
		self.mixer.master_strip().set_volume_control(EncoderElement(MIDI_CC_TYPE, 14, 3, _map_modes.relative_smooth_two_compliment))

	
	
	def _create_transport(self):
		self.transport = MyTransportComponent()
		self.transport.name = u'Transport'
		
		play_button = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 14, 36)
		play_button.name = u'Play_Button'
		self.transport.set_play_button(play_button)
		#ButtonElement(is_momentary, MIDI_NOTE_TYPE, 14, 36) does not work
		
		#shiftb = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 14, 12)
		#shiftb.name = 'shift_button'
		#self.transport.shift_button = shiftb

		ctempo_encoder = EncoderElement(MIDI_CC_TYPE, 14, 0, _map_modes.relative_smooth_two_compliment)
		ctempo_encoder.name = u'Coarse_Tempo_Control'
		self.transport.set_coarse_tempo_encoder(ctempo_encoder)

		ftempo_encoder = EncoderElement(MIDI_CC_TYPE, 14, 1, _map_modes.relative_smooth_two_compliment)
		ftempo_encoder.name = u'FineTempo_Control'
		self.transport.set_fine_tempo_encoder(ftempo_encoder)

		#self.transport.set_tempo_fine_control(SliderElement(MIDI_CC_TYPE, 14, 16))
		#new(self.tranport, SliderElement(MIDI_CC_TYPE, 14, 16))
		#self.transport.set_tempo_control(SliderElement(MIDI_CC_TYPE, 14, 16), SliderElement(MIDI_CC_TYPE, 14, 17))
		
	
