import os
import sys
import webbrowser
from typing import Dict

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QTimer, QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox

from exceptions.exceptions import RenaError
from rena import config
from rena.configs.configs import AppConfigs
from rena.presets.Presets import Presets, PresetType, DataType
from rena.sub_process.TCPInterface import RenaTCPInterface
from rena.threadings.LongTasks import LongTaskThread, LoadingDialog
from rena.ui.AddWiget import AddStreamWidget
from rena.ui.LSLWidget import LSLWidget
from rena.ui.ScriptingTab import ScriptingTab
from rena.ui.SplashScreen import SplashLoadingTextNotifier
from rena.ui.VideoDeviceWidget import VideoDeviceWidget
from rena.ui.VideoWidget import VideoWidget
from rena.ui.ZMQWidget import ZMQWidget
from rena.ui_shared import num_active_streams_label_text
from rena.presets.presets_utils import get_experiment_preset_streams, check_preset_exists, create_default_lsl_preset, \
    create_default_zmq_preset
from rena.utils.test_utils import some_test

try:
    import rena.config
except ModuleNotFoundError as e:
    print('Make sure you set the working directory to ../RealityNavigation/rena, cwd is ' + os.getcwd())
    raise e
import rena.threadings.workers as workers
from rena.ui.StreamWidget import StreamWidget
from rena.ui.RecordingsTab import RecordingsTab
from rena.ui.SettingsWidget import SettingsWidget
from rena.ui.ReplayTab import ReplayTab
from rena.utils.buffers import DataBuffer
from rena.utils.ui_utils import dialog_popup, \
    another_window

import numpy as np


