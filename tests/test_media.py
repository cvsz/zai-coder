import tempfile
import unittest
from pathlib import Path

from zai_coder.media import generate_svg_image, generate_music_wav, generate_voice_wav, generate_animation_svg, generate_video_storyboard


class MediaTest(unittest.TestCase):
    def test_media_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            paths = [
                generate_svg_image("test", str(d / "image.svg")),
                generate_music_wav("test", str(d / "music.wav"), seconds=0.1),
                generate_voice_wav("hi", str(d / "voice.wav")),
                generate_animation_svg("test", str(d / "animation.svg")),
                generate_video_storyboard("test", str(d / "video.json")),
            ]
            for p in paths:
                self.assertTrue(Path(p).exists(), p)
                self.assertGreater(Path(p).stat().st_size, 10, p)


if __name__ == "__main__":
    unittest.main()
