import pandas as pd
from sklearn.feature_extraction import _stop_words
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pickle

joy_words = [
    "happiness",
    "ecstasy",
    "bliss",
    "euphoria",
    "elation",
    "glee",
    "delight",
    "jubilation",
    "merriment",
    "exhilaration",
    "contentment",
    "cheerfulness",
    "vivacity",
    "rapture",
    "triumph",
    "elevation",
    "elation",
    "festivity",
    "enchantment",
    "rejoicing",
    "celebration",
    "hilarity",
    "mirth",
    "exultation",
    "radiance",
    "cheer",
    "paradise",
    "upbeat",
    "hurray",
    "jollity",
    "joviality",
    "thrill",
    "gratification",
    "enjoyment",
    "rhapsody",
    "sunshine",
    "euphoric",
    "blissful",
    "heartwarming",
    "reverie",
    "beaming",
    "felicity",
    "exuberance",
    "buoyancy",
    "rapturous",
    "serenity",
    "festive",
    "gladness",
    "hymn",
    "elated",
    "happy",
    "like",
    "fine",
    "glad",
    "happy",
    "happier"
]

anger_words = [
    "rage",
    "fury",
    "ire",
    "wrath",
    "outrage",
    "resentment",
    "indignation",
    "hostility",
    "hatred",
    "animosity",
    "agitation",
    "annoyance",
    "bitterness",
    "exasperation",
    "fuming",
    "irritation",
    "enmity",
    "frustration",
    "temper",
    "madness",
    "displeasure",
    "vexation",
    "discontent",
    "disgust",
    "provocation",
    "frenzy",
    "fuss",
    "aggravation",
    "aggression",
    "resentful",
    "fume",
    "frown",
    "acerbic",
    "incensed",
    "livid",
    "sullen",
    "infuriated",
    "outraged",
    "incitement",
    "acerbity",
    "vitriol",
    "tempest",
    "anger management",
    "wrathful",
    "enrage",
    "animus",
    "hate",
    "boiling point",
    "fiery",
    "violent",
    "weapon",
    "war",
    "dangerous",
    "dangerously"
]

sadness_words = [
    "sorrow",
    "grief",
    "melancholy",
    "heartache",
    "desolation",
    "teardrops",
    "mourning",
    "lament",
    "loneliness",
    "anguish",
    "despair",
    "dejection",
    "woe",
    "misery",
    "weeping",
    "unhappiness",
    "dismay",
    "disheartened",
    "downcast",
    "depressed",
    "forlorn",
    "regret",
    "bittersweet",
    "brokenhearted",
    "wistful",
    "sullen",
    "blue",
    "somber",
    "pensive",
    "downhearted",
    "mournful",
    "weep",
    "lonesome",
    "despondency",
    "tragedy",
    "deplorable",
    "gloomy",
    "grief-stricken",
    "heartbroken",
    "dolorous",
    "sombre",
    "funereal",
    "morose",
    "crying",
    "sigh",
    "wailing",
    "drowning",
    "hurting",
    "melancholic",
    "sobbing",
    "alone",
    "fool",
    "cry",
    "poor",
    "unforgiven",
    "drunk",
    "drowned",
    "lost",
    "lose",
    "losses",
    "disappointed",
    "mockin",
    "missed",
    "away",
    "cold",
    "die",
    "fall",
    "fell",
    "lonely",
    "sad",
    "sadness"
]

love_words = [
    "passion",
    "affection",
    "devotion",
    "adoration",
    "romance",
    "intimacy",
    "desire",
    "adoration",
    "infatuation",
    "tenderness",
    "warmth",
    "closeness",
    "yearning",
    "fondness",
    "attachment",
    "tenderness",
    "amour",
    "endearment",
    "sweetheart",
    "crush",
    "flame",
    "heartfelt",
    "enchantment",
    "rapture",
    "amorous",
    "passionate",
    "tender",
    "sentiment",
    "yearn",
    "cherish",
    "embrace",
    "caress",
    "intimate",
    "beloved",
    "tantalize",
    "bliss",
    "soulmate",
    "limerence",
    "worship",
    "honeyed",
    "inamorata",
    "intimacy",
    "swoon",
    "woo",
    "paramour",
    "relationship",
    "connection",
    "hold",
    "cuddle",
    "loving",
    "love",
    "loved",
    "heart",
    "kiss",
    "kissing",
    "darling",
    "baby"
]

