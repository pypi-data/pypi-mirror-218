import urllib
from typing import Any, Optional, Sequence
from urllib.parse import urljoin

import click
import requests as requests
from requests import request

from .config import settings


class KortAPIException(Exception):
    pass


class ConfigurationException(KortAPIException):
    pass


class KortAPI:
    URLS = {
        "authorize": "oauth/authorize/",
        "token": "oauth/token/",
        "status": "app/kort/api/v1/printers/{}/status/",
        "printer": "app/kort/api/v1/printers/",
        "next_job": "app/kort/api/v1/printers/{}/jobs/next/",
        "job_status": "app/kort/api/v1/jobs/{}/status/",
        "chip_number": "app/kort/api/v1/jobs/{}/chip_number/",
    }

    def __init__(self):
        self.settings = settings
        self._validate_settings()

    def get_printer(self) -> dict[str, Any]:
        r = self._do_request("GET", "printer")
        return r

    def get_printer_id(self) -> int:
        r = self.get_printer()
        return r["id"]

    def get_next_job(self, printer_id: int) -> Optional[dict[str, Any]]:
        r = self._do_request("GET", "next_job", [printer_id])
        print(r)
        if r.get("status") == "no_job":
            return None
        return r

    def set_job_status(
        self, job_id: int, status: str, status_text: str = None
    ) -> dict[str, Any]:
        data = {"status": status}
        if status_text is not None:
            data["status_text"] = status_text
        r = self._do_request("PUT", "job_status", [job_id], data=data)
        return r

    def set_chip_number(self, job_id: int, chip_number: str) -> dict[str, Any]:
        data = {"chip_number": chip_number}
        r = self._do_request("PUT", "chip_number", [job_id], data=data)
        return r

    def set_printer_status(
        self, printer_id: int, status: str, status_text: str = None
    ) -> dict[str, Any]:
        data = {"status": status}
        if status_text is not None:
            data["status_text"] = status_text
        r = self._do_request("PUT", "status", [printer_id], data=data)
        return r

    def _validate_settings(self):
        if not self.settings.client_id:
            raise ConfigurationException("No client_id set.")
        if not self.settings.client_secret:
            raise ConfigurationException("No client_secret set.")
        if not self.settings.base_url:
            raise ConfigurationException("No base_url set.")

    def _do_request(
        self, method: str, url: str, attrs: Optional[Sequence] = None, **kwargs
    ) -> dict[str, Any]:
        if url in self.URLS:
            url = self.URLS[url]
        if attrs:
            url = url.format(*attrs)
        url = urljoin(settings.base_url, url)
        try:
            r = request(
                method,
                url,
                auth=(
                    urllib.parse.quote(self.settings.client_id),
                    urllib.parse.quote(self.settings.client_secret),
                ),
                **kwargs
            )
            if not r.ok:
                click.secho("Error {}: {}".format(r.status_code, r.text), fg="red")
                raise KortAPIException("Error {}: {}".format(r.status_code, r.text))
            return r.json()
        except (requests.RequestException, requests.JSONDecodeError) as e:
            click.secho("Error: " + str(e), fg="red")
            raise KortAPIException(e)
