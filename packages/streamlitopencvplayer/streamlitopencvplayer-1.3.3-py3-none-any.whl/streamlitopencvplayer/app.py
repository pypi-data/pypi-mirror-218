import time
import urllib.request,json

import cv2
import streamlit as st

# Initiate all session states used
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
if 'cap' not in st.session_state:
    st.session_state['cap'] = None
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


# Function to display video in the Streamlit app

def display_video(video_path, json_file):
    # Open the video file
    
    st.session_state['cap'] = cv2.VideoCapture(video_path)
    fps = st.session_state['cap'].get(cv2.CAP_PROP_FPS)
    # Opening JSON file and returns JSON object as a dictionnary
    if json_file is not None:
        response = urllib.request.urlopen(json_file)
        fileReader = json.loads(response.read())
        list_ts = []
        list_data = []

        for alert in fileReader["alerts"]:
            list_ts.append(alert["timestamp"])
            list_data.append(alert["data"])
        
        st.session_state['alerts_list'] = list_ts
        #print(list_ts)
        #print(st.session_state['name_vid_sel'])
        alerts = []
        data = []

        for x in range(len(list_ts)):
                time_alert = float(list_ts[x])-float(
                    st.session_state['name_vid_sel'].partition('_')[0])
                alerts.append(int((time_alert)*fps))
                
                data.append(list_data[x])
    i = 0

    draw_detections = st.checkbox("Draw detections",value=True)
    resume = False
    column1, column2, column3 = st.columns([1, 2, 1])
    with column1:
        # zone to display images
        stframe = st.empty()
    with column3:
        # Alerts
        st.subheader('Alerts :')
        num_buttons = len(alerts)

        button_values = {f'{i}': 0 for i in range(num_buttons)}

        for button_label, button_value in button_values.items():
            if st.button(str('Alert ')+button_label):
                button_values = {label: 1 if label == button_label else 0 for label in button_values}

        for button_label, button_value in button_values.items():
            if button_value == 1:
                #print(alerts[int(button_label)])
                st.session_state['counter'] = alerts[int(button_label)]
                resume = True

    # Buttons and zone of display
    col1, col2, col3, col4, col5,col6,col7 = st.columns(7, gap="small")
    with col1:

        container_2 = st.empty()
        pause = container_2.button('⏸')

    with col2:

        plus = st.button("➕")
    with col4:

        replay = st.button("↻")
    with col3:

        minus = st.button("➖")
    with col5:
        st.write('')


    if replay:
        st.session_state['counter'] = 0
        st.session_state['frames'] = []
        resume = False


        # get all the frames from video when the list is empty
    if not st.session_state['frames']:
        while True:
            successs, frames = st.session_state['cap'].read()
            if successs:
                frames = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)
                st.session_state['frames'].append(frames)
            else:
                break
        st.session_state['cap'].release()
    # back to the first frame if the video is finished
    if st.session_state['counter'] == len(st.session_state['frames']):
        st.session_state['counter'] = 0
    #print(len(data))
    stframe.image(st.session_state['frames']
                  [st.session_state['counter']], caption='', width=450)
    if not resume:
        while st.session_state['counter'] < len(st.session_state['frames']):         
                for i in range(len(data)):
                    if draw_detections:
                        if st.session_state['counter'] == int(alerts[i]):
                            # draw all detections on the frame
                            for j in range(len(data[i])):
                                output = cv2.rectangle(st.session_state['frames'][st.session_state['counter']], (data[i][j][0][0], data[i][j][0][1]), (
                                    data[i][j][0][2], data[i][j][0][3]), color=(128, 0, 0), thickness=2)
                                output = cv2.putText(
                                    st.session_state['frames'][st.session_state['counter']], data[i][j][3], (data[i][j][0][0], data[i][j][0][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                            # update image zone with detections
                            stframe.image(output, caption='', width=500)
                            time.sleep(0.05)
                            # the detection is drawn, to the next one
                            st.session_state['counter'] += 1

                stframe.image(
                    st.session_state['frames'][st.session_state['counter']], caption='', width=500)
                time.sleep(0.05)
                st.session_state['counter'] += 1
                    

                if pause:
                    resume = True
                    break
                if plus:
                    resume = True
                    break
                if minus:
                    st.session_state['counter'] = st.session_state['counter']-2           
                    resume = True
                    break

                    # back to the first frame if the video is finished
                if st.session_state['counter'] == len(st.session_state['frames']):
                    st.session_state['counter'] = 0
                    resume = True
                    break


    if resume:
        container_2.empty()
        pause = container_2.button('▶')
        resume = False

def main():


    video_path = "https://cvlogger.blob.core.windows.net/jsonconcat/1687441603.4032989_1687441609.4032989.webm?se=2023-07-11T11%3A34%3A13Z&sp=r&sv=2021-08-06&sr=b&sig=GW3M0UHASHtfWJ9wbHV5v7oDbreSv5F6ApGIRW6Ypz8%3D"
    down_json = "https://cvlogger.blob.core.windows.net/jsonconcat/1687441603.4032989_1687441609.4032989_global.json?sv=2021-10-04&st=2023-07-10T11%3A21%3A13Z&se=2023-07-18T11%3A21%3A00Z&sr=b&sp=r&sig=NvwsYEALxwRizyL2eOAsPxQbCV7SpywLVepv6S%2FNUiQ%3D"
    if video_path is not None:
        display_video(video_path, down_json)



if __name__ == "__main__":
    main()

