# test_reader.py
from smartcard.System import readers

def test_reader():
    print("🔍 Checking for readers...")
    r = readers()
    
    if len(r) == 0:
        print("❌ No readers found")
        print("Try:")
        print("1. sudo systemctl restart pcscd")
        print("2. Unplug and replug the USB device")
        return False
    
    for reader in r:
        print(f"✅ Found reader: {reader}")
    
    return True

if __name__ == "__main__":
    test_reader()