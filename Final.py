
#from google.colab import drive
#drive.mount('/content/drive')
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import ConvLSTM2D, Dense, Flatten
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("/content/Dataset.csv")
#"C:\Users\ADMIN\OneDrive\Desktop\ammonia\Dataset.csv"

# Extract features and labels
features = df.iloc[:, 2:-1].values
labels = df.iloc[:, -1].values

# Normalize features
scaler = MinMaxScaler()
features_norm = scaler.fit_transform(features)

# Define sequence length and other parameters
seq_length = 5
n_features = features.shape[1]
n_channels = 1

# Prepare sequences and labels
X = []
y = []

for i in range(seq_length, len(features_norm)):
    X.append(features_norm[i-seq_length:i, :, np.newaxis])
    y.append(labels[i])

X = np.array(X)
y = np.array(y)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Reshape data according to the model requirements
X_train = X_train.reshape((X_train.shape[0], seq_length, 1, n_features, n_channels))
X_test = X_test.reshape((X_test.shape[0], seq_length, 1, n_features, n_channels))

# Define the model architecture
model = Sequential()
model.add(ConvLSTM2D(filters=64, kernel_size=(1, 3), activation='relu', input_shape=(seq_length, 1, n_features, n_channels), padding='same', return_sequences=True, batch_size=None))
model.add(ConvLSTM2D(filters=64, kernel_size=(1, 3), activation='relu', padding='same', batch_size=None))
model.add(Flatten())
model.add(Dense(units=2, activation='softmax'))
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model and record the history
history = model.fit(X_train, y_train, epochs=10, batch_size=32)

# Plot training accuracy values
plt.plot(history.history['accuracy'], marker='o', linestyle='-')
plt.title('Training Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.grid(True)
plt.show()