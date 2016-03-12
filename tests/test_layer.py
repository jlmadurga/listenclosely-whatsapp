#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from yowsup.layers import YowProtocolLayerTest
from listenclosely_whatsapp.layer import ListenCloselyLayer
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
try:
    from unittest import mock
except ImportError:
    import mock  # noqa

class TestListenCloselyLayer(YowProtocolLayerTest, ListenCloselyLayer):
    
    def setUp(self):
        ListenCloselyLayer.__init__(self)
        
    def test_on_message(self):
        content = "Received message"
        jid = "bbb@s.whatsapp.net"
        with mock.patch("yowsup.layers.YowLayer.getStack", callable=mock.MagicMock()) as mock_stack:
            mock_stack.return_value.caller.on_message = mock.MagicMock()
            msg = TextMessageProtocolEntity(content, _from=jid)
            self.receive(msg)      
            msg_to_upper = self.upperSink.pop()  
            self.assertEqual(msg_to_upper.getFrom(), jid)
            self.assertEqual(msg_to_upper.getBody(), content)
            self.assertEqual(mock_stack.return_value.caller.on_message.call_count, 1)
            args, kwargs = mock_stack.return_value.caller.on_message.call_args
            self.assertEqual(args[0], msg.getId())
            self.assertEqual(args[1], jid)
            self.assertEqual(args[2], content)
        

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
