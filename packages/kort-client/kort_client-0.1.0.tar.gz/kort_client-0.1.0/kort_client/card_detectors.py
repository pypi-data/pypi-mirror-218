import os
import subprocess  # noqa
import time
from binascii import hexlify

import click
from nfc import ContactlessFrontend

from .usb_barcode_scanner.scanner import BarcodeReader


class CardDetector:
    id_ = None
    interactive = False

    def read_id(self):
        raise NotImplementedError()

    def abort(self):
        pass

    def clear(self):
        pass

    @classmethod
    def get_id(cls):
        if not cls.id_:
            raise NotImplementedError()
        return cls.id_

    @classmethod
    def get_card_detectors(cls):
        card_detectors = cls.__subclasses__()
        return {d.get_id(): d() for d in card_detectors}


class EvolisCardDetector(CardDetector):
    """This is a card detector for Evolis card printers like Evolis Primacy.

    To use it, you have to get the evocom tool from the Evolis customer support.
    Then place it at /opt/evocom/evocom.
    """

    id_ = "evolis_evocom"
    EVOCOM_PATH = "/opt/evocom/evocom"

    def get_detector(self):
        from kort_client.run import KortClientException

        files = []
        for __, __, files in os.walk("/dev/"):
            files = files
            break
        files = {f for f in files if f.startswith("hidraw")}
        possible_interfaces = []
        for hid_interface in list(files):
            path_to_read = f"/sys/class/hidraw/{hid_interface}/device/uevent"
            with open(path_to_read) as f:
                content = f.read()
                if "rfid" in content.lower():
                    possible_interfaces.append(hid_interface)

        if len(possible_interfaces) != 1:
            raise KortClientException("No or more than one  reader found")

        return os.path.join("/dev", possible_interfaces[0])

    def get_printer(self):
        from kort_client.run import KortClientException

        files = []
        for __, __, files in os.walk("/dev/usb/"):
            files += files

        files = {f for f in files if f.startswith("lp")}

        if len(files) != 1:
            raise KortClientException("No or more than one printer found")

        suffix = list(files)[0]
        return f"/dev/usb/{suffix}"

    def read_id(self):
        from kort_client.run import KortClientException

        reader = BarcodeReader(self.get_detector())
        # Transport the card to the printer
        try:
            r = subprocess.run(  # noqa
                [self.EVOCOM_PATH, "-p", self.get_printer(), "Sis"]
            )
        except (subprocess.CalledProcessError, OSError) as e:
            raise KortClientException(e)

        # Read the card
        chip_number = reader.read_barcode()

        try:
            r.check_returncode()
        except (subprocess.CalledProcessError, OSError) as e:
            raise KortClientException(e)
        return chip_number

    def clear(self):
        subprocess.run([self.EVOCOM_PATH, "-p", self.get_printer(), "Ser"])  # noqa

    def abort(self):
        self.clear()


class NfcReadUidDetector(CardDetector):
    id_ = "nfc_read_uid"

    def read_id(self):
        reader = ContactlessFrontend()
        reader.open("usb")
        from kort_client.run import KortClientException

        try:
            click.secho("→ Please hold your card to the reader")
            tag = reader.connect(rdwr={"on-connect": lambda tag: False})
            uid = hexlify(tag._nfcid).decode("utf-8")
            click.secho("Card successfully detected", fg="green")
            click.secho(f"UID: {uid}", fg="white")

            click.secho("Please remove the card from the reader", fg="red")
            while True:
                started = time.time()
                after5s = lambda: time.time() - started > 0.5
                tag = reader.connect(
                    rdwr={"on-connect": lambda tag: False}, terminate=after5s
                )
                if not tag:
                    break
                new_uid = hexlify(tag._nfcid).decode("utf-8")
                if uid != new_uid:
                    break
            click.secho("The card has been removed.", fg="green")

        except Exception as e:
            raise KortClientException(e.args)

        return uid
