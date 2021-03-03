# Accessing Drives

Drive navigation is handled within the app to provide deeper explorer (and file)
flow. Base Drives are pre-cached and stored for long-term tracking. A user selects the preferred devices to initially _monitor_, later configuring for file selections.


# Windows

The windows drive interface provides access to all logical drives, If the drive content is missing (such as an init run), The drive content is populated.

This takes a while, therefore the population performs 2 stages

## Quick Reference.

All logical drive _letters_ present quickly. Each is stored as an incoming _complex_ analysis of each drive records _names_ and sizes.


## Long Store

Once the user selects the monitored drives, They store for long-monitoring.
A user may use the drives within the _app explorer_ view for navigation.

# Linux

Undocumented


## Welcome Steps.

1. The UI identifies a "first install" with Welcome
2. Backend provides _letters_ and requests complex drive info
3. The user select some or ALL drives to _allow visibility_
4. Backend stores the root drives for further UI navigation.
