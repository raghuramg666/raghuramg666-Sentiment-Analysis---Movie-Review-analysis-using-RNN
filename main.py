##importing all the libraries
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import load_model

# Load the IMDB dataset word index
word_index=imdb.get_word_index()
reverse_word_index={value:key for key,value in word_index.items()}
from tensorflow.keras.models import load_model

# Define a custom function to ignore 'time_major'
def simple_rnn_custom(**kwargs):
    kwargs.pop('time_major', None)  # Remove 'time_major' if it exists
    return tf.keras.layers.SimpleRNN(**kwargs)

model = load_model('simple_rnn_imdb.h5', custom_objects={'SimpleRNN': simple_rnn_custom}, compile=False)


#Load the pre-traiend model with ReLU activation

###Helper functions to decode the review
def decode_review(encoded_review):
    return ' '.join([reverse_word_index.get(i-3,'?') for i in encoded_review])
##Function to preprocess user input
def preprocess_text(text):
    words=text.lower().split()
    encoded_review=[word_index.get(word,2)+3 for word in words]
    padded_review=sequence.pad_sequences([encoded_review],maxlen=500)
    return padded_review





##create streamlit app
import streamlit as st
st.title('Movie Review - Sentiment Analysis')
st.write('Enter a movie review to classify it as positive or Ngetaive .')

#user input
user_input=st.text_area('Movie Review')

if st.button('Classify'):
    preprocessed_input=preprocess_text(user_input)

    ##Make prediction
    prediction=model.predict(preprocessed_input)
    sentiment='Postivie ' if prediction[0][0]>0.5 else "Negative"

    #Display the result
    st.write(f'Sentiment " {sentiment}')
    st.write(f'Prediction Score: {prediction[0][0]}')
else:
    st.write('please enter a movie review.')