nostalgia_words = [
    "reminisce",
    "recollection",
    "longing",
    "memories",
    "wistful",
    "sentimental",
    "nostalgic",
    "retrospection",
    "yearning",
    "nostalgia",
    "reminiscence",
    "melancholy",
    "past",
    "memory",
    "reflect",
    "flashback",
    "recall",
    "revive",
    "reverie",
    "recollect",
    "olden days",
    "yesteryears",
    "fondness",
    "timeless",
    "antique",
    "days gone by",
    "ageless",
    "retro",
    "reverie",
    "homesick",
    "longing",
    "looking back",
    "ancient",
    "reflecting",
    "reflective",
    "miss",
    "saudade",
    "bygone",
    "yearn",
    "pining",
    "cherish",
    "yearning",
    "retrospective",
    "sentiment",
    "pastime",
    "heritage",
    "antiquity",
    "bittersweet",
    "haunting",
    "poor",
    "meditation",
    "fade"
]

fear_words = [
    "terror",
    "dread",
    "horror",
    "anxiety",
    "apprehension",
    "panic",
    "alarm",
    "fright",
    "scare",
    "fearfulness",
    "phobia",
    "trepidation",
    "consternation",
    "spooked",
    "shiver",
    "nightmare",
    "tension",
    "dismay",
    "unease",
    "worried",
    "intimidation",
    "jitters",
    "tremor",
    "horrified",
    "paranoia",
    "chill",
    "shudder",
    "haunting",
    "creepy",
    "eerie",
    "creep",
    "foreboding",
    "petrified",
    "dismal",
    "hysteria",
    "apparition",
    "startled",
    "frightened",
    "spooky",
    "ghostly",
    "unseen",
    "worry",
    "dreadful",
    "alarm",
    "ominous",
    "ghastly",
    "ghoulish",
    "threat",
    "shriek",
    "fearful",
    "drowned",
    "dead",
    "attack",
    "attacks",
    "dark",
    "dig",
    "gun",
    "enemy"
]

hope_words = [
    "optimism",
    "faith",
    "confidence",
    "expectation",
    "aspiration",
    "dream",
    "desire",
    "belief",
    "inspiration",
    "encouragement",
    "positivity",
    "anticipation",
    "assurance",
    "ambition",
    "trust",
    "promise",
    "prospect",
    "renewal",
    "providence",
    "potential",
    "reassurance",
    "upliftment",
    "upbeat",
    "resolve",
    "persistence",
    "illumination",
    "brighten",
    "sanguine",
    "idealism",
    "enlightenment",
    "glow",
    "transformation",
    "sanguinity",
    "conviction",
    "reverie",
    "faithful",
    "affirmation",
    "vigor",
    "inspire",
    "promise",
    "prosperity",
    "yearning",
    "optimistic",
    "bright",
    "rejuvenation",
    "cheer",
    "overcome",
    "illuminate",
    "wishes",
    "true", 
    "truth",
    "rapture",
    "sober",
    "all right",
    "dancing",
    "hope",
    "friend",
    "sushine"
]

punctuation = ["'", "?", ".", "!", ","]

df = pd.read_excel("NewSongs.xlsx")
print(df)
df = df.astype(str)
list_dico_feeling = []
for i in range(len(df)):
    song = str(df.loc[i, "lyrics"])
    lyr_song = " ".join(word for word in song.split("||") if word not in punctuation and word not in _stop_words.ENGLISH_STOP_WORDS)
    cpt_joy = 0
    cpt_anger = 0
    cpt_sadness = 0
    cpt_love = 0
    cpt_nostalgia = 0
    cpt_fear = 0
    cpt_hope = 0
    for word in lyr_song.split(' '):
        if word in joy_words:
            cpt_joy += 1
        elif word in anger_words:
            cpt_anger += 1
        elif word in sadness_words:
            cpt_sadness += 1
        elif word in love_words:
            cpt_love +=1
        elif word in nostalgia_words:
            cpt_nostalgia +=1
        elif word in fear_words:
            cpt_fear +=1
        elif word in hope_words:
            cpt_hope +=1
        
    dico_feeling = {
        'Joy' : cpt_joy,
        'Anger': cpt_anger,
        'Sadness' : cpt_sadness,
        'Love' : cpt_love,
        'Nostalgia' : cpt_nostalgia,
        'Fear' : cpt_fear,
        'Hope' : cpt_hope
    }
    list_dico_feeling.append(dico_feeling)

