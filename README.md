# 🎨 Real-Time HSV Color Detection Using Laptop Camera in Google Colab

This project allows you to detect colors in **real-time** using your **laptop's webcam** in a Google Colab environment. It uses the **HSV color system** to provide more robust color classification than standard RGB, and it allows the user to verify the detected color and automatically calculate accuracy.

## 📌 Features

- 🎥 Captures webcam frames using JavaScript in Google Colab
- 🧠 Detects color based on HSV values at the center of the image
- 🔤 Displays color name, HSV values, and allows user input for accuracy checking
- 💾 Saves each detected frame with annotation
- 📥 Automatically downloads the result image to your local machine
- 🧪 Calculates and prints detection accuracy based on user feedback

## 🚀 Technologies Used

- Python
- OpenCV (`cv2`)
- NumPy
- Google Colab webcam integration via JavaScript
- HSV (Hue, Saturation, Value) color model

## 🛠️ Setup Instructions

1. **Open Google Colab**: Upload or open the script in Google Colab.
2. **Run All Cells**: Execute the script. It will automatically access the webcam using your browser.
3. **Capture**: Press the **"Capture"** button that appears below the webcam preview.
4. **Color Detection**: The program will detect the HSV color at the center of the captured image.
5. **Feedback**: You'll be prompted to enter the expected color name.
6. **Accuracy Calculation**: The system compares your input with the detected result and prints accuracy.
7. **Image Saving**: Each image is saved and automatically downloaded to your local machine.

## 🎯 Supported Color Names

This project uses a simple HSV rule-based mapping for the following colors:

- `Red`
- `Orange`
- `Yellow`
- `Green`
- `Cyan`
- `Blue`
- `Magenta`
- `Black`
- `White`
- `Gray`

## 📂 Output

- Saved images are named in the format: `ColorName_YYYYMMDD_HHMMSS.jpg`
- Images include:
  - Detected color name
  - HSV values
  - A dot marking the center pixel
- Automatically downloaded to your local **Downloads** folder.

## ⚠️ Notes & Limitations

- **This code is optimized for Google Colab only.** Local usage (e.g., with OpenCV live webcam) is not enabled in this version.
- Color detection uses **simple HSV thresholds**, so edge cases might return incorrect names.
- Lighting conditions can affect the accuracy of detection.
- Some color shades might not be recognized properly (e.g., pastel or blended tones).

## 📌 To-Do (Optional Enhancements)

- Add a full HSV range-based dataset for better accuracy.
- Extend support for continuous video streaming and pixel selection.
- Build a GUI version for local desktop use (e.g., using `tkinter` or `PyQt`).

## 👤 Author

- Developed by **Mostafa** with help from **Puma (ChatGPT by OpenAI)** 🐾

## 📜 License

This project is open-source and available for educational use.

---

**Enjoy building your smart color detector! **
