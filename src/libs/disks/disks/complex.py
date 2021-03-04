import win32com.client
import os


strComputer = "."
objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
# colItems = objSWbemServices.ExecQuery("Select * from Win32_LogicalDisk")
# dcolItems = objSWbemServices.ExecQuery("Select * from Win32_DiskDrive")
# cdcolItems = objSWbemServices.ExecQuery("Select * from CIM_DiskDrive")
# pcolItems = objSWbemServices.ExecQuery("Select * from Win32_DiskDriveToDiskPartition")
# ccolItems = objSWbemServices.ExecQuery("Select * from CIM_LogicalDevice")

def main():
    for name, fields in win_queries:
        make(*arrange(name, fields))


def arrange(name, fields):
    return (f"Select * from {name}", fields, f'{name}.txt')


class data_map:
    uint16 = int
    uint32 = int
    uint64 = int
    string = str
    boolean = bool
    datetime = str


logical2part_fields = (
  ("EndingAddress", "uint64",),
  ("StartingAddress", "uint64",),
  ("Antecedent", "Win32_DiskPartition",),
  ("Dependent", "Win32_LogicalDisk",),
)


cim_fields = (
  ("Caption", "string",),
  ("Description", "string",),
  ("InstallDate", "datetime",),
  ("Name", "string",),
  ("Status", "string",),
  ("Availability", "uint16",),
  ("ConfigManagerErrorCode", "uint32",),
  ("ConfigManagerUserConfig", "boolean",),
  ("CreationClassName", "string",),
  ("DeviceID", "string",),
  ("PowerManagementCapabilities[]", "uint16",),
  ("ErrorCleared", "boolean",),
  ("ErrorDescription", "string",),
  ("LastErrorCode", "uint32",),
  ("PNPDeviceID", "string",),
  ("PowerManagementSupported", "boolean",),
  ("StatusInfo", "uint16",),
  ("SystemCreationClassName", "string",),
  ("SystemName", "string",),

)

d2d_fields = (
    ('Antecedent', 'Win32_DiskDrive',),
    ('Dependent', 'Win32_DiskPartition',),
)


disk_fields = (
    ("Capabilities[]", "uint16",),
    ("CapabilityDescriptions[]", "string",),
    ("PowerManagementCapabilities[]", "uint16",),

    ("Availability", "uint16",),
    ("BytesPerSector", "uint32",),
    ("Caption", "string",),
    ("CompressionMethod", "string",),
    ("ConfigManagerErrorCode", "uint32",),
    ("ConfigManagerUserConfig", "boolean",),
    ("CreationClassName", "string",),
    ("DefaultBlockSize", "uint64",),
    ("Description", "string",),
    ("DeviceID", "string",),
    ("ErrorCleared", "boolean",),
    ("ErrorDescription", "string",),
    ("ErrorMethodology", "string",),
    ("FirmwareRevision", "string",),
    ("Index", "uint32",),
    ("InstallDate", "datetime",),
    ("InterfaceType", "string",),
    ("LastErrorCode", "uint32",),
    ("Manufacturer", "string",),
    ("MaxBlockSize", "uint64",),
    ("MaxMediaSize", "uint64",),
    ("MediaLoaded", "boolean",),
    ("MediaType", "string",),
    ("MinBlockSize", "uint64",),
    ("Model", "string",),
    ("Name", "string",),
    ("NeedsCleaning", "boolean",),
    ("NumberOfMediaSupported", "uint32",),
    ("Partitions", "uint32",),
    ("PNPDeviceID", "string",),
    ("PowerManagementSupported", "boolean",),
    ("SCSIBus", "uint32",),
    ("SCSILogicalUnit", "uint16",),
    ("SCSIPort", "uint16",),
    ("SCSITargetId", "uint16",),
    ("SectorsPerTrack", "uint32",),
    ("SerialNumber", "string",),
    ("Signature", "uint32",),
    ("Size", "uint64",),
    ("Status", "string",),
    ("StatusInfo", "uint16",),
    ("SystemCreationClassName", "string",),
    ("SystemName", "string",),
    ("TotalCylinders", "uint64",),
    ("TotalHeads", "uint32",),
    ("TotalSectors", "uint64",),
    ("TotalTracks", "uint64",),
    ("TracksPerCylinder", "uint32",),
)


logical_fields = (
    ("Access", "uint16",),
    ("Availability", "uint16",),
    ("BlockSize", "uint64",),
    ("Caption", "string",),
    ("Compressed", "boolean",),
    ("ConfigManagerErrorCode", "uint32",),
    ("ConfigManagerUserConfig", "boolean",),
    ("CreationClassName", "string",),
    ("Description", "string",),
    ("DeviceID", "string",),
    ("DriveType", "uint32",),
    ("ErrorCleared", "boolean",),
    ("ErrorDescription", "string",),
    ("ErrorMethodology", "string",),
    ("FileSystem", "string",),
    ("FreeSpace", "uint64",),
    ("InstallDate", "datetime",),
    ("LastErrorCode", "uint32",),
    ("MaximumComponentLength", "uint32",),
    ("MediaType", "uint32",),
    ("Name", "string",),
    ("NumberOfBlocks", "uint64",),
    ("PNPDeviceID", "string",),
    ("PowerManagementCapabilities[]", "uint16",),
    ("PowerManagementSupported", "boolean",),
    ("ProviderName", "string",),
    ("Purpose", "string",),
    ("QuotasDisabled", "boolean",),
    ("QuotasIncomplete", "boolean",),
    ("QuotasRebuilding", "boolean",),
    ("Size", "uint64",),
    ("Status", "string",),
    ("StatusInfo", "uint16",),
    ("SupportsDiskQuotas", "boolean",),
    ("SupportsFileBasedCompression", "boolean",),
    ("SystemCreationClassName", "string",),
    ("SystemName", "string",),
    ("VolumeDirty", "boolean",),
    ("VolumeName", "string",),
    ("VolumeSerialNumber", "string",),
)


win_queries = (
    ("Win32_LogicalDisk", logical_fields,),
    ("CIM_DiskDrive", disk_fields,),
    ("Win32_DiskDrive", disk_fields,),
    ("Win32_DiskDriveToDiskPartition", d2d_fields,),
    ("CIM_LogicalDevice", cim_fields,),
    ("Win32_LogicalDiskToPartition", logical2part_fields,),
)


import re

def camel_to_snake(name):
  name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
  return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def get_logical(fields=None):
    name = 'Win32_LogicalDisk'
    fields = fields or logical_fields
    return make(*arrange(name, fields))


def make(query, fields, filename):
    items = objSWbemServices.ExecQuery(query)
    stream = open(os.path.join('', filename), 'w')

    def out(*a):
        stream.write(''.join(map(str, a)))
        stream.write('\n')

    _max = max([len(x[0]) for x in fields]) + 3

    res = []
    case_convert = camel_to_snake

    for objItem in items:

        o = {}
        for field, _type in fields:
            if field.endswith('[]'):
                name = field[:-2]
                d = getattr(objItem, name)
                if d is None:
                    #print('missing', name)
                    continue
                for x in d:
                    o[case_convert(name)] = x
                continue

            d = getattr(objItem, field)
            # out(f'{field:<{_max}}', d)
            o[case_convert(field)] = d

        res.append(o)
        # o("---")
    return res


if __name__ == '__main__':
    main()