df_feeling = pd.DataFrame(list_dico_feeling)
# print(df_feeling)

pca = PCA(whiten=False)
pca.fit(df_feeling)

# print(pca.explained_variance_)
# print(pca.explained_variance_ratio_)
# print(pca.components_)

eig = pd.DataFrame(
    {
        "Dimension" : ["Dim" + str(x + 1) for x in range(7)], 
        "Variance expliquée" : pca.explained_variance_,
        "% variance expliquée" : np.round(pca.explained_variance_ratio_ * 100),
        "% cum. var. expliquée" : np.round(np.cumsum(pca.explained_variance_ratio_) * 100)
    }
)
#print(eig)

df_pca = pca.transform(df_feeling)

df_pca_df = pd.DataFrame({
    "Dim 1": df_pca[:, 0],
    "Dim 2": df_pca[:, 1],
    "Dim 3": df_pca[:, 2],
    "Dim 4": df_pca[:, 3],
    "Dim 5": df_pca[:, 4],
    "Dim 6": df_pca[:, 5],
    "Dim 7": df_pca[:, 6]
})

# print(df_pca_df.head(5))

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(df_pca_df["Dim 1"], df_pca_df["Dim 2"], df_pca_df["Dim 3"])

# ax.set_xlabel("Dimension 1")
# ax.set_ylabel("Dimension 2")
# ax.set_zlabel("Dimension 3")
# plt.suptitle("Premier espace 3D factoriel")
# plt.show()
df_forClustering = df_pca_df.copy()
kmeans_kwargs = {
"init": "random",
"n_init": 10,
"random_state": 1,
}

sse = []
for k in range(1, 21):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs) 
    kmeans.fit(df_forClustering)
    sse.append(kmeans.inertia_)
# visualize results
plt.plot(range(1, 21), sse)
plt.xticks(range(1, 21))
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
#plt.show()

kmeans = KMeans(n_clusters=5).fit(df_forClustering)

centroids = kmeans.cluster_centers_
# print(centroids)

# plt.scatter(df_pca_df['Dim 1'], df_pca_df['Dim 2'], c=kmeans.labels_.astype(float), s=50, alpha=0.5)
# plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)  # indicate the centroids in red
# plt.show()

df_copy = df_forClustering.copy()
df_copy['Label'] = kmeans.labels_
X_dist = kmeans.transform(df_forClustering)**2
df_copy['dist'] = X_dist.min(axis=1)

# print(kmeans.labels_)

for i in range (0,4):
    points = df_copy.query("Label == @i")  # creates a DataFrame of points - because returning rows where label == i is True
    # print(points.shape)
    bestPoint = points.sort_values(by='dist', ascending=False).head(5)
    # print(bestPoint)

colonne = df_pca_df.columns
fig, axes = plt.subplots(nrows=len(colonne), ncols=len(colonne), figsize=(15, 15))

cpt = 0 
for i in range(len(colonne)):
    for j in range(len(colonne)):
        if i != j:
            axes[i, j].scatter(df_pca_df[colonne[i]], df_pca_df[colonne[j]], c = kmeans.labels_.astype(float), s = 50, alpha = 0.5)
            axes[i, j].scatter(centroids[:, i], centroids[:, j], c='red', s=50)
            axes[i, j].set_xlabel(colonne[i])
            axes[i, j].set_ylabel(colonne[j])
            
        else:
            axes[i, j].axis('off')
        
plt.tight_layout()
# plt.show()



final_df = df.copy()
for i in range(len(df)):
    my_list = [df_copy.loc[i, 'Dim 1'], df_copy.loc[i, 'Dim 2'], df_copy.loc[i, 'Dim 3'], df_copy.loc[i, 'Dim 4'], df_copy.loc[i, 'Dim 5'], df_copy.loc[i, 'Dim 6'], df_copy.loc[i, 'Dim 7']]
    sl = sorted(my_list, key=abs, reverse=True)
    final_df.loc[i,'score1'] = sl[0]
    for col in df_copy.columns:
            if sl[0] == df_copy.loc[i, col]:
                final_df.loc[i,'dim1'] = col
    final_df.loc[i,'score2'] = sl[1]
    for col in df_copy.columns:
            if sl[1] == df_copy.loc[i, col]:
                final_df.loc[i,'dim2'] = col
    final_df.loc[i,'score3'] = sl[2]
    for col in df_copy.columns:
            if sl[2] == df_copy.loc[i, col]:
                final_df.loc[i,'dim3'] = col

