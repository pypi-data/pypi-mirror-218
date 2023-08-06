from pathlib import Path

DEFAULT_HOOKS_CONFIG = {
    'train.hooks': [{
        'type': 'CheckpointHook',
        'interval': 1
    }, {
        'type': 'TextLoggerHook',
        'interval': 10
    }, {
        'type': 'IterTimerHook'
    }]
}


HOOK_KEY_CHAIN_MAP = {
    'TextLoggerHook': 'train.logging',
    'CheckpointHook': 'train.checkpoint.period',
    'BestCkptSaverHook': 'train.checkpoint.best',
    'EvaluationHook': 'evaluation.period',
}



DEFAULT_CACHE_DIR = Path.home().joinpath('.cache', 'weathon')
