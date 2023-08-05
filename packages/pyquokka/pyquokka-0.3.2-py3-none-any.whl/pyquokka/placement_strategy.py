class PlacementStrategy:
    def __init__(self) -> None:
        pass

'''
Launch a single channel. Useful for aggregator nodes etc.
'''
class SingleChannelStrategy(PlacementStrategy):
    def __init__(self) -> None:
        super().__init__()

'''
Launch a custom number of channels per node. Note the default is cpu_count for SourceNodes and 1 for task nodes.
'''
class CustomChannelsStrategy(PlacementStrategy):
    def __init__(self, channels) -> None:
        super().__init__()
        self.channels_per_node = channels


'''
Launch a custom number of channels per ip address.
'''
class DatasetStrategy(PlacementStrategy):
    def __init__(self, total_channels) -> None:
        super().__init__()
        self.total_channels = total_channels

'''
Lance a custom umber of channels per node within a tag. 
'''
class TaggedCustomChannelsStrategy(PlacementStrategy):
    def __init__(self, channels, tag) -> None:
        super().__init__()
        self.channels_per_node = channels
        self.tag = tag
