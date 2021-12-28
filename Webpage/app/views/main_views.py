from flask import Blueprint
from flask import Flask, render_template
from .preprocess_text import *
import pandas as pd
import numpy as np
import random

bp = Blueprint('main', __name__, url_prefix='/')

df = pd.read_csv("C:/Users/USER-PC/Desktop/MasterThesis/Web/ToS_test_data.csv", error_bad_lines=False)
df_pp = pd.read_csv("C:/Users/USER-PC/Desktop/MasterThesis/Web/PP_test_data.csv", error_bad_lines=False)

@bp.route('/')
def index():
    return render_template("index.html")

@bp.route('/sign_up')
def sign_up():
    return render_template("sign_up.html")

@bp.route('/tos_and_pp_control', methods=("POST", "GET"))
def show_tos_pp_control():
    for index, row in df.iterrows():
        # prob_result = predict_sentence_threshold4(convert_text_to_bert_input(row['English']))
        row['Percent'] = 0
        df.iloc[index] = row

    for index, row in df_pp.iterrows():
        # prob_result = predict_sentence_threshold4(convert_text_to_bert_input(row['English']))
        row['Percent'] = 0
        df_pp.iloc[index] = row

    return render_template('tos_pp_control.html', \
            probs_tos=df.Percent.values.tolist(), row_data_tos=df.Korean.values.tolist(),\
            enter_flag_tos=df.Tab.values.tolist(), title_flag_tos=df.Title.values.tolist(),\
            probs_pp=df_pp.Percent.values.tolist(), row_data_pp=df_pp.Korean.values.tolist(),\
            enter_flag_pp=df_pp.Tab.values.tolist(), title_flag_pp=df_pp.Title.values.tolist(), zip=zip, enumerate=enumerate)

@bp.route('/tos_and_pp_test', methods=("POST", "GET"))
def show_tos_pp_test():
    for index, row in df.iterrows():
        prob_result = predict_sentence_threshold4(convert_text_to_bert_input(row['English']))
        row['Percent'] = prob_result
        df.iloc[index] = row

    for index, row in df_pp.iterrows():
        prob_result = predict_sentence_threshold4(convert_text_to_bert_input(row['English']))
        row['Percent'] = prob_result
        df_pp.iloc[index] = row

    return render_template('tos_pp_test.html', \
            probs_tos=df.Percent.values.tolist(), row_data_tos=df.Korean.values.tolist(),\
            enter_flag_tos=df.Tab.values.tolist(), title_flag_tos=df.Title.values.tolist(),\
            probs_pp=df_pp.Percent.values.tolist(), row_data_pp=df_pp.Korean.values.tolist(),\
            enter_flag_pp=df_pp.Tab.values.tolist(), title_flag_pp=df_pp.Title.values.tolist(), zip=zip, enumerate=enumerate)

# Confirm whether highlighting is significant?
@bp.route('/tos_and_pp_random', methods=("POST", "GET"))
def show_tos_pp_random():
    df['Percent'] = 0
    list = []

    # Make a random number about sentence position.
    for i in range(15):
        a = random.randint(0, 111)
        while True:
            if a in list:
                a = random.randint(0, 111)
            else:
                break
        list.append(a)

    for i in range(15):
        # t = df['English'][list[i]] 
        # p = np.squeeze(predict_sentence_threshold4(convert_text_to_bert_input(t))) # Shape (1,1) -> array() using squeeze func.
        # p = np.squeeze(p)[()] # array() -> scalar
        # df.loc[list[i], ['Percent']] = p
        if i <= 1:
            df.loc[list[i], ['Percent']] = 0.9 # red
        elif 2 <= i <= 7:
            df.loc[list[i], ['Percent']] = 0.7 # orange
        else:
            df.loc[list[i], ['Percent']] = 0.5 # yellow

    df_pp['Percent'] = 0
    list = []
    for i in range(92):
        a = random.randint(0, 121)
        while True:
            if a in list:
                a = random.randint(0, 121)
            else:
                break
        list.append(a)

    for i in range(92):
        # t = df_pp['English'][list[i]]
        # p = np.squeeze(predict_sentence_threshold4(convert_text_to_bert_input(t)))
        # p = np.squeeze(p)[()]
        # df_pp.loc[list[i], ['Percent']] = p
        if i <= 47:
            df_pp.loc[list[i], ['Percent']] = 0.9 # red
        elif 48 <= i <= 82:
            df_pp.loc[list[i], ['Percent']] = 0.7 # orange
        else:
            df_pp.loc[list[i], ['Percent']] = 0.5 # yellow

    return render_template('tos_pp_random.html', \
            probs_tos=df.Percent.values.tolist(), row_data_tos=df.Korean.values.tolist(),\
            enter_flag_tos=df.Tab.values.tolist(), title_flag_tos=df.Title.values.tolist(),\
            probs_pp=df_pp.Percent.values.tolist(), row_data_pp=df_pp.Korean.values.tolist(),\
            enter_flag_pp=df_pp.Tab.values.tolist(), title_flag_pp=df_pp.Title.values.tolist(), zip=zip, enumerate=enumerate)

