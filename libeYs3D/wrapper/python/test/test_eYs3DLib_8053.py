import pytest
import time

import eys3d
import eys3dPy

from utils import print_and_save

mode = 1
snapshot = False
def test_class():
    global pipe
    pipe = eys3d.Pipeline()


def test_config():
    global dev
    dev = 0
    conf = eys3d.Config()
    conf.set_color_stream(
        eys3d.COLOR_RAW_DATA_TYPE.COLOR_RAW_DATA_YUY2,
        1280,
        720,
        fps=60,
    )
    conf.set_depth_stream(
        eys3d.DEPTH_TRANSFER_CTRL.DEPTH_IMG_COLORFUL_TRANSFER,
        640,
        360,
        fps=30,
    )
    dev = pipe.get_device()
    conf.set_preset_mode_config(0x138, mode, dev.get_usb_type())
    pipe.start(conf)
    import time
    time.sleep(1)


def test_ModeConfig():  # To test ModeConfig
    modeConfig = eys3d.ModeConfig(0x138, mode, 3)
    modeConfig.get_current_index()
    modeConfig.get_mode_count()
    modeConfig.select_current_index(mode)
    modeConfig.get_current_mode_info()
    modeConfig.select_current_index(mode)

def test_z_near_far():
    #print("[Python][ZDTable] z range= {}".format(dev.get_z_range()))
    print_and_save(pipe, "Device", "ZDtable", "Z range", "range", dev.get_z_range(), snapshot, False)
    dev.set_z_range(123, 998)
    setting = dev.get_z_range()
    assert 123 == setting['Near']
    assert 998 == setting['Far']
    print_and_save(pipe, "Device", "ZDtable", "Z range", "range", dev.get_z_range(), snapshot, False)
    #print("[Python][ZDTable] z range= {}".format(dev.get_z_range()))

def test_color_frame():
    cret, cframe = pipe.get_color_frame()
    cret, raw_frame = pipe.get_color_frame(True)

def test_depth_frame():
    dret, dframe = pipe.get_depth_frame()
    dret, raw_frame = pipe.get_depth_frame(True)

def test_get_depth_zValue():
    z_map = pipe.get_depth_zValue()

def test_interleave_mode():
    pipe.disable_interleave_mode()
    assert False == pipe.is_interleave_mode_enabled()
    pipe.enable_interleave_mode()
    assert True == pipe.is_interleave_mode_enabled()

val = [x for x in range(6)]
@pytest.mark.parametrize('val', val)
def test_IR_property(val):
    global ir_property
    ir_property = dev.get_IRProperty()
    ir_property.enable_extendIR()
    assert True == ir_property.is_extendIR_enabled()
    assert 15 == ir_property.get_IR_max()
    ir_property.disable_extendIR()
    assert False == ir_property.is_extendIR_enabled()
    assert 6 == ir_property.get_IR_max()
    # Range validation
    ir_property.set_IR_value(val)
    assert val == ir_property.get_IR_value()
    print_and_save(pipe, "IRProperty", "IRValue", "value", "ir_value", ir_property.get_IR_value(), snapshot)

def test_reset_IR_Property():
    ir_property.set_IR_value(3)

def test_get_rectify_mat_log_data():
    nRectifyLogIndex = 0
    rectLogData = dev.get_rectify_mat_log_data(nRectifyLogIndex)
    rectLogData.save_json()

def test_get_usb_type():
    assert True == (dev.get_usb_type() in (2, 3)) , "get_usb_type"
    print("[Python] Usb = {}".format(dev.get_usb_type()))

def test_write_read_fw_register():
    # Its setting is available for 8053
    register = dev.get_register_options()
    fw_addr = 0xE0
    fw_value = 0x02
    register.set_FW_register(fw_addr, fw_value)
    assert fw_value == register.get_FW_register(fw_addr), "get_FW_register"
    
    print("[Python][Register]The FW value = 0x{:02x} @(0x{:02x})".format(
        fw_value, fw_addr))

