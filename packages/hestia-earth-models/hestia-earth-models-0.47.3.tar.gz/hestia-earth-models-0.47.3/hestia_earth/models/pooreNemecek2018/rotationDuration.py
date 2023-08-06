from hestia_earth.schema import PracticeStatsDefinition

from hestia_earth.models.utils.practice import _new_practice
from .orchardDuration import _get_value as get_orchardDuration
from .longFallowPeriod import _get_value as get_longFallowPeriod
from .utils import run_products_average
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "products": [{"@type": "Product", "value": "", "term.termType": "crop"}]
    }
}
LOOKUPS = {
    "crop": ["Orchard_duration", "Orchard_longFallowPeriod"]
}
RETURNS = {
    "Practice": [{
        "value": "",
        "statsDefinition": "modelled"
    }]
}
TERM_ID = 'rotationDuration'


def _get_value(product: dict):
    orchardDuration = get_orchardDuration(product)
    longFallowPeriod = get_longFallowPeriod(product)
    return orchardDuration + longFallowPeriod if orchardDuration is not None and longFallowPeriod is not None else None


def _practice(value: float):
    practice = _new_practice(TERM_ID, MODEL)
    practice['value'] = [value]
    practice['statsDefinition'] = PracticeStatsDefinition.MODELLED.value
    return practice


def run(cycle: dict):
    value = run_products_average(cycle, TERM_ID, _get_value)
    return [_practice(value)] if value is not None else []
