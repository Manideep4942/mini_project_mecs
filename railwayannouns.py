import os
import mysql.connector
import gtts
from gtts import gTTS
from pydub import AudioSegment
import streamlit as st

# Function to generate skeleton audio files from Indian-Railways_Announcement.mp3
def generateSkeleton(audio_path):
    try:
        audio_file = os.path.join(audio_path, 'Indian-Railways_Announcement.mp3')

        if not os.path.exists(audio_file):
            st.error(f"File '{audio_file}' not found.")
            return

        audio = AudioSegment.from_mp3(audio_file)

        # Define the segments
        segments = {
            1: (0, 1550), 2: (1800, 4150), 5: (8950, 9750), 7: (11100, 11850), 9: (12650, 15850), 11: (16400, 19500),
            12: (36950, 39800), 14: (44200, 44750), 16: (45600, 46150), 18: (47100, 47650), 20: (49000, 52100), 22: (52800, 54800),
            23: (19600, 22350), 26: (27200, 28450), 29: (30800, 33700), 31: (34200, 36900)
        }

        for part_number, (start, finish) in segments.items():
            filename = os.path.join(audio_path, f'Part-{part_number}.mp3')
            audioProcessed = audio[start:finish]
            audioProcessed.export(filename, format="mp3")
            if not os.path.exists(filename):  # Check if file exists after exporting
                st.error(f"File '{filename}' was not created successfully.")
                return

        st.success("Skeleton Generated Successfully!")

    except Exception as e:
        st.error(f"Error generating skeleton: {e}")

# Function to convert text to speech in different languages
def textToSpeech(text, filename, language):
    try:
        mytext = str(text)
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save(filename)
        if not os.path.exists(filename):  # Check if file exists after saving
            st.error(f"File '{filename}' was not created successfully.")
    except Exception as e:
        st.error(f"Error generating text to speech: {e}")

# Function to merge multiple audio files into one
def mergeAudios(audios):
    try:
        combined = AudioSegment.empty()
        for audio in audios:
            if os.path.exists(audio):
                combined += AudioSegment.from_mp3(audio)
            else:
                st.error(f"File '{audio}' does not exist.")
                return None
        return combined
    except Exception as e:
        st.error(f"Error merging audios: {e}")
        return None

# Function to fetch train details from database
def fetchTrainDetails():
    try:
        # Database connection details (modify as per your setup)
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'mani',
            'database': 'railways_db'
        }

        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch all train details from database
        cursor.execute("SELECT Train_No, Train_Name, From_City, To_City, Via_City, Platform_No FROM TrainAnnouncements")
        train_details = cursor.fetchall()

        return train_details

    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Function to cleanup audio files
def cleanupAudioFiles(audio_path):
    try:
        for file in os.listdir(audio_path):
            if file.startswith('Part-') and file.endswith('.mp3'):
                os.remove(os.path.join(audio_path, file))
        st.success("Cleaned up generated audio files successfully.")
    except Exception as e:
        st.error(f"Error cleaning up audio files: {e}")

