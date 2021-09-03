import tensorflow as tf
import tensorflow_hub as hub
from official.nlp.data import classifier_data_lib
from official.nlp.bert import tokenization
# from keras.models import load_model
 
# load model
model_3 = tf.keras.models.load_model('C:/Users/USER-PC/Desktop/MasterThesis/Classfication/threshold3_model.h5', custom_objects={'KerasLayer':hub.KerasLayer})
model_4 = tf.keras.models.load_model('C:/Users/USER-PC/Desktop/MasterThesis/Classfication/threshold4_model.h5', custom_objects={'KerasLayer':hub.KerasLayer})

def load_bert_model():
    label_list = [0, 1] # Label categories
    max_seq_length = 60 # maximum length of (token) input sequences
    
    model_path = "C:/Users/USER-PC/Downloads/bert_en_uncased_L-12_H-768_A-12_2"
    bert_layer = hub.KerasLayer(model_path, trainable=True)

    vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
    do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
    tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case)

    return label_list, max_seq_length, tokenizer

label_list, max_seq_length, tokenizer = load_bert_model()

def convert_text_to_bert_input(txt):
    sample_example = []
    sample_example.append(txt)
    test_data = tf.data.Dataset.from_tensor_slices((sample_example, [0]*len(sample_example)))
    test_data = (test_data.map(to_feature_map).batch(1))

    return test_data

def predict_sentence_threshold3(t):
    preds = model_3.predict(t)
    # threshold = 0.7
    # result = ['privacy' if pred >=threshold else 'Not Privacy' for pred in preds]
    return preds

def predict_sentence_threshold4(t):
    preds = model_4.predict(t)
    return preds

def to_feature(text, label, label_list=label_list, max_seq_length=max_seq_length, tokenizer=tokenizer):
    example = classifier_data_lib.InputExample(guid=None,
                                             text_a = text.numpy(),
                                             text_b = None,
                                             label = label.numpy())
 
    feature = classifier_data_lib.convert_single_example(0, example, label_list, max_seq_length, tokenizer)

    return (feature.input_ids, feature.input_mask, feature.segment_ids, feature.label_id)

def to_feature_map(text, label):
    input_ids, input_mask, segment_ids, label_id = tf.py_function(to_feature, inp=[text, label], Tout=[tf.int32, tf.int32, tf.int32, tf.int32])
  
    input_ids.set_shape([max_seq_length])
    input_mask.set_shape([max_seq_length])
    segment_ids.set_shape([max_seq_length])
    label_id.set_shape([])

    x = {
        'input_word_ids': input_ids,
        'input_mask': input_mask,
        'input_type_ids': segment_ids
    }

    return (x, label_id)