@bp.route('/tos_and_pp_check_test', methods=("POST", "GET"))
def show_tos_pp_check_test():
    for index, row in df.iterrows():
        prob_result = predict_sentence_threshold4(convert_text_to_bert_input(row['English']))
        row['Percent'] = prob_result
        df.iloc[index] = row

    for index, row in df_pp.iterrows():
        prob_result = predict_sentence_threshold4(convert_text_to_bert_input(row['English']))
        row['Percent'] = prob_result
        df_pp.iloc[index] = row

    return render_template('tos_pp_check_test.html', \
            probs_tos=df.Percent.values.tolist(), row_data_tos=df.Korean.values.tolist(),\
            enter_flag_tos=df.Tab.values.tolist(), title_flag_tos=df.Title.values.tolist(),\
            probs_pp=df_pp.Percent.values.tolist(), row_data_pp=df_pp.Korean.values.tolist(),\
            enter_flag_pp=df_pp.Tab.values.tolist(), title_flag_pp=df_pp.Title.values.tolist(), zip=zip, enumerate=enumerate)

# Confirm whether highlighting is significant?
@bp.route('/tos_and_pp_check_random', methods=("POST", "GET"))
def show_tos_pp_check_random():
    df['Percent'] = 0
    list = []

    # Make a random number about sentence position.
    for i in range(15):
        a = random.randint(0, 111)
        while True:
            if a in list:
                a = random.randint(0, 111)
            else:
                break
        list.append(a)

    for i in range(15):
        # t = df['English'][list[i]] 
        # p = np.squeeze(predict_sentence_threshold4(convert_text_to_bert_input(t))) # Shape (1,1) -> array() using squeeze func.
        # p = np.squeeze(p)[()] # array() -> scalar
        # df.loc[list[i], ['Percent']] = p
        if i <= 1:
            df.loc[list[i], ['Percent']] = 0.9 # red
        elif 2 <= i <= 7:
            df.loc[list[i], ['Percent']] = 0.7 # orange
        else:
            df.loc[list[i], ['Percent']] = 0.5 # yellow

    df_pp['Percent'] = 0
    list = []
    for i in range(92):
        a = random.randint(0, 121)
        while True:
            if a in list:
                a = random.randint(0, 121)
            else:
                break
        list.append(a)

    for i in range(92):
        # t = df_pp['English'][list[i]]
        # p = np.squeeze(predict_sentence_threshold4(convert_text_to_bert_input(t)))
        # p = np.squeeze(p)[()]
        # df_pp.loc[list[i], ['Percent']] = p
        if i <= 47:
            df_pp.loc[list[i], ['Percent']] = 0.9 # red
        elif 48 <= i <= 82:
            df_pp.loc[list[i], ['Percent']] = 0.7 # orange
        else:
            df_pp.loc[list[i], ['Percent']] = 0.5 # yellow

    return render_template('tos_pp_check_random.html', \
            probs_tos=df.Percent.values.tolist(), row_data_tos=df.Korean.values.tolist(),\
            enter_flag_tos=df.Tab.values.tolist(), title_flag_tos=df.Title.values.tolist(),\
            probs_pp=df_pp.Percent.values.tolist(), row_data_pp=df_pp.Korean.values.tolist(),\
            enter_flag_pp=df_pp.Tab.values.tolist(), title_flag_pp=df_pp.Title.values.tolist(), zip=zip, enumerate=enumerate)

@bp.route('/tos_and_pp_threshold3', methods=("POST", "GET"))
def show_tos_pp_3():
    for index, row in df.iterrows():
        prob_result = predict_sentence_threshold3(convert_text_to_bert_input(row['English']))
        row['Percent'] = prob_result
        df.iloc[index] = row

    for index, row in df_pp.iterrows():
        prob_result = predict_sentence_threshold3(convert_text_to_bert_input(row['English']))
        row['Percent'] = prob_result
        df_pp.iloc[index] = row

    return render_template('tos_pp_prestudy3.html', \
            probs_tos=df.Percent.values.tolist(), row_data_tos=df.Korean.values.tolist(),\
            enter_flag_tos=df.Tab.values.tolist(), title_flag_tos=df.Title.values.tolist(),\
            probs_pp=df_pp.Percent.values.tolist(), row_data_pp=df_pp.Korean.values.tolist(),\
            enter_flag_pp=df_pp.Tab.values.tolist(), title_flag_pp=df_pp.Title.values.tolist(), zip=zip, enumerate=enumerate)

@bp.route('/tos_and_pp_threshold4', methods=("POST", "GET"))
def show_tos_pp_4():
    for index, row in df.iterrows():
        prob_result = predict_sentence_threshold4(convert_text_to_bert_input(row['English']))
        row['Percent'] = prob_result
        df.iloc[index] = row

    for index, row in df_pp.iterrows():
        prob_result = predict_sentence_threshold4(convert_text_to_bert_input(row['English']))
        row['Percent'] = prob_result
        df_pp.iloc[index] = row

    return render_template('tos_pp_prestudy4.html', \
            probs_tos=df.Percent.values.tolist(), row_data_tos=df.Korean.values.tolist(),\
            enter_flag_tos=df.Tab.values.tolist(), title_flag_tos=df.Title.values.tolist(),\
            probs_pp=df_pp.Percent.values.tolist(), row_data_pp=df_pp.Korean.values.tolist(),\
            enter_flag_pp=df_pp.Tab.values.tolist(), title_flag_pp=df_pp.Title.values.tolist(), zip=zip, enumerate=enumerate)


