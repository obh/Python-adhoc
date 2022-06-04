import datetime
from typing import Any, Dict
import json
import re
import requests

JSON = Dict[str, Any]
dt = datetime.datetime


class Alert:
    def __init__(self, resource: str, event: str, **kwargs) -> None:
        self.merchantId = kwargs.get('merchantId')
        self.paymentGroup = kwargs.get("paymentGroup")
        self.description = kwargs.get("description")
        self.merchantName = kwargs.get("merchantName")
        self.expectedSR = kwargs.get("expectedSR")
        self.actualSR = kwargs.get("actualSR")
        self.startTime = kwargs.get("startTime")
        self.status = kwargs.get("severity")

    def print(self):
        print("MID: %s, alertname: %s" % (self.merchantId, self.alertname))


def parse_prometheus(alert: JSON, external_url: str):

    status = alert.get('status', 'firing')

    # Allow labels and annotations to use python string formats that refer to
    # other labels eg. runbook = 'https://internal.myorg.net/wiki/alerts/{app}/{alertname}'
    # See https://github.com/prometheus/prometheus/issues/2818

    labels = {}
    for k, v in alert['labels'].items():
        try:
            labels[k] = v.format(**alert['labels'])
        except Exception:
            labels[k] = v

    annotations = {}
    for k, v in alert['annotations'].items():
        try:
            annotations[k] = v.format(**labels)
        except Exception:
            annotations[k] = v

    if status == 'firing':
        severity = labels.pop('severity', 'warning')
    elif status == 'resolved':
        severity = "normal"
    else:
        severity = 'unknown'

    # labels
    resource = labels.pop('exported_instance', None) or labels.pop('instance', 'n/a')
    event = labels.pop('event', None) or labels.pop('alertname')
    environment = labels.pop('environment', "production")
    customer = labels.pop('customer', None)
    correlate = labels.pop('correlate').split(',') if 'correlate' in labels else None
    service = labels.pop('service', '').split(',')
    group = labels.pop('group', None) or labels.pop('job', 'Prometheus')
    origin = 'prometheus/' + labels.pop('monitor', '-')


    eventProps = event.split("|")
    merchantId = int(eventProps[0].split(":")[1].strip())
    merchantName = eventProps[1].split(":")[1].strip()
    paymentGroup = eventProps[2].split(":")[1].strip()


    # annotations
    value = annotations.pop('value', None)
    summary = annotations.pop('summary', None)
    description = annotations.pop('description', None)
    text = description or summary or f'{severity.upper()}: {resource} is {event}'
    pattern = re.compile(r'expected sr: (.*?) and actual sr: (.*?)$')
    match = pattern.search(description)
    sr = match.groups()

    # attributes
    attributes = {
        'startsAt': alert['startsAt'],
        'endsAt': alert['endsAt']
    }

    return Alert(
        resource=resource,
        event=event,
        environment=environment,
        merchantId=merchantId,
        merchantName=merchantName,
        paymentGroup=paymentGroup,
        expectedSR=sr[0],
        actualSR=sr[1],
        startTime=attributes['startsAt'],
        severity=severity,
        text=text,
        event_type='prometheusAlert',
        raw_data=alert,
    )


class PrometheusWebhook:
    """
    Prometheus Alertmanager webhook receiver
    See https://prometheus.io/docs/operating/integrations/#alertmanager-webhook-receiver
    """

    def incoming(self, path, query_string, payload):
        if payload and 'alerts' in payload:
            external_url = payload.get('externalURL')
            return [parse_prometheus(alert, external_url) for alert in payload['alerts']]
        else:
            raise IOError('no alerts in Prometheus notification payload', 400)


def send_to_slack(alert: Alert) -> None:
    if alert.status != "firing":
        return
    header = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    url = get_slack_endpoint(alert.merchantId)
    payload = {
        "merchantId": str(alert.merchantId),
        "merchantName": alert.merchantName,
        "paymentGroup": alert.paymentGroup,
        "expectedSR": alert.expectedSR,
        "actualSR": alert.actualSR,
        "startTime": alert.startTime
    }
    print(payload)
    req = requests.post(url, headers=header, data=json.dumps(payload))
    print(req.status_code)
    # print(req.text)


