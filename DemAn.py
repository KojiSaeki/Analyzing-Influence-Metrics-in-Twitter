import json
import networkx as nx
import operator
import scipy
import sklearn

#Functions---------------------------------------------------------
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

        if(t==25000):
            break
        else:
            t=t+1
G = nx.Graph()
followers = {}
hashtags = {}
text = {}
for i in range(0,len(data)):
    print str(data[i]['user']['id'])+":",
    G.add_node(data[i]['user']['id'])               #adding the User1
    followers[data[i]['user']['id']]=data[i]['user']['followers_count']
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
        print k['id'],
        G.add_node(k['id'])                         #adding the Users that User1 mentions
        G.add_edge(data[i]['user']['id'],k['id'])   #adding edge between the 2 users


    print ""


#print data[0]['entities']['user_mentions'][0]['id']

print G.nodes()

#----------------------------------------------------------------Metrics on Graph G

centrality = nx.degree_centrality(G)
print "Centrality ok"
sorted_cen = sorted(centrality.items(), key=operator.itemgetter(1),reverse = True)
print "Centrality Sorted ok"
betweeness = nx.betweenness_centrality(G,50)
print "betweeness ok"
sorted_bet = sorted(betweeness.items(), key=operator.itemgetter(1),reverse = True)
print "Betweeness Sorted ok"
pagerank = nx.pagerank(G)
print "Pagerank ok"
sorted_pag = sorted(pagerank.items(), key=operator.itemgetter(1),reverse = True)
print "Pagerank Sorted ok"

sorted_fol = sorted(followers.items(), key=operator.itemgetter(1),reverse = True)

print str(len(followers))+" "+str(len(centrality))+" "+str(len(betweeness))+" "+str(len(pagerank))

print sorted_fol

#Kendall Tau----------------------------------------
print "Betweeness x Pagerank: "+str(Kendal_tau(betweeness,pagerank))
print "Betweeness x Centrality: "+str(Kendal_tau(betweeness,centrality))
print "Centrality x Pagerank: "+str(Kendal_tau(centrality,pagerank))
print "Followers x Pagerank: "+str(Kendal_tau(followers,pagerank))
print "Followers x Centrality: "+str(Kendal_tau(followers,centrality))
print "Betweeness x Followers: "+str(Kendal_tau(betweeness,followers))
print  sorted_fol
print  hashtags
print len(hashtags)
print len(text)

j=0
for i in range(0,30):
    if sorted_pag[i][0] in text:
        print str(i)+": ",
        print text[sorted_pag[i][0]]
        if sorted_pag[i][0] in hashtags:
            print "Hashtags: "+str(hashtags[sorted_pag[i][0]])
        print "Sorted "+str(sorted_pag[i][0])
        if j==4:
            break;
        else:
            j=j+1
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

print hashtags



#followers[i]

#---------------------functions






