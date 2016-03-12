from yowsup.layers.interface import YowInterfaceLayer
from yowsup.layers.interface import ProtocolEntityCallback
import logging

logger = logging.getLogger(__name__)

class ListenCloselyLayer(YowInterfaceLayer):    
    """
    Layer to be just down the top layer of the Yowsup Stack. 
    """
    @ProtocolEntityCallback("message")
    def on_message(self, message_protocol_entity):
        """
        Callback function when receiving message from whatsapp server first to up
        """
        logger.info("Service receives: Message id %s" % message_protocol_entity.getId())
        self.toUpper(message_protocol_entity)
        stack = self.getStack()
        stack.caller.on_message(message_protocol_entity.getId(),
                                message_protocol_entity.getFrom(),
                                message_protocol_entity.getBody())
        
    def __str__(self):
        return "ListenClosely layer"        