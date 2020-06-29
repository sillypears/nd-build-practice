import os

class Config(object):
    ND_FOLDER = os.path.join("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Crypt of the NecroDancer")
    DATA_FOLDER = "data"
    MOD_FOLDER = "mods"
    IMAGES = os.path.join("data", "edited")
    DEBUG = False

class DevelopmentConfig(Config):
    ND_FOLDER = "testdata"
    DEBUG = True


class ProductionConfig(Config):
    pass

app_config = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig
}
