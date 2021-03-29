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

NUM_TRACKS = 4
NUM_RETURNS = 4
NUM_SCENES = 7
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
		self.transport = TransportComponent()
		self.transport.name = 'Transport'
		
		play_button = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 14, 36)
		play_button.name = 'play_button'
		self.transport.set_play_button(play_button)
		#ButtonElement(is_momentary, MIDI_NOTE_TYPE, 14, 36)
		
		
		

	