def test_write_read_hw_register():
    # Its setting is available for 8053
    register = dev.get_register_options()

    hw_addr = 0xF402
    hw_value = register.get_HW_register(hw_addr)

    ValidDataRange = 0xff
    NotValidDataRange = ~ValidDataRange
    Data = 0xEF
    hw_value = hw_value & NotValidDataRange
    hw_value |= Data

    register.set_HW_register(hw_addr, hw_value)
    assert hw_value == register.get_HW_register(hw_addr), "get_HW_register"
    print("[Python][Register]The HW value = 0x{:02x} @(0x{:02x})".format(
        hw_value, hw_addr))

def test_write_read_sensor_register():
    #[Test case not confirm]
    # Its setting is available for 8062
    camera_property = pipe.get_cameraProperty()
    camera_property.disable_AE() # It needed to disable auto exposure.

    register = dev.get_register_options()
    sensor_addr = 0x01 # 8053
    sensor_n_id = 0x60 # 8053
    sensor_type = eys3d.SENSORMODE_INFO.SENSOR_BOTH
    sensor_value = register.get_sensor_register(sensor_addr, sensor_type,
                                     sensor_n_id)
    print("[Python][Register]#1The sensor value = 0x{:02x} @(0x{:02x})".format(
        sensor_value, sensor_addr))
    # Byte Swap
    def byteswap(value):
        low = (value & 0xFF00) >> 8
        high = (value & 0x00FF) << 8
        value = high + low
        return value

    # sensor_value = byteswap(sensor_value)
    register.set_sensor_register(sensor_addr, (sensor_value - 1), sensor_type,
                      sensor_n_id)
    sensor_value2 = register.get_sensor_register(sensor_addr, sensor_type,
                                    sensor_n_id)
    print("[Python][Register]#2The sensor value = 0x{:02x} @(0x{:02x})".format(
        sensor_value2, sensor_addr))
    assert sensor_value - 1 == sensor_value2
    camera_property.enable_AE() 

def test_saveLog():
    register = dev.get_register_options()
    register.enable_saveLog()
    assert True == register.is_saveLog()
    register.disable_saveLog()
    assert False == register.is_saveLog()

def test_periodic_read():
    register = dev.get_register_options()
    register.enable_periodic_read()
    assert True == register.is_periodic_read()
    register.disable_periodic_read()
    assert False == register.is_periodic_read()
    register.enable_periodic_read()

def test_property():
    global camera_property
    camera_property = pipe.get_cameraProperty()

val = [x for x in range(-13, 4)]
@pytest.mark.parametrize('val', val)
def test_exposure(val):
    camera_property.enable_AE()
    assert True == camera_property.get_AE_status()
    # print("[Test][Python][Property] Exposure enable? {}".format(
    #         camera_property.get_AE_status()))
    camera_property.disable_AE()
    assert False == camera_property.get_AE_status()
    # print("[Test][Python][Property] Exposure enable? {}".format(
    #         camera_property.get_AE_status()))

    # Range Validation
    # print("[Test][Python][Property] Exposure value: {}".format(
    #         camera_property.get_exposure_value()))
    camera_property.set_exposure_value(val)
    assert val == camera_property.get_exposure_value()
    print_and_save(pipe, "CameraProperty", "Exposure", "exposure value ", "exposure_value", camera_property.get_exposure_value(), snapshot)

    # print("[Test][Python][Property] Exposure value: {}".format(
    #         camera_property.get_exposure_value()))


def test_manual_exposure_time():
    value = round(camera_property.get_manual_exposure_time())
    # print("[Test][Python][Property] Manual exposure time: {}".format(value))
    camera_property.set_manual_exposure_time(value+1)
    assert value+1 == round(camera_property.get_manual_exposure_time())
    print_and_save(pipe, "CameraProperty", "Exposure", "manual exposure time", "exposure_time", camera_property.get_manual_exposure_time(), snapshot)
    # print("[Test][Python][Property] Manual exposure time: {}".format(
    #         camera_property.get_manual_exposure_time()))

