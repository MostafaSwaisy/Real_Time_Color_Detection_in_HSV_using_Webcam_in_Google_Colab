import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime

# Function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B, csv):
    minimum = float('inf')
    color_name = ""
    
    # Calculate distance from all colors in the CSV and find the closest match
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d < minimum:
            minimum = d
            color_name = csv.loc[i, "Color Name"]
    
    return color_name

# Setup output directory for saving images
def setup_output_dir():
    output_dir = "color_detection_results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

# Function to save the frame with detected color
def save_frame(frame, color_name, output_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{color_name}_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    return filename

# For Google Colab, we need to set up the camera access
def setup_camera_in_colab():
    from google.colab.patches import cv2_imshow
    from IPython.display import display, Javascript
    from google.colab.output import eval_js
    from base64 import b64decode
    
    def take_photo(filename='photo.jpg', quality=0.8):
        js = Javascript('''
            async function takePhoto(quality) {
                const div = document.createElement('div');
                const capture = document.createElement('button');
                capture.textContent = 'Capture';
                div.appendChild(capture);
                
                const video = document.createElement('video');
                video.style.display = 'block';
                const stream = await navigator.mediaDevices.getUserMedia({video: true});
                document.body.appendChild(div);
                div.appendChild(video);
                video.srcObject = stream;
                await video.play();
                
                // Resize the output to fit the video element.
                google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);
                
                // Wait for capture button click
                await new Promise((resolve) => {
                    capture.onclick = resolve;
                });
                
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);
                stream.getVideoTracks()[0].stop();
                div.remove();
                return canvas.toDataURL('image/jpeg', quality);
            }
            ''')
        display(js)
        data = eval_js('takePhoto({})'.format(quality))
        binary = b64decode(data.split(',')[1])
        with open(filename, 'wb') as f:
            f.write(binary)
        return filename

    return take_photo

# Main function for real-time color detection
def main():
    # Check if we're in Colab
    try:
        import google.colab
        in_colab = True
    except:
        in_colab = False
    
    # Load the colors dataset
    # Create a simple color dataset if you don't have one
    color_data = {
        'Color Name': ['Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Purple', 'Pink', 'Brown', 'Black', 'White', 
                      'Gray', 'Cyan', 'Magenta', 'Lime', 'Teal', 'Navy', 'Maroon', 'Olive', 'Silver', 'Gold'],
        'R': [255, 0, 0, 255, 255, 128, 255, 165, 0, 255, 128, 0, 255, 0, 0, 0, 128, 128, 192, 255],
        'G': [0, 255, 0, 255, 165, 0, 192, 42, 0, 255, 128, 255, 0, 255, 128, 0, 0, 128, 192, 215],
        'B': [0, 0, 255, 0, 0, 128, 203, 42, 0, 255, 128, 255, 255, 0, 128, 128, 0, 0, 192, 0]
    }
    
    # Create DataFrame
    colors = pd.DataFrame(color_data)
    
    # For a more comprehensive dataset, download from:
    # URL = "https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv"
    # colors = pd.read_csv(URL)
    
    # Set up output directory
    output_dir = setup_output_dir()
    
    if in_colab:
        # For Google Colab
        take_photo = setup_camera_in_colab()
        
        while True:
            # Take a photo
            filename = take_photo()
            
            # Read the captured image
            img = cv2.imread(filename)
            
            # Get the center pixel
            height, width, _ = img.shape
            center_x, center_y = width // 2, height // 2
            
            # Get RGB values of the center pixel
            b, g, r = img[center_y, center_x]
            
            # Get color name
            color_name = get_color_name(r, g, b, colors)
            
            # Create text to display
            text = f"{color_name} (R={r},G={g},B={b})"
            
            # Put text on image
            cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.circle(img, (center_x, center_y), 5, (0, 0, 0), 2)
            
            # Save the frame
            saved_file = save_frame(img, color_name, output_dir)
            print(f"Detected {color_name} and saved to {saved_file}")
            
            # Display the image in Colab
            from google.colab.patches import cv2_imshow
            cv2_imshow(img)
            
            # Ask if the user wants to continue
            user_input = input("Press 'q' to quit or any other key to continue: ")
            if user_input.lower() == 'q':
                break
    else:
        # For local environment
        cap = cv2.VideoCapture(0)
        
        # Check if camera opened successfully
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        
        clicked = False
        
        # Function to handle mouse click
        def mouse_click(event, x, y, flags, param):
            nonlocal clicked
            if event == cv2.EVENT_LBUTTONDOWN:
                clicked = True
        
        cv2.namedWindow('Color Detection')
        cv2.setMouseCallback('Color Detection', mouse_click)
        
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Get the center of the frame
            height, width, _ = frame.shape
            center_x, center_y = width // 2, height // 2
            
            # Get RGB values of the center pixel
            b, g, r = frame[center_y, center_x]
            
            # Get color name
            color_name = get_color_name(r, g, b, colors)
            
            # Create text to display
            text = f"{color_name} (R={r},G={g},B={b})"
            
            # Display the color name on the frame
            cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 0), 2)
            
            # Display the frame
            cv2.imshow('Color Detection', frame)
            
            # Save the frame if clicked
            if clicked:
                saved_file = save_frame(frame, color_name, output_dir)
                print(f"Detected {color_name} and saved to {saved_file}")
                clicked = False
            
            # Break the loop with 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release everything when done
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
