import json
from collections import defaultdict
from random import randint

from moviepy.editor import VideoFileClip, concatenate_videoclips

data = json.load(open('trump.json'))


def build_index(data):
    words = []
    for result in data['response']['results']:
        alternative = result['alternatives'][0]
        #for alternative in result['alternatives']:
        for word in alternative['words']:
            words.append(word)

    index = defaultdict(lambda: [])

    for word in words:
        key = word['word'].lower()
        index[key].append({
            'start': word['startTime'][0: len(word['startTime']) - 1],
            'end': word['endTime'][0: len(word['endTime']) - 1]
        })

    return index


index = build_index(data)

for key, value in index.items():
    print(key)

sentence = ["respect", "our", "national", "anthem", "because", "i'm", "god"]
video = VideoFileClip('full_speech.mkv')

clips = []
for word in sentence:
    options = index[word]
    num_options = len(options)
    if num_options == 0:
        print("Word %s is not in index" % word)
        continue
    start_end = options[randint(0, num_options - 1)]
    clip = video.subclip(float(start_end['start']), float(start_end['end']))
    clips.append(clip)

final_clip = concatenate_videoclips(clips, padding=0.0)
final_clip.write_videofile("out.mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264",
                           audio_codec="aac")