def test_reset_exposure():
    camera_property.set_exposure_value(-13)
    camera_property.enable_AE()

def test_exposure_range():
    exposure_range = camera_property.get_exposure_range()
    assert 3 == exposure_range['Max']
    assert -13 == exposure_range['Min']
    assert 1 == exposure_range['Step']
    assert -13 == exposure_range['Default']
    # print("[Test][Python][Property] Exposure range: {}".format(
    #         camera_property.get_exposure_range()))

val = [x for x in range(2800, 6501, 100)]
@pytest.mark.parametrize('val', val)
def test_white_balance(val):
    camera_property.enable_AWB()
    assert True == camera_property.get_AWB_status()
    # print("[Test][Python][Property] White balance enable? {}".format(
    #         camera_property.get_AWB_status()))
    camera_property.disable_AWB()
    assert False == camera_property.get_AWB_status()
    # print("[Test][Python][Property] White balance enable? {}".format(
    #         camera_property.get_AWB_status()))
    # print("[Test][Python][Property] White balance value: {}".format(
    #         camera_property.get_white_balance_temperature()))
    camera_property.set_white_balance_temperature(val)
    assert val == camera_property.get_white_balance_temperature()
    print_and_save(pipe, "CameraProperty", "WhiteBalance", "Value", "white balance value", camera_property.get_white_balance_temperature(), snapshot)
    # print("[Test][Python][Property] White balance value: {}".format(
    #         camera_property.get_white_balance_temperature()))

def test_white_balance_range():
    white_balance_range = camera_property.get_white_balance_temperature_range()
    assert 6500 == white_balance_range['Max']
    assert 2800 == white_balance_range['Min']
    assert 1 == white_balance_range['Step']
    assert 5500 == white_balance_range['Default']
    # print("[Test][Python][Property] White balance range: {}".format(
    #         camera_property.get_white_balance_temperature_range()))

def test_reset_white_balance():
    camera_property.set_white_balance_temperature(5500)
    camera_property.enable_AWB()

def test_low_light_compensation():
    camera_property.enable_low_light_compensation()
    assert True == camera_property.get_low_light_compensation_status()
    print_and_save(pipe, "CameraProperty", "LowLightCompensation", "Enable", "enable ", camera_property.get_low_light_compensation_status(), snapshot)
    # print("[Test][Python][Property] Low light compensation status: {}".format(
    #         camera_property.get_low_light_compensation_status()))
    camera_property.disable_low_light_compensation()
    assert False == camera_property.get_low_light_compensation_status()
    print_and_save(pipe, "CameraProperty", "LowLightCompensation", "Enable", "enable ", camera_property.get_low_light_compensation_status(), snapshot)
    
def test_light_source():
    # print("[Test][Python][Property] Light source: {}".format(
    #         camera_property.get_light_source_status()))
    camera_property.set_light_source(eys3d.LIGHT_SOURCE_VALUE.VALUE_50HZ)
    assert eys3d.LIGHT_SOURCE_VALUE.VALUE_50HZ == camera_property.get_light_source_status()
    print_and_save(pipe, "CameraProperty", "LightSource", "Source", "source ", camera_property.get_light_source_status(), snapshot)
    # print("[Test][Python][Property] Light source: {}".format(
    #         camera_property.get_light_source_status()))
    camera_property.set_light_source(eys3d.LIGHT_SOURCE_VALUE.VALUE_60HZ)
    assert eys3d.LIGHT_SOURCE_VALUE.VALUE_60HZ == camera_property.get_light_source_status()
    print_and_save(pipe, "CameraProperty", "LightSource", "Source", "source ", camera_property.get_light_source_status(), snapshot)
    # print("[Test][Python][Property] Light source: {}".format(
    #         camera_property.get_light_source_status()))

