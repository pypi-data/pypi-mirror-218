import os.path

import pyqtgraph
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from rena.configs.GlobalSignals import GlobalSignals
from rena.configs.configs import AppConfigs
from rena.presets.Presets import Presets
from rena.presets.presets_utils import get_presets_path
from rena.ui.SplashScreen import SplashLoadingTextNotifier
from rena.ui_shared import *
from rena import config, config_ui
from rena.utils.ui_utils import dialog_popup

default_settings_dict = {'theme': config_ui.default_theme}
def load_settings(revert_to_default=True, reload_presets=True, reload_configs=True):
    SplashLoadingTextNotifier().set_loading_text('Loading presets...')
    print("Settings are stored at {0}".format(config.settings.fileName()))
    if revert_to_default:
        config.settings.setValue('theme', config_ui.default_theme)
        load_default_recording_file_location()
        config.settings.setValue('viz_display_duration', config.VIZ_DISPLAY_DURATION)
        config.settings.setValue('main_window_meta_data_refresh_interval', config.MAIN_WINDOW_META_DATA_REFRESH_INTERVAL)
        config.settings.setValue('downsample_method_mean_sr_threshold', config.downsample_method_mean_sr_threshold)
        config.settings.setValue('default_channel_display_num', config.DEFAULT_CHANNEL_DISPLAY_NUM)
    else:
        if not config.settings.contains('theme') or config.settings.value('theme') is None:
            config.settings.setValue('theme', config_ui.default_theme)
        if not config.settings.contains('recording_file_location') or config.settings.value('recording_file_location') is None:
            load_default_recording_file_location()
        if not config.settings.contains('viz_display_duration') or config.settings.value('viz_display_duration') is None:
            config.settings.setValue('viz_display_duration', config.VIZ_DISPLAY_DURATION)
        if not config.settings.contains('downsample_method_mean_sr_threshold') or config.settings.value('downsample_method_mean_sr_threshold') is None:
            config.settings.setValue('downsample_method_mean_sr_threshold', config.downsample_method_mean_sr_threshold)
        if not config.settings.contains('main_window_meta_data_refresh_interval') or config.settings.value('main_window_meta_data_refresh_interval') is None:
            config.settings.setValue('main_window_meta_data_refresh_interval', config.MAIN_WINDOW_META_DATA_REFRESH_INTERVAL)
        if not config.settings.contains('default_channel_display_num') or config.settings.value('default_channel_display_num') is None:
            config.settings.setValue('default_channel_display_num', config.DEFAULT_CHANNEL_DISPLAY_NUM)
    config.settings.sync()
    # load the presets, reload from local directory the default LSL, device and experiment presets
    preset_root = get_presets_path()
    Presets(_preset_root=preset_root, _reset=reload_presets)  # create the singleton presets object

    # instantiate the GlabalSignals singleton object
    GlobalSignals()
    pyqtgraph.setConfigOptions(useNumba=True, useOpenGL=True)

def load_ui_shared():
    global stream_unavailable_pixmap
    global stream_available_pixmap
    global stream_active_pixmap
    stream_unavailable_pixmap = QPixmap('../media/icons/streamwidget_stream_unavailable.png')
    stream_available_pixmap = QPixmap('../media/icons/streamwidget_stream_available.png')
    stream_active_pixmap = QPixmap('../media/icons/streamwidget_stream_viz_active.png')

def show_splash():
    splash = QLabel()
    pixmap = QPixmap('../media/logo/RenaLabApp.png')
    splash.setPixmap(pixmap)
    splash.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
    splash.show()
    pass


def load_default_recording_file_location():
    config.settings.setValue('recording_file_location', config.DEFAULT_DATA_DIR)
    if not os.path.isdir(config.settings.value('recording_file_location')):
        try:
            os.mkdir(config.settings.value('recording_file_location'))
        except FileNotFoundError:
            dialog_popup(msg='Unable to create recording file location at {0}. '
                             'Please go to File->Settings and set the the recording file save location before'
                             'start recording.'.format(config.settings.value('recording_file_location')),
                         title='Warning')
    print("Using default recording location {0}".format(config.settings.value('recording_file_location')))
