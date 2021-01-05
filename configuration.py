class ConfigClass:
    def __init__(self):
        # link to a zip file in google drive with your pretrained model
        self._model_url = None
        # False/True flag indicating whether the testing system will download
        # and overwrite the existing model files. In other words, keep this as
        # False until you update the model, submit with True to download
        # the updated model (with a valid model_url), then turn back to False
        # in subsequent submissions to avoid the slow downloading of the large
        # model file with every submission.
        self._download_model = False

        self.corpusPath = ''
        self.savedFileMainFolder = ''
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        self.toStem = False
        self.google_news_vectors_negative300_path = '../../../../GoogleNews-vectors-negative300.bin'
        self.glove_twitter_27B_25d_path = '../../../../glove.twitter.27B.25d.txt'

        print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath

    def get_model_url(self):
        return self._model_url

    def get_download_model(self):
        return self._download_model