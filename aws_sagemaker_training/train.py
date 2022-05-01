import os
import time

import tensorflow as tf


if __name__ == "__main__":
    print("tf.test.is_gpu_available(): ", tf.test.is_gpu_available())

    print(os.getenv("TESTING_ENV", "NOT FOUND"))

    with open("/opt/ml/input/data/training/input.txt") as f:
        input_data = f.read()
    print("input txt data: " + input_data)

    time.sleep(60) # ADD YOUR TRAINING CODE HERE

    with open("/opt/ml/model/model.txt", "w") as f:
        f.write("your model!")

    print("Training complete")
