# Interdiarization

A fake word conveniently lacking google results.

Setup.sh is intended to be run on a clean VM in my home XCP-ng server. You probably don't want to run it on your own machine as-is. If this works I'll make it cleaner and more compatible.

The goal is to use WhisperX diarized transcriptions of a single spoken audio corpus (in this case, youtube channels inserted into shared/workspace/urls_list.txt) along with some type of agentic pipeline for entity extraction, to reliably figure out the ground truth transcript names. If that fails I plan to get weird with multimodality. Llava-1.6-34b may be involved.

![Screenshot from 2024-04-23 07-50-18](https://github.com/calhounpaul/interdiarization/assets/26489865/1ba2309c-753d-4a4b-ac83-b9d6d43d5617)
