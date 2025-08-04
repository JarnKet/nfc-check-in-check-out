# acr122u_nfc_reader_api.py
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.Exceptions import CardConnectionException, NoCardException
import requests
import time
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/lailaolabdev/nfc-check-in-check-out/nfc-reader.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

API_URL = "https://hr-api.lailaolab.com/v1/api/entry-exit/nfc"

def send_uid_to_api(uid):
    try:
        response = requests.post(API_URL, json={"serialNumber": uid})
        if response.status_code == 200:
            print(f"✅ Sent UID {uid} to API: {response.json()}")
        else:
            print(f"⚠️ API responded with {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Failed to send UID to API: {e}")

def read_uid(connection):
    get_uid = [0xFF, 0xCA, 0x00, 0x00, 0x00]
    response, sw1, sw2 = connection.transmit(get_uid)
    if sw1 == 0x90 and sw2 == 0x00:
        return toHexString(response).replace(" ", "")
    return None

def main():
    print("🔍 Looking for connected readers...")
    r = readers()

    if len(r) == 0:
        print("❌ No smart card readers found.")
        return

    reader = r[0]
    print(f"✅ Using reader: {reader}")
    print("📖 Waiting for an NFC card (Ctrl+C to exit)...")

    last_uid = None
    card_present = False

    while True:
        try:
            connection = reader.createConnection()
            connection.connect()

            uid = read_uid(connection)
            if uid:
                if not card_present or uid != last_uid:
                    print(f"🎉 CARD DETECTED! UID: {uid}")
                    send_uid_to_api(uid)
                    last_uid = uid
                    card_present = True
            else:
                print("⚠️ Failed to read UID. Card may be unsupported.")

            time.sleep(0.2)

        except NoCardException:
            if card_present:
                print("🛑 Card removed.")
            last_uid = None
            card_present = False
            time.sleep(0.2)
        except CardConnectionException:
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            break

if __name__ == "__main__":
    main()
