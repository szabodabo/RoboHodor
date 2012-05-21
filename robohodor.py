
import reddit
import time
from random import choice

def tryCommentReply(comment, replyText):
	appends = ['!', '?', '...', '']
	punc = choice(appends)

	realReplyText = str(replyText) + str(punc)

	try:
		comment.reply(realReplyText)
	except reddit.errors.RateLimitExceeded as RLE:
		exit()
	time.sleep(2)

def trollCommentThread(comment):
	#print '  ' + str(comment.body)
	if shouldReply(comment):
		print '    REPLYING'
		tryCommentReply(comment, 'HODOR')			
	else:
		pass
	
	#for reply in comment.replies:
	#	trollCommentThread(reply)
	trollCollection(comment.replies)

def isMyComment(comment):
	if str(comment.author) == 'ROBOHODOR':
		return True
	else:
		return False

def alreadyReplied(comment):
	return checkRepliesForMyReply(comment.replies)		

def checkRepliesForMyReply(someReplies):
	for reply in someReplies:
		if isinstance(reply, reddit.objects.MoreComments):
			moar = reply.comments()
			return checkRepliesForMyReply(moar)
		if isMyComment(reply):
			return True
	return False

def shouldReply(comment):
	#Reply if a comment contains HODOR and I haven't already replied to it
	commentText = comment.body.lower()
	if commentText.find('hodor') is not -1:
		#This is a hodor comment,
		print '  **** ' + str(commentText)

		if isMyComment(comment):
			#It's my own comment
			return False
		else:
			#Someone else wrote this comment
			comment.upvote()
			#Have I already replied?
			if alreadyReplied(comment):
				return False
			else:
				return True
	else:
		return False

def trollCollection(commentCollection):
	for comment in commentCollection:
		if isinstance(comment, reddit.objects.MoreComments):
			try:
				moar = comment.comments()
				trollCollection(moar)
			except KeyError:
				continue
		else:
			trollCommentThread(comment)

api = reddit.Reddit(user_agent='ROBOHODOR')

api.login('ROBOHODOR', 'hodorhodor')

topposts = list(api.get_subreddit('gameofthrones').get_top(50))

for submission in topposts:
	title = submission.title.lower()
	print str(title)
	trollCollection(submission.comments)