def get_slack_endpoint(mid: int):
    host = "https://hooks.slack.com/"
    mapping = {
        211191: "workflows/TM3MZ586R/A03JNDVTS8Z/410701577607722349/CfsnGYvU4KUco13h1c4ipWz6",
    }
    return host + mapping.get(mid, "")


def main():
    raw = """
    {
    "receiver": "pg-merchant-sr-api",
    "status": "firing",
    "alerts":
    [
        {
            "status": "firing",
            "labels":
            {
                "alertgroup": "midpaymentcodethresholdalert",
                "alertname": "Alert for MID : 211191 | MerchantName : CRED | paymentCodeGroup : Visa\\/MC credit cards",
                "api": "pg-merchant-sr-api",
                "product": "pg",
                "team": "pg-merchant-sr"
            },
            "annotations":
            {
                "description": "Success rate for Merchant: CRED and paymentCodeGroup: Visa\\/MC credit cards, expected sr: 58.00 and actual sr: 55.52",
                "summary": "Success rate low for Merchant CRED and paymentCodeGroup Visa\\/MC credit cards"
            },
            "startsAt": "2022-06-03T09:01:54.145601707Z",
            "endsAt": "0001-01-01T00:00:00Z",
            "generatorURL": "http:\\/\\/vmalert-pg-vm-cb8d96cf8-chphg:8080\\/api\\/v1\\/3249388433328818964\\/14695981039346656037\\/status",
            "fingerprint": "a85c98442d2fd27a"
        },
        {
            "status": "firing",
            "labels":
            {
                "alertgroup": "midpaymentcodethresholdalert",
                "alertname": "Alert for MID : 72061 | MerchantName : Easy Trip Planners | paymentCodeGroup : HDFC Net banking",
                "api": "pg-merchant-sr-api",
                "product": "pg",
                "team": "pg-merchant-sr"
            },
            "annotations":
            {
                "description": "Success rate for Merchant: Easy Trip Planners and paymentCodeGroup: HDFC Net banking, expected sr: 75.00 and actual sr: 72.89",
                "summary": "Success rate low for Merchant Easy Trip Planners and paymentCodeGroup HDFC Net banking"
            },
            "startsAt": "2022-06-03T10:32:14.148826814Z",
            "endsAt": "0001-01-01T00:00:00Z",
            "generatorURL": "http:\\/\\/vmalert-pg-vm-cb8d96cf8-chphg:8080\\/api\\/v1\\/3249388433328818964\\/14695981039346656037\\/status",
            "fingerprint": "ce11b85a411a1199"
        },
        {
            "status": "firing",
            "labels":
            {
                "alertgroup": "midpaymentcodethresholdalert",
                "alertname": "Alert for MID : 72061 | MerchantName : Easy Trip Planners | paymentCodeGroup : Rupay debit card",
                "api": "pg-merchant-sr-api",
                "product": "pg",
                "team": "pg-merchant-sr"
            },
            "annotations":
            {
                "description": "Success rate for Merchant: Easy Trip Planners and paymentCodeGroup: Rupay debit card, expected sr: 57.00 and actual sr: 51.18",
                "summary": "Success rate low for Merchant Easy Trip Planners and paymentCodeGroup Rupay debit card"
            },
            "startsAt": "2022-06-03T11:17:14.160865004Z",
            "endsAt": "0001-01-01T00:00:00Z",
            "generatorURL": "http:\\/\\/vmalert-pg-vm-cb8d96cf8-chphg:8080\\/api\\/v1\\/3249388433328818964\\/14695981039346656037\\/status",
            "fingerprint": "90c4cee5100dbc36"
        }
    ],
    "groupLabels":
    [],
    "commonLabels":
    {
        "alertgroup": "midpaymentcodethresholdalert",
        "api": "pg-merchant-sr-api",
        "product": "pg",
        "team": "pg-merchant-sr"
    }
}
    """
    promwebhook = PrometheusWebhook()
    alerts = promwebhook.incoming("/incoming", "", json.loads(raw))
    for alert in alerts:
        send_to_slack(alert)

if __name__ == "__main__":
    main()
