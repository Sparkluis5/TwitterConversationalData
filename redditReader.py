import pandas as pd

#read csv and transformation to dataframe
def read_data():
    data = pd.read_csv('reddit_data.csv', encoding='utf-8', sep=';',header=None)
    data = data.rename(columns={0: 'post_id', 1: 'post_title', 2: 'post_category', 3: 'author_id', 4: 'comment_text', 5: 'comment_id',
                                6: 'reply_comment_id', 7: 'comment_level'})
    return data

#Junction of all interactions between users, joining through comment_id and reply_comment_id values
def create_conversations(dataframe):
    conversation_list = []
    for index, row in dataframe.iterrows():
        if(row['reply_comment_id'] == '-1'):
            conversation_list.append(row['comment_text'])
            response_list = []
            for aux_index, aux_row in dataframe.iterrows():
                if(aux_row['reply_comment_id'] == row['comment_id']):
                    response_list.append(aux_row['comment_text'])
            print(conversation_list)
            print(response_list)
            conversation_list.append(response_list)
    return conversation_list


def create_paired_interaction(dataframe):
    paired_conversation = []
    for index, row in dataframe.iterrows():
        for aux_index, aux_row in dataframe.iterrows():
            if (aux_row['reply_comment_id'] == row['comment_id']):
                paired_conversation.append([row['comment_text'],aux_row['comment_text'],row['post_category']])
    return paired_conversation

if __name__ == "__main__":
    data = read_data()
    print(create_paired_interaction(data))