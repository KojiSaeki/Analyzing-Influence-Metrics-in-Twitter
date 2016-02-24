import json
import networkx as nx
import operator
import math
import scipy
import sklearn

#Functions---------------------------------------------------------
def compute_fol_metric(dic_fol,dic_frien):        #log(followers) - |1- (2*followers)/(followers+following)|
    sc = {}
    score = float(0)
    #print len(dic_fol)
    #print len(dic_frien)
    for user in dic_fol:
        try:
            followers = dic_fol[user]
            friends = dic_frien[user]
            score = math.log(followers)-math.fabs(1 - float(2*followers)/(followers+friends))
            sc[user] = score
        except ValueError:
            score = 0
            sc[user] = score
    return sc





def Kendal_tau(obs1,obs2):
    size = len(obs1)
    Kt = 0
    deno = float(size)*(size-1)/2
    disco = 0
    conco = 0


    for i in obs1:
        for j in obs1:
            if obs1[i]==obs1[j]:
                break
            else:
                try:

                    if (obs1[i]>obs1[j] and obs2[i]>obs2[j]) or (obs1[i]<obs1[j] and obs2[i]<obs2[j]):
                        conco = conco+1
                    elif (obs1[i]>obs1[j] and obs2[i]<obs2[j]) or (obs1[i]<obs1[j] and obs2[i]>obs2[j]):
                        disco = disco+1
                except KeyError:
                    continue

    Kt = (conco-disco)/deno

    return Kt

def text_compare(user1,user2):

    return 1


def print_hashtags(sorted):
    k=0
    for i in range(0,105):
        if (sorted[i][0] in hashtags) and ( hashtags[sorted[i][0]]):
        # print "!"+str(sorted[i][0])
            k=k+1
            print str(i)+": "+str(sorted[i][0])+" - ",
            for j in hashtags[sorted[i][0]]:
                print j['text'],
            if k==5:
                 break

        else:
             continue
        print ""


    print ""
    return 1

#----------------------------------------------------Reading and constructing Graph

data = []
t = 0
with open('tweets.json.1') as f:
    for line in f:
        data.append(json.loads(line))

        if(t==25000): # Number of users to enter the graph
            break
        else:
            t=t+1
G = nx.Graph()
followers = {}
friends = {}
hashtags = {}
text = {}
for i in range(0,len(data)):
    #print str(data[i]['user']['id'])+":",
    G.add_node(data[i]['user']['id'])               #adding the User1
    followers[data[i]['user']['id']]=data[i]['user']['followers_count']
    friends[data[i]['user']['id']]=data[i]['user']['friends_count']
    try:
        hash = []
        for p in range(0,len(data[i]['entities']['hashtags'])):
            hash.append(data[i]['entities']['hashtags'][p]['text'])
        hashtags[data[i]['user']['id']]=data[i]['entities']['hashtags']
        text[data[i]['user']['id']]=data[i]['text']
    except KeyError :
        continue
    except IndexError:
        continue

    for k in data[i]['entities']['user_mentions']:
        #print k['id'],
        G.add_node(k['id'])                         #adding the Users that User1 mentions
        G.add_edge(data[i]['user']['id'],k['id'])   #adding edge between the 2 users


    print ""


#print data[0]['entities']['user_mentions'][0]['id']

print G.nodes()

#--------------------------------------------------------------------------Metrics on Graph G

centrality = nx.degree_centrality(G)
print "Centrality ok"
sorted_cen = sorted(centrality.items(), key=operator.itemgetter(1),reverse = True) # list Ranking of Degree Centrality
print "Centrality Sorted ok"
betweeness = nx.betweenness_centrality(G,20)
print "betweeness ok"
sorted_bet = sorted(betweeness.items(), key=operator.itemgetter(1),reverse = True) # list Ranking of betweeness
print "Betweeness Sorted ok"
pagerank = nx.pagerank(G)
print "Pagerank ok"
sorted_pag = sorted(pagerank.items(), key=operator.itemgetter(1),reverse = True) # list Ranking of Pagerank
print "Pagerank Sorted ok"

sorted_fol = sorted(followers.items(), key=operator.itemgetter(1),reverse = True) # list Ranking of Followers

new_metric = compute_fol_metric(followers,friends)
sorted_new_metric = sorted(new_metric.items(), key=operator.itemgetter(1),reverse = True) # list Ranking of New Metric
print "New Metric Sorted ok"
print sorted_new_metric
#print str(len(followers))+" "+str(len(centrality))+" "+str(len(betweeness))+" "+str(len(pagerank))

#print sorted_fol

#----------------------------------------------------------------------------------------Kendall Tau
print "Betweeness x Pagerank: "+str(Kendal_tau(betweeness,pagerank))
print "Betweeness x Centrality: "+str(Kendal_tau(betweeness,centrality))
print "Centrality x Pagerank: "+str(Kendal_tau(centrality,pagerank))
print "Followers x Pagerank: "+str(Kendal_tau(followers,pagerank))
print "Followers x Centrality: "+str(Kendal_tau(followers,centrality))
print "Betweeness x Followers: "+str(Kendal_tau(betweeness,followers))

print "Centrality x New Metric: "+str(Kendal_tau(centrality,new_metric))
print "Followers x New Metric: "+str(Kendal_tau(followers,new_metric))
print "Betweeness x New Metric: "+str(Kendal_tau(betweeness,new_metric))
print "Pagerank x New Metric: "+str(Kendal_tau(pagerank,new_metric))
#print  sorted_fol
#print  hashtags
#print len(hashtags)
#print len(text)

#j=0
#for i in range(0,30):
    #if sorted_pag[i][0] in text:
        #print str(i)+": ",
        #print text[sorted_pag[i][0]]
        #if sorted_pag[i][0] in hashtags:
         #   print "Hashtags: "+str(hashtags[sorted_pag[i][0]])
        #print "Sorted "+str(sorted_pag[i][0])
        #if j==4:
         #   break;
        #else:
         #   j=j+1
print "Pagerank"
print_hashtags(sorted_pag)
print ""
print "Centrality"
print_hashtags(sorted_cen)
print ""
print "Betweeness"
print_hashtags(sorted_bet)
print ""
print "Followers"
print_hashtags(sorted_fol)
print ""

#print hashtags



#followers[i]

#---------------------functions






