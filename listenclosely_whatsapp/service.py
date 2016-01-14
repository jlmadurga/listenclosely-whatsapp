# -*- coding: utf-8 -*-
from yowsup_celery.stack import YowsupStack
from yowsup_celery import exceptions as yowsup_exceptions
from listenclosely.services.base import BaseMessageServiceBackend
from listenclosely.services import exceptions as listenclosely_exceptions
from listenclosely_whatsapp import conf
from django.utils.module_loading import import_string
from listenclosely_whatsapp.layer import ListenCloselyLayer
import logging

logger = logging.getLogger(__name__)

class YowsupMessageServiceBackend(BaseMessageServiceBackend):
    """
    Message Service Backend implementation to send instant messages with yowsup
    """
    
    def _get_top_layers(self):
        top_layers = []
        if conf.LISTENCLOSELY_YOWSUP_TOP_LAYERS:
            for top_layer_string in conf.LISTENCLOSELY_YOWSUP_TOP_LAYERS:
                top_layer = import_string(top_layer_string)
                top_layers.append(top_layer)
        top_layers.append(ListenCloselyLayer)
        return tuple(top_layers)
    
    def __init__(self, caller, fail_silently=False, **kwargs):
        super(YowsupMessageServiceBackend, self).__init__(fail_silently, **kwargs)
        try:
            self.stack = YowsupStack((conf.LISTENCLOSELY_YOWSUP_NUMBER, conf.LISTENCLOSELY_YOWSUP_PASS), 
                                     conf.LISTENCLOSELY_YOWSUP_ENCRYPTION, self._get_top_layers())
        except yowsup_exceptions.ConfigurationError as e:
            logger.error("Configuration error") 
            raise listenclosely_exceptions.ConfigurationError("{0}".format(e))
        self.stack.caller = caller
        
    def listen(self):
        """
        Loop to receive messages from whatsapp server. Set autoconnect option to True
        """
        if not self.stack.listening:
            try:
                self.stack.asynloop(auto_connect=True)
            except yowsup_exceptions.AuthenticationError as e:
                raise listenclosely_exceptions.AuthenticationError(str(e))
            except yowsup_exceptions.UnexpectedError as e:
                logger.error("Unexpected error %s" % str(e))
                raise listenclosely_exceptions.UnexpectedError(str(e))
        else:
            logger.warning("Already listening")
            
    def send_message(self, id_service, content):
        """
        Send message to a 
        """
        try:
            message = self.stack.facade.send_message(id_service, content)
            return message.getId()
        except yowsup_exceptions.ConnectionError as e:
            logger.error("Connection error: Message to %s not sent. Please listen before sending messages" % id_service)
            raise listenclosely_exceptions.ConnectionError(str(e))
        except yowsup_exceptions.UnexpectedError as e:
            logger.error("Unexpected error %s" % str(e))
            raise listenclosely_exceptions.UnexpectedError(str(e))
        
    def disconnect(self):
        """
        Disconnect from connection
        """
        try:
            self.stack.facade.disconnect()
        except yowsup_exceptions.ConnectionError as e:
            logger.warning("Trying to disconnect not connected service")
        except yowsup_exceptions.UnexpectedError as e:
            logger.error("Unexpected error %s" % str(e))
            raise listenclosely_exceptions.UnexpectedError(str(e))