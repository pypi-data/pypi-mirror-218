import tempfile
import time
from urllib.parse import urljoin

import click
import cups
import requests

from kort_client.api import KortAPIException
from kort_client.card_detectors import CardDetector


class KortClientException(Exception):
    pass


IPP_CODES = {y: x for x, y in cups.__dict__.items() if x.startswith("IPP_JOB")}


class PrintClient:
    def __init__(self, settings, api, interactive=False):
        self.settings = settings
        self.api = api
        self.interactive = interactive
        self.with_printer = True

        self.printer_id = None
        self.conn = cups.Connection()
        self.card_detectors = CardDetector.get_card_detectors()
        self.card_detector = None
        self.card_detector_in_process = False

    def run(self):
        try:
            while True:
                try:
                    self.step()
                except (KortAPIException, KortClientException) as e:
                    printer_status = "with_errors"
                    status_text = str(e)
                    click.secho(
                        "An error occurred, try again in five seconds: {}".format(e),
                        fg="red",
                    )
                    if self.card_detector_in_process and self.card_detector:
                        self.card_detector.abort()
                else:
                    printer_status = "online"
                    status_text = ""

                if self.printer_id:
                    # Set status
                    self.api.set_printer_status(
                        self.printer_id, printer_status, status_text
                    )

                if printer_status == "with_errors":
                    time.sleep(5)
                else:
                    time.sleep(1)

        except (EOFError, KeyboardInterrupt):
            if self.printer_id:
                click.echo("Set printer as offline")
                self.api.set_printer_status(
                    self.printer_id, "offline", "Printer client was stopped by user."
                )
            if self.card_detector and self.card_detector_in_process:
                self.card_detector.abort()
            raise

    def _validate_printer(self):
        self.with_printer = self.printer_config.get("cups_printer")
        self.card_detector = self.card_detectors.get(
            self.printer_config["card_detector"], None
        )

        if not self.with_printer and not self.card_detector:
            raise KortClientException(
                "No printer or card detector configured for printer {}".format(
                    self.printer_config["name"]
                )
            )

        if self.with_printer:
            cups_printers = self.conn.getPrinters()
            if self.printer_config["cups_printer"] not in cups_printers:
                raise KortClientException(
                    "CUPS printer {} not found".format(
                        self.printer_config["cups_printer"]
                    ),
                )

    def step(self):
        self.printer_config = self.api.get_printer()
        print(self.printer_config)

        self.printer_id = self.printer_config["id"]

        self._validate_printer()

        self.card_detector_in_process = False
        if self.card_detector:
            self.interactive = self.card_detector.interactive
            self.card_detector.clear()

        next_job = self.api.get_next_job(self.printer_id)

        print(next_job)
        if next_job:
            job_id = next_job["id"]
            click.secho("Got new print job {}".format(next_job), fg="green")

            self.api.set_job_status(
                job_id,
                "in_progress",
            )

            if not self.printer_config.get("generate_number_on_server"):
                # Now do something to set the number, but irrelevant for this example
                click.secho("Generate number on server disabled", fg="yellow")
                if self.card_detector:
                    self.card_detector_in_process = True
                    chip_number = self.card_detector.read_id()
                    if chip_number:
                        next_job = self.api.set_chip_number(job_id, str(chip_number))
                        time.sleep(1)
                    else:
                        raise KortClientException("No valid chip number read")
                else:
                    raise KortClientException("No card detector configured")

            if self.with_printer and next_job["card"]["chip_number"]:
                # Download PDF file
                with tempfile.NamedTemporaryFile("wb") as f:
                    r = requests.get(
                        urljoin(self.settings.base_url, next_job["card"]["pdf_file"])
                    )
                    f.write(r.content)
                    f.flush()

                    cups_job_id = self.conn.printFile(
                        self.printer_config["cups_printer"],
                        f.name,
                        f"AlekSIS: #{job_id}",
                        {},
                    )

                last_job_state = None
                while True:
                    a = self.conn.getJobAttributes(cups_job_id)
                    current_job_state = a["job-state"]
                    status = "in_progress"

                    if current_job_state in (
                        cups.IPP_JOB_STOPPED,
                        cups.IPP_JOB_CANCELED,
                        cups.IPP_JOB_ABORTED,
                        cups.IPP_JOB_HELD,
                    ):
                        status = "failed"
                    elif current_job_state == cups.IPP_JOB_COMPLETED:
                        status = "finished"

                    if last_job_state != current_job_state:
                        click.echo(
                            click.style(
                                f"Print job is in state {status}: {current_job_state}",
                                fg="yellow",
                            )
                        )
                        last_job_state = current_job_state
                        self.api.set_job_status(
                            job_id,
                            status,
                            IPP_CODES.get(current_job_state, str(current_job_state)),
                        )

                    if status in ("failed", "finished"):
                        break

                    time.sleep(0.5)
