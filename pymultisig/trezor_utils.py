from trezorlib.client import TrezorClient
from trezorlib.transport import enumerate_devices, get_transport
from trezorlib.ui import ClickUI


from trezorlib.device import TrezorDevice

def get_trezor_client() -> TrezorClient:
    """
    Wrapper to open connection to Trezor One

    Returns: 
        TrezorClient object
    """
    
    # List all connected TREZORs on USB
    devices = enumerate_devices()

    # Check whether we found any
    if len(devices) == 0:
        raise ConnectionError('No TREZOR found')

    # Use first connected device
    #transport = devices[0]

    transport = get_transport()

    ui = ClickUI()
    # Creates object for manipulating TREZOR
    client = TrezorClient(transport, ui)

    return client
