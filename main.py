#!/usr/bin/env python3
"""Find available vaccine bookings"""

import sys
from time import sleep
from datetime import datetime

import requests  # type: ignore


CVCS = {
    "Southern: Gleneagles": 42,
    "Eastern: Sai Wan Ho Sports Centre": 28,
    "Kwun Tong: Hiu Kwong Street Sports Centre": 46,
    "Sham Shui Po: Lai Chi Kok Park Sports Centre": 37,
    "Kwai Tsing: Osman Ramju Sadick": 142,
    "Sha Tin: CUHK": 36,
    "Yuen Long: Yuen Long": 27
}


def open_timeslots(cvc_id: int, look_ahead: int = 8) -> list:
    """Get open timeslots"""
    endpoint = "https://bookingform.covidvaccine.gov.hk/forms/api_center"
    data = {"center_id": cvc_id,
            "cv_ctc_type": "CVC",
            "cv_name": "BioNTech/Fosun",
            "first_dose_date": "2021-05-02"}
    response = requests.post(endpoint, data=data)
    response.raise_for_status()
    response_dict = response.json()

    timeslots = []
    for date in response_dict["avalible_timeslots"][:look_ahead]:
        timeslots += [datetime.strptime(timeslot["datetime"], "%Y-%m-%d %H:%M")
                      for timeslot in date["timeslots"]
                      if timeslot["value"] == 1]
    return timeslots


def main() -> None:
    """Entry point"""
    while True:
        for cvc_name, cvc_id in CVCS.items():
            timeslots = open_timeslots(cvc_id)
            if timeslots:
                print(cvc_name)
                for date in timeslots:
                    print(date.strftime("%Y-%m-%d %H:%M (%A)"))
                return
        sleep_time = 5
        print(f"Sleeping for {sleep_time} seconds...", file=sys.stderr)
        sleep(sleep_time)


if __name__ == "__main__":
    main()
