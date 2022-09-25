import cv2
# import numpy as np
from gui_buttons import Buttons

# Initialize buttons
button = Buttons()
button.add_button("Person", 20, 20)
button.add_button("Bottle", 20, 100)
button.add_button("Spoon", 20, 180)
button.add_button("Cell phone", 20, 260)

# OpenCv dnn module
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams( size = (320, 320), scale = 1/255)

# Load class list
classes = []
with open('dnn_model/classes.txt', 'r') as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        classes.append(class_name)
    print(classes)

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

button_person = False

def click_button(event, x, y, flags, param):
    global button_person
    if event == cv2.EVENT_LBUTTONDOWN:
        button.button_click(x,y)


        # polygon = np.array([[(20, 20), (200, 20), (220, 70), (20,70)]])
        #
        # is_inside = cv2.pointPolygonTest(polygon, (x, y), False)
        # if is_inside > 0:
        #     print("We are inside the polygon", x, y)
        #
        #     if button_person == False:
        #         button_person = True
        #     else:
        #         button_person = False
        #     print("Button person: ", button_person)

# Create Window
cv2.namedWindow("frame")
cv2.setMouseCallback("frame", click_button)

while True:
    # Get the frame
    ret, frame = cap.read()
    active_buttons = button.active_buttons_list()
    print(active_buttons)

    # Detect the objects
    (class_ids, scores, bboxes) = model.detect(frame)

    for class_id, score, bbox in zip (class_ids, scores, bboxes):
        (x, y, w, h) = bbox
        # print(x, y, w, h)

        class_name = classes[class_id]
        # if class_name == "person" and button_person == True:
        if class_name in active_buttons:
            cv2.putText(frame,class_name, (x, y-10), cv2.FONT_HERSHEY_PLAIN, 2, (200, 0, 50), 2)
            cv2.rectangle(frame,(x,y), (x+w, y+h), (200,0,50), 3)

    # Create the Button
    # cv2.rectangle(frame, (20,20), (220,70), (0,0,200), -1)
    # polygon = np.array([[(20,20), (220,20), (220,70), (20,70)]])
    # cv2.fillPoly(frame, polygon, (0,0,200))
    # cv2.putText(frame, "Person", (30, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)


    # print('class_ids: ', class_ids)
    # print("scores: ", scores)
    # print("bboxes: ", bboxes)

    # Display Button
    button.display_buttons(frame)

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()