def test_depthFilter():
    global depthFilterOptions
    depthFilterOptions = pipe.get_depthFilter_options()

    depthFilterOptions.disable()
    assert False == depthFilterOptions.is_enabled()
    print_and_save(pipe, "DepthFilter", "DepthFilter", "Enable", "enble ", depthFilterOptions.is_enabled(), snapshot, False)
    # print("[Test][Python][DepthFilter] DepthFilter enable? {}".format(
    #     depthFilterOptions.is_enabled()))
    depthFilterOptions.enable()
    assert True == depthFilterOptions.is_enabled()
    print_and_save(pipe, "DepthFilter", "DepthFilter", "Enable", "enble ", depthFilterOptions.is_enabled(), snapshot, False)
    assert 2 == depthFilterOptions.get_bytes_per_pixel()
    # print("[Test][Python][DepthFilter] DepthFilter enable? {}".format(
    #     depthFilterOptions.is_enabled()))
    # print("[Test][Python][DepthFilter] Bytes_per_pixel? {}".format(
    #     depthFilterOptions.get_bytes_per_pixel()))

val = [0,1,2,3] 
@pytest.mark.parametrize('val', val)
def test_depthFilter_subsample(val):
    depthFilterOptions.subsample.disable()
    assert False == depthFilterOptions.subsample.is_enabled()
    print_and_save(pipe, "DepthFilter", "Subsample", "Enable", "enble ", depthFilterOptions.subsample.is_enabled(), snapshot, False)
    # print("[Test][Python][DepthFilter] Subsample enable? {}".format(
    #     depthFilterOptions.subsample.is_enabled()))
    depthFilterOptions.subsample.enable()
    assert True == depthFilterOptions.subsample.is_enabled()
    print_and_save(pipe, "DepthFilter", "Subsample", "Enable", "enble ", depthFilterOptions.subsample.is_enabled(), snapshot, False)
    # print("[Test][Python][DepthFilter] Subsample enable? {}".format(
    #     depthFilterOptions.subsample.is_enabled()))
    depthFilterOptions.subsample.set(val)
    assert val + 2 == depthFilterOptions.subsample.get()["factor"]
    print_and_save(pipe, "DepthFilter", "Subsample", "Index", "mode index ", depthFilterOptions.subsample.get(), snapshot, False)
    # print("[Test][Python][DepthFilter] Subsample config: {}".format(
    #     depthFilterOptions.subsample.get()))

testdata = [(0.1, 2), (0.1, 3), (0.2, 2), (0.2, 3), (0.3, 2), (0.3, 3),
        (0.4, 2), (0.4, 3), (0.5, 2), (0.5, 3), (0.6, 2), (0.6, 3),
        (0.7, 2), (0.7, 3), (0.8, 2), (0.8, 3), (0.9, 2), (0.9, 3)]
@pytest.mark.parametrize('alpha, history', testdata)
def test_depthFilter_temporalFilter(alpha, history):
    depthFilterOptions.temporalFilter.disable()
    assert False == depthFilterOptions.temporalFilter.is_enabled()
    print_and_save(pipe, "DepthFilter", "TemporalFilter", "Enable", "enble ", depthFilterOptions.temporalFilter.is_enabled(), snapshot, False)
    # print("[Test][Python][DepthFilter] TemporalFilter enable? {}".format(
    #     depthFilterOptions.temporalFilter.is_enabled()))
    depthFilterOptions.temporalFilter.enable()
    assert True == depthFilterOptions.temporalFilter.is_enabled()
    print_and_save(pipe, "DepthFilter", "TemporalFilter", "Enable", "enble ", depthFilterOptions.temporalFilter.is_enabled(), snapshot, False)
    # print("[Test][Python][DepthFilter] TemporalFilter enable? {}".format(
    #     depthFilterOptions.temporalFilter.is_enabled()))
    depthFilterOptions.temporalFilter.set_alpha(alpha)
    assert alpha == round(depthFilterOptions.temporalFilter.get_alpha(), 1)
    print_and_save(pipe, "DepthFilter", "TemporalFilter", "Alpha", "alpha ", depthFilterOptions.temporalFilter.get_alpha(), snapshot, False)
    # print("[Test][Python][DepthFilter] TemporalFilter alpha: {}".format(
    #     depthFilterOptions.temporalFilter.get_alpha()))
    depthFilterOptions.temporalFilter.set_history(history)
    assert history == round(depthFilterOptions.temporalFilter.get_history(), 1)
    print_and_save(pipe, "DepthFilter", "TemporalFilter", "History", "history ", depthFilterOptions.temporalFilter.get_history(), snapshot, False)
    # print("[Test][Python][DepthFilter] TemporalFilter history: {}".format(
    #     depthFilterOptions.temporalFilter.get_history()))
    depthFilterOptions.temporalFilter.set(alpha=0.1, history=2)
    setting = depthFilterOptions.temporalFilter.get()
    assert 0.1 == setting["alpha"]
    assert 2 == setting["history"]
    # print("[Test][Python][DepthFilter] TemporalFilter config: {}".format(
    #     depthFilterOptions.temporalFilter.get()))


