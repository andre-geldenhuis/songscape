"""A detector for Hihi. This is just a specific version of
TFGraphDetector with some hardcoded parameters to point to a pre-trained
Hihi detector."""
import os
import sys
import time
import io
import numpy as np

from django.core.management.base import BaseCommand
from kokako.score import Detector
from www.recordings.models import Score, Recording, Snippet, Detector
from wavy import get_audio
from kokako.score import Audio
from kokako.detectors.tfgraph import TFGraphUser

class HihiCNN(Detector, TFGraphUser):
    code = 'hihi'
    description = 'Loads a trained convolutional neural net for Hihi detection'
    version = '0.0.1'

    def __init__(self, detector_path=None):
        """Loads a hihi detector.

        Args:
            detector_path (Optional[str]): path to the hihi detector. If not
                specified, looks for a file ./models/hihi.pb relative to the
                directory of this file.

        Raises:
            NotFoundError: if we can't find the file.
        """
        if not detector_path:
            detector_path = os.path.join(
                os.path.dirname(__file__), 'models', 'hihi.pb')

        super(HihiCNN, self).__init__(detector_path)

        # some constants
        self._audio_chunk_size = 7680  # how many samples we deal with at once
        self._audio_framerate = 24000  # expected sample rate of the audio
        self._audio_hop_size = self._audio_chunk_size // 2

    def score(self, audio):
        """score some audio using the tensorflow graph"""
        db_detectors =Detector.objects.get(code=detector.code, version=detector.version)
        # prepare the audio (convert to floating point, ensure the framerate)
        for recording in recordings:
            snippets = Snippet.objects.filter(recording=recording).exclude(scores__detector=hihi_detector).order_by('offset')
            if len(snippets):
                for snippet in snippets:
                        audio_data = Audio(*get_audio(recording.path, snippet.offset, snippet.duration))  # assume 16 bit (the loading code does)
                        audio_data = audio_data.astype(np.float32) / (2**15)
                        if audio.framerate != self._audio_framerate:
                            print('framerate is wrong (expected {}, found {})'.format(
                            self._audio_framerate, audio.framerate))
                        else:
                            result = self.average_graph_outputs(audio_data,self._audio_chunk_size,self._audio_hop_size)
                            s = Score(detector=db_detector, snippet=snippet,score=result)
                            s.save()
