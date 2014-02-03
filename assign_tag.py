import videoTagFetch
import json

def work(txt):

    def f(word):
        while not word[-1].isalnum():
            word = word[:-1]
        return word

    ret = list()

    words = txt.split()
    i = 0
    while i < len(words):
        try:
            word = f(str(words[i]))
            gram = list()
            j = i
            while word[0].isupper():
                gram.append(word)
                j += 1
                if j >= len(words):
                    break
                try:
                    word = f(str(words[j]))
                except:
                    break
            if len(gram) > 0:
                ret.append(' '.join(gram))
            i = j + 1
        except:
           i += 1
    return ret


def unique_list(l):
    s = set()
    ret = []
    for item in l:
        if not item in s:
            s.add(item)
            ret.append(item)
    return ret



if __name__ == '__main__':
    videos = json.load(open("CodeAssignmentDataSet.json", "r"))

    for video in videos:
        candidates = list()
        candidates += work(video['title'])      # extract keywords from title of each video
        candidates += work(video['description'])	# extract keywords from description of each video
        candidates = unique_list(candidates)	# delete the repeated keywords and make sure every keywords is unique 
        showName, showGenre, showType, actors = None, None, None, list()
        for candidate in candidates:
            words = candidate.split()
            found = False
			# for each keywords, try from the longest keywords to one keyword to fetch the desired tag, 
			# if the desired tag can be found, stop trying keywords with smaller length 
            for l in range(len(words), 1, -1):
                for i in range(0, len(words) - l + 1):
                    s = ' '.join(words[i:i + l])
                    if videoTagFetch.fetchVideo_DBpedia(s):
                        actors.append(s)
                        found = True
                    else:
                        t_showName, t_Genre, t_Type = videoTagFetch.fetchVideo_OMDB(s)
                        if not t_showName is None:
                            showName, showGenre, showType = t_showName, t_Genre, t_Type
                            found = True
                if found:
                    break
        try:
            showName = str(showName)
            for i in range(len(actors)):
                actors[i] = str(actors[i])
            print '%s, %s' % (showName, actors)
            if not showName is None:    # assign the fetched tags to this video
                video['ShowName'] = showName
                video['Genre'] = showGenre
                video['Type'] = showType
                video['Actors'] = actors
        except:
            print
	# save the assign tags to CodeAssignmentDataSet_new.json
    with open('CodeAssignmentDataSet_new.json', 'w') as outfile:
        json.dump(videos, outfile)