def test_depthFilter_removeCurve():
    depthFilterOptions.removeCurve.disable()
    assert False == depthFilterOptions.removeCurve.is_enabled()
    print_and_save(pipe, "DepthFilter", "RemoveCurve", "Enable", "enable ", depthFilterOptions.removeCurve.is_enabled(), snapshot, False)
    # print("[Test][Python][DepthFilter] RemoveCurve enable? {}".format(
    #     depthFilterOptions.removeCurve.is_enabled()))
    depthFilterOptions.removeCurve.enable()
    assert True == depthFilterOptions.removeCurve.is_enabled()
    print_and_save(pipe, "DepthFilter", "RemoveCurve", "Enable", "enable ", depthFilterOptions.removeCurve.is_enabled(), snapshot, False)
    # print("[Test][Python][DepthFilter] RemoveCurve enable? {}".format(
    #     depthFilterOptions.removeCurve.is_enabled()))

val = [1,2,3] 
@pytest.mark.parametrize('val', val)
def test_depthFilter_hollFill(val):
    depthFilterOptions.holeFill.disable()
    assert False == depthFilterOptions.holeFill.is_enabled()
    print_and_save(pipe, "DepthFilter", "HoleFill", "Enable", "enable ", depthFilterOptions.holeFill.is_enabled(), snapshot, False)
    # print("[Test][Python][DepthFilter] HoleFill enable? {}".format(
    #     depthFilterOptions.holeFill.is_enabled()))
    depthFilterOptions.holeFill.enable()
    assert True == depthFilterOptions.holeFill.is_enabled()
    print_and_save(pipe, "DepthFilter", "HoleFill", "Enable", "enable ", depthFilterOptions.holeFill.is_enabled(), snapshot, False)
    depthFilterOptions.holeFill.set_kernel_size()
    assert 1 == depthFilterOptions.holeFill.get_kernel_size()
    # print("[Test][Python][DepthFilter] HoleFill enable? {}".format(
    #     depthFilterOptions.holeFill.is_enabled()))
    # print("[Test][Python][DepthFilter] HoleFill kernel size: {}".format(
    #     depthFilterOptions.holeFill.get_kernel_size()))
    depthFilterOptions.holeFill.set_level(val)
    assert val == depthFilterOptions.holeFill.get_level()
    print_and_save(pipe, "DepthFilter", "HoleFill", "Level", "level ", depthFilterOptions.holeFill.get_level(), snapshot, False)
    # print("[Test][Python][DepthFilter] HoleFill level: {}".format(
    #     depthFilterOptions.holeFill.get_level()))

