import pandas as pd

from .._common.const import (
    EstimateDataComponentType,
    FinancialDataComponentType,
    MarketDataComponentType,
    PrecalculatedDataComponentType,
    IndexDataComponentType,
    EventDataComponentType,
    OtherDataComponentType,
    IndustryComponentType,
)
from .._core._req_builder import _dataquery
from .._prismcomponent.prismcomponent import _PrismComponent, _PrismDataComponent, _PrismFinancialComponent
from .._utils import _validate_args, _req_call


# ------------------------------------------------------------------------------------------------------------------- #
#                                                        Market                                                       #
# ------------------------------------------------------------------------------------------------------------------- #
class _Open(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.OPEN

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Close(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.CLOSE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _High(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.HIGH

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Low(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.LOW

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Bid(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.BID

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Ask(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.ASK

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _VWAP(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.VWAP

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _MarketCap(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.MARKETCAP

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Volume(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.VOLUME

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _ShortInterest(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.SHORT_INTEREST

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Dividend(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.DIVIDEND

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _DividendAdjustmentFactor(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.DIVIDEND_ADJ_FACTOR

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Split(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.SPLIT

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _SplitAdjustmentFactor(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.SPLIT_ADJ_FACTOR

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _ExchangeRate(_PrismDataComponent, _PrismComponent):
    _component_name = MarketDataComponentType.EXCHANGERATE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @_validate_args
    @_req_call(_dataquery)
    def get_data(self, startdate: str = None, enddate: str = None, name = None,) -> pd.DataFrame:
        pass


# ------------------------------------------------------------------------------------------------------------------- #
#                                                      Financial                                                      #
# ------------------------------------------------------------------------------------------------------------------- #
class _BalanceSheet(_PrismDataComponent, _PrismFinancialComponent):
    _component_name = FinancialDataComponentType.BALANCE_SHEET

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _IncomeStatement(_PrismDataComponent, _PrismFinancialComponent):
    _component_name = FinancialDataComponentType.INCOME_STATEMENT

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _DPS(_PrismDataComponent, _PrismFinancialComponent):
    _component_name = FinancialDataComponentType.DPS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _EPS(_PrismDataComponent, _PrismFinancialComponent):
    _component_name = FinancialDataComponentType.EPS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _CashFlow(_PrismDataComponent, _PrismFinancialComponent):
    _component_name = FinancialDataComponentType.CASH_FLOW

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _FinancialDate(_PrismDataComponent):
    _component_name = FinancialDataComponentType.FINANCIAL_DATE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Segment(_PrismDataComponent):
    _component_name = FinancialDataComponentType.SEGMENT

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Ratio(_PrismDataComponent):
    _component_name = FinancialDataComponentType.RATIO

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Commitment(_PrismDataComponent):
    _component_name = FinancialDataComponentType.COMMITMENT

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Pension(_PrismDataComponent):
    _component_name = FinancialDataComponentType.PENSION

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class _Option(_PrismDataComponent):
    _component_name = FinancialDataComponentType.OPTION

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# ------------------------------------------------------------------------------------------------------------------- #
#                                                       Estimate                                                      #
# ------------------------------------------------------------------------------------------------------------------- #
class _Consensus(_PrismDataComponent, _PrismComponent):
    _component_name = EstimateDataComponentType.CONSENSUS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Growth(_PrismDataComponent, _PrismComponent):
    _component_name = EstimateDataComponentType.GROWTH

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Guidance(_PrismDataComponent, _PrismComponent):
    _component_name = EstimateDataComponentType.GUIDANCE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Revision(_PrismDataComponent, _PrismComponent):
    _component_name = EstimateDataComponentType.REVISION

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Actual(_PrismDataComponent, _PrismComponent):
    _component_name = EstimateDataComponentType.ACTUAL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Surprise(_PrismDataComponent, _PrismComponent):
    _component_name = EstimateDataComponentType.SURPRISE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# ------------------------------------------------------------------------------------------------------------------- #
#                                                          SM                                                         #
# ------------------------------------------------------------------------------------------------------------------- #
class _SecurityMasterAttribute(_PrismDataComponent, _PrismComponent):
    _component_name = OtherDataComponentType.SM

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# ------------------------------------------------------------------------------------------------------------------- #
#                                                    Precalculated                                                    #
# ------------------------------------------------------------------------------------------------------------------- #
class _AFL(_PrismDataComponent, _PrismComponent):
    _component_name = PrecalculatedDataComponentType.AFL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# ------------------------------------------------------------------------------------------------------------------- #
#                                                        Index                                                        #
# ------------------------------------------------------------------------------------------------------------------- #
class _IndexShare(_PrismDataComponent, _PrismComponent):
    _component_name = IndexDataComponentType.SHARE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @_validate_args
    @_req_call(_dataquery)
    def get_data(self, startdate: str = None, enddate: str = None, shownid = None, name = None,) -> pd.DataFrame:
        pass


class _IndexWeight(_PrismDataComponent, _PrismComponent):
    _component_name = IndexDataComponentType.WEIGHT

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @_validate_args
    @_req_call(_dataquery)
    def get_data(self, startdate: str = None, enddate: str = None, shownid = None, name = None,) -> pd.DataFrame:
        pass


class _IndexLevel(_PrismDataComponent, _PrismComponent):
    _component_name = IndexDataComponentType.LEVEL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @_validate_args
    @_req_call(_dataquery)
    def get_data(self, startdate: str = None, enddate: str = None, name = None,) -> pd.DataFrame:
        pass


# ------------------------------------------------------------------------------------------------------------------- #
#                                                        Event                                                        #
# ------------------------------------------------------------------------------------------------------------------- #
class _News(_PrismDataComponent):
    _component_name = EventDataComponentType.NEWS


# ------------------------------------------------------------------------------------------------------------------- #
#                                                       Industry                                                      #
# ------------------------------------------------------------------------------------------------------------------- #
class _Airlines(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.AIRLINES

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Bank(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.BANK

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _CapitalMarket(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.CAPITAL_MARKET

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _FinancialServices(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.FINAICIAL_SERVICES

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Healthcare(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.HEALTHCARE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Homebuilders(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.HOMBUILDERS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _HotelandGaming(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.HOTEL_AND_GAMING

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Insurance(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.INSURANCE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _InternetMedia(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.INTERNET_MEDIA

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _ManagedCare(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.MANAGED_CARE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _MetalsandMining(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.METALS_AND_MINING

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _OilandGas(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.OIL_AND_GAS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Pharmaceutical(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.PHARMA

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _RealEstate(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.REAL_ESTATE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Restaurant(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.RESTAURANT

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Retail(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.RETAIL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Semiconductors(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.SEMICONDUCTORS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Telecom(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.TELECOM

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Utility(_PrismDataComponent, _PrismComponent):
    _component_name = IndustryComponentType.UTILITY

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
