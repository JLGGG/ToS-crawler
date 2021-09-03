from flask import Blueprint
from flask import Flask, render_template
from .preprocess_text import *
import pandas as pd

bp = Blueprint('main', __name__, url_prefix='/')

df = pd.read_csv("C:/Users/USER-PC/Desktop/MasterThesis/Web/ToS_test_data.csv", error_bad_lines=False)
df_pp = pd.read_csv("C:/Users/USER-PC/Desktop/MasterThesis/Web/PP_test_data.csv", error_bad_lines=False)

@bp.route('/')
def index():
    return render_template("index.html")

@bp.route('/sign_up')
def sign_up():
    return render_template("sign_up.html")

@bp.route('/tos_and_pp', methods=("POST", "GET"))
def show_tos_pp():
    for index, row in df.iterrows():
        prob_result = predict_sentence_threshold4(convert_text_to_bert_input(row['English']))
        row['Percent'] = prob_result
        df.iloc[index] = row

    for index, row in df_pp.iterrows():
        prob_result = predict_sentence_threshold4(convert_text_to_bert_input(row['English']))
        row['Percent'] = prob_result
        df_pp.iloc[index] = row

    return render_template('tos_pp_first.html', \
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

    return render_template('tos_pp_threshold3.html', \
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

    return render_template('tos_pp_threshold4.html', \
            probs_tos=df.Percent.values.tolist(), row_data_tos=df.Korean.values.tolist(),\
            enter_flag_tos=df.Tab.values.tolist(), title_flag_tos=df.Title.values.tolist(),\
            probs_pp=df_pp.Percent.values.tolist(), row_data_pp=df_pp.Korean.values.tolist(),\
            enter_flag_pp=df_pp.Tab.values.tolist(), title_flag_pp=df_pp.Title.values.tolist(), zip=zip, enumerate=enumerate)


