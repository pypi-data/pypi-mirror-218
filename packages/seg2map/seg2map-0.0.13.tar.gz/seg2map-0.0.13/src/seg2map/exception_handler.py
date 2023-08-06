# standard python imports
import os
import logging
import traceback
from typing import Union

# internal python imports
from seg2map import exceptions
from seg2map import common
from seg2map.roi import ROI

logger = logging.getLogger(__name__)

NO_CONFIG_ROIS = (
    "No ROIs were selected. Cannot save ROIs to config until ROIs are selected."
)
NO_CONFIG_SETTINGS = "Settings must be loaded before configuration files can be made.\nClick save settings"
ROIS_NOT_DOWNLOADED = (
    "Not all ROI directories exist on your computer. Try downloading the ROIs again."
)
EMPTY_SELECTED_ROIS = "Must select at least one ROI on the map"
SETTINGS_NOT_FOUND = "No settings found. Click save settings."
NO_ROI_SETTINGS = (
    "No roi settings found. Click download imagery first or upload configs"
)

# Separate different exception checking and handling
# Checking decides the message
# Handling it sends message to user


def config_check_if_none(feature, feature_type: str = ""):
    if feature is None:
        message = (
            f"{feature_type} must be loaded before configuration files can be saved."
        )
        raise exceptions.Object_Not_Found(feature_type, message)


def check_file_not_found(path: str, filename: str, search_path: str):
    # if path is None raises FileNotFoundError
    if path is None:
        logger.error(f"{filename} file was not found at {search_path}")
        raise FileNotFoundError(f"{filename} file was not found at {search_path}")


def check_if_subset(subset: set, superset: set, superset_name: str, message: str = ""):
    if not subset.issubset(superset):
        logger.error(f"Missing keys {subset-superset} from {superset_name}\n{message}")
        raise ValueError(
            f"Missing keys {subset-superset} from {superset_name}\n{message}</br>Try clicking save settings"
        )


def check_if_rois_downloaded(roi_settings: dict, roi_ids: list):
    if common.were_rois_downloaded(roi_settings, roi_ids) == False:
        logger.error(f"Not all rois were downloaded{roi_settings}")
        raise FileNotFoundError(ROIS_NOT_DOWNLOADED)


def can_feature_save_to_file(feature, feature_type: str = ""):
    if feature is None:
        logger.error(f"Feature {feature_type} did not exist. Cannot Save to File")
        raise ValueError(f"Feature {feature_type} did not exist. Cannot Save to File")


def check_empty_dict(feature, feature_type: str = ""):
    if feature == {}:
        if feature_type == "roi_settings":
            raise Exception(NO_ROI_SETTINGS)


def check_empty_layer(layer, feature_type: str = ""):
    if layer is None:
        if feature_type == ROI.LAYER_NAME:
            logger.error(f"No ROI layer found on map")
            raise Exception("No ROI layer found on map")
        if feature_type == ROI.SELECTED_LAYER_NAME:
            logger.error(f"No selected ROI layer found on map")
            raise Exception("No selected ROI layer found on map")
        logger.error(f"Cannot add an empty {feature_type} layer to the map.")
        raise Exception(f"Cannot add an empty {feature_type} layer to the map.")


def check_if_None(feature, feature_type: str = "", message: str = ""):
    if feature is None:
        if feature_type == "settings":
            message = SETTINGS_NOT_FOUND
        logger.error(f"{feature_type} is None")
        raise exceptions.Object_Not_Found(feature_type, message)


def check_path_already_exists(full_path: str, dir_name=""):
    if os.path.exists(full_path):
        msg = (
            f"Directory already exists at {full_path}"
            if dir_name == ""
            else f"{dir_name} directory already exists at {full_path}"
        )
        raise Exception(msg)


def check_empty_roi_layer(layer):
    if layer is None:
        raise Exception(EMPTY_SELECTED_ROIS)


def check_selected_set(selected_set):
    if selected_set is None:
        raise Exception(EMPTY_SELECTED_ROIS)
    if len(selected_set) == 0:
        raise Exception(EMPTY_SELECTED_ROIS)


def check_if_gdf_empty(feature, feature_type: str, message: str = ""):
    if feature.empty == True:
        logger.error(f"{feature_type} {feature} is empty")
        raise exceptions.Object_Not_Found(feature_type, message)


def handle_exception(error, row: "ipywidgets.HBox", title: str = None, msg: str = None):
    error_message = f"{error}</br>Additional Information</br>" + traceback.format_exc()
    logger.error(f"{traceback.format_exc()}")
    if isinstance(error, exceptions.Object_Not_Found):
        error_message = str(error)
    logger.error(f"{error_message}")
    launch_error_box(row, title="Error", msg=error_message)


def handle_bbox_error(
    error_msg: Union[exceptions.TooLargeError, exceptions.TooSmallError],
    row: "ipywidgets.HBox",
):
    logger.error(f"Bounding Box Error{error_msg}")
    launch_error_box(row, title="Error", msg=error_msg)


def launch_error_box(row: "ipywidgets.HBox", title: str = None, msg: str = None):
    # Show user error message
    warning_box = common.create_warning_box(title=title, msg=msg)
    # clear row and close all widgets in self.file_row before adding new warning_box
    common.clear_row(row)
    # add instance of warning_box to row
    row.children = [warning_box]
