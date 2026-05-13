import cv2
import requests

API_URL = "http://localhost:8000/faces/search/"

cap = cv2.VideoCapture(0)

print("=========================================")
print("🚪 SMART SECURITY DOOR ACTIVE 🚪")
print("Press SPACEBAR to scan face.")
print("Press 'q' to quit.")
print("=========================================")


while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture video. Exiting.")
        break

    cv2.imshow("Smart Door Camera Feed", frame)

    key = cv2.waitKey(1) & 0xFF

    #if spacebar is pressed, take a snapshot and send it to the API for face recognition
    if key == ord(' '): 
        print("\n📸 Snapping photo and checking database...")
        #convert raw frame to JPEG bytes
        _, buffer = cv2.imencode('.jpg', frame)

        #package how FastAPI expects file uploads to be sent
        files = {'file' : ("webcam.jpg",buffer.tobytes(), 'image/jpeg')}

        try:
            response = requests.post(API_URL, files=files)
            if response.status_code == 200:
                data = response.json()
                matches = data.get("matches",[])

                # Check if we have a match and if the distance is close enough
                if matches and matches[0]['distance'] < 1.0:
                    best_match = matches[0]['filename']
                    print(f"✅ Access Granted! Welcome, {best_match}!")
                else:
                    print("❌ Access Denied! No matching face found.")
            else:             
                print(f"Error: Received status code {response.status_code} from API.")
        except requests.exceptions.ConnectionError:
            print("🚨 ERROR: Cannot connect to server. Is Docker running?")
    
    #if 'q' is pressed, exit the loop and close the application
    elif key == ord('q'):
        print("Exiting Smart Door application. Goodbye!")
        break

cap.release()
cv2.destroyAllWindows()