for i in range(len(final_df['dim1'])):
    if final_df.loc[i, 'dim1'] == 'Dim 1':
        final_df.loc[i, 'dim1'] = 'Love'
    elif final_df.loc[i, 'dim1'] == 'Dim 2':
        final_df.loc[i, 'dim1'] = 'Sadness'
    elif final_df.loc[i, 'dim1'] == 'Dim 3':
        final_df.loc[i, 'dim1'] = 'Joy'
    elif final_df.loc[i, 'dim1'] == 'Dim 4':
        final_df.loc[i, 'dim1'] = 'Anger'
    elif final_df.loc[i, 'dim1'] == 'Dim 5':
        final_df.loc[i, 'dim1'] = 'Nostalgia'
    elif final_df.loc[i, 'dim1'] == 'Dim 6':
        final_df.loc[i, 'dim1'] = 'Hope'
    elif final_df.loc[i, 'dim1'] == 'Dim 7':
        final_df.loc[i, 'dim1'] = 'Fear'

for i in range(len(final_df['dim2'])):
    if final_df.loc[i, 'dim2'] == 'Dim 1':
        final_df.loc[i, 'dim2'] = 'Love'
    elif final_df.loc[i, 'dim2'] == 'Dim 2':
        final_df.loc[i, 'dim2'] = 'Sadness'
    elif final_df.loc[i, 'dim2'] == 'Dim 3':
        final_df.loc[i, 'dim2'] = 'Joy'
    elif final_df.loc[i, 'dim2'] == 'Dim 4':
        final_df.loc[i, 'dim2'] = 'Anger'
    elif final_df.loc[i, 'dim2'] == 'Dim 5':
        final_df.loc[i, 'dim2'] = 'Nostalgia'
    elif final_df.loc[i, 'dim2'] == 'Dim 6':
        final_df.loc[i, 'dim2'] = 'Hope'
    elif final_df.loc[i, 'dim2'] == 'Dim 7':
        final_df.loc[i, 'dim2'] = 'Fear'
for i in range(len(final_df['dim3'])):
    if final_df.loc[i, 'dim3'] == 'Dim 1':
        final_df.loc[i, 'dim3'] = 'Love'
    elif final_df.loc[i, 'dim3'] == 'Dim 2':
        final_df.loc[i, 'dim3'] = 'Sadness'
    elif final_df.loc[i, 'dim3'] == 'Dim 3':
        final_df.loc[i, 'dim3'] = 'Joy'
    elif final_df.loc[i, 'dim3'] == 'Dim 4':
        final_df.loc[i, 'dim3'] = 'Anger'
    elif final_df.loc[i, 'dim3'] == 'Dim 5':
        final_df.loc[i, 'dim3'] = 'Nostalgia'
    elif final_df.loc[i, 'dim3'] == 'Dim 6':
        final_df.loc[i, 'dim3'] = 'Hope'
    elif final_df.loc[i, 'dim3'] == 'Dim 7':
        final_df.loc[i, 'dim3'] = 'Fear'
# Dim 1 : Love
# Dim 2 : Sadness
# Dim 3 : Joy
# Dim 4 : Anger
# Dim 5 : Nostalgia
# Dim 6 : Hope
# Dim 7 : Fear
print(final_df)



# def get_song(songA, songB, songC = None):
#     if songC == None:
#         if songA == songB:
#             return songA
#         else: 
#             A = final_df.loc[final_df['Name '] == songA]
#             B = final_df.loc[final_df["Name "] == songB]
            
#             avg_dim_1 = (float(A['Score 1']) + float(B['Score 1']))/2
#             avg_dim_2 = (float(A['Score 2']) + float(B['Score 2']))/2
#             avg_dim_3 = (float(A['Score 3']) + float(B['Score 3']))/2
            
#             valeur_proche1 = None
#             valeur_proche2 = None
#             valeur_proche3 = None
#             diff_abs1 = float('inf')
#             diff_abs2 = float('inf')
#             diff_abs3 = float('inf')
            
