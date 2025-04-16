from time import perf_counter
from faceRecUtils import FaceRecognition

if __name__ == "__main__":
    tic = perf_counter()
    fr = FaceRecognition()
    fr.run_recognition()
    toc = perf_counter()

    elapsed = toc - tic
    print(f"Total Execution Time: {elapsed:.2f} second(s)")
