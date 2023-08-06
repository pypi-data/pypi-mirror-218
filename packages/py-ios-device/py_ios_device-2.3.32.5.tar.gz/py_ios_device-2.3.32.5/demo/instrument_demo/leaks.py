"""
启动 app
"""
import os
import sys

sys.path.append(os.getcwd())

from ios_device.servers.Instrument import InstrumentServer


def _launch_app(rpc, bundleid):
    launch_environment = {'OS_ACTIVITY_DT_MODE': '1',
                          'NSDisableAutoreleasePoolCache': 'YES',
                          'DYLD_PRINT_TO_STDERR': '1',
                          'HIPreventRefEncoding': '1'}

    def on_channel_message(res):
        print(res.auxiliaries, res.selector)

    alloc_channel = 'com.apple.instruments.server.services.objectalloc'
    environment = rpc.call(alloc_channel, "preparedEnvironmentForLaunch:eventsMask:", {}, 2145255176).selector
    launch_environment.update(environment)

    channel = "com.apple.instruments.server.services.processcontrol"
    rpc.register_channel_callback(channel, on_channel_message)
    pid = rpc.call(channel, "launchSuspendedProcessWithDevicePath:bundleIdentifier:environment:arguments:options:", "",
                   bundleid, launch_environment, [], {"StartSuspendedKey": True}).selector
    print("start", pid)


if __name__ == '__main__':
    rpc = InstrumentServer().init()
    _launch_app(rpc, 'cn.rongcloud.im')
    rpc.stop()