# Define function to import external files when using PyInstaller.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, app, ask_to_close=True, *args, **kwargs):
        """
        This is the main entry point to RenaLabApp
        :param app: the main QT app
        :param ask_to_close: whether to show a 'confirm exit' dialog and ask for
         user's confirmation in a close event
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        SplashLoadingTextNotifier().set_loading_text('Creating main window...')
        self.ui = uic.loadUi("ui/mainwindow.ui", self)
        self.setWindowTitle('RenaLabApp')
        self.app = app
        self.ask_to_close = ask_to_close

        ############
        self.stream_widgets: Dict[str, StreamWidget] = {}
        ############

        # create sensor threads, worker threads for different sensors
        self.device_workers = {}
        self.lsl_workers = {}

        ######### init server
        print('Creating Rena Client')
        # self.rena_dsp_client = RenaTCPInterface(stream_name=config.rena_server_name,
        #                                         port_id=config.rena_server_port,
        #                                         identity='client')

        #########
        # meta data update timer
        self.meta_data_update_timer = QTimer()
        self.meta_data_update_timer.setInterval(config.MAIN_WINDOW_META_DATA_REFRESH_INTERVAL)  # for 15 Hz refresh rate
        self.meta_data_update_timer.timeout.connect(self.update_meta_data)
        self.meta_data_update_timer.start()

        self.addStreamWidget = AddStreamWidget(self)
        self.MainTabVerticalLayout.insertWidget(0, self.addStreamWidget)  # add the add widget to visualization tab's
        self.addStreamWidget.add_btn.clicked.connect(self.add_btn_clicked)

        self.start_all_btn.setEnabled(False)
        self.stop_all_btn.setEnabled(False)

        self.start_all_btn.clicked.connect(self.on_start_all_btn_clicked)
        self.stop_all_btn.clicked.connect(self.on_stop_all_btn_clicked)
        # scripting buffer
        self.inference_buffer = np.empty(shape=(0, config.INFERENCE_CLASS_NUM))  # time axis is the first

        # add other tabs
        self.recording_tab = RecordingsTab(self)
        self.recordings_tab_vertical_layout.addWidget(self.recording_tab)

        self.replay_tab = ReplayTab(self)
        self.replay_tab_vertical_layout.addWidget(self.replay_tab)

        self.scripting_tab = ScriptingTab(self)
        self.scripting_tab_vertical_layout.addWidget(self.scripting_tab)

        # windows
        self.pop_windows = {}
        self.current_dialog = None

        # actions for context menu
        self.actionDocumentation.triggered.connect(self.fire_action_documentation)
        self.actionRepo.triggered.connect(self.fire_action_repo)
        self.actionShow_Recordings.triggered.connect(self.fire_action_show_recordings)
        self.actionExit.triggered.connect(self.fire_action_exit)
        self.actionSettings.triggered.connect(self.fire_action_settings)

        # create the settings window
        self.settings_widget = SettingsWidget(self)
        self.settings_window = another_window('Settings')
        self.settings_window.get_layout().addWidget(self.settings_widget)
        self.settings_window.hide()

        # global buffer object for visualization, recording, and scripting
        self.global_stream_buffer = DataBuffer()

    def add_btn_clicked(self):
        """
        This is the only entry point to adding a stream widget
        :return:
        """
        # self.addStreamWidget.add_btn.setEnabled(False)
        # self.loading_dialog = LoadingDialog(self, message=f"Adding stream {self.addStreamWidget.get_selected_stream_name()}")
        # self.loading_dialog.show()
        # task_thread = LongTaskThread(self, "process_add")
        # task_thread.completed.connect(self.add_completed)
        # task_thread.start()
        self.process_add()

    def add_completed(self):
        self.addStreamWidget.add_btn.setEnabled(True)
        self.loading_dialog.close()

    def process_add(self):
        if self.recording_tab.is_recording:
            dialog_popup(msg='Cannot add while recording.')
            return
        selected_text, data_type, port  = self.addStreamWidget.get_selected_stream_name(), \
                                                               self.addStreamWidget.get_data_type(), \
                                                               self.addStreamWidget.get_port_number()
        if len(selected_text) == 0:
            return
        try:
            if selected_text in self.stream_widgets.keys():  # if this inlet hasn't been already added
                dialog_popup('Nothing is done for: {0}. This stream is already added.'.format(selected_text),title='Warning')
                return

            selected_type, is_new_preset = self.addStreamWidget.get_current_selected_type()
            if is_new_preset:
                self.create_preset(selected_text, selected_type, data_type=data_type, port=port)
                self.scripting_tab.update_script_widget_input_combobox()  # add the new preset to the combo box

            if selected_type == PresetType.WEBCAM:  # add video device
                self.init_video_device(selected_text, video_preset_type=selected_type)
            elif selected_type == PresetType.MONITOR:
                self.init_video_device(selected_text, video_preset_type=selected_type)
            elif selected_type == PresetType.CUSTOM:  # if this is a device preset
                raise NotImplementedError
                self.init_device(selected_text)  # add device stream
            elif selected_type == PresetType.LSL:
                self.init_LSL_streaming(selected_text, data_type)  # add lsl stream
            elif selected_type == PresetType.ZMQ:
                self.init_ZMQ_streaming(selected_text, port, data_type)  # add lsl stream
            elif selected_type == PresetType.EXPERIMENT:  # add multiple streams from an experiment preset
                streams_for_experiment = get_experiment_preset_streams(selected_text)
                self.add_streams_to_visualize(streams_for_experiment)
            else:
                raise Exception("Unknow preset type {}".format(selected_type))
            self.update_active_streams()
        except RenaError as error:
            dialog_popup('Failed to add: {0}. {1}'.format(selected_text, str(error)), title='Error')
        self.addStreamWidget.check_can_add_input()

    def create_preset(self, stream_name, preset_type, data_type=DataType.float32, num_channels=1, nominal_sample_rate=None, **kwargs):
        if preset_type == PresetType.LSL:
            create_default_lsl_preset(stream_name, num_channels, nominal_sample_rate, data_type=data_type)  # create the preset
        elif preset_type == PresetType.ZMQ:
            try:
                assert 'port' in kwargs.keys()
            except AssertionError:
                raise ValueError("Port number must be specified for ZMQ preset")
            create_default_zmq_preset(stream_name, kwargs['port'], num_channels, nominal_sample_rate, data_type=data_type)  # create the preset
        elif preset_type == PresetType.CUSTOM:
            raise NotImplementedError
        else:
            raise ValueError(f"Unknown preset type {preset_type}")
        self.addStreamWidget.update_combobox_presets()  # add thew new preset to the combo box

    def remove_stream_widget(self, target):
        self.streamsHorizontalLayout.removeWidget(target)
        self.update_active_streams()
        self.addStreamWidget.check_can_add_input()  # check if the current selected preset has already been added

    def update_active_streams(self):
        available_widget_count = len([x for x in self.stream_widgets.values() if x.is_stream_available])
        streaming_widget_count = len([x for x in self.stream_widgets.values() if x.is_widget_streaming()])
        self.numActiveStreamsLabel.setText(
            num_active_streams_label_text.format(len(self.stream_widgets), available_widget_count,
                                                 streaming_widget_count, self.replay_tab.get_num_replay_channels()))
        # enable/disable the start/stop all buttons
        self.start_all_btn.setEnabled(available_widget_count > streaming_widget_count)
        self.stop_all_btn.setEnabled(streaming_widget_count > 0)

    def on_start_all_btn_clicked(self):
        [x.start_stop_stream_btn_clicked() for x in self.stream_widgets.values() if x.is_stream_available and not x.is_widget_streaming()]

    def on_stop_all_btn_clicked(self):
        [x.start_stop_stream_btn_clicked() for x in self.stream_widgets.values() if x.is_widget_streaming and x.is_widget_streaming()]

    def init_video_device(self, video_device_name, video_preset_type):
        widget_name = video_device_name + '_widget'
        widget = VideoWidget(parent_widget=self,
                           parent_layout=self.camHorizontalLayout,
                             video_preset_type=video_preset_type,
                           video_device_name=video_device_name,
                           insert_position=self.camHorizontalLayout.count() - 1)
        widget.setObjectName(widget_name)
        self.stream_widgets[video_device_name] = widget

    def add_streams_to_visualize(self, stream_names):
        for stream_name in stream_names:
            # check if the stream in setting's preset
            if stream_name not in self.stream_widgets.keys():
                if check_preset_exists(stream_name):
                    self.addStreamWidget.select_by_stream_name(stream_name)
                    self.addStreamWidget.add_btn.click()
                else:  # add a new preset if the stream name is not defined
                    self.addStreamWidget.set_selection_text(stream_name)
                    self.addStreamWidget.add_btn.click()

    def add_streams_from_replay(self, stream_names):
        # switch tab to stream
        self.ui.tabWidget.setCurrentWidget(self.visualization_tab)
        self.add_streams_to_visualize(stream_names)

    def init_LSL_streaming(self, stream_name, data_type=None):
        widget_name = stream_name + '_widget'
        stream_widget = LSLWidget(parent_widget=self,
                                 parent_layout=self.streamsHorizontalLayout,
                                 stream_name=stream_name,
                                 data_type=data_type,
                                 insert_position=self.streamsHorizontalLayout.count() - 1)
        stream_widget.setObjectName(widget_name)
        self.stream_widgets[stream_name] = stream_widget

    def init_ZMQ_streaming(self, topic_name, port_number, data_type):
        widget_name = topic_name + '_widget'
        stream_widget = ZMQWidget(parent_widget=self,
                                 parent_layout=self.streamsHorizontalLayout,
                                 topic_name=topic_name,
                                  port_number=port_number,
                                 data_type=data_type,
                                 insert_position=self.streamsHorizontalLayout.count() - 1)
        stream_widget.setObjectName(widget_name)
        self.stream_widgets[topic_name] = stream_widget

    def update_meta_data(self):
        # get the stream viz fps
        fps_list = np.array([[s.get_fps() for s in self.stream_widgets.values()]])
        pull_data_delay_list = np.array([[s.get_pull_data_delay() for s in self.stream_widgets.values()]])
        if len(fps_list) == 0:
            return
        if np.all(fps_list == 0):
            self.visualizationFPSLabel.setText("0")
        else:
            self.visualizationFPSLabel.setText("%.2f" % np.mean(fps_list))

        if len(pull_data_delay_list) == 0:
            return
        if np.all(pull_data_delay_list == 0):
            self.pull_data_delay_label.setText("0")
        else:
            self.pull_data_delay_label.setText("%.5f ms" % (1e3 * np.mean(pull_data_delay_list)))

    def init_device(self, device_name):
        config.settings.beginGroup('presets/streampresets/{0}'.format(device_name))
        device_type = config.settings.value('DeviceType')

        if device_name not in self.device_workers.keys() and device_type == 'OpenBCI':
            serial_port = config.settings.value('_SerialPort')
            board_id = config.settings.value('_Board_id')
            # create and start this device's worker thread
            worker = workers.OpenBCIDeviceWorker(device_name, serial_port, board_id)
            config.settings.endGroup()
            self.init_network_streaming(device_name, networking_interface='Device', worker=worker)
        else:
            dialog_popup('We are not supporting this Device or the Device has been added')
        config.settings.endGroup()

    def reload_all_presets_btn_clicked(self):
        if self.reload_all_presets():
            self.update_presets_combo_box()
            dialog_popup('Reloaded all presets', title='Info')

    def update_presets_combo_box(self):
        self.preset_LSLStream_combo_box.clear()
        self.preset_LSLStream_combo_box.addItems(self.lslStream_presets_dict.keys())
        self.device_combo_box.clear()
        self.device_combo_box.addItems(self.device_presets_dict.keys())
        self.experiment_combo_box.clear()
        self.experiment_combo_box.addItems(self.experiment_presets_dict.keys())

    def closeEvent(self, event):
        if self.ask_to_close:
            reply = QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to exit?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        else:
            reply = QMessageBox.StandardButton.Yes
        if reply == QMessageBox.StandardButton.Yes:
            if self.settings_window is not None:
                self.settings_window.close()

            # close other tabs
            stream_close_calls = [s_widgets.try_close for s_widgets in self.stream_widgets.values()]
            [c() for c in stream_close_calls]
            self.scripting_tab.try_close()
            self.replay_tab.try_close()

            Presets().__del__()
            AppConfigs().__del__()
            event.accept()
        else:
            event.ignore()

    def fire_action_documentation(self):
        webbrowser.open("https://realitynavigationdocs.readthedocs.io/")

    def fire_action_repo(self):
        webbrowser.open("https://github.com/ApocalyVec/RealityNavigation")

    def fire_action_show_recordings(self):
        self.recording_tab.open_recording_directory()

    def fire_action_exit(self):
        self.close()

    def fire_action_settings(self):
        self.open_settings_tab()

    def open_settings_tab(self, tab_name: str='Streams'):
        self.settings_window.show()
        self.settings_window.activateWindow()
        if tab_name is not None:
            self.settings_widget.switch_to_tab(tab_name)

    def get_added_stream_names(self):
        return list(self.stream_widgets.keys())

    def is_any_stream_widget_added(self):
        return len(self.stream_widgets) > 0

    def is_any_streaming(self):
        """
        Check if any stream is streaming. Checks if any stream widget or video device widget is streaming.
        @return: return True if any network streams or video device is streaming, False otherwise
        """
        is_stream_widgets_streaming = np.any([x.is_widget_streaming() for x in self.stream_widgets.values()])
        return np.any(is_stream_widgets_streaming)

