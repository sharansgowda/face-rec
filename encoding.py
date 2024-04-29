import face_recognition
import numpy as np
import multiprocessing
import os
import pickle
from pathlib import Path

DEFAULT_FACE_DIR_PATH: str | Path = "./faces"

def encode_face(image_name: str, path_to_faces: str) -> tuple[str, np.ndarray]:
    ''' Gets all the 128 encodings of the face in the image '''
    image_path = os.path.join(path_to_faces, image_name)
    face_image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(face_image)[0]
    return image_name, face_encoding

def get_face_encodings(image_name: str, face_path: Path | str = DEFAULT_FACE_DIR_PATH) -> tuple[str, np.ndarray]:
    """ wrapper function around encode_face() can accept only image_name as arg """
    _, face_encodings = encode_face(image_name, face_path)
    return (image_name, face_encodings)


def encode_faces(self, path_to_faces: str = DEFAULT_FACE_DIR_PATH, encoding_file: str = 'assets/encodings.pkl'):
        ''' Encode the faces and saves them in a binary pickle file '''
        if os.path.exists(encoding_file):
            with open(encoding_file, 'rb') as f:
                self.known_face_encodings, self.known_face_names = pickle.load(f)
            print("Encodings loaded from file.")
            return                              # Exit if encodings found
        else:
            print("No existing encoding file found.")

        # Check for new images
        existing_images = set(os.listdir(path_to_faces))
        encoded_images = set([name + ".pkl" for name in self.known_face_names])
        new_images = existing_images - encoded_images

        if new_images:
            print("New images found. Updating encodings...")

            # Multiprocessing 
            num_processes = multiprocessing.cpu_count()
            pool = multiprocessing.Pool(processes=num_processes)

            results = pool.starmap(self.encode_face, [(image_name, path_to_faces) for image_name in new_images])
            pool.close()
            pool.join()

            for image_name, face_encoding in results:
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(os.path.splitext(image_name)[0])
                print(f"ENCODED: {image_name}")

            with open(encoding_file, 'wb') as f:
                pickle.dump((self.known_face_encodings, self.known_face_names), f)
            print("Encodings updated and saved to file.")
        else:
            print("No new images found.")

