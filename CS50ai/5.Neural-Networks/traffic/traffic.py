import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

def main():
    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels, NUM_CATEGORIES)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS, validation_split=0.2)

    # Evaluate neural network performance
    model.evaluate(x_test, y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")

def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []

    # Loop over all categories (0 to NUM_CATEGORIES-1)
    for n in range(NUM_CATEGORIES):
        sub_dir = os.path.join(data_dir, str(n))  # To concatenate file-path

        # Loop over all files in each sub-directory
        for filename in os.listdir(sub_dir):
            image_path = os.path.join(sub_dir, filename)  # To get path of image in sub-directory
            image = cv2.imread(image_path)

            if image is not None:
                # Resize the image to desired size
                image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
                images.append(image)
                labels.append(n)
            else:
                print(f"Warning: Unable to load image {image_path}")

    # Convert lists to np-arrays
    images = np.array(images)
    labels = np.array(labels)

    return (images, labels)

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential([
        # Convolution layer with 32 filters using 3x3 kernel
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

        # Pooling layer using 2x2 region
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Hidden layer with 128 units
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),  # To avoid overfitting

        # Output layer
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])

    # Compile the CNN
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model

if __name__ == "__main__":
    main()
