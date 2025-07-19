from ultralytics import YOLO
import cv2
import numpy as np
import time

# Function to calculate Euclidean distance between two points (centers of bounding boxes)
def calculate_distance(point1, point2):
    return np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def main():
    # Load YOLOv8 model
    model = YOLO('yolov8n.pt')

    # Load video
    video_path = './test.mp4'
    cap = cv2.VideoCapture(video_path)

    vehicle_positions = {}  # Store positions of tracked vehicles
    vehicle_speeds = {}     # Store speeds of tracked vehicles
    frame_time = time.time()  # Time of the current frame
    moving_objects = set()    # Store moving object IDs
    stationary_objects = set()  # Store stationary object IDs
    movement_threshold = 2  # Define a threshold in pixels to detect movement

    ret = True
    # Read frames
    while ret:
        ret, frame = cap.read()

        if ret:
            # Resize frame to decrease window size
            frame = cv2.resize(frame, (1080, 720))  # Adjust the size as needed

            # Get the time of the current frame
            current_frame_time = time.time()
            time_diff = current_frame_time - frame_time
            frame_time = current_frame_time

            # Detect objects and track them
            results = model.track(frame, persist=True, conf=0.5, iou=0.5)

            moving_objects.clear()  # Clear moving objects for this frame
            stationary_objects.clear()  # Clear stationary objects for this frame

            # Get tracked vehicles from results
            for result in results:
                # Extract bounding boxes and object IDs
                boxes = result.boxes.xywh  # Get bounding boxes in (x_center, y_center, width, height)
                ids = result.boxes.id       # Get IDs of detected objects

                if ids is not None:  # Ensure ids is not None before proceeding
                    for i, box in enumerate(boxes):
                        obj_id = int(ids[i])  # Convert the object ID to integer
                        center_x, center_y, width, height = box

                        # Check if the vehicle was detected in the previous frame
                        if obj_id in vehicle_positions:
                            # Calculate the distance between previous and current position
                            prev_position = vehicle_positions[obj_id]
                            current_position = (center_x, center_y)
                            distance_pixels = calculate_distance(prev_position, current_position)

                            # Check if the vehicle is moving or stationary
                            if distance_pixels > movement_threshold:
                                moving_objects.add(obj_id)  # Mark object as moving
                            else:
                                stationary_objects.add(obj_id)  # Mark object as stationary

                            # Convert pixel distance to real-world distance
                            # Assumption: 1 pixel = 0.05 meters (calibrate based on your camera setup)
                            distance_meters = distance_pixels * 0.05

                            # Calculate speed in meters per second (m/s)
                            if time_diff > 0:
                                speed_mps = distance_meters / time_diff
                                vehicle_speeds[obj_id] = speed_mps

                                # Display speed on the frame
                                cv2.putText(frame, f"ID {obj_id} Speed: {speed_mps:.2f} m/s",
                                            (int(center_x - width/2), int(center_y - height/2 - 10)),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                        # Update the position of the vehicle
                        vehicle_positions[obj_id] = (center_x, center_y)

            # Display the number of moving and stationary objects on the frame
            cv2.putText(frame, f"Moving objects: {len(moving_objects)}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f"Stationary objects: {len(stationary_objects)}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Plot results (bounding boxes, etc.)
            frame_ = results[0].plot()

            # Visualize the frame
            cv2.imshow('frame', frame_)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()