#             list_score1 = final_df['Score 1'].tolist()
#             list_score2 = final_df['Score 2'].tolist()
#             list_score3 = final_df['Score 3'].tolist()
#             for i in range(len(list_score1)):
#                 val = float(list_score1[i])
#                 diff = abs(avg_dim_1 - float(val))
#                 if diff < diff_abs1:
#                     valeur_proche1 = float(val)
#                     diff_abs1 = diff
#             rmv1 = None
#             for i in range(len(list_score1)):
#                 if list_score1[i] == valeur_proche1:
#                     rmv1 = i
#             del list_score2[rmv1]
#             for i in range(len(list_score2)):
#                 val = float(list_score2[i])
#                 diff = abs(avg_dim_2 - float(i))
#                 if diff < diff_abs2:
#                     valeur_proche2 = float(val)
#                     diff_abs2 = diff
#             rmv2 = None
#             for i in range(len(list_score2)):
#                 if list_score2[i] == valeur_proche2:
#                     rmv2 = i
#             del list_score3[rmv1]
#             del list_score3[rmv2]
#             for i in range(len(list_score3)):
#                 val = float(list_score3[i])
#                 diff = abs(avg_dim_3 - float(i))
#                 if diff < diff_abs3:
#                     valeur_proche3 = float(val)
#                     diff_abs3 = diff
            
#             idx1 = final_df.loc[final_df['Score 1'] == valeur_proche1]
#             idx2 = final_df.loc[final_df['Score 2'] == valeur_proche2]
#             idx3 = final_df.loc[final_df['Score 3'] == valeur_proche3]
           
#             song1 = idx1['Name ']
#             song2 = idx2['Name ']
#             song3 = idx3['Name ']
            
#             song1 = song1.values[0]
#             song2 = song2.values[0]
#             song3 = song3.values[0]
#             list_song = [song1, song2, song3]
#             return(list_song)
#     else:
#         if songA == songB and songA == songC:
#             return songA
#         else: 
#             A = final_df.loc[final_df['Name '] == songA]
#             B = final_df.loc[final_df["Name "] == songB]
#             C = final_df.loc[final_df["Name "] == songC]
            
#             avg_dim_1 = (float(A['Score 1']) + float(B['Score 1']) + float(C['Score 1']))/3
#             avg_dim_2 = (float(A['Score 2']) + float(B['Score 2']) + float(C['Score 2']))/3
#             avg_dim_3 = (float(A['Score 3']) + float(B['Score 3']) + float(C['Score 3']))/3
            
#             valeur_proche1 = None
#             valeur_proche2 = None
#             valeur_proche3 = None
#             diff_abs1 = float('inf')
#             diff_abs2 = float('inf')
#             diff_abs3 = float('inf')
            
#             list_score1 = final_df['Score 1'].tolist()
#             list_score2 = final_df['Score 2'].tolist()
#             list_score3 = final_df['Score 3'].tolist()
#             for i in range(len(list_score1)):
#                 val = float(list_score1[i])
#                 diff = abs(avg_dim_1 - float(val))
#                 if diff < diff_abs1:
#                     valeur_proche1 = float(val)
#                     diff_abs1 = diff
#             rmv1 = None
#             for i in range(len(list_score1)):
#                 if list_score1[i] == valeur_proche1:
#                     rmv1 = i
#             del list_score2[rmv1]
#             for i in range(len(list_score2)):
#                 val = float(list_score2[i])
#                 diff = abs(avg_dim_2 - float(i))
#                 if diff < diff_abs2:
#                     valeur_proche2 = float(val)
#                     diff_abs2 = diff
#             rmv2 = None
#             for i in range(len(list_score2)):
#                 if list_score2[i] == valeur_proche2:
#                     rmv2 = i
#             del list_score3[rmv1]
#             del list_score3[rmv2]
#             for i in range(len(list_score3)):
#                 val = float(list_score3[i])
#                 diff = abs(avg_dim_3 - float(i))
#                 if diff < diff_abs3:
#                     valeur_proche3 = float(val)
#                     diff_abs3 = diff
            
#             idx1 = final_df.loc[final_df['Score 1'] == valeur_proche1]
#             idx2 = final_df.loc[final_df['Score 2'] == valeur_proche2]
#             idx3 = final_df.loc[final_df['Score 3'] == valeur_proche3]
            
            
#             song1 = idx1['Name ']
#             song2 = idx2['Name ']
#             song3 = idx3['Name ']
            
#             song1 = song1.values[0]
#             song2 = song2.values[0]
#             song3 = song3.values[0]
#             list_song = [song1, song2, song3]
#             return(list_song)

with open('DF_Song.pkl', 'wb') as file_pickle:
    pickle.dump(final_df, file_pickle)
