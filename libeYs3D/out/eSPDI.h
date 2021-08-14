/*! \file eSPDI.h
  	\brief Etron SDK API export functions, data structure and variable definition
  	Copyright:
	This file copyright (C) 2017 by

	eYs3D an Etron company

	An unpublished work.  All rights reserved.

	This file is proprietary information, and may not be disclosed or
	copied without the prior permission of eYs3D an Etron company.
 */
#ifndef LIB_ESPDI_H
#define LIB_ESPDI_H

#include "eSPDI_def.h"
#include "eSPDI_version.h"
#include <stdlib.h>
extern "C" {

/*! \fn int EtronDI_Init(
        void **ppHandleEtronDI,
        bool bIsLogEnabled)
    \brief entry point of Etron camera SDK including
        1.create a CEtronDI class for accessing oncming APIs
        2.find out Etron devices
        3.create a CVideoDevice class for video streaming and hardware access
    \param **ppHandleEtronDI	a pointer of pointer to access CEtronDI class
    \param bIsLogEnabled	generate log or not
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_Init(void **ppHandleEtronDI, bool bIsLogEnabled);

/*! \fn int EtronDI_FindDevice(
        void *pHandleEtronDI)
    \brief find out all Etron USB devices by PID, VID and ChipID, also remember device types
    \param void *pHandleEtronDI	CEtronDI handler
    \return success: EtronDI_OK, others: see eSPDI_def.h
 */
int  EtronDI_FindDevice(void *pHandleEtronDI);

/*! \fn void EtronDI_Release(
        void **ppHandleEtronDI)
    \brief release resource that EtronDI_Init had allocated
    \param void **ppHandleEtronDI	array of CEtronDI class handlers
    \return none
*/
void EtronDI_Release(void **ppHandleEtronDI);

/*! \fn int EtronDI_RefreshDevice(
        void *pHandleEtronDI)
    \brief refresh all Etron UVC devices
    \param void *pHandleEtronDI	CEtronDI handler
    \return success: EtronDI_OK, others: see eSPDI_def.h
 */
int  EtronDI_RefreshDevice(void *pHandleEtronDI);

/*! \fn int EtronDI_SwitchBaseline(
        int index)
    \brief Swich the baseline index
    \param int index Baseline index
        1: 30   mm
        2: 60   mm
        3: 150  mm
    \return success: EtronDI_OK, others: see eSPDI_def.h
 */
int EtronDI_SwitchBaseline(int index);

/*! \fn bool EtronDI_IsMLBaseLine(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo)
    \brief Check the device is multiple baseline device.
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \return true: multiplies baseline device, false: normally device.
*/
bool EtronDI_IsMLBaseLine(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int EtronDI_DoFusion(
        unsigned char ** pDepthBufList,
        double *pDepthMerge,
        unsigned char *pDepthMergeFlag,
        int nDWidth,
        int nDHeight,
        double fFocus,
        double *pBaseline,
        double *pWRNear,
        double *pWRFar,
        double *pWRFusion,
        int nMergeNum,
        bool bdepth2Byte11bit,
        int method)
    \brief Do Fusion Merge
    \param unsigned char **pDepthBufList Point to Depth Buffer List
    \param double *pDepthMerge Point to Fusion output.
    \param unsigned char *pDepthMergeFlag Point to Fusion select
    \paramdouble fFocus Focus vale
    \param int nDWidth Image width
    \param int nDHeight Image Height
    \param double *pBaseline Point to baseline array
            m_baselineDist[0] = 30.0;
            m_baselineDist[1] = 60.0;
            m_baselineDist[2] = 150.0;
    \param double *pWRNear NearWorkingRange Vecror(Container)
    \param double *pWRFar FarWorkingRange Vecror(Container)
    \param double *pWRFusion FusionWorkingRange Vecror(Container)
    \param int nMergeNum Total merges
    \param int  method method select
        0: MBLBase
        1: MBRbaseV0
        2: MBRbaseV1
    \return  success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_DoFusion(unsigned char **pDepthBufList, double *pDepthMerge, unsigned char *pDepthMergeFlag, int nDWidth, int nDHeight, double fFocus, double *pBaseline, double *pWRNear, double *pWRFar, double *pWRFusion, int nMergeNum, bool bdepth2Byte11bit, int method);

/*! \fn int EtronDI_GetDeviceNumber(
        void *pHandleEtronDI)
    \brief get Etron USB device numbers
    \param void *pHandleEtronDI	CEtronDI handler
    \return number of Etron device
*/
int  EtronDI_GetDeviceNumber(void *pHandleEtronDI);

/*! \fn int EtronDI_GetDeviceInfo(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        DEVINFORMATION* pdevinfo)
    \brief get informations of Etron UVC devices, see DEVINFORMATION
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param DEVINFORMATION* pdevinfo	pointer of device information
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetDeviceInfo(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo ,DEVINFORMATION* pdevinfo);

/*! \fn int EtronDI_GetDeviceInfoMBL_15cm(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        DEVINFORMATION* pdevinfo)
    \brief get informations of Etron UVC devices, see DEVINFORMATION
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param DEVINFORMATION* pdevinfo	pointer of device information
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetDeviceInfoMBL_15cm(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo ,DEVINFORMATION* pdevinfo);

/*! \fn int EtronDI_SelectDevice(
        void *pHandleEtronDI,
        int dev_index)
    \brief do not support currently
    \return ETronDI_NotSupport
*/
int  EtronDI_SelectDevice(void *pHandleEtronDI, int dev_index);

/*! \fn bool EtronDI_IsInterleaveDevice(
void *pHandleEtronDI,
PDEVSELINFO pDevSelInfo)
\brief check module support interleave function or not
\param pHandleEtronDI	 the pointer to the initilized EtronDI SDK instance
\param pDevSelInfo	pointer of device select index
\return true: support interleave, false: not support
*/
bool EtronDI_IsInterleaveDevice(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int EtronDI_EnableInterleave(
void *pHandleEtronDI,
PDEVSELINFO pDevSelInfo, bool enable
)
\brief enable or disable interleave function
\param pHandleEtronDI	 the pointer to the initilized EtronDI SDK instance
\param pDevSelInfo	pointer of device select index
\param enable	set true to enable interleave, or set false to disable interleave
\return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int EtronDI_EnableInterleave(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, bool enable);

/*! \fn int EtronDI_SetControlCounterMode(
void *pHandleEtronDI,
PDEVSELINFO pDevSelInfo,
unsigned char nValue)
\brief enable or disable interleave function
\param pHandleEtronDI	 the pointer to the initilized EtronDI SDK instance
\param pDevSelInfo	pointer of device select index
\param nValue	0: Frame Counter Mode, 1: Serial Counter Mode,
\return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int EtronDI_SetControlCounterMode(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char nValue);

/*! \fn int EtronDI_GetControlCounterMode(
void *pHandleEtronDI,
PDEVSELINFO pDevSelInfo, unsigned char *nValue)
\brief enable or disable interleave function
\param pHandleEtronDI	 the pointer to the initilized EtronDI SDK instance
\param pDevSelInfo	pointer of device select index
\param *nValue	pointer to frame counter mode value, 0: Frame Counter Mode, 1: Serial Counter Mode,
\return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int EtronDI_GetControlCounterMode(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char *nValue);

// register APIs +

/*! \fn int EtronDI_GetSensorRegister(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nId,
        unsigned short address,
        unsigned short *pValue,
        int flag,
        SENSORMODE_INFO SensorMode)
    \beirf get value from sensor register
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nId	sensor slave address
        see Videodevice.h for sensor slave address setting
    \param unsigned short address	register address
    \param unsigned short *pValue	pointer of value got from register address
    \param int flag	address and value data length(2 or 1 byte)
        ie FG_Address_2Byte | FG_Value_2Byte is 2 byte address and 2 byte value
        #define FG_Address_1Byte 0x01
        #define FG_Address_2Byte 0x02
        #define FG_Value_1Byte   0x10
        #define FG_Value_2Byte   0x20
    \param SENSORMODE_INFO SensorMode	sensor mode(sensor A, B or Both)
        A is 0, B is 1, Both is 2
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetSensorRegister(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nId, unsigned short address, unsigned short *pValue, int flag, SENSORMODE_INFO SensorMode);

/*! \fn int EtronDI_SetSensorRegister(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nId,
        unsigned short address,
        unsigned short nValue,
        int flag,
        SENSORMODE_INFO SensorMode)
    \brief set sensor register value
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nId	sensor slave address
        see Videodevice.h for sensor slave address setting
    \param unsigned short address	register address
    \param unsigned short nValue	value to set
    \param int flag	address and value data length(2 or 1 byte)
        ie FG_Address_1Byte | FG_Value_1Byte is 1 byte address and 1 byte value
        #define FG_Address_1Byte 0x01
        #define FG_Address_2Byte 0x02
        #define FG_Value_1Byte   0x10
        #define FG_Value_2Byte   0x20
    \param SENSORMODE_INFO SensorMode	sensor mode(sensor A, B or Both)
        A is 0, B is 1, Both is 2
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetSensorRegister(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nId, unsigned short address, unsigned short nValue,  int flag, SENSORMODE_INFO SensorMode);

/*! \fn int EtronDI_GetFWRegister(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short address,
        unsigned short *pValue,
        int flag)
    \brief get firmware register value
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short address	register address
    \param unsigned short *pValue	pointer of value got from register address
    \param int flag	address and value data length(2 or 1 byte)
        ie FG_Address_2Byte | FG_Value_2Byte is 2 byte address and 2 byte value
        #define FG_Address_1Byte 0x01
        #define FG_Address_2Byte 0x02
        #define FG_Value_1Byte   0x10
        #define FG_Value_2Byte   0x20
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetFWRegister(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short address, unsigned short *pValue, int flag);

/*! \fn int EtronDI_SetFWRegister(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short address,
        unsigned short nValue,
        int flag)
    \brief set firmware register value
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short address	register address
    \param unsigned short nValue	register value to set
    \param int flag	address and value data length(2 or 1 byte)
        ie FG_Address_1Byte | FG_Value_1Byte is 1 byte address and 1 byte value
        #define FG_Address_1Byte 0x01
        #define FG_Address_2Byte 0x02
        #define FG_Value_1Byte   0x10
        #define FG_Value_2Byte   0x20
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetFWRegister(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short address, unsigned short nValue,  int flag);

/*! \fn int EtronDI_GetHWRegister(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short address,
        unsigned short *pValue,
        int flag)
    \brief get hardware register value
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short address	register address
    \param unsigned short *pValue	pointer of value got from register address
    \param int flag	address and value data length(2 or 1 byte)
        ie FG_Address_2Byte | FG_Value_2Byte is 2 byte address and 2 byte value
        #define FG_Address_1Byte 0x01
        #define FG_Address_2Byte 0x02
        #define FG_Value_1Byte   0x10
        #define FG_Value_2Byte   0x20
    \return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int  EtronDI_GetHWRegister(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short address, unsigned short *pValue, int flag);

/*! \fn int EtronDI_SetHWRegister(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short address,
        unsigned short nValue,
        int flag)
    \brief set hardware register
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short address	register address
    \param unsigned short nValue	register value to set
    \param int flag	address and value data length(2 or 1 byte)
        ie FG_Address_1Byte | FG_Value_1Byte is 1 byte address and 1 byte value
        #define FG_Address_1Byte 0x01
        #define FG_Address_2Byte 0x02
        #define FG_Value_1Byte   0x10
        #define FG_Value_2Byte   0x20
    \return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int  EtronDI_SetHWRegister(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short address, unsigned short nValue,  int flag);
// register APIs -

// File ID +

/*! \fn int EtronDI_GetBusInfo(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        char *pszBusInfo,
        int nBufferSize,
        int *pActualLength)
    \brief get the firmware version of device, the version is a string
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param char *pszBusInfo	Bus information string
    \param int *pActualLength	the actual length of Bus info in byte
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetBusInfo(    void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, char *pszBusInfo, int *pActualLength);

/*! \fn int EtronDI_GetFwVersion(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        char *pszFwVersion,
        int nBufferSize,
        int *pActualLength)
    \brief get the firmware version of device, the version is a string
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param char *pszFwVersion	firmware version string
    \param int nBufferSize	input buffer length to receive FW version
    \param int *pActualLength	the actual length of FW version in byte
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetFwVersion(    void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, char *pszFwVersion, int nBufferSize, int *pActualLength);

/*! \fn int EtronDI_GetPidVid(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short *pPidBuf,
        unsigned short *pVidBuf)
    \brief get PID(product ID) and VID(vendor ID) of device
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short *pPidBuf	4 byte buffer to store PID value
    \param unsigned short *pVidBuf	4 byte buffer to store VID value
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetPidVid(       void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short *pPidBuf, unsigned short *pVidBuf );

/*! \fn int EtronDI_SetPidVid(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short *pPidBuf,
        unsigned short *pVidBuf)
    \brief set PID and VID to device
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short *pPidBuf	4 byte PID value buffer to set
    \param unsigned short *pVidBuf	4 byte VID value buffer to set
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetPidVid(       void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short *pPidBuf, unsigned short *pVidBuf );

/*! \fn int EtronDI_GetSerialNumber(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned char* pData,
        int nbufferSize,
        int *pLen)
    \brief get device serial number
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *pData	output buffer to store serial number string
    \param int nbufferSize	pData buffer length in byte, 2 byte(WideChar) is a unit
    \param int *pLen	pointer of actual serial number length
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetSerialNumber (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* pData, int nbufferSize, int *pLen);

/*! \fn int EtronDI_SetSerialNumber(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned char* pData,
        int nLen)
    \brief set serial number to device
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *pData	pointer of buffer to store serial number, it is WildChar
    \param int nLen	pData length in byte
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetSerialNumber (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* pData, int nLen);

/*! \fn int EtronDI_GetYOffset(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *buffer,
        int BufferLength,
        int *pActualLength,
        int index)
    \brief get Y offset (file ID 30+) value
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *buffer	buffer to store Y offset values
    \param int BufferLength	must be 256
    \param int *pActualLength	the buffer length, always be 256
    \param int index	index value to file ID 30
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetYOffset      (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, BYTE *buffer, int BufferLength, int *pActualLength, int index);

/*!	\fn int EtronDI_GetRectifyTable(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *buffer,
        int BufferLength,
        int *pActualLength,
        int index)
    \brief get rectify values (file ID 40+) from flash
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *buffer	buffer to store rectify table data
    \param int BufferLength	input buffer length, must be 1024
    \param int *pActualLength	actual length has written to buffer
    \param int index	index(from 0 ~ 9) to identify rectify table for corresponding depth
    \return success:EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetRectifyTable (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, BYTE *buffer, int BufferLength, int *pActualLength, int index);

/*! \fn int EtronDI_GetZDTable(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *buffer,
        int BufferLength,
        int *pActualLength,
        PZDTABLEINFO pZDTableInfo)
    \brief get disparity and Z values from flash
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *buffer	bufer to store ZD table
    \param int BufferLength	input buffer length
    \param int *pActualLength	actual length has written to buffer
    \param PZDTABLEINFO pZDTableInfo	index to identify ZD table and data type for corrresponding depth
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetZDTable      (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, BYTE *buffer, int BufferLength, int *pActualLength, PZDTABLEINFO pZDTableInfo);

/*! \fn int EtronDI_GetLogData(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *buffer,
        int BufferLength,
        int *pActualLength,
        int index,
        CALIBRATION_LOG_TYPE type)
    \brief get log data from flash
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *buffer	buffer to store log data
    \param int BufferLength	input buffer length, must be 4096
    \param int *pActualLength	actual length has written to buffer
    \param int index	index to identify log data for corresponding depth
    \param CALIBRATION_LOG_TYPE type	which calibration log to get
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetLogData      (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, BYTE *buffer, int BufferLength, int *pActualLength, int index, CALIBRATION_LOG_TYPE type);

/*! \fn int EtronDI_GetUserData(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *buffer,
        int BufferLength,
        USERDATA_SECTION_INDEX usi)
    \brief get user data from flash
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *buffer	buffer to store user data
    \param int BufferLength	input buffer length
    \param USERDATA_SECTION_INDEX usi	which user index data to select
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetUserData     (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, BYTE *buffer, int BufferLength, USERDATA_SECTION_INDEX usi);

/*! \fn int EtronDI_SetYOffset(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *buffer,
        int BufferLength,
        int *pActualLength,
        int index)
    \brief set Y offset values
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *buffer	buffer data to set
    \param int BufferLength	buffer length
    \param int *pActualLength	always return 256
    \param int index	index value to file ID 30
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetYOffset      (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, BYTE *buffer, int BufferLength, int *pActualLength, int index);

/*! \fn int EtronDI_SetRectifyTable(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *buffer,
        int BufferLength,
        int *pActualLength,
        int index)
    \brief set rectify values to flash
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *buffer	rectify values to set
    \param int BufferLength	bufer length, must be 1024
    \param int *pActualLength	always return 1024
    \param int index	index(from 0 ~ 9) to identify rectify table for corresponding depth
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetRectifyTable (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, BYTE *buffer, int BufferLength, int *pActualLength, int index);

/*! \fn int EtronDI_SetZDTable(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *buffer,
        int BufferLength,
        int *pActualLength,
        PZDTABLEINFO pZDTableInfo)
    \brief set disparity and Z values to flash
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *buffer	ZD values to set
    \param int BufferLength	corresponding length of ZD table in buffer
    \param int *pActualLength	buffer lenth written to flash, should be same as BufferLength
    \param PZDTABLEINFO pZDTableInfo	index and depth type of this ZD
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetZDTable      (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, BYTE *buffer, int BufferLength, int *pActualLength, PZDTABLEINFO pZDTableInfo);

/*! \fn int EtronDI_SetLogData(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *buffer,
        int BufferLength,
        int *pActualLength,
        int index)
    \brief set log data to flash
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *buffer	log data to set
    \param int BufferLength	buffer length, must be 4096
    \param int *pActualLength	always return 4096
    \param int index	index to identify log data for corresponding depth
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetLogData      (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, BYTE *buffer, int BufferLength, int *pActualLength, int index);

/*! \fn int EtronDI_SetUserData(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *buffer,
        int BufferLength,
        USERDATA_SECTION_INDEX usi)
    \brief set user data to flash
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *buffer	user buffer data to set
    \param int BufferLength	buffer length to write
    \param USERDATA_SECTION_INDEX usi	which user section data to set
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetUserData     (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, BYTE *buffer, int BufferLength, USERDATA_SECTION_INDEX usi);

/*! \fn int EtronDI_ReadFlashData(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        FLASH_DATA_TYPE fdt,
        BYTE *pBuffer,
        unsigned long int BufferLength,
        unsigned long int *pActualLength)
    \brief read firmware code(.bin) form flash
        The firmware code is the combination of boot loader, firmware body and plug-in data.
        This input buffer length has to match with the flash data type
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param FLASH_DATA_TYPE fdt	segment type of flash be read
    \param BYTE *pBuffer	buffer to store firmware code
    \param unsigned long int BufferLength	input buffer length
    \param unsigned long int *pActualLength	actual length has written to pBuffer
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_ReadFlashData   (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, FLASH_DATA_TYPE fdt,  
							  BYTE *pBuffer, unsigned long int BufferLength, unsigned long int *pActualLength);

/*! \fn int EtronDI_WriteFlashData(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        FLASH_DATA_TYPE fdt,
        BYTE *pBuffer,
        unsigned long int BufferLength,
        bool bIsDataVerify,
        KEEP_DATA_CTRL kdc)
    \brief write firmware code(.bin) to flash
        The firmware code is the combination of boot loader, firmware body and plug-in data,
        also can keep original functions(Serial Number, Sensor Position, RectificationTable, ZD Table
        and CalibrationLog) on camera flash by KEEP_DATA_CTRL control
    \param void *pHandleEtronDI	CEronDI class
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param FLASH_DATA_TYPE fdt	segment type of flash be wrote
    \param BYTE *pBuffer	buffer of firmware code
    \param unsigned long int BufferLength	Buffer length to be wrote
    \param BOOL bIsDataVerify	write data verification flag, if true this function will read data again
        and do a byte to byte comparison
    \param KEEP_DATA_CTRL kdc	keep function flags
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_WriteFlashData  (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, FLASH_DATA_TYPE fdt, BYTE *pBuffer, 
							  unsigned long int BufferLength, bool bIsDataVerify, KEEP_DATA_CTRL kdc);

/*! \fn int ETRONDI_API EtronDI_GetDevicePortType(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, USB_PORT_TYPE* pUSB_Port_Type)
\brief Get Device USB-port-type.
*/
int  EtronDI_GetDevicePortType(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, USB_PORT_TYPE* pUSB_Port_Type);
// File ID -

// image +

/*! \fn int EtronDI_GetDeviceResolutionList(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nMaxCount0,
        ETRONDI_STREAM_INFO *pStreamInfo0,
        int nMaxCount1,
        ETRONDI_STREAM_INFO *pStreamInfo1)
    \brief get the device resolution list
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nMaxCount0	max count of endpoint1 resolutions
    \param ETRONDI_STREAM_INFO *pStreamInfo0	resolution infos of endpoint1
    \param int nMaxCount1	max count of endpoint2 resolutions
    \param ETRONDI_STREAM_INFO *pStreamInfo1	resolutions infos of endpoint2
    \return success: EtronDI_OK, others: see eSPDI_def.h
 */
int  EtronDI_GetDeviceResolutionList(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, 
									  int nMaxCount, ETRONDI_STREAM_INFO *pStreamInfo0, 
                                      int nMaxCvoidount1, ETRONDI_STREAM_INFO *pStreamInfo1);

/*! \fn int EtronDI_Setup_v4l2_requestbuffers(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int cnt)
    \brief Setup v4l2 request buffers, default = 4
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int cnt Should be >= 0

    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_Setup_v4l2_requestbuffers(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int cnt);

/*! \fn int EtronDI_OpenDevice(
    void *pHandleEtronDI,
    PDEVSELINFO pDevSelInfo,
    int nEP0Width,
    int nEP0Height,
    bool bEP0MJPG,
    int nEP1Width,
    int nEP1Height,
    DEPTH_TRANSFER_CTRL dtc,
    bool bIsOutputRGB24,
    void *phWndNotice,
    int *pFPS,
    CONTROL_MODE cm)
    \brief the implement layer to open Etron camera device by V4L2(https://en.wikipedia.org/wiki/Video4Linux),
        can open color and depth at one time call, do functions as below,
        1. initialize the USB device by V4L2 protocol
          1.1 query device v4l2 capability
          1.2 must have video capability
          1.3 must have streaming capability
          1.4 issue resolution mode to UVC driver and check result
          1.5 initialize memory buffer mapping from kernel to user mode
        2. enumerate frame interval to set frame rate
        3. start video capture processes
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nEP0Width	width of endpoint1(color) resolution
    \param int nEP0Height	height of endpoint1(color) resolution
    \param bool bEP0MJPG	endpoint1 output is MJPEG ?
    \param int *pFPS	input frame rate setting
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_OpenDevice(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo,
                          int nEP0Width, int nEP0Height, bool bEP0MJPG,
                          int nEP1Width, int nEP1Height,
                          DEPTH_TRANSFER_CTRL dtc=DEPTH_IMG_NON_TRANSFER,
                          bool bIsOutputRGB24=false, void *phWndNotice=0,
                          int *pFPS=0, CONTROL_MODE cm=IMAGE_SN_NONSYNC);
                                     			
/*! \fn int EtronDI_OpenDevice2(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nEP0Width,
        int nEP0Height,
        bool bEP0MJPG,
        int nEP1Width,
        int nEP1Height,
        DEPTH_TRANSFER_CTRL dtc,
        bool bIsOutputRGB24,
        void *phWndNotice,
        int *pFPS,
        CONTROL_MODE cm)
    \brief the implement layer to open Etron camera device by V4L2(https://en.wikipedia.org/wiki/Video4Linux),
        can open color and depth at one time call, do functions as below,
        1. initialize the USB device by V4L2 protocol
          1.1 query device v4l2 capability
          1.2 must have video capability
          1.3 must have streaming capability
          1.4 issue resolution mode to UVC driver and check result
          1.5 initialize memory buffer mapping from kernel to user mode
        2. enumerate frame interval to set frame rate
        3. start video capture processes
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nEP0Width	width of endpoint1(color) resolution
    \param int nEP0Height	height of endpoint1(color) resolution
    \param bool bEP0MJPG	endpoint1 output is MJPEG ?
    \param int nEP1Width	width of endpoint2(depth) resolution
    \param int nEP1Height	height of endpoint2(depth) resolution
    \param DEPTH_TRANSFER_CTRL dtc	depth image output transfer
        1. default is transferred to color(DEPTH_IMG_COLORFUL_TRANSFER)
            by calling from EtronDI_OpenDevice()
        2. DEPTH_IMG_GRAY_TRANSFER : transfer to gray
        3. DEPTH_IMG_NON_TRANSFER : no transfer
    \param bool bIsOutputRGB24	output color image is RGB format
    \param void *phWndNotice	reserved, not use
    \param int *pFPS	input frame rate setting
    \param CONTROL_MODE cm	reserved, not use
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_OpenDevice2(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, 
						  int nEP0Width, int nEP0Height, bool bEP0MJPG, 
						  int nEP1Width, int nEP1Height, 
						  DEPTH_TRANSFER_CTRL dtc=DEPTH_IMG_NON_TRANSFER,
						  bool bIsOutputRGB24=false, void *phWndNotice=0, 
						  int *pFPS=0, CONTROL_MODE cm=IMAGE_SN_NONSYNC);	

/*! \fn int EtronDI_OpenDeviceMBL(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nEP0Width,
        int nEP0Height,
        bool bEP0MJPG,
        int nEP1Width,
        int nEP1Height,
        DEPTH_TRANSFER_CTRL dtc,
        bool bIsOutputRGB24,
        void *phWndNotice,
        int *pFPS,
        CONTROL_MODE cm)
    \brief the implement layer to open Multiple Base Line Etron camera device by V4L2(https://en.wikipedia.org/wiki/Video4Linux),
        can open color and depth at one time call, do functions as below,
        1. initialize the USB device by V4L2 protocol
          1.1 query device v4l2 capability
          1.2 must have video capability
          1.3 must have streaming capability
          1.4 issue resolution mode to UVC driver and check result
          1.5 initialize memory buffer mapping from kernel to user mode
        2. enumerate frame interval to set frame rate
        3. start video capture processes
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nEP0Width	width of endpoint1(color) resolution
    \param int nEP0Height	height of endpoint1(color) resolution
    \param bool bEP0MJPG	endpoint1 output is MJPEG ?
    \param int nEP1Width	width of endpoint2(depth) resolution
    \param int nEP1Height	height of endpoint2(depth) resolution
    \param DEPTH_TRANSFER_CTRL dtc	depth image output transfer
        1. default is transferred to color(DEPTH_IMG_COLORFUL_TRANSFER)
            by calling from EtronDI_OpenDevice()
        2. DEPTH_IMG_GRAY_TRANSFER : transfer to gray
        3. DEPTH_IMG_NON_TRANSFER : no transfer
    \param bool bIsOutputRGB24	output color image is RGB format
    \param void *phWndNotice	reserved, not use
    \param int *pFPS	input frame rate setting
    \param CONTROL_MODE cm	reserved, not use
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_OpenDeviceMBL(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo,
                          int nEP0Width, int nEP0Height, bool bEP0MJPG,
                          int nEP1Width, int nEP1Height,
                          DEPTH_TRANSFER_CTRL dtc=DEPTH_IMG_NON_TRANSFER,
                          bool bIsOutputRGB24=false, void *phWndNotice=0,
                          int *pFPS=0, CONTROL_MODE cm=IMAGE_SN_NONSYNC);


/*! \fn int EtronDI_CloseDeviceMBL(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo)
    \brief close Multiple Base Linedevice and free resource
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_CloseDeviceMBL(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int EtronDI_CloseDevice(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo)
    \brief close device and free resource
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_CloseDevice(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int EtronDI_CloseDeviceEx(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo)
    \brief close device and free resource for warm reset
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_CloseDeviceEx(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int EtronDI_GetImage(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *pBuf,
        unsigned long int *pImageSize,
        int *pSerial, int nDepthDataType)
    \brief get color or depth pin image
        by issuing V4L2's IOCTL to get frame data
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *pBuf	buffer to store image data
    \param unsigned long int *pImageSize	the actual buffer size getting from device
    \param int *pSerial	the serial number for synchronizing color and depth image
    \param int nDepthDataType	the depth data type, see definition in eSPDI_def.h
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetImage(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo,
                        BYTE *pBuf, unsigned long int *pImageSize,
                        int *pSerial = 0, int nDepthDataType =0);

/*! \fn int EtronDI_GetColorImage(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *pBuf,
        unsigned long int *pImageSize,
        int *pSerial, int nDepthDataType)
    \brief get color image
        by issuing V4L2's IOCTL to get frame data
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *pBuf	buffer to store image data
    \param unsigned long int *pImageSize	the actual buffer size getting from device
    \param int *pSerial	the serial number for synchronizing color and depth image
    \param int nDepthDataType reserved, no used.
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetColorImage(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo,
                        BYTE *pBuf, unsigned long int *pImageSize,
                        int *pSerial = 0, int nDepthDataType =0);

/*! \fn int EtronDI_GetDepthImage(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *pBuf,
        unsigned long int *pImageSize,
        int *pSerial, int nDepthDataType)
    \brief get depth image
        by issuing V4L2's IOCTL to get frame data
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *pBuf	buffer to store image data
    \param unsigned long int *pImageSize	the actual buffer size getting from device
    \param int *pSerial	the serial number for synchronizing color and depth image
    \param int nDepthDataType	the depth data type, see definition in eSPDI_def.h
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetDepthImage(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo,
                        BYTE *pBuf, unsigned long int *pImageSize,
                        int *pSerial = 0, int nDepthDataType =0);


/*! \fn int EtronDI_SetupBlock(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        bool enable)
    \brief get color or depth pin image
        by issuing V4L2's IOCTL to get frame data
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param bool enable Enable the Blocking mode or not)
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_SetupBlock(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, bool enable);

/*! \fn int EtronDI_Get_Color_30_mm_depth(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *pBuf,
        unsigned long int *pImageSize,
        int *pSerial, int nDepthDataType)
    \brief get color or depth pin image
        by issuing V4L2's IOCTL to get frame data
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *pBuf	buffer to store image data
    \param unsigned long int *pImageSize	the actual buffer size getting from device
    \param int *pSerial	the serial number for synchronizing color and depth image
    \param int nDepthDataType	the depth data type, see definition in eSPDI_def.h
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_Get_Color_30_mm_depth(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo,
                        BYTE *pBuf, unsigned long int *pImageSize,
                        int *pSerial = 0, int nDepthDataType =0);

/*! \fn int EtronDI_Get_60_mm_depth(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *pBuf,
        unsigned long int *pImageSize,
        int *pSerial, int nDepthDataType)
    \brief get color or depth pin image
        by issuing V4L2's IOCTL to get frame data
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *pBuf	buffer to store image data
    \param unsigned long int *pImageSize	the actual buffer size getting from device
    \param int *pSerial	the serial number for synchronizing color and depth image
    \param int nDepthDataType	the depth data type, see definition in eSPDI_def.h
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_Get_60_mm_depth(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo,
                        BYTE *pBuf, unsigned long int *pImageSize,
                        int *pSerial = 0, int nDepthDataType =0);

/*! \fn int EtronDI_Get_150_mm_depth(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *pBuf,
        unsigned long int *pImageSize,
        int *pSerial, int nDepthDataType)
    \brief get color or depth pin image
        by issuing V4L2's IOCTL to get frame data
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *pDepthImgBuf	buffer to store image data
    \param unsigned long int *pImageSize	the actual buffer size getting from device
    \param int *pDepthSerial	the serial number for synchronizing depth image
    \param int nDepthDataType	the depth data type, see definition in eSPDI_def.h
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_Get_150_mm_depth(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo,
                        BYTE *pBuf, unsigned long int *pImageSize,
                        int *pSerial = 0, int nDepthDataType =0);


/*! \fn int EtronDI_Get2Image(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE *pColorImgBuf,
        BYTE *pDepthImgBuf,
        unsigned long int *pColorImageSize,
        unsigned long int *pDepthImageSize,
        int *pColorSerial,
        int *pDepthSerial,
        int nDepthDataType)
    \brief get color and/or depth pin images
        see EtronDI_GetImage for detailed description
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE *pColorImgBuf	buffer to store color image
    \param BYTE *pDepthImgBuf	buffer to store depth image
    \param unsigned long int *pColorImageSize	the actual color buffer size
    \param unsigned long int *pDepthImageSize	the actual depth buffer size
    \param int *pColorSerial		color serial number
    \param int *pDepthSerial	depth serial number
    \param int nDepthDataType	the depth data type, see definition in eSPDI_def.h
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_Get2Image (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo,
                        BYTE *pColorImgBuf, BYTE *pDepthImgBuf,
                        unsigned long int *pColorImageSize, unsigned long int *pDepthImageSize,
                        int *pSerial = 0, int *pSerial2 = 0, int nDepthDataType =0);
// image -			

// for AEAWB Control +

/*! \fn int EtronDI_GetExposureTime(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nSensorMode,
        float *pfExpTimeMS)
    \brief get exposure time of ISP setting in millisecond
        the target sensor type was set in EtronDI_SetSensorTypeName()
    \param void *pHandleEtronDI	pHandleEtronDI
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nSensorMode	which sensor(sensor A, B or Both) to get
        A is 0, B is 1, Both is 2
    \param float *pfExpTimeMS	pointer of getting exposure time in millisecond
        by pixel clock, pixel per line, exposure line to get exposure time
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetExposureTime(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nSensorMode, float *pfExpTimeMS);

/*! \fnint EtronDI_SetExposureTime(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nSensorMode,
        float fExpTimeMS)
    \brief set exposure time of ISP sensor setting
        the target sensor type was set in EtronDI_SetSensorTypeName()
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nSensorMode	which sensor(sensor A, B or Both) to set
        A is 0, B is 1, Both is 2
    \param float fExpTimeMS	pointer of setting exposure time in millisecond
        check sensor spec for detailed setting,
        we need pixel clock, pixel per line, V blank and exposure line
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetExposureTime(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nSensorMode, float fExpTimeMS);

/*! \fn int EtronDI_GetGlobalGain(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nSensorMode,
        float *pfGlobalGain)
    \brief get global gain of ISP setting
        the target sensor type was set in EtronDI_SetSensorTypeName()
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nSensorMode	which sensor(sensor A, B or Both) to get
        A is 0, B is 1, Both is 2
    \param float *pfGlobalGain	pointer of global gain value
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetGlobalGain(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nSensorMode, float *pfGlobalGain);

/*! \fn int EtronDI_SetGlobalGain(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nSensorMode,
        float fGlobalGain)
    \brief set global gain of ISP sensor setting
        the target sensor type was set in EtronDI_SetSensorTypeName()
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nSensorMode	which sensor(sensor A, B or Both) to get
        A is 0, B is 1, Both is 2
    \param float fGlobalGain	pointer of global gain value
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetGlobalGain(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nSensorMode, float fGlobalGain);

/*! \fn int EtronDI_SetSensorTypeName(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        SENSOR_TYPE_NAME stn)
    \brief set the sensor type you want to work on
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param SENSOR_TYPE_NAME stn which sensor you want to work on
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetSensorTypeName(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, SENSOR_TYPE_NAME stn);

/*! \fn int EtronDI_GetColorGain(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nSensorMode,
        float *pfGainR,
        float *pfGainG,
        float *pfGainB)
    \brief get color gain of ISP setting
        the target sensor type was set in EtronDI_SetSensorTypeName()
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nSensorMode	which sensor(sensor A, B or Both) to get
        A is 0, B is 1, Both is 2
    \param float *pfGainR	pointer of red gain value of ISP setting
    \param float *pfGainG	pointer of green gain value of ISP setting
    \param float *pfGainB	pointer of blue gain value of ISP setting
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetColorGain(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nSensorMode, float *pfGainR, float *pfGainG, float *pfGainB);

/*! \fn int EtronDI_SetColorGain(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nSensorMode,
        float fGainR,
        float fGainG,
        float fGainB)
    \brief set color gain of ISP
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nSensorMode	which sensor(sensor A, B or Both) to get
        A is 0, B is 1, Both is 2
    \param float fGainR	Red channel color gain value
    \param float fGainG	Green channel color gain value
    \param float fGainB	Blue channel color gain value
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetColorGain(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nSensorMode, float fGainR, float fGainG, float fGainB);
//+[Thermal device]
bool EtronDI_GetThermalFD(void *pHandleEtronDI,int *p_FD);
//-[Thermal device]

#ifndef DOXYGEN_SHOULD_SKIP_THIS

int  EtronDI_GetAccMeterValue(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int *pX, int *pY, int *pZ);
#endif

/*! \fn int EtronDI_EnableAE(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo)
    \brief enable auto exposure(AE) function of ISP
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_EnableAE     (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int EtronDI_DisableAE(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo)
    \brief disable auto exposure(AE) function of ISP
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_DisableAE    (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int EtronDI_EnableAWB(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo)
    \brief enable auto white balance function of ISP
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_EnableAWB    (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int EtronDI_DisableAWB(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo)
    \brief disable auto white balance of ISP
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_DisableAWB   (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int EtronDI_GetAEStatus(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        PAE_STATUS pAEStatus)
    \brief get auto exposure(AE) is enabled or disable
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param PAE_STATUS pAEStatus	see enum definition as to AE_STATUS in eSPDI_def.h
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetAEStatus (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, PAE_STATUS pAEStatus);

/*! \fn int EtronDI_GetAWBStatus(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        PAWB_STATUS pAWBStatus)
    \brief get auto white balance(AWB) is enabled or disable
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param PAWB_STATUS pAWBStatus	see enum definition as to AWB_STATUS in eSPDI_def.h
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetAWBStatus (void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, PAWB_STATUS pAWBStatus);

/*! \fn int EtronDI_GetGPIOValue(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nGPIOIndex, BYTE *pValue)
    \brief get GPIO values
*/
int  EtronDI_GetGPIOValue(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nGPIOIndex, BYTE *pValue);

/*! \fn int EtronDI_SetGPIOValue(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nGPIOIndex,
        BYTE nValue)
    \brief set GPIO values
*/
int  EtronDI_SetGPIOValue(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nGPIOIndex, BYTE nValue);

/*! \fn int EtronDI_SetGPIOCtrl(
    void *pHandleEtronDI,
    PDEVSELINFO pDevSelInfo,
    int nGPIOIndex,
    BYTE nValue)
    \brief set GPIO I/O control

*/
int  EtronDI_SetGPIOCtrl(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nGPIOIndex, BYTE nValue);

/*! \fn int EtronDI_GetCTPropVal(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nId,
        long int *pValue)
    \brief get camera terminal(CT) property value
        By v4l2_control to get control value of camera terminal

        this enumeration contained the following properties:
        V4L2_CID_EXPOSURE_AUTO;
        V4L2_CID_EXPOSURE_AUTO_PRIORITY
        V4L2_CID_EXPOSURE_ABSOLUTE
        V4L2_CID_EXPOSURE
        V4L2_CID_FOCUS_ABSOLUTE
        V4L2_CID_FOCUS_RELATIVE
        V4L2_CID_FOCUS_AUTO
        V4L2_CID_IRIS_ABSOLUTE
        V4L2_CID_IRIS_RELATIVE
        V4L2_CID_ZOOM_ABSOLUTE
        V4L2_CID_ZOOM_RELATIVE
        V4L2_CID_PAN_ABSOLUTE
        V4L2_CID_PAN_RELATIVE
        V4L2_CID_TILT_ABSOLUTE
        V4L2_CID_TILT_RELATIVE
        V4L2_CID_PRIVACY
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nId	specifies the member of the property set,
        see CT Property ID defined in eSPDI_def.h
    \param int *pValue	pointer of store CT property value
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetCTPropVal(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nId, long int *pValue);

/*! \fn int EtronDI_SetCTPropVal(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nId,
        long int nValue)
    \brief set camera terminal property values
        By v4l2_control to set
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nId	specifies the member of the property set
        see CT Property ID defined in eSPDI_def.h
    \param long int nValue	CT property value to set
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetCTPropVal(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nId, long int nValue);

/*! \fn int EtronDI_GetPUPropVal(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nId,
        long int *pValue)
    \brief get processing unit property value
        by v4l2_control to get processing unit(PU) property value

        this enumeration contained the following properties:
        V4L2_CID_BACKLIGHT_COMPENSATION
        V4L2_CID_BRIGHTNESS
        V4L2_CID_CONTRAST
        V4L2_CID_GAIN
        V4L2_CID_POWER_LINE_FREQUENCY
        V4L2_CID_HUE
        V4L2_CID_HUE_AUTO
        V4L2_CID_SATURATION
        V4L2_CID_SHARPNESS
        V4L2_CID_GAMMA
        V4L2_CID_WHITE_BALANCE_TEMPERATURE
        V4L2_CID_AUTO_WHITE_BALANCE
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nId	specifies the member of the property set
        see PU property ID defined in eSPDI_def.h
    \param long int *pValue	pointer of store PU property value
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetPUPropVal(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nId, long int *pValue);

/*! \fn int EtronDI_SetPUPropVal(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int nId,
        long int nValue)
    \brief set processing unit property value
        by v4l2_control to set processing unit(PU) property value
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nId	specifies the member of the property set
        see PU Property ID defined in eSPDI_def.h
    \param int nValue	value to set
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_SetPUPropVal(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nId, long int nValue);

/*! \fn int EtronDI_GetCTRangeAndStep(
        void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nId, int *pMax, int *pMin, int *pStep, int *pDefault, int *pFlags)
    \brief set camera terminal property values
        By v4l2_queryctrl to get control values of camera terminal(CT)
        this enumeration contained the following properties:
        V4L2_CID_EXPOSURE_AUTO
        V4L2_CID_EXPOSURE_AUTO_PRIORITY
        V4L2_CID_EXPOSURE_ABSOLUTE
        V4L2_CID_EXPOSURE
        V4L2_CID_FOCUS_ABSOLUTE
        V4L2_CID_FOCUS_RELATIVE
        V4L2_CID_FOCUS_AUTO
        V4L2_CID_IRIS_ABSOLUTE
        V4L2_CID_IRIS_RELATIVE
        V4L2_CID_ZOOM_ABSOLUTE
        V4L2_CID_ZOOM_RELATIVE
        V4L2_CID_PAN_ABSOLUTE
        V4L2_CID_PAN_RELATIVE
        V4L2_CID_TILT_ABSOLUTE
        V4L2_CID_TILT_RELATIVE
        V4L2_CID_PRIVACY
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nId	specifies the member of the property set,
        see CT Property ID defined in eSPDI_def.h
    \param long int *pMax	maximum value, inclusive.
        This field gives an upper bound for the control
    \param long int *pMin	minimum value, inclusive.
        This field gives a lower bound for the control
    \param long int *pStep	This field gives a step size for the control
        see enum https://www.linuxtv.org/downloads/v4l-dvb-apis-old/vidioc-queryctrl.html#v4l2-ctrl-type
        how the step value is to be used for each possible control type. Note that this an unsigned 32-bit value
    \param long int *pDefault	The default value of a V4L2_CTRL_TYPE_INTEGER, _BOOLEAN, _BITMASK,
        _MENU or _INTEGER_MENU control. Not valid for other types of controls.
        Note that drivers reset controls to their default value only when the driver is first loaded, never afterwards.
    \param long int *pFlags	control flags,
        see https://www.linuxtv.org/downloads/v4l-dvb-apis-old/vidioc-queryctrl.html#control-flags
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetCTRangeAndStep(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nId, int *pMax, int *pMin, int *pStep, int *pDefault, int *pFlags);

/*! \fn int EtronDI_GetPURangeAndStep(
    void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nId, int *pMax, int *pMin, int *pStep, int *pDefault, int *pFlags)
    \brief get processing unit property value
        By v4l2_queryctrl to get property values of processing unit(PU)
        this enumeration contained the following properties:
        V4L2_CID_BACKLIGHT_COMPENSATION
        V4L2_CID_BRIGHTNESS
        V4L2_CID_CONTRAST
        V4L2_CID_GAIN
        V4L2_CID_POWER_LINE_FREQUENCY
        V4L2_CID_HUE
        V4L2_CID_HUE_AUTO
        V4L2_CID_SATURATION
        V4L2_CID_SHARPNESS
        V4L2_CID_GAMMA
        V4L2_CID_WHITE_BALANCE_TEMPERATURE
        V4L2_CID_AUTO_WHITE_BALANCE
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param int nId	nId	specifies the member of the property set,
        see CT Property ID defined in eSPDI_def.h
    \param long int *pMax	maximum value, inclusive.
        This field gives an upper bound for the control
    \param long int *pMin	minimum value, inclusive.
        This field gives a lower bound for the control
    \param long int *pStep	This field gives a step size for the control
        see enum https://www.linuxtv.org/downloads/v4l-dvb-apis-old/vidioc-queryctrl.html#v4l2-ctrl-type
        how the step value is to be used for each possible control type. Note that this an unsigned 32-bit value
    \param long int *pDefault	The default value of a V4L2_CTRL_TYPE_INTEGER, _BOOLEAN, _BITMASK,
        _MENU or _INTEGER_MENU control. Not valid for other types of controls.
        Note that drivers reset controls to their default value only when the driver is first loaded, never afterwards.
    \param long int *pFlags	control flags,
        see https://www.linuxtv.org/downloads/v4l-dvb-apis-old/vidioc-queryctrl.html#control-flags
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetPURangeAndStep(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int nId, int *pMax, int *pMin, int *pStep, int *pDefault, int *pFlags);

// for AEAWB Control -		

// for depth data type selection +

/*! \fn EtronDI_SetDepthDataType(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short nValue)
    \brief set depth data type, 11 bit for disparity data, 14 bit for Z data
        notice: only PUMA type IC can support this setting
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short nValue	depth data type you want to set,
        see ETronDI_DEPTH_DATA_xxx in eSPDI_def.h
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_SetDepthDataType(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short nValue);

/*! \fn int EtronDI_GetDepthDataType(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short *pValue)
    \brief get current depth data type setting
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param WORD *pValue	pointer of current depth data type in device
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_GetDepthDataType(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short *pValue);
// for depth data type selection -

// IR support

/*! \fn t EtronDI_SetCurrentIRValue(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short nValue)
    \brief set infrared radiation(IR) value of PUMA type IC
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short nValue	1 byte IR value to set
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_SetCurrentIRValue(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short nValue);

/*! \fn int EtronDI_GetCurrentIRValue(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short *pValue)
    \brief get infrared radiation(IR) value of PUMA type IC
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short *pValue	current 1 byte IR value setting
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_GetCurrentIRValue(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short *pValue);

/*! \fn int EtronDI_GetIRMinValue(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short *pValue)
    \brief get minimum IR value of camera module
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short *pValue	the minimum 1 byte IR value can be set
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_GetIRMinValue(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short *pValue);

/*! \fn int EtronDI_GetIRMaxValue(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short nValue)
    \brief get maximum IR value of camera module
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short nValue	the IR maximum setting value
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_SetIRMaxValue(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short nValue);

/*! \fn int EtronDI_GetIRMaxValue(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short *pValue)
    \brief get maximum IR value of camera module
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short *pValue	the maximum 1 byte IR value can be set
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_GetIRMaxValue(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short *pValue);

/*! \fn EtronDI_SetIRMode(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short nValue)
    \brief enable or disable IRs
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short nValue	8 bit definition as below to turn on/off IR
        D[7:4]: Reserved
        D3: Channel 3
        D2: Channel 2
        D1: Channel 1
        D0: Channel 0
        1: Enable Channel
        0: Disable Channel
        If want to control ch0 and ch1, ubMode[3:0] must set to 0x03
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_SetIRMode(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short nValue);

/*! \fn int EtronDI_GetIRMode(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short *pValue)
    \brief to check IR is turn on or off
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param unsigned short *pValue	get IR was enabled or not
        D[7:4]: Reserved
        D3: Channel 3
        D2: Channel 2
        D1: Channel 1
        D0: Channel 0
        1: Enable Channel
        0: Disable Channel
        If want to control ch0 and ch1, ubMode[3:0] must set to 0x03
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_GetIRMode(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short *pValue);
// ~IR support

// for Calibration Log +

/*! \fn int EtronDI_GetRectifyLogData(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        eSPCtrl_RectLogData *pData,
        int index)
    \brief get rectify log data from flash, just for AXES1 device type
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param eSPCtrl_RectLogData *pData	4096 bytes of rectify log data,
        see eSPCtrl_RectLogData for detailed members
    \param index, user data section from 0 ~ 9
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetRectifyLogData(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, eSPCtrl_RectLogData *pData, int index);

/*! \fn int EtronDI_GetRectifyMatLogData(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        eSPCtrl_RectLogData *pData,
        int index)
    \brief get rectify log data from flash, just for PUMA device type
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param eSPCtrl_RectLogData *pData 4096 bytes of rectify log data,
        see eSPCtrl_RectLogData for detailed members
    \param index, user data section from 0 ~ 9
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_GetRectifyMatLogData(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, eSPCtrl_RectLogData *pData, int index);
// for Calibration Log -
// for Post Process +
#ifndef DOXYGEN_SHOULD_SKIP_THIS
/*! \fn int EtronDI_EnablePostProcess(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        bool bEnable)
    \brief Not support now.
*/
int  EtronDI_EnablePostProcess(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, bool bEnable);

/*! \fn int EtronDI_PostInitial(
        void *pHandleEtronDI)
    \brief Not support now.
*/
int  EtronDI_PostInitial(void *pHandleEtronDI);

/*! \fn int EtronDI_PostEnd(
        void *pHandleEtronDI)
    \brief Not support now.
*/
int  EtronDI_PostEnd(void *pHandleEtronDI);

/*! \fn int EtronDI_ProcessFrame(
        void *pHandleEtronDI,
        unsigned char *pYUY2Buf,
        unsigned char *pDepthBuf,
        unsigned char *OutputBuf,
        int width,
        int height)
    \brief Not support now.
*/
int  EtronDI_ProcessFrame(void *pHandleEtronDI, unsigned char *pYUY2Buf, unsigned char *pDepthBuf, unsigned char *OutputBuf, int width, int height);

/*! \fn int EtronDI_PostSetParam(
        void *pHandleEtronDI,
        int Idx,
        int Val)
    \brief Not support now.
*/
int  EtronDI_PostSetParam(void *pHandleEtronDI, int Idx, int Val);	

/*! \fn int EtronDI_PostGetParam(
        void *pHandleEtronDI,
        int Idx,
        int *pVal)
    \brief Not support now.
*/
int  EtronDI_PostGetParam(void *pHandleEtronDI, int Idx, int *pVal);	
#endif

/*! \fn int EtronDI_CreateSwPostProc(
    int depthBits,
    void **handle)
    \brief create a software post process class
    \param int depthBits	depth bit to set
    \param void **handle	handle pointer to this software post process class
    \return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int EtronDI_CreateSwPostProc(int depthBits, void **handle);

/*! \fn int EtronDI_ReleaseSwPostProc(void** handle)
    \brief release a software post process class
    \param void** handle	handle pointer to this software post process class
    \return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int EtronDI_ReleaseSwPostProc(void** handle);

/*! \fn int EtronDI_DoSwPostProc(void* handle, unsigned char* colorBuf, bool isColorRgb24, unsigned char* depthBuf, unsigned char* outputBuf, int width, int height)
    \brief do software post process on a depth buffer
    \param void* handle	handle of this software post process class
    \param unsigned char* colorBuf	input color buffer
    \param bool isColorRgb24	is this color buffer RGB888
    \param unsigned char* depthBuf	input depth buffer
    \param unsigned char* outputBuf	output buffer
    \param int width	image width
    \param int height	image height
    \return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int EtronDI_DoSwPostProc(void *pHandleEtronDI, unsigned char* colorBuf, bool isColorRgb24,
    unsigned char* depthBuf, unsigned char* outputBuf, int width, int height);

/*! \fn int EtronDI_FlyingDepthCancellation_D8(
    unsigned char *pdepthD8,
    int width,
    int height)
    \brief Flying Pixcel Depth Cancellation, just for EX8029
    \param unsigned char *pdepthD8	point toinput  depth buffer
    \param int width depth width
    \param int height depth height
    \return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int EtronDI_FlyingDepthCancellation_D8(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char *pdepthD8, int width, int height);

/*! \fn int EtronDI_FlyingDepthCancellation_D11(
    unsigned char *pdepthD11,
    int width,
    int height)
    \brief Flying Pixcel Depth Cancellation
    \param unsigned char *pdepthD11	point toinput  depth buffer
    \param int width depth width
    \param int height depth height
    \return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int EtronDI_FlyingDepthCancellation_D11( void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* pdepthD11, int width, int height );

/*! \fn int EtronDI_Convert_Depth_Y_To_Buffer(
                void *pHandleEtronDI,
                PDEVSELINFO pDevSelInfo,
                unsigned char *depth_y,
                unsigned char *rgb,
                unsigned int width,
                unsigned int height,
                bool color,
                unsigned short nDepthDataType)
        \brief Convert Depth to RGB color or gray
        \param void *pHandleEtronDI     CEtronDI handler
        \param PDEVSELINFO pDevSelInfo  pointer of device select index
        \param unsigned char *depth_y   depth data,
        \param unsigned char *rgb               output data,
        \param int width                                image width,
        \param int height                               image height,
        \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_Convert_Depth_Y_To_Buffer(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char *depth_y, unsigned char *rgb, unsigned int width, unsigned int height, bool color, unsigned short nDepthDataType);

/*! \fn int EtronDI_Convert_Depth_Y_To_Buffer_offset(
                void *pHandleEtronDI,
                PDEVSELINFO pDevSelInfo,
                unsigned char *depth_y,
                unsigned char *rgb,
                unsigned int width,
                unsigned int height,
                bool color,
                unsigned short nDepthDataType,
                int offset)
        \brief Convert Depth to RGB color or gray, added offset for 3cm baseline
        \param void *pHandleEtronDI     CEtronDI handler
        \param PDEVSELINFO pDevSelInfo  pointer of device select index
        \param unsigned char *depth_y   depth data,
        \param unsigned char *rgb               output data,
        \param int width                                image width,
        \param int height                               image height,
        \param int offset                               dpeth_y offset,
        \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_Convert_Depth_Y_To_Buffer_offset(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char *depth_y, unsigned char *rgb, unsigned int width, unsigned int height, bool color, unsigned short nDepthDataType, int offset);
// for Post Process -
// for sensorif +

/*! \fn int EtronDI_EnableSensorIF(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        bool bIsEnable)
    \brief enable or disable sensor IF
    \param void *pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param bool bIsEnable	true is enable, false is disable
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int  EtronDI_EnableSensorIF(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, bool bIsEnable);
// for sensorif -

#ifndef __WEYE__ 
// for Gyro +
#ifndef UAC_NOT_SUPPORTED

/*! \fn int EtronDI_getUACNAME(char *input, char *output)
    \brief Get Etron UAC Name
    \param char *input Point to device Address.
    \param char *output Point to device Name.
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_getUACNAME(char *input, char *output);

/*! \fn int EtronDI_InitialUAC(
        char *deviceName)
    \param char *deviceName Point to device Name.
    \brief UAC inital function
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_InitialUAC(char *deviceName);

/*! \fn int EtronDI_WriteWaveHeader(
        int fd)
    \brief Write Wave Header
    \param int fd wave file descript.
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_WriteWaveHeader(int fd);

/*! \fn int EtronDI_WriteWaveEnd(
        int fd, size_t length)
    \brief Modified Wave Header
    \param int fd wave file descript.
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_WriteWaveEnd(int fd, size_t length);

/*! \fn int EtronDI_GetUACData(
        unsigned char *buffer,
        int length)
    \brief UAC inital function
    \param unsigned char *buffer pointer of UAC buffer
    \param int length UAC buffer length
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_GetUACData(unsigned char *buffer, int length);

/*! \fn int EtronDI_ReleaseUAC(
    void)
    \brief UAC inital function
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_ReleaseUAC(void);
#endif //UAC_NOT_SUPPORTED

/*! \fn int EtronDI_InitialFlexibleGyro(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo)
    \brief gyro sensor inital function
    \param void* pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_InitialFlexibleGyro(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int EtronDI_ReleaseFlexibleGyro(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo)
    \brief gyro sensor release function
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/

int EtronDI_ReleaseFlexibleGyro(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int EtronDI_GetFlexibleGyroData(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        int length,
        unsigned char *pGyroData)
    \brief getting gyro data function
    \param void* pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo  pointer of device select index
    \param int length  Gyro Data Length
    \param unsigned char *pGyroData  pointer of Gyro Data.
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_GetFlexibleGyroData(void* pHandleEtronDI,PDEVSELINFO pDevSelInfo, int length, unsigned char* pGyroData);

/*! \fn int EtronDI_GetFlexibleGyroLength(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short* GyroLen)
    \brief getting length of gyro data function.
    \param void* pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo  pointer of device select index
    \param unsigned short* GyroLen  pointer of Gyro Data Lenhth.
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_GetFlexibleGyroLength(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short* GyroLen);

/*! \fn int EtronDI_GetImageInterrupt()
    \brief Get Image interrupt function
        Get the image interrupt and then read Gyro data.
    \return success: 0, others: not got interrupt
*/
int EtronDI_GetImageInterrupt(void);

/*! \fn int EtronDI_InitialHidGyro(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo)
    \brief gyro sensor inital function
    \param void* pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_InitialHidGyro(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int EtronDI_ReleaseHidGyro(
        void* pHandleEtronDI,
        PDEVSELINFO pDevSelInfo)
    \brief gyro sensor release function
    \param void* pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/

int EtronDI_ReleaseHidGyro(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int EtronDI_GetHidGyro(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned char *pBuffer,
        int length)
    \brief getting gyro data function
    \param void* pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo  pointer of device select index
    \param unsigned char *pGyroData  pointer of Gyro Data Buffer.
    \param int length  Input buffer Length, should be >= 24
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_GetHidGyro(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char *pBuffer, int length);

/*! \fn int EtronDI_SetupHidGyro(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned char *pCmdBuf,
        int cmdlength)
    \brief getting gyro data function
    \param void* pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo  pointer of device select index
    \param unsigned char *pGyroData  pointer of Gyro Data Buffer.
    \param int length  Input buffer Length, shoul
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_SetupHidGyro(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char *pCmdBuf, int cmdlength);

/*! \fn int EtronDI_GetInfoHidGyro(
        void *pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned char *pCmdBuf,
        int cmdlength,
        unsigned char *pResponseBuf,
        int *resplength)
    \brief getting gyro data function
    \param void* pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo  pointer of device select index
    \param unsigned char *pCmdBuf  pointer of Gyro Cmd Buffer.
    \param int cmdlength Command Lehgth.
    \param unsigned char *pResponseBuf  pointer of ResponseBuffer.
    \param int resplength Response Length
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_GetInfoHidGyro(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char *pCmdBuf, int cmdlength, unsigned char *pResponseBuf, int *resplength);
#endif //__WEYE__
// for Gyro -


#ifndef TINY_VERSION

/*! \fn int EtronDI_GenerateLutFile(
        void* pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        const char* filename)
    \brief generate look up table(LUT) for spherical display
        this function reads the camera user data and generate a LUT file using for 360 degree preview
    \param void* pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param const char* filename	output LUT file name
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_GenerateLutFile(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo, const char* filename);

/*! \fn int EtronDI_SaveLutData(
        void* pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        const char* filename)
    \brief Save LUT parameters in the specified file
    \param void* pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param const char* filename	output LUT file name
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_SaveLutData(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo, const char* filename);

/*! \fn int EtronDI_GetLutData(
        void* pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        BYTE* buffer, int nSize)
    \brief Read LUT parameters into the specified buffer
    \param void* pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param BYTE* buffer	memory to store LUT data
    \param int nSize  length of buffer in bytes
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_GetLutData(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo, BYTE* buffer, int nSize);

/*! \fn int EtronDI_EncryptMP4(
        void* pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        const char *filename)
    \brief encrypt a H.264 video
    \param void* pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param const char *filename	the input video file for encryption
    \return success: EtronDI_OK, others:see En-Decrypt.h
*/
int EtronDI_EncryptMP4(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo, const char* filename);

/*! \fn int EtronDI_DecryptMP4(
        void* pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        const char* filename)
    \brief decrypt a H.264 video was generated by EtronDI_EncryptMP4()
    \param void* pHandleEtronDI	CEtronDI handler
    \param PDEVSELINFO pDevSelInfo	pointer of device select index
    \param const char *filename	the input video file for decryption
    \return success: EtronDI_OK, others:see En-Decrypt.h
*/
int EtronDI_DecryptMP4(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo, const char* filename);
} // end of extern "C" 01
#ifndef DOXYGEN_SHOULD_SKIP_THIS

int EtronDI_InjectExtraDataToMp4(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo, 
		const char* filename, const char* data, int dataLen);
int EtronDI_RetrieveExtraDataFromMp4(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo, 
		const char* filename, char* data, int* dataLen);
int EtronDI_EncryptString(const char* src, char* dst);
int EtronDI_DecryptString(const char* src, char* dst);
int EtronDI_EncryptString(const char* src1, const char* src2, char* dst);
int EtronDI_DecryptString(const char* src, char* dst1, char* dst2);
#endif

#endif //TINY_VERSION

/*! \fn int EtronDI_GetAutoExposureMode(
        void* pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short *mode)
    \brief Get Auto Exposure Mode.
    \param void* pHandleEtronDI	CEtronDI handler.
    \param PDEVSELINFO pDevSelInfo	pointer of device select index.
    \param unsigned short* mode	pointer of the mode value.
    0: Average,
    1: Left (or Front) camera,
    2: Right (or Back) camera
    \return success: EtronDI_OK, others:eSPDI_def.h
*/
extern "C" {
int EtronDI_GetAutoExposureMode(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short* mode);

/*! \fn int EtronDI_SetAutoExposureMode(
        void* pHandleEtronDI,
        PDEVSELINFO pDevSelInfo,
        unsigned short mode)
    \brief Setup Auto Exposure Mode.
    \param void* pHandleEtronDI	CEtronDI handler.
    \param PDEVSELINFO pDevSelInfo	pointer of device select index.
    \param unsigned short mode The setup mode value.
    0: Average,
    1: Left (or Front) camera,
    2: Right (or Back) camera
    \return success: EtronDI_OK, others:eSPDI_def.h
*/
int EtronDI_SetAutoExposureMode(void* pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned short mode);
/*! \fn int EtronDI_RotateImg90(
    EtronDIImageType::Value imgType, int width, int height,
        unsigned char *src, unsigned char *dstBuf, int len, bool clockwise)
    \brief Rotate the image to 90 degree.
    \param EtronDIImageType::Value mgType Image Type
    \param int width image width
    \param int height image height
    \param unsigned char *src image source
    \param unsigned char *dstBuf image desteration
    \param int len desteration buffer length
    \param bClockwise, false not supported.
    \param bOpencv useage, not supported.
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_RotateImg90(EtronDIImageType::Value imgType, int width, int height, unsigned char *src, unsigned char *dst, int len, bool clockwise);

/*! \fn int EtronDI_RotateImg180(
    EtronDIImageType::Value imgType, int width, int height,
        unsigned char *src, unsigned char *dstBuf, int len)
    \brief Rotate the image to 180 degree.
    \param EtronDIImageType::Value mgType Image Type
    \param int width image width
    \param int height image height
    \param unsigned char *src image source
    \param unsigned char *dstBuf image desteration
    \param int len desteration buffer length
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_RotateImg180(EtronDIImageType::Value imgType, int width, int height,unsigned char *src, unsigned char *dst, int len);

/*! \fn int EtronDI_ResizeImgToHalf(
        EtronDIImageType::Value imgType, int width, int height,
            unsigned char *src, unsigned char *dst, int len)
    \brief Resize the image to half.
    \param EtronDIImageType::Value mgType Image Type
    \param int width image width
    \param int height image height
    \param unsigned char *src image source
    \param unsigned char *dst image desteration
    \param int len desteration buffer length
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_ResizeImgToHalf(EtronDIImageType::Value imgType, int width, int height, unsigned char *src, unsigned char *dst, int len);

/*! \fn int EtronDI_ImgMirro(
    EtronDIImageType::Value imgType, int width, int height,
        unsigned char *src, unsigned char *dstBuf)
    \brief Make the image to Mirro.
    \param EtronDIImageType::Value imgType Image Type
    \param int width image width
    \param int height image height
    \param unsigned char *src image source
    \param unsigned char *dstBuf image desteration
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_ImgMirro(EtronDIImageType::Value imgType, int width, int height, unsigned char *src, unsigned char *dst);

/*! \fn int EtronDI_RGB2BMP(
    char *filename, int width, int height, unsigned char *data)
    \brief RGB to BMP.
    \param *filename Ouput BMP file name
    \param int width image width
    \param int height image height
    \param *data input RGB buffer.
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_RGB2BMP(char *filename, int width, int height, unsigned char *data);

/*! \fn int EtronDI_HoleFilled(
     unsigned short *pDImgIn, unsigned short *pDImgOut, int width, int height, int holeFilldiff)
    \brief Hole Filled.
    \param unsigned short *pDImgIn Image Input
    \param unsigned short *pDImgOut Image Output
    \param int width image width
    \param int height image height
    \param int holeFilldiff Hole filled strangth, value from 0 to 2047.
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_HoleFilled(unsigned short *pDImgIn, unsigned short *pDImgOut, int width, int height, int holeFilldiff);

/*! \fn int EtronDI_InitialCmdFiFo(
        const char *pfifoName,
        int *pFileDescrption,
        bool bRead)
    \brief Cmd FiFo Initial function
    \param const char *pfifoName Point to the cmd fifo name
    \param int *pFileDescrption Point to the file description
    \param bRead Indicate Read or Write Cmd fifo
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_InitialCmdFiFo(const char *pfifoName, int *pFileDescrption, bool bRead);

/*! \fn int EtronDI_CloseCmdFiFo(
        int FileDescrption)
    \brief Cmd FiFo Close function
    \param int FileDescrption  File Description
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_CloseCmdFiFo(int FileDescrption);

/*! \fn int EtronDI_WriteCmdFiFo(
        int FileDescrption,
        unsigned char *pCmd,
        int len)
    \brief Write Cmd FiFo function
    \param int FileDescrption File description
    \param unsigned char *pCmd Point to the cmd buffer
    \param int lenIndicate the cmd lemgth.
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_WriteCmdFiFo(int FileDescrption, unsigned char *pCmd, int len);

/*! \fn EtronDI_ReadCmdFiFo(
        int FileDescrption,
        unsigned char *pBuf,
        int len)
    \brief Read Cmd FiFo function
    \param int FileDescrption File description
    \param unsigned char *pCmd Point to the cmd buffer
    \param int lenIndicate the cmd lemgth.
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_ReadCmdFiFo(int FileDescrption, unsigned char *pBuf, int len);

/*! \fn int EtronDI_InitSRB(void **pSrbHandle,
        int QueueSize,
        char *queueName)
    \brief Inital the SRB(Share Ring Buffering)
    \param void **pSrbHandle a pointer of pointer to SRB class
    \param int QueueSize
    \param char srbName SRM Name
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_InitSRB(void **pSmbHandle, int QueueSize, char *queueName);

/*! \fn int EtronDI_PutSRB(void *pSrbHandle,
       srb_packet_s *pPacket)
    \brief Put Packet to SRB
    \param void *pSrbHandle pointer to SRB class
    \param packet_s *pPacket Input Packet
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_PutSRB(void *pSmbHandle, srb_packet_s *pPacket);

/*! \fn int EtronDI_GetSRB(void *pSrbHandle,
       srb_packet_s *pPacket)
    \brief Get Packet from SRB
    \param void *pSrbHandle pointer to SRB class
    \param packet_s *pPacket Input Packet
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_GetSRB(void *pSmbHandle, srb_packet_s *pPacket);


/*! \fn int EtronDI_DepthMerge(
void *pHandleEtronDI,
PDEVSELINFO pDevSelInfo)
    \brief enable or disable interleave function
    \param pHandleEtronDI	 the pointer to the initilized EtronDI SDK instance
    \param pDevSelInfo	pointer of device select index
    \return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int EtronDI_DepthMerge( void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char** pDepthBufList, float *pDepthMergeOut,
    unsigned char *pDepthMergeFlag, int nDWidth, int nDHeight, float fFocus, float * pBaseline, float * pWRNear, float * pWRFar, float * pWRFusion, int nMergeNum );

/*! \fn int EtronDI_EnableSerialCount(
void *pHandleEtronDI,
PDEVSELINFO pDevSelInfo)
    \brief enable or disable interleave function
    \param pHandleEtronDI	 the pointer to the initilized EtronDI SDK instance
    \param pDevSelInfo	pointer of device select index
    \param ImgColor	RGB-buffer
    \param CW	ImgColor width
    \param CH	ImgColor height
    \param ImgDepth	depth-buffer
    \param DW	ImgDepth width
    \param DH	ImgDepth height
    \param pPointCloudInfo	point-cloud information
    \param pPointCloudRGB	point-cloud RGB value
    \param pPointCloudXYZ	point-cloud XYZ value
    \param Near	filter range near dist.
    \param Far	filter range far dist.
    \return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int EtronDI_GetPointCloud( void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* ImgColor, int CW, int CH,
                           unsigned char* ImgDepth, int DW, int DH,
                           PointCloudInfo* pPointCloudInfo,
                           unsigned char* pPointCloudRGB, float* pPointCloudXYZ, float Near, float Far );

/*! \fn int EtronDI_ColorFormat_to_RGB24(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* ImgDst, unsigned char* ImgSrc, int width, int height, EtronDIImageType::Value type)
    \brief get hardware post processing status
    \param pHandleEtronDI	 the pointer to the initilized EtronDI SDK instance
    \param pDevSelInfo	pointer of device select index
    \param ImgDst 	output image buffer
    \param ImgSrc	input  image buffer
    \param width	input  image width
    \param height	input  image height
    \param type     input  image-format
    \return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int EtronDI_ColorFormat_to_RGB24( void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* ImgDst, unsigned char* ImgSrc, int SrcSize, int width, int height, EtronDIImageType::Value type );
} // end of extern "C" 02
int EtronDI_RotateImg90(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, EtronDIImageType::Value imgType, int width, int height, unsigned char *src, unsigned char *dst, int len, bool clockwise);

/*! \fn int EtronDI_ImgMirro(
    EtronDIImageType::Value imgType, int width, int height,
        unsigned char *src, unsigned char *dstBuf)
    \brief Make the image to Mirro.
    \param pHandleEtronDI	 the pointer to the initilized EtronDI SDK instance
    \param pDevSelInfo	pointer of device select index
    \param EtronDIImageType::Value imgType Image Type
    \param int width image width
    \param int height image height
    \param unsigned char *src image source
    \param unsigned char *dstBuf image desteration
    \return success: EtronDI_OK, others: see eSPDI_def.h
*/
int EtronDI_ImgMirro(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, EtronDIImageType::Value imgType, int width, int height, unsigned char *src, unsigned char *dst);

extern "C" {
/*! \fn int EtronDI_SubSample(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* depthBuf, int bytesPerPixel, int width, int height, int& new_width, int& new_height, int mode = 0, int factor = 3)
*/
int EtronDI_SubSample(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char** SubSample, unsigned char* depthBuf, int bytesPerPixel, int width, int height, int& new_width, int& new_height, int mode = 0, int factor = 3);

/*! \fn int EtronDI_HoleFill(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* depthBuf, int bytesPerPixel, int kernel_size, int width, int height, int level, bool horizontal)
*/
int EtronDI_HoleFill(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* depthBuf, int bytesPerPixel, int kernel_size, int width, int height, int level, bool horizontal);

/*! \fn int EtronDI_TemporalFilter(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* depthBuf, int bytesPerPixel, int width, int height, float alpha, int history).
*/
int EtronDI_TemporalFilter(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* depthBuf, int bytesPerPixel, int width, int height, float alpha, int history);

/*! \fn int EtronDI_EdgePreServingFilter(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* depthBuf, int type, int width, int height, int level, float sigma, float lumda)
*/
int EtronDI_EdgePreServingFilter(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* depthBuf, int type, int width, int height, int level, float sigma, float lumda);

/*! \fn int EtronDI_ApplyFilters(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* depthBuf, unsigned char* subDisparity, int bytesPerPixel, int width, int height, int sub_w, int sub_h, int threshold=64)
*/
int EtronDI_ApplyFilters(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, unsigned char* depthBuf, unsigned char* subDisparity, int bytesPerPixel, int width, int height, int sub_w, int sub_h, int threshold=64);

/*! \fn int EtronDI_ResetFilters(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo)
*/
int EtronDI_ResetFilters(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo);

/*! \fn int ETRONDI_API EtronDI_EnableGPUAcceleration(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, bool enable)
*/
int EtronDI_EnableGPUAcceleration(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, bool enable);

/*! \fn int EtronDI_TableToData(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int width, int height, unsigned char* Table, unsigned char* Src, unsigned char* Dst)
    \brief transfer Src to Dst by Table
    \param pHandleEtronDI	 the pointer to the initilized EtronDI SDK instance
    \param pDevSelInfo	pointer of device select index
    \param width 	 input  image width
    \param height	 input  image height
    \param TableSize input  Table size in bytes
    \param Table	 input  Table buffer
    \param Src	     input  Src   buffer
    \param Dst       output Dst   buffer
    \return success: EtronDI_OK, others: see eSPDI_ErrCode.h
*/
int EtronDI_TableToData(void *pHandleEtronDI, PDEVSELINFO pDevSelInfo, int width, int height, int TableSize, unsigned short* Table, unsigned short* Src, unsigned short* Dst);

}// extern "C" 03

/*! \fn EtronDI_InitPostProcess(void **ppPostProcessHandle, unsigned int
   nWidth, unsigned int nHeight, EtronDIImageType::Value imageType);
*/
int EtronDI_InitPostProcess(void **ppPostProcessHandle, unsigned int nWidth,
                            unsigned int nHeight,
                            EtronDIImageType::Value imageType);
/*! \fn EtronDI_PostProcess(void *pPostProcessHandle, unsigned char
 * *pDepthData);
 */
int EtronDI_PostProcess(void *pPostProcessHandle, unsigned char *pDepthData);
/*! \fn EtronDI_ReleasePostProcess(void *pPostProcessHandle);
 */
int EtronDI_ReleasePostProcess(void *pPostProcessHandle);
#endif // LIB_ESPDI_H
