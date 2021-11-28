#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import face_recognition
from PIL import Image, ImageDraw
import pickle
from cv2 import cv2
import json


def detect_person_in_video():
    cap = cv2.VideoCapture("My_obrez.mp4")
    count, data = 0, []

    if not os.path.exists("dataset_from_video"):
        os.mkdir("dataset_from_video")

    while True:
        ret, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)
        multiplier = int(fps)

        if ret:
            frame_id = int(round(cap.get(1)))


            cv2.imshow("Video", frame)
            cv2.resizeWindow("Video", 900, 900)
            k = cv2.waitKey(20)

            if frame_id % multiplier == 0:
                cv2.imwrite(f"dataset_from_video/{count}.jpg", frame)

                people_face_img = face_recognition.load_image_file(f"dataset_from_video/{count}.jpg")
                people_face_location = face_recognition.face_locations(people_face_img)

                if people_face_location:
                    top, right, bottom, left = people_face_location[0]

                    face_img = people_face_img[top:bottom, left:right]

                    pil_img = Image.fromarray(face_img)
                    pil_img.save(f"dataset_from_video/faces/{count}_face_img.jpg")
                    os.remove(f"dataset_from_video/{count}.jpg")

                    face_encodings = face_recognition.face_encodings(face_img)[0]

                    data.append({
                        count: face_encodings.tolist()
                    })

                    for i in data[count].values():
                        print(i)
                        # проверить схожи ли данные
                        if face_recognition.compare_faces([i], i):
                            pass

                    with open("data.json", "w", encoding="utf-8") as file:
                        json.dump(data, file, indent=4)
                    count += 1


                elif len(people_face_location) > 1:
                    print("Программа не поддерживает два лица в кадре. Пусть кто-то отойдёт!")
                    os.remove(f"dataset_from_video/{count}.jpg")

                else:
                    os.remove(f"dataset_from_video/{count}.jpg")

            if k == ord("q"):
                print("Q pressed, closing the app")
                break

        else:
            print("[Error] Can't get the frame...")
            break


def main():
    detect_person_in_video()


if __name__ == "__main__":
    main()
