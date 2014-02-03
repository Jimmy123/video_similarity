import numpy
import numpy.linalg
import math
import re
import json



log_v = numpy.vectorize(math.log)


def process_all(videos):
    words = list()
    word_idx = {}
    word_df = {}
    actors = {}
    for video in videos:
        words_in_video = set()
        for word in (video.get('title', '') + ' ' + video.get('description', '')).split():
            try:
                for w in re.split("\\W+", str(word)):
                    if len(w) > 2:
                        w = w.lower()
                        if not w in words_in_video:
                            words_in_video.add(w)
                            word_df[w] = word_df.get(w, 0) + 1
                        if not word_idx.has_key(w):
                            word_idx[w] = len(word_idx)
                            words.append(w)
            except:
                pass
        try:
            for actor in video.get('Actors'):
                if not actor in actors:
                    actors[actor] = len(actors)
        except:
            pass
    tmp = word_df
    word_df = [0.0] * len(word_df)
    for word in tmp.keys():
        word_df[word_idx[word]] = float(tmp[word])
    return (word_idx, word_df, words, actors)


def calc_sim(va, vb, videos, word_idx, word_df, words, actors):

    def build_actors(video):
        ret = [0.0] * len(actors)
        try:
           for actor in video.get('Actors'):
               ret[actors[actor]] = 1.0
        except:
           pass
        return ret

    def build_tf(video):
        total_terms = 0.0
        tf = [0.0] * len(word_idx)
        for word in (video.get('title', '') + ' ' + video.get('description', '')).split():
            try:
                for w in re.split("\\W+", str(word)):
                    if len(w) > 2:
                        w = w.lower()
                        tf[word_idx[w]] += 1
                        total_terms += 1
            except:
                pass
        return tf, total_terms

#Get Show Actors Similarity score
    score_actors = numpy.inner(
            numpy.array(build_actors(va)),
            numpy.array(build_actors(vb)))
#Get Show Name Similarity Score
    try:
        score_name = 1.0 if va['ShowName'] == vb['ShowName'] else 0.0
    except:
        score_name = 0.0
#Get TFIDF score
    tf_a, total_terms_a = build_tf(va)
    tf_b, total_terms_b = build_tf(vb)
    vector_a = numpy.array(tf_a) / total_terms_a * (-log_v(numpy.array(word_df) / float(len(videos))))
    vector_b = numpy.array(tf_b) / total_terms_b * (-log_v(numpy.array(word_df) / float(len(videos))))
    score_tfidf = numpy.inner(vector_a, vector_b) / (numpy.linalg.norm(vector_a) * numpy.linalg.norm(vector_b))
    return 0.6 * score_actors + 0.2 * score_name + 0.2 * score_tfidf
    

if __name__ == '__main__':
    videos = json.load(open("CodeAssignmentDataSet_new.json", "r"))
    word_idx, word_df, words, actors = process_all(videos)
    sim_m = numpy.zeros((len(videos), len(videos)))
    for i in range(len(videos)):
        for j in range(len(videos)):
            sim_m[i][j] = calc_sim(videos[i], videos[j], videos, word_idx, word_df, words, actors)
        sim_m[i][i] = -1.0
    for i in range(len(videos)):
        r = list(sorted(zip(sim_m[i], videos), key=lambda x: -x[0]))
        print videos[i]['title']
        for item in r[:3]:
            print '\t' + item[1]['title']
