"""Test script."""

import argparse
import uuid

import streamlit as st
from streamlitopencvplayer.app import display_video


# Initiate all session states used
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
if 'frames' not in st.session_state:
    st.session_state['frames'] = []
if 'alerts' not in st.session_state:
    st.session_state['alerts'] = []
if 'data' not in st.session_state:
    st.session_state['data'] = []
if 'alerts_list' not in st.session_state:
    st.session_state['alerts_list'] = []
if 'name_vid_sel' not in st.session_state:
    st.session_state['name_vid_sel'] = "1687441603.4032989_1687441609.4032989"

class opencvplayer:
    """Class streamlit opencv player."""

    def __init__(self, video_path, json_file):
        self.video_path = video_path
        self.json_file = json_file


    def main(self):
        """Test function.

        Args:
            video_path (required): video file path or video url.
            json_file

        Returns:
            The video Player.
        """
        if self.video_path is not None:
            return display_video(self.video_path, self.json_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runnnig...")
    parser.add_argument(
        "--video-path",
        "-V",
        help="Enter the video path",
        default=str(uuid.uuid4().hex),
    )
    parser.add_argument(
        "--json-file",
        "-J",
        help="Enter the json file path",
    )
    args = parser.parse_args()
    opencvplayer = opencvplayer(
        args.video_path, args.json_file)
    opencvplayer.main()

'''
    video_path = "https://cvlogger.blob.core.windows.net/jsonconcat/1687441603.4032989_1687441609.4032989.webm?sp=r&st=2023-07-04T15:19:38Z&se=2023-07-06T23:19:38Z&spr=https&sv=2022-11-02&sr=b&sig=beK2pXlTRKEEPSEQ31sZjkpc%2FPtQU1vpDLUN4gvX2xQ%3D"
    down_json = "https://cvlogger.blob.core.windows.net/jsonconcat/1687441603.4032989_1687441609.4032989_global.json?se=2023-07-05T20%3A24%3A12Z&sp=r&sv=2021-08-06&sr=b&sig=q0O120LhDaxSl63TIYOCcsKUeZDQ2ANwGV1rZT0bkPU%3D"
'''