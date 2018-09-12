import pandas as pd
import pickle
import sys

class Data_API():
    '''
    To Do: Implement Filtering of Data :
        - Delete data with no PHQ-9 Score
        - Delete data if row is empty
    '''
    def __init__(self,screen=None,avec=None,gemaps=None,mapping=None):
        if screen == None or avec == None or gemaps == None or mapping == None:
            print("There's missing data that has not been passed to the DATA API object")
            print("Please provide missing information")
            sys.exit(1)
        self.screen = self.screen_clean(screen)
        self.mapping = self.mapping_clean(mapping)
        self.gemaps = self.gemaps_clean(gemaps)
        self.avec = self.avec_clean(avec)
        self.score = self.get_score()
        self.severity = self.get_severity()
    def screen_clean(self,data_file):
        screen = pd.read_excel(data_file)
        screen = screen.rename(columns={'Submission ID':'SubmissionID'},inplace=False)
        return screen

    def get_score(self):
        return self.join_data_by_audio()['Score']

    def get_severity(self):
        return self.join_data_by_audio()['Result']

    def mapping_clean(self,data_file):
        mapping = pd.read_csv(data_file)
        mapping = mapping[['AudioFile','SubmissionID']]
        return mapping

    def gemaps_clean(self,data_file):
        gemaps = pickle.load(open(data_file,'rb'))
        gemaps = gemaps.drop(columns=['class'])
        gemaps = gemaps.rename(columns={'name':'AudioFile'},inplace=False)
        return gemaps

    def avec_clean(self,data_file):
        avec = pickle.load(open(data_file,'rb'))
        avec = avec.drop(columns=['unused_target_label'])
        avec = avec.rename(columns={'name':'AudioFile'},inplace=False)
        return avec

    def join_data_by_audio(self):
        data_df = self.gemaps.merge(self.avec,how='left',left_on= 'AudioFile',right_on='AudioFile')
        data_df = data_df.merge(self.mapping,how='left',left_on= 'AudioFile',right_on='AudioFile')
        data_df = data_df.merge(self.screen,how='left',left_on= 'SubmissionID',right_on='SubmissionID')
        return data_df

    def join_avec_gemaps(self):
        return pd.merge(self.gemaps,self.avec,on='AudioFile')

    def map_score_to_gemaps(self):
        score_df = self.screen[['SubmissionID','Score']]
        data_df = self.mapping.merge(score_df,how='left',left_on= 'SubmissionID',right_on='SubmissionID')
        data_df = self.gemaps.merge(data_df,how='left',left_on= 'AudioFile',right_on='AudioFile')
        data_df = data_df.drop(columns=['SubmissionID'])
        return data_df

    def map_score_to_avec(self):
        score_df = self.screen[['SubmissionID','Score']]
        data_df = self.mapping.merge(score_df,how='left',left_on= 'SubmissionID',right_on='SubmissionID')
        data_df = self.avec.merge(data_df,how='left',left_on= 'AudioFile',right_on='AudioFile')
        data_df = data_df.drop(columns=['SubmissionID'])
        return data_df

    def map_severity_to_gemaps(self):
        score_df = self.screen[['SubmissionID','Result']]
        data_df = self.mapping.merge(score_df,how='left',left_on= 'SubmissionID',right_on='SubmissionID')
        data_df = self.gemaps.merge(data_df,how='left',left_on= 'AudioFile',right_on='AudioFile')
        data_df = data_df.drop(columns=['SubmissionID'])
        return data_df

    def map_severity_to_avec(self):
        score_df = self.screen[['SubmissionID','Result']]
        data_df = self.mapping.merge(score_df,how='left',left_on= 'SubmissionID',right_on='SubmissionID')
        data_df = self.avec.merge(data_df,how='left',left_on= 'AudioFile',right_on='AudioFile')
        data_df = data_df.drop(columns=['SubmissionID'])
        return data_df

    def demographic_analysis(self):
        print("YO")


# def main():
#     gemaps = './FeatureSets/Julygemaps.p'
#     avec = './FeatureSets/Julyavec.p'
#     screen = './Screens/July_screens.xlsx'
#     mapping = './SubmissionIDs/JulyBatchSubmissionID.csv'
#     d_api = MHA_Data_API(screen,avec,gemaps,mapping)
#     d_api.join_data_by_audio()
# if __name__ == '__main__':
#     main()
