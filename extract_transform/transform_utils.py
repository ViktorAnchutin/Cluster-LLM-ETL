from datetime import timedelta
import srt
import pandas as pd


TRIGGER_LENGTH = 750  # 30-60 seconds
base_url_format = "https://www.youtube.com/watch?v={id}"
query_params_format = "&t={start}s"

def merge(subtitles, idx):
    new_content = combine_content(subtitles)

    # preserve start as timedelta
    new_start = seconds_float_to_timedelta(subtitles[0]["start"])
    # merge durations as timedelta
    new_duration = seconds_float_to_timedelta(sum(sub["duration"] for sub in subtitles))
    
    # combine
    new_end = new_start + new_duration
    
    return srt.Subtitle(index=idx, start=new_start, end=new_end, content=new_content)


def combine_content(subtitles):
    contents = [subtitle["text"].strip() for subtitle in subtitles]
    return " ".join(contents) + "\n\n"


def get_charcount(subtitle):
    return len(subtitle["text"])


def seconds_float_to_timedelta(x_seconds):
    return timedelta(seconds=x_seconds)


def merge_subtitles(subtitles):
    merged_subtitles = []
    current_chunk, current_length, chunk_idx = [], 0, 1

    for subtitle in subtitles:
        current_chunk.append(subtitle)
        added_length = get_charcount(subtitle)
        new_length = current_length + added_length

        if new_length >= TRIGGER_LENGTH:
            merged_subtitle = merge(current_chunk, chunk_idx)
            merged_subtitles.append(merged_subtitle)
            current_chunk, current_length = [], 0
            chunk_idx += 1
        else:
            current_length = new_length

    if current_chunk:
        merged_subtitle = merge(current_chunk, chunk_idx)
        merged_subtitles.append(merged_subtitle)

    return merged_subtitles


def create_split_video_df(subtitles, base_url):
    rows = []
    for subtitle in subtitles:
        raw_text = subtitle.content
        text = raw_text.strip()
        start = timestamp_from_timedelta(subtitle.start)
        url = base_url + query_params_format.format(start=start)

        rows.append({"text": text, "source": url})

    video_df = pd.DataFrame.from_records(rows)
    return video_df


def timestamp_from_timedelta(td):
    return int(td.total_seconds())