val = [1,2,3,4,5,6,7,8,9,10] 
@pytest.mark.parametrize('val', val)
def test_depthFilter_edgePreServingFilter(val):
    depthFilterOptions.edgePreServingFilter.disable()
    assert False == depthFilterOptions.edgePreServingFilter.is_enabled()
    print_and_save(pipe, "DepthFilter", "EdgePreServingFilter", "Enable", "enable ", depthFilterOptions.edgePreServingFilter.is_enabled(), snapshot, False)
    # print("[Test][Python][DepthFilter] EdgePreServingFilter enable? {}".format(
    #     depthFilterOptions.edgePreServingFilter.is_enabled()))
    depthFilterOptions.edgePreServingFilter.enable()
    assert True == depthFilterOptions.edgePreServingFilter.is_enabled()
    print_and_save(pipe, "DepthFilter", "EdgePreServingFilter", "Enable", "enable ", depthFilterOptions.edgePreServingFilter.is_enabled(), snapshot, False)
    # print("[Test][Python][DepthFilter] EdgePreServingFilter enable? {}".format(
    #     depthFilterOptions.edgePreServingFilter.is_enabled()))
    # For range validation
    depthFilterOptions.edgePreServingFilter.set_edge_level(val)
    assert val == depthFilterOptions.edgePreServingFilter.get_edge_level()
    assert 0.015 == depthFilterOptions.edgePreServingFilter.get_sigma()
    assert 0.1 == depthFilterOptions.edgePreServingFilter.get_lambda()
    print_and_save(pipe, "DepthFilter", "EdgePreServingFilter", "Edge_level", "level ", depthFilterOptions.edgePreServingFilter.get_edge_level(), snapshot, False)
    # print("[Test][Python][DepthFilter] EdgePreServingFilter edge_level: {}".
    #       format(depthFilterOptions.edgePreServingFilter.get_edge_level()))
    # print("[Test][Python][DepthFilter] EdgePreServingFilter sigma: {}".format(
    #     depthFilterOptions.edgePreServingFilter.get_sigma()))
    # print("[Test][Python][DepthFilter] EdgePreServingFilter lumda: {}".format(
    #     depthFilterOptions.edgePreServingFilter.get_lambda()))
    depthFilterOptions.edgePreServingFilter.set(edge_level=2)
    setting = depthFilterOptions.edgePreServingFilter.get()
    assert 2 == setting['level']
    assert 0.015 == setting['sigma']
    assert 0.1 == setting['lambda']
    # print("[Test][Python][DepthFilter] EdgePreServingFilter config: {}".format(
    #     depthFilterOptions.edgePreServingFilter.get()))


testdata = [(x, y) for x in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7] for y in range(200, 500, 100)] 
@pytest.mark.parametrize('ratio, dist', testdata)
def test_accuracy(ratio, dist):
    depthAccuracy = pipe.get_depthAccuracy()
    depthAccuracy.disable()
    assert False == depthAccuracy.is_enabled()
    # print("[Python][Accuracy] Enable? {}".format(depthAccuracy.is_enabled()))
    depthAccuracy.enable()
    assert True == depthAccuracy.is_enabled()
    depthAccuracy.set_region_ratio(ratio)
    depthAccuracy.set_groundTruth_distance(dist)
    assert ratio == round(depthAccuracy.get_region_ratio(), 2)
    assert dist == depthAccuracy.get_groundTruth_distance()
    # print("[Python][Accuracy] Region ratio: {}".format(
    #     depthAccuracy.get_region_ratio()))
    # print("[Python][Accuracy] Ground truth: {}".format(
    #     depthAccuracy.get_groundTruth_distance()))
    info = pipe.get_accuracy_info()
    assert dict == type(info)
    print_and_save(pipe, "Accuracy", "Accuracy", "Accuracy Ratio", "ratio and distance ", (round(depthAccuracy.get_region_ratio(), 2), depthAccuracy.get_groundTruth_distance()), snapshot, False)
    # print("[Python][Accuracy] Info: {}".format(info))

def test_dump_IMU_data():
    dev.dump_IMU_data(128)

def test_get_IMU_device_info():
    imu_info = dev.get_IMU_device_info()
    assert type(imu_info) == dict

def test_dump_frame_info():
    dev.dump_frame_info(30)
    time.sleep(2) # wait for frame dump

def test_dump_system_info():
    dev.dump_system_info()

# It is a issue caused system hanged occasionally.
def test_pipe_close():
    pipe.stop()

