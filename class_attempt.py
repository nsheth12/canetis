import os
from segment import Segment
from pydub import AudioSegment

import sys



class Segmentizer(object):
	def __init__(self, gentle_output, audio_file, anchor_length=7):
		self.gentle_output = gentle_output
		self.audio_file = audio_file
		self.anchor_length = anchor_length

		
		self.rel_audio_start = gentle_output[0].start
		self.total_gentle_len = len(gentle_output)
		self.correct_count = 0
		self.end_prev_anchor = 0
		self.first_correct_index = None
		self.segs = []



	def get_segment(self, bounded_gentle_output, aligned):

		# relative audio start time plus the audio time of the first/last word
		audio_start = self.rel_audio_start + bounded_gentle_output[0].start
		audio_finish = self.rel_audio_start + bounded_gentle_output[-1].end

		seg = Segment(audio_start, audio_finish,
					  bounded_gentle_output, aligned, self.audio_file,
					  self.total_gentle_len)

		return seg

	def append_unaligned_segment(self):

		# check if there is an unaligned seg before anchor point
		if self.end_prev_anchor != self.first_correct_index:

			# store the previous unanchored segments as a seg and append
			seg = self.get_segment(self.gentle_output[self.end_prev_anchor: \
				self.first_correct_index], False)	
			
			self.segs.append(seg)

	def append_aligned_segment(self, end_anchor_index):

		if self.correct_count > self.anchor_length:

			# store the anchor segment
			seg = self.get_segment(self.gentle_output[self.first_correct_index: \
				end_anchor_index], True)

			self.segs.append(seg)

			# update end of prev anchor tracker
			self.end_prev_anchor = end_anchor_index

			# reset counter variables
			self.correct_count = 0
			self.first_correct_index = None	


	def get_segments(self):

		# run through the list of Word objects
		for index, word in enumerate(self.gentle_output):
			# if the word was successfully aligned
			if word.success():
				# update variable values and move on
				self.correct_count += 1
			
				# update first_correct tracker
				if self.first_correct_index is None:
					self.first_correct_index = index	


			# if unaligned check if there are enough correct for anchor
			elif self.correct_count >= self.anchor_length:

				self.append_unaligned_segment()
				self.append_aligned_segment(index)	

			else:
				# reset counter variables
				self.correct_count = 0
				self.first_correct_index = None
		
		# if current seg is an anchor point ...
		if self.correct_count < self.anchor_length:
			self.first_correct_index = None

		self.append_unaligned_segment()	
		self.append_aligned_segment(None)

		return self.segs
		

	





