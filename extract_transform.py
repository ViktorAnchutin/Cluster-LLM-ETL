
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from transform_utils import *


def main():
    with open("videos.txt", 'r') as file:
        videos = [line.strip() for line in file]

    transcripts = [YouTubeTranscriptApi.get_transcript(video_id) for video_id in videos]


    subtitle_collections = [merge_subtitles(transcript) for transcript in transcripts]

    split_video_dfs = [
        create_split_video_df(subtitles, base_url_format.format(id=video_id))
        for subtitles, video_id in zip(subtitle_collections, videos)
    ]

    split_video_df = pd.concat(split_video_dfs, ignore_index=True)

    documents_json = split_video_df.to_json(orient="index")

    with open("transcripts.json", "w") as f:
        f.write(documents_json)


if __name__ == "__main__":
    main()