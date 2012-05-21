
import reddit
import time
import re
from datetime import timedelta
from random import choice

regex = re.compile(r'((?P<hours>\d+?) hours)?((?P<minutes>\d+?) minutes)?((?P<seconds>\d+?) seconds)?')

def parse_time(time_str):
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.iteritems():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)

def tryCommentReply(comment, replyText):
	appends = ['!', '?', '...', '~']
	punc = choice(appends)

	realReplyText = str(replyText) + str(punc)

	try:
		comment.reply(realReplyText)
	except reddit.errors.RateLimitExceeded as RLE:
		stringRep = str(RLE)
		print "Caught RLE:"
		print stringRep
		frontGone = stringRep[44:]
		backGone = frontGone[:-24]
		print backGone
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
	alreadyRepliedFlag = False
	for reply in comment.replies:
		if isMyComment(reply):
			alreadyRepliedFlag = True
	return alreadyRepliedFlag
		

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
