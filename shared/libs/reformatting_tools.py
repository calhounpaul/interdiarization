import os, sys, json, shutil, getpass, atexit, time, hashlib

this_dir = libs_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir_path = os.path.dirname(libs_dir)
outputs_dir_path = os.path.join(shared_dir_path, "workspace", "outputs")

def group_diarizations(json_dict, max_jitter_gap=2.0):
    segments = json_dict["segments"]
    speech_segments = []
    for segment in segments:
        if len(segment["words"]) == 0:
            continue
        for word in segment["words"]:
            if "speaker" not in word:
                word["speaker"] = "UNKNOWN"
        prior_speaker = segment["words"][0]["speaker"]
        for word in segment["words"]:
            speaker = word["speaker"]
            if speaker != prior_speaker:
                speech_segments.append({
                    "speaker": prior_speaker,
                    "text": " ".join([w["word"] for w in segment["words"]])
                })
                segment["words"] = []
                break
    grouped_segments = []
    current_segment = None
    for segment in speech_segments:
        if not current_segment:
            current_segment = segment
            continue
        if segment["speaker"] == current_segment["speaker"]:
            current_segment["text"] += " " + segment["text"]
        else:
            grouped_segments.append(current_segment)
            current_segment = segment
    if current_segment:
        grouped_segments.append(current_segment)
    return grouped_segments

            

def reformat_all_transcription_json_to_transcripts():
    #iterate over all transcription.json files, check for transcription.txt in the same directory, and if it doesn't exist, create it
    for parent_dir in os.listdir(outputs_dir_path):
        for transcript_folder in os.listdir(os.path.join(outputs_dir_path, parent_dir)):
            transcript_folder_path = os.path.join(outputs_dir_path, parent_dir, transcript_folder)
            if os.path.exists(os.path.join(transcript_folder_path, "transcription.txt")):
                #verify size of transcription.txt
                try:
                    if os.path.getsize(os.path.join(transcript_folder_path, "transcription.txt")) > 10:
                        continue
                except:
                    continue
            if not os.path.exists(os.path.join(transcript_folder_path, "transcription.json")):
                continue
            json_dict = json.load(open(os.path.join(transcript_folder_path, "transcription.json"), 'r'))
            with open(os.path.join(transcript_folder_path, "transcription.txt"), 'w') as f:
                try:
                    grouped_segments = group_diarizations(json_dict)
                    for segment in grouped_segments:
                        f.write(f"{segment['speaker']}:\n{segment['text']}\n\n")
                    print(f"Created transcription.txt for {transcript_folder}")
                except Exception as e:
                    print(f"Error processing {transcript_folder}: {e}")
                    #save to transcription.txt anyway
                    f.write(e)
                    continue

            