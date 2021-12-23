# master_thesis_code
Terms of Service와 Privacy Policy는 중요한 법적 문서임에도 대부분의 사용자들은 두 문서의 낮은 UX로 인해 두 문서를 읽지 않고 동의 버튼을 누른다. 이러한 확인 없는 동의는 개인정보자기결정권을 침해할 수 있다. 이러한 문제를 극복하기 위해 Terms of Service와 Privacy Policy를 인터넷에서부터 수집하는 과정부터 최종적으로 만들어진 프로그램이 인간에게 얼마나 유의미한지 확인하기 위해 Human-Computer Interaction의 실험 방법인 User-study를 진행했다. 결과적으로 Privacy Highlighting Generator는 사용자의 behavior와 attention을 개선시키는 결과를 확인할 수 있다. 자세한 내용은 논문을 참조해주세요.

## Process
1. Crawling data on the web: 구글 검색엔진에서 Terms of Service와 Privacy Policy를 crawler를 사용해서 crawling 합니다. Crawler code는 DataCollecting에 들어 있습니다.
2. Data Preprocessing: Crawler로 부터 수집한 raw dataset을 전처리하여 crowdsoucing의 입력으로 변환하는 과정입니다. DataProcessing/clear_sentence_**.ipynb를 사용해서 전처리를 합니다.
3. Data Crowdsourcing: Amazon MTurk 후 dataset를 정제하는 postprocessing은 DataProcessing/mturk.ipynb를 사용합니다.
4. Create a language model for text classification: pre-trained BERT를 사용하여 Privacy 문장을 구분해주는 binary classification model을 만듭니다. 모델의 코드는 classification/privacy_classification_bert.ipynb를 사용합니다.
5. Create a test webpage for testing: User-study 시 사용할 test webpage 구현은 Flask 프레임워크를 사용해서 구현합니다. webpage의 코드는 Webpage에 있습니다.

Dataset에는 User-study 시 NLP의 입력으로 사용한 test dataset이 들어있습니다. NLP 훈련 시 사용한 dataset은 이메일로 요청 시 검토한 후 공유해드립니다.
Code used in master thesis. 
