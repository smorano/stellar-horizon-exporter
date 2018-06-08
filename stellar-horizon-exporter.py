from prometheus_client import start_http_server, Metric, REGISTRY
import argparse
import json
import logging
import sys
import time
from stellar_base.horizon import horizon_livenet
from collections import defaultdict
import copy
import requests

# logging setup
log = logging.getLogger('stellar-horizon-exporter')
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


class StatsCollector():

  def collect(self):

    for k,v in previous_data.items():
      metric = Metric(k, 'stellar base metric values', 'summary')
      metric.add_sample(k, value=float(v), labels={'name': 'horizon.stellar.org'})
      yield metric
    metric = Metric('payment_detail', 'stellar payment metric values', 'gauge')
    for asset, asset_data in previous_payment_detail.items():
          metric.add_sample('sum_payment', value=asset_data['sum'], labels={'asset': asset})
          metric.add_sample('nb_payment', value=asset_data['nb'], labels={'asset': asset})
    yield metric
    metric = Metric('large_native_payment_detail', 'large native stellar payment metric values', 'gauge')
    for from_addr, amount_by_dest in previous_large_native_payment_detail.items():
        for to_addr, amount in amount_by_dest.items():
            metric.add_sample('sum_large_native_payment', value=amount, labels={'from_addr': from_addr, 'to_addr': to_addr})
    yield metric


def main_loop():

    LARGE_PAYMENT_MIN_AMOUNT = 10000

    global previous_data
    previous_data = defaultdict(lambda: 0)
    
    global previous_payment_detail
    previous_payment_detail = defaultdict(lambda: defaultdict(lambda: 0))
    
    global previous_large_native_payment_detail
    previous_large_native_payment_detail = defaultdict(lambda: defaultdict(lambda: 0))

    parser = argparse.ArgumentParser(
      description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--port', nargs='?', const=9101, help='The TCP port to listen on.  Defaults to 9101.', default=9101)
    args = parser.parse_args()
    log.info(args.port)

    current_data = defaultdict(lambda: 0)
    current_payment_detail = defaultdict(lambda: defaultdict(lambda: 0))
    current_large_native_payment_detail = defaultdict(lambda: defaultdict(lambda: 0))
  
    REGISTRY.register(StatsCollector())
    start_http_server(int(args.port))

    h = horizon_livenet()
    p = {
      'limit': 200,
      'cursor': 'now',
    }

    current_minute = None

    r = h.operations(sse=True, params=p)
    try:
        for resp in r:
          try:
            m = json.loads(str(resp))
          except json.decoder.JSONDecodeError:
              pass

          if m == 'hello':
            continue

          cm = m['created_at'][:-4]
          if cm != current_minute:
             
            log.info('minute change %s => %s' % (current_minute, cm))
            current_minute = cm

            previous_data = copy.deepcopy(current_data)
            previous_payment_detail = copy.deepcopy(current_payment_detail)
            previous_large_native_payment_detail = copy.deepcopy(current_large_native_payment_detail)

            current_data = defaultdict(lambda: 0)
            current_payment_detail = defaultdict(lambda: defaultdict(lambda: 0))
            current_large_native_payment_detail = defaultdict(lambda: defaultdict(lambda: 0))

          op_type = m['type']

          current_data['nb_operation'] += 1
          current_data['nb_operation_%s' % op_type] += 1

          if op_type == 'payment':
            current_data['total_amount_payment'] += float(m['amount'])

            if m['asset_type'] == 'native':
                asset = 'native'

                v = float(m['amount'])
                if v >= LARGE_PAYMENT_MIN_AMOUNT:

                    from_addr = m['from']
                    to_addr = m['to']
                    current_large_native_payment_detail[from_addr][to_addr] += v

            else:
                asset = m['asset_code']

            current_payment_detail[asset]['nb'] += 1
            current_payment_detail[asset]['sum'] += float(m['amount'])

    except requests.exceptions.HTTPError as e:
        log.info(str(e))
        lolog.infoo('http exception, restarting')
        return

if __name__ == '__main__':
  try:
    while True:
        main_loop()
        time.sleep(1)
  except KeyboardInterrupt:
    print(" Interrupted")
    exit(0)
