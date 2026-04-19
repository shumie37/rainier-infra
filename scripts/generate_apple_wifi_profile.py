#!/usr/bin/env python3

import argparse
import plistlib
import uuid
from pathlib import Path


def payload_uuid() -> str:
    return str(uuid.uuid4()).upper()


def build_profile(
    *,
    ssid: str,
    device_name: str,
    username: str,
    radius_host: str,
    profile_display_name: str,
    root_ca_bytes: bytes,
    pkcs12_bytes: bytes,
    pkcs12_password: str,
):
    root_uuid = payload_uuid()
    identity_uuid = payload_uuid()
    wifi_uuid = payload_uuid()
    profile_uuid = payload_uuid()

    root_payload = {
        "PayloadType": "com.apple.security.root",
        "PayloadVersion": 1,
        "PayloadIdentifier": f"net.shumie.blackridge.ca.{device_name}",
        "PayloadUUID": root_uuid,
        "PayloadDisplayName": "Blackridge Root CA",
        "PayloadDescription": "Trust anchor for Blackridge Wi-Fi certificates.",
        "PayloadContent": root_ca_bytes,
    }

    identity_payload = {
        "PayloadType": "com.apple.security.pkcs12",
        "PayloadVersion": 1,
        "PayloadIdentifier": f"net.shumie.blackridge.identity.{device_name}",
        "PayloadUUID": identity_uuid,
        "PayloadDisplayName": "Blackridge Device Identity",
        "PayloadDescription": "Client identity for Blackridge WPA3-Enterprise Wi-Fi.",
        "Password": pkcs12_password,
        "PayloadContent": pkcs12_bytes,
    }

    wifi_payload = {
        "PayloadType": "com.apple.wifi.managed",
        "PayloadVersion": 1,
        "PayloadIdentifier": f"net.shumie.blackridge.wifi.{device_name}",
        "PayloadUUID": wifi_uuid,
        "PayloadDisplayName": "Blackridge Secure Wi-Fi",
        "PayloadDescription": f"Managed Wi-Fi configuration for {ssid}.",
        "AutoJoin": True,
        "EncryptionType": "WPA",
        "SSID_STR": ssid,
        "HIDDEN_NETWORK": False,
        "EAPClientConfiguration": {
            "AcceptEAPTypes": [13],
            "UserName": username,
            "TLSTrustedServerNames": [radius_host],
            "PayloadCertificateAnchorUUID": [root_uuid],
            "PayloadCertificateUUID": identity_uuid,
        },
    }

    profile = {
        "PayloadType": "Configuration",
        "PayloadVersion": 1,
        "PayloadIdentifier": f"net.shumie.blackridge.profile.{device_name}",
        "PayloadUUID": profile_uuid,
        "PayloadDisplayName": profile_display_name,
        "PayloadDescription": "Blackridge WPA3-Enterprise EAP-TLS Wi-Fi profile.",
        "PayloadOrganization": "Blackridge",
        "PayloadRemovalDisallowed": False,
        "PayloadScope": "System",
        "PayloadContent": [root_payload, identity_payload, wifi_payload],
    }
    return profile


def main():
    parser = argparse.ArgumentParser(description="Generate an Apple Wi-Fi .mobileconfig for EAP-TLS.")
    parser.add_argument("--ssid", required=True)
    parser.add_argument("--device-name", required=True)
    parser.add_argument("--username", required=True)
    parser.add_argument("--radius-host", required=True)
    parser.add_argument("--profile-display-name", default="Blackridge Secure Wi-Fi")
    parser.add_argument("--root-ca", required=True, type=Path)
    parser.add_argument("--pkcs12", required=True, type=Path)
    parser.add_argument("--pkcs12-password", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    profile = build_profile(
        ssid=args.ssid,
        device_name=args.device_name,
        username=args.username,
        radius_host=args.radius_host,
        profile_display_name=args.profile_display_name,
        root_ca_bytes=args.root_ca.read_bytes(),
        pkcs12_bytes=args.pkcs12.read_bytes(),
        pkcs12_password=args.pkcs12_password,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("wb") as f:
        plistlib.dump(profile, f, sort_keys=False)


if __name__ == "__main__":
    main()
