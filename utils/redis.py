import json
import time
from decimal import Decimal

from pages.base_page import BasePage


class RedisUtils(BasePage):

    def __init__(self, config, driver):
        super().__init__(driver)
        self.config = config
        if "qa-testing" in config['credential']['url']:
            self.redis_host = self.config['redis']['qa-host']
        else:
            self.redis_host = self.config['redis']['stage-host']
    
    @staticmethod
    def establish_connection_and_get_campaign_rule(redis_connection, campaign_id, key='campaignRule', max_retries=20):
        retries = 0
        while retries < max_retries:
            try:
                keys = redis_connection.keys('{}.{}'.format(key, campaign_id))
                if keys:
                    output = redis_connection.get(keys[0])
                    if output:
                        output = json.loads(output)
                        return output
                raise KeyError("No matching keys found for pattern: {}.{}".format(key, campaign_id))
            except Exception as e:
                retries += 1
                if retries < max_retries:
                    time.sleep(2)
                else:
                    raise e

    @staticmethod
    def get_exchange_list(json_data):
        exchange_list = json_data['dspConfig']['exchanges']
        return exchange_list

    def get_total_spent_amount(self, redis_connection, campaign_id):
        amount = self.establish_connection_and_get_campaign_rule(redis_connection, campaign_id, key="spent.currency")
        redis_budget_multiplier = Decimal("1000000")
        redis_budget_scale = 6
        amount = Decimal(amount)
        rounded_amount = amount.quantize(Decimal("1e-" + str(redis_budget_scale)))
        rounded_multiplier = redis_budget_multiplier.quantize(Decimal("1e-" + str(redis_budget_scale)))
        amount_already_spent = rounded_amount / rounded_multiplier
        return float(amount_already_spent)

    def get_today_spent_amount(self, redis_connection, campaign_id):
        current_day = self.get_current_date_with_specific_format("%Y%m%d")
        key = "{}.spent.currency.tz".format(current_day)
        amount = self.establish_connection_and_get_today_spend(redis_connection, campaign_id, key=key)
        if amount is None:
            return 0.00
        redis_budget_multiplier = Decimal("1000000")
        redis_budget_scale = 6
        amount = Decimal(amount)
        rounded_amount = amount.quantize(Decimal("1e-" + str(redis_budget_scale)))
        rounded_multiplier = redis_budget_multiplier.quantize(Decimal("1e-" + str(redis_budget_scale)))
        amount_already_spent = rounded_amount / rounded_multiplier
        return float(amount_already_spent)

    @staticmethod
    def establish_connection_and_get_today_spend(redis_connection, campaign_id, key, max_retries=5):
        full_key = '{}.{}'.format(key, campaign_id)
        retries = 0
        while retries < max_retries:
            try:
                output = redis_connection.get(full_key)
                if output is None:
                    return None
                output = json.loads(output)
                return output
            except Exception as e:
                retries += 1
                if retries < max_retries:
                    time.sleep(2)
                else:
                    raise e
