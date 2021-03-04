https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-logicaldisk


     Access                          0
     Availability                    None
     BlockSize                       None
    *Caption                         C:
    *Compressed                      False
     ConfigManagerErrorCode          None
     ConfigManagerUserConfig         None
     CreationClassName               Win32_LogicalDisk
     Description                     Local Fixed Disk
     DeviceID                        C:
    *DriveType                       3
     ErrorCleared                    None
     ErrorDescription                None
     ErrorMethodology                None
     FileSystem                      NTFS
    *FreeSpace                       83105959936
     InstallDate                     None
     LastErrorCode                   None
     MaximumComponentLength          255
     MediaType                       12
    *Name                            C:
     NumberOfBlocks                  None
     PNPDeviceID                     None
     PowerManagementSupported        None
    *ProviderName                    None
     Purpose                         None
     QuotasDisabled                  None
     QuotasIncomplete                None
     QuotasRebuilding                None
    *Size                            512107737088
     Status                          None
     StatusInfo                      None
     SupportsDiskQuotas              False
     SupportsFileBasedCompression    True
     SystemCreationClassName         Win32_ComputerSystem
    *SystemName                      SADIE
     VolumeDirty                     None
    *VolumeName                      SSD 476
     VolumeSerialNumber              5EFC6A97

Highlighted fields are _of interest_ for the API, without storing serials.

Usage:

+ **Caption**
  The short name for the drive

+ **VolumeName**
  Preferred Name for the drive

+ **FreeSpace**:
  To calculate the total _potential inital_ size required

+ **Name**
  if the Volume name is None

+ **Compressed**
  Denote if the info is _already_ compressed, and should work with lower write

+ **ProviderName**
  If exists, this field indicates the drive does not exist locally (a network drive), and maybe duplicated through the system during sharing.

+ **Size**
  Denote the potential expected amount for a total upload.

+ **SystemName**
  As a parent if more than one system exists within the infastructure.
