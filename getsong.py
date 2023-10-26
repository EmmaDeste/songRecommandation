import pickle as pk
import pandas as pd
df = pd.DataFrame(pk.load(open('DF_song.pkl', 'rb')))
print(df.columns)
#def get_song(songA, songB, songC):
def get_song(*args, **kwargs):
    if len(args) == 2:
        songA, songB = args
        if songA == songB:
            return [songA, None, None]
        else: 
            A = df[df['title'] == songA]
            df2 = df.drop(A.index)
            
            B = df2[df2["title"] == songB]
            final_df = df2.drop(B.index)
            
            avg_dim_1 = (float(A['score1']) + float(B['score1']))/2
            avg_dim_2 = (float(A['score2']) + float(B['score2']))/2
            avg_dim_3 = (float(A['score3']) + float(B['score3']))/2
            
            valeur_proche1 = None
            valeur_proche2 = None
            valeur_proche3 = None
            diff_abs1 = float('inf')
            diff_abs2 = float('inf')
            diff_abs3 = float('inf')
            
            list_score1 = final_df['score1'].tolist()
            list_score2 = final_df['score2'].tolist()
            list_score3 = final_df['score3'].tolist()
            for i in range(len(list_score1)):
                val = float(list_score1[i])
                diff = abs(avg_dim_1 - float(val))
                if diff < diff_abs1:
                    valeur_proche1 = float(val)
                    diff_abs1 = diff
            rmv1 = None
            for i in range(len(list_score1)):
                if list_score1[i] == valeur_proche1:
                    rmv1 = i
            del list_score2[rmv1]
            for i in range(len(list_score2)):
                val = float(list_score2[i])
                diff = abs(avg_dim_2 - float(i))
                if diff < diff_abs2:
                    valeur_proche2 = float(val)
                    diff_abs2 = diff
            rmv2 = None
            for i in range(len(list_score2)):
                if list_score2[i] == valeur_proche2:
                    rmv2 = i
            del list_score3[rmv1]
            del list_score3[rmv2]
            for i in range(len(list_score3)):
                val = float(list_score3[i])
                diff = abs(avg_dim_3 - float(i))
                if diff < diff_abs3:
                    valeur_proche3 = float(val)
                    diff_abs3 = diff
            
            idx1 = final_df.loc[final_df['score1'] == valeur_proche1]
            idx2 = final_df.loc[final_df['score2'] == valeur_proche2]
            idx3 = final_df.loc[final_df['score3'] == valeur_proche3]

            s1 = idx1['title'].values[0]
            s2 = idx2['title'].values[0]
            s3 = idx3['title'].values[0]

            a1 = idx1['artist'].values[0]
            a2 = idx2['artist'].values[0]
            a3 = idx3['artist'].values[0]

            song1 = a1 + ' - ' + s1
            song2 = a2 + ' - ' + s2
            song3 = a3 + ' - ' + s3
            list_song = [song1, song2, song3]
            return(list_song)
    elif len(args) == 3:
        songA, songB, songC = args
        if songA == songB and songA == songC:
            return [songA, None, None]
        else:
            if songA == songB and songA != songC:
                A = df[df['title'] == songA]
                df2 = df.drop(A.index)
                
                C = df2[df2["title"] == songC]
                final_df = df2.drop(C.index)
            elif songA != songB and songA == songC:
                A = df[df['title'] == songA]
                df2 = df.drop(A.index)
                
                B = df2[df2["title"] == songB]
                final_df = df2.drop(C.index)
            elif songA != songB and songB == songC:
                A = df[df['title'] == songA]
                df2 = df.drop(A.index)
                
                B = df2[df2["title"] == songB]
                final_df = df2.drop(C.index)
            else:
                A = df[df['title'] == songA]
                df2 = df.drop(A.index)
                
                B = df2[df2["title"] == songB]
                df3 = df2.drop(B.index)
                
                C = df3[df3["title"] == songC]
                final_df = df3.drop(C.index)
            
            avg_dim_1 = (float(A['score1']) + float(B['score1']) + float(C['score1']))/3
            avg_dim_2 = (float(A['score2']) + float(B['score2']) + float(C['score2']))/3
            avg_dim_3 = (float(A['score3']) + float(B['score3']) + float(C['score3']))/3
            
            valeur_proche1 = None
            valeur_proche2 = None
            valeur_proche3 = None
            diff_abs1 = float('inf')
            diff_abs2 = float('inf')
            diff_abs3 = float('inf')
            
            list_score1 = final_df['score1'].tolist()
            list_score2 = final_df['score2'].tolist()
            list_score3 = final_df['score3'].tolist()
            for i in range(len(list_score1)):
                val = float(list_score1[i])
                diff = abs(avg_dim_1 - float(val))
                if diff < diff_abs1:
                    valeur_proche1 = float(val)
                    diff_abs1 = diff
            rmv1 = None
            for i in range(len(list_score1)):
                if list_score1[i] == valeur_proche1:
                    rmv1 = i
            del list_score2[rmv1]
            for i in range(len(list_score2)):
                val = float(list_score2[i])
                diff = abs(avg_dim_2 - float(i))
                if diff < diff_abs2:
                    valeur_proche2 = float(val)
                    diff_abs2 = diff
            rmv2 = None
            for i in range(len(list_score2)):
                if list_score2[i] == valeur_proche2:
                    rmv2 = i
            del list_score3[rmv1]
            del list_score3[rmv2]
            for i in range(len(list_score3)):
                val = float(list_score3[i])
                diff = abs(avg_dim_3 - float(i))
                if diff < diff_abs3:
                    valeur_proche3 = float(val)
                    diff_abs3 = diff
            
            idx1 = final_df.loc[final_df['score1'] == valeur_proche1]
            idx2 = final_df.loc[final_df['score2'] == valeur_proche2]
            idx3 = final_df.loc[final_df['score3'] == valeur_proche3]
            
            
            s1 = idx1['title'].values[0]
            s2 = idx2['title'].values[0]
            s3 = idx3['title'].values[0]
            
            a1 = idx1['artist'].values[0]
            a2 = idx2['artist'].values[0]
            a3 = idx3['artist'].values[0]
            
            song1 = a1 + ' - ' + s1
            song2 = a2 + ' - ' + s2
            song3 = a3 + ' - ' + s3
            list_song = [song1, song2, song3]
            return(list_song)
