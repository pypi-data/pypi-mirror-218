from shortGPT.audio.eleven_voice_module import ElevenLabsVoiceModule
from shortGPT.config.asset_db import AssetDatabase
from shortGPT.config.api_db import get_api_key
from shortGPT.database.content_database import ContentDatabase
from shortGPT.config.languages import Language
from abc import ABC
import os
CONTENT_DB = ContentDatabase()

class AbstractContentEngine(ABC):
    def __init__(self, short_id: str, content_type:str, language: Language):
        if short_id:
            self.dataManager = CONTENT_DB.getContentDataManager(
                short_id, content_type
            )
        else:
            self.dataManager = CONTENT_DB.createContentDataManager(content_type)
        self.id = str(self.dataManager._getId())
        self.prepareEditingPaths()
        self._db_language = language.value
        self.voiceModule = ElevenLabsVoiceModule(get_api_key("ELEVEN LABS"))
        self.assetStore = AssetDatabase()
        self.stepDict = {}
        self.logger = lambda _: print(_)

    def __getattr__(self, name):
            if name.startswith('_db_'):
                db_path = name[4:]  # remove '_db_' prefix
                cache_attr = '_' + name
                if not hasattr(self, cache_attr):
                    setattr(self, cache_attr, self.dataManager.get(db_path))
                return getattr(self, cache_attr)
            else:
                return super().__getattr__(name)

    def __setattr__(self, name, value):
        if name.startswith('_db_'):
            db_path = name[4:]  # remove '_db_' prefix
            cache_attr = '_' + name
            setattr(self, cache_attr, value)
            self.dataManager.save(db_path, value)
        else:
            super().__setattr__(name, value)
    
    def prepareEditingPaths(self):
        self.dynamicAssetDir = f".editing_assets/{self.dataManager.contentType}_assets/{self.id}/"
        if not os.path.exists(self.dynamicAssetDir):
            os.makedirs(self.dynamicAssetDir)

    def verifyParameters(*args, **kargs):
        keys = list(kargs.keys())
        for key in keys:
            if not kargs[key]:
                print(kargs)
                raise Exception(f"Parameter :{key} is null")
            
    def isShortDone(self):
        return self._db_ready_to_upload

    def makeShort(self):
        while (not self.isShortDone()):
            currentStep = self._db_last_completed_step + 1
            if currentStep not in self.stepDict:
                raise Exception(f'Incorrect step {currentStep}')
            if  self.stepDict[currentStep].__name__ == "_editAndRenderShort":
                yield currentStep, f'Current step ({currentStep} / {self.get_total_steps()}) : ' + "Preparing rendering assets..."
            else:
                yield currentStep, f'Current step ({currentStep} / {self.get_total_steps()}) : ' + self.stepDict[currentStep].__name__
            print(f'Step {currentStep} {self.stepDict[currentStep].__name__}')
            self.stepDict[currentStep]()
            self._db_last_completed_step = currentStep

    def get_video_output_path(self):
        return self._db_video_path
    
    def get_total_steps(self):
        return len(self.stepDict)
    
    def set_logger(self,logger):
        self.logger = logger