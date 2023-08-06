from typing import Optional
from datetime import datetime
from pytz import timezone

__all__ = (
    'NextBus',
    'BusArrivalService',
)

class NextBus:
    def __init__(self, **kwargs):
        load_map = {'SEA':"Seats Available", 'SDA':"Standing Avaialble", 'LSD':"Limited Standing"}
        type_map = {'SD':"Single Decker", 'DD':"Double Decker", 'BD':"Bendy"}
        self.orgin_code = kwargs.get('OrginCode',"Not Available")
        self.destination_code = kwargs.get('DestinationCode',"Not Available")
        self.estimated_arrival = datetime.strptime(kwargs['EstimatedArrival'],r'%Y-%m-%dT%H:%M:%S%z') if kwargs.get('EstimatedArrival','') != '' else "No Estimated Time"
        self.latitude = kwargs.get('Latitude',0.0)
        self.longitude = kwargs.get('Longitude',0.0)
        self.visit_number = int(kwargs['VisitNumber']) if kwargs.get('VisitNumber','') != '' else "Not Available"
        self.load = load_map.get(kwargs.get('Load',None),"Not Available")
        self.feature = "Not Wheel-chair Accessible" if kwargs.get('Feature','') == '' else "Wheel-chair Accessible"
        self.type = type_map.get(kwargs.get('Type'),"Not Available")

class BusArrivalService:
    def __init__(self,**kwargs):
        '''
        service_no: Optional[int]
        operator: str
        next_1: NextBus
        next_2: NextBus
        next_3: NextBus
        secs_to_arrival: Optional[int]
        '''
        operator_map = {'SBST': "SBS Transit",
                        'SMRT': "SMRT Corporation",
                        'TTS': "Tower Transit Singapore",
                        'GAS': "Go Ahead Singapore"}
        self.service_no : Optional[int] = kwargs.get('ServiceNo',None)
        self.operator : str = operator_map.get(kwargs.get('Operator',None),"Not Available")
        self.next_1: NextBus = NextBus(**kwargs.get('NextBus',{}))
        self.next_2: NextBus = NextBus(**kwargs.get('NextBus2',{}))
        self.next_3: NextBus = NextBus(**kwargs.get('NextBus3',{}))
        self.secs_to_arrival : Optional[int] = None
        if self.next_1.estimated_arrival == "No Estimated Time":
            self.secs_to_arrival = None
        secs_to_arrival = self.next_1.estimated_arrival - timezone('Asia/Singapore').localize(datetime.now())
        if secs_to_arrival.days == -1:
            self.secs_to_arrival = 0
        else:
            self.secs_to_arrival = secs_to_arrival.seconds