# Function to generate the final announcement
def generateAnnouncement(selected_train, selected_languages, audio_path):
    try:
        audios = []

        for lang in selected_languages:
            if lang == 'Hindi':
                textToSpeech(selected_train['Train_No'] + "  " + selected_train['Train_Name'], os.path.join(audio_path, 'Part-3.mp3'), 'hi')
                textToSpeech(selected_train['From_City'], os.path.join(audio_path, 'Part-4.mp3'), 'hi')
                textToSpeech(selected_train['Via_City'], os.path.join(audio_path, 'Part-6.mp3'), 'hi')
                textToSpeech(selected_train['To_City'], os.path.join(audio_path, 'Part-8.mp3'), 'hi')
                textToSpeech(selected_train['Platform_No'], os.path.join(audio_path, 'Part-10.mp3'), 'hi')
                audios.extend([os.path.join(audio_path, f"Part-{i}.mp3") for i in range(1, 12)])

            elif lang == 'English':
                textToSpeech(selected_train['Train_No'] + "  " + selected_train['Train_Name'], os.path.join(audio_path, 'Part-13.mp3'), 'en')
                textToSpeech(selected_train['From_City'], os.path.join(audio_path, 'Part-15.mp3'), 'en')
                textToSpeech(selected_train['To_City'], os.path.join(audio_path, 'Part-17.mp3'), 'en')
                textToSpeech(selected_train['Via_City'], os.path.join(audio_path, 'Part-19.mp3'), 'en')
                textToSpeech(selected_train['Platform_No'], os.path.join(audio_path, 'Part-21.mp3'), 'en')
                audios.extend([os.path.join(audio_path, f"Part-{i}.mp3") for i in range(12, 22)])

            elif lang == 'Gujarati':
                textToSpeech(selected_train['Train_No'] + "  " + selected_train['Train_Name'], os.path.join(audio_path, 'Part-24.mp3'), 'gu')
                textToSpeech(selected_train['From_City'], os.path.join(audio_path, 'Part-25.mp3'), 'gu')
                textToSpeech(selected_train['Via_City'], os.path.join(audio_path, 'Part-27.mp3'), 'gu')
                textToSpeech(selected_train['To_City'], os.path.join(audio_path, 'Part-28.mp3'), 'gu')
                textToSpeech(selected_train['Platform_No'], os.path.join(audio_path, 'Part-30.mp3'), 'gu')
                audios.extend([os.path.join(audio_path, f"Part-{i}.mp3") for i in range(23, 32)])
            

        # Check if all audio files exist before merging
        missing_files = [audio for audio in audios if not os.path.exists(audio)]
        if missing_files:
            st.error(f"Missing audio files: {', '.join(missing_files)}")
            return

        # Merge audios
        announcement = mergeAudios(audios)
        if announcement:
            output_file = os.path.join(audio_path, f"announcement_{selected_train['Train_No']}.mp3")
            announcement.export(output_file, format="mp3")

            # Provide a downloadable link for the final audio file
            with open(output_file, "rb") as file:
                st.download_button(label="Download Announcement", data=file, file_name=f"announcement_{selected_train['Train_No']}.mp3", mime="audio/mp3")

            st.success(f"Announcement audio generated successfully: {output_file}")

            # Cleanup audio files after generating the announcement
            cleanupAudioFiles(audio_path)

    except Exception as e:
        st.error(f"Error generating announcement: {e}")

# Streamlit UI code
def main():
    audio_path = "D:/MINI_PROJECT_MECS/New folder/Indian-Railways-Automated-Announcement-Software-main/Indian-Railways-Automated-Announcement-Software-main"
    
    st.title("Railway Announcement Generator")
    st.markdown("---")

    st.subheader("Select Languages to Generate Audio:")
    selected_languages = st.multiselect("Select Languages:", ["Hindi", "English", "Gujarati"], default=["Hindi", "English"])

    if st.button("Generate Skeleton"):
        generateSkeleton(audio_path)

    st.subheader("Select Train Details:")
    train_details = fetchTrainDetails()

    if train_details:
        train_numbers = [train['Train_No'] for train in train_details]
        selected_train_no = st.selectbox("Train No:", train_numbers)

        selected_train = next((train for train in train_details if train['Train_No'] == selected_train_no), None)

        if selected_train:
            st.write(f"Train Name: {selected_train['Train_Name']}")
            st.write(f"From City: {selected_train['From_City']}")
            st.write(f"To City: {selected_train['To_City']}")
            st.write(f"Via City: {selected_train['Via_City']}")
            st.write(f"Platform No: {selected_train['Platform_No']}")

            if st.button("Generate Announcement"):
                generateAnnouncement(selected_train, selected_languages, audio_path)

if __name__ == "__main__":
    main()
