import praw
import csv

#Variables for acessing Reddit API
r = praw.Reddit(username = 'XYZ',
password = 'XYZ',
client_id = 'XYZ',
client_secret = 'XYZ',
user_agent = 'XYZ')

#Auxiliary function to go deep in comment tree
def get_replies(comment, level,post,top_level_comment):
    for level_comment in comment:
        # print(("\t"*level) + "-----------------")
        # print(("\t"*level) + "COMMENT AUTHOR: " + str(level_comment.author))
        # print(("\t"*level) + "COMMENT TEXT: " + str(level_comment.body))
        # print(("\t"*level) + "-----------------")
        try:
            if (level_comment.author == 'None' or level_comment.body == '[removed]'):
                pass # Passing over deleted coments
            else:
                level_author_id = r.redditor(level_comment.author).id # Get author ID, Data Privacy Rules
                writer.writerow([post.id, post.title, post.link_flair_text, level_author_id, level_comment.body, level_comment.id, top_level_comment.id,str(level)])
                if len(level_comment.replies) > 0:
                    #Going down in the tree, recursive form
                    get_replies(level_comment.replies, (level+1),post,level_comment)
        except:
            continue

#Fuction to start extraction of data
def extraction(sub_name):
    #Specification of subreddit, number of posts to search, and hot topics (+interation)
    hot_posts = r.subreddit(sub_name).hot(limit=10)
    for post in hot_posts:
        #Looping through subreddit posts
        print("TITLE: " + str(post.title))
        print("CATEGORY: " + str(post.link_flair_text))

        #Get post information by searching through the ID
        submission = r.submission(id=post.id)
        for top_level_comment in submission.comments:
            #Looping through comments
            # print("-----------------")
            # print("COMMENT AUTHOR: " + str(top_level_comment.author))
            # print("COMMENT TEXT: " + str(top_level_comment.body))
            # print("-----------------")
            if(top_level_comment.author == None or top_level_comment.body == '[removed]'):
                pass #Ignoring deleted coments
            else:
                author_id = r.redditor(top_level_comment.author).id
                # print("AUTH ID: " + str(author_id))
                writer.writerow([post.id, post.title, post.link_flair_text, author_id,top_level_comment.body,top_level_comment.id,-1,0])
                if len(top_level_comment.replies) > 0:
                    #Going down the comments tree
                    get_replies(top_level_comment.replies,1,post,top_level_comment)



if __name__ == "__main__":
    with open('reddit_data.csv', 'a', encoding='utf8') as f:
        writer = csv.writer(f, delimiter=';')
        extraction()
