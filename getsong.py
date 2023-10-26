import pickle as pk

final_df = pk.load('DF_song.pkl', 'rb')
def get_song(songA, songB, songC = None):
    if songC == None:
        if songA == songB:
            return songA
        else: 
            A = final_df.loc[final_df['Name '] == songA]
            B = final_df.loc[final_df["Name "] == songB]
            
            avg_dim_1 = (float(A['Score 1']) + float(B['Score 1']))/2
            avg_dim_2 = (float(A['Score 2']) + float(B['Score 2']))/2
            avg_dim_3 = (float(A['Score 3']) + float(B['Score 3']))/2
            
            valeur_proche1 = None
            valeur_proche2 = None
            valeur_proche3 = None
            diff_abs1 = float('inf')
            diff_abs2 = float('inf')
            diff_abs3 = float('inf')
            
            list_score1 = final_df['Score 1'].tolist()
            list_score2 = final_df['Score 2'].tolist()
            list_score3 = final_df['Score 3'].tolist()
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
            
            idx1 = final_df.loc[final_df['Score 1'] == valeur_proche1]
            idx2 = final_df.loc[final_df['Score 2'] == valeur_proche2]
            idx3 = final_df.loc[final_df['Score 3'] == valeur_proche3]
           
            song1 = idx1['Name ']
            song2 = idx2['Name ']
            song3 = idx3['Name ']
            
            song1 = song1.values[0]
            song2 = song2.values[0]
            song3 = song3.values[0]
            list_song = [song1, song2, song3]
            return(list_song)
    else:
        if songA == songB and songA == songC:
            return songA
        else: 
            A = final_df.loc[final_df['Name '] == songA]
            B = final_df.loc[final_df["Name "] == songB]
            C = final_df.loc[final_df["Name "] == songC]
            
            avg_dim_1 = (float(A['Score 1']) + float(B['Score 1']) + float(C['Score 1']))/3
            avg_dim_2 = (float(A['Score 2']) + float(B['Score 2']) + float(C['Score 2']))/3
            avg_dim_3 = (float(A['Score 3']) + float(B['Score 3']) + float(C['Score 3']))/3
            
            valeur_proche1 = None
            valeur_proche2 = None
            valeur_proche3 = None
            diff_abs1 = float('inf')
            diff_abs2 = float('inf')
            diff_abs3 = float('inf')
            
            list_score1 = final_df['Score 1'].tolist()
            list_score2 = final_df['Score 2'].tolist()
            list_score3 = final_df['Score 3'].tolist()
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
            
            idx1 = final_df.loc[final_df['Score 1'] == valeur_proche1]
            idx2 = final_df.loc[final_df['Score 2'] == valeur_proche2]
            idx3 = final_df.loc[final_df['Score 3'] == valeur_proche3]
            
            
            song1 = idx1['Name ']
            song2 = idx2['Name ']
            song3 = idx3['Name ']
            
            song1 = song1.values[0]
            song2 = song2.values[0]
            song3 = song3.values[0]
            list_song = [song1, song2, song3]
            return(list_song)