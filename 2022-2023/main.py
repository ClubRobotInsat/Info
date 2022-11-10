import can

bus = can.Bus(interface='socketcan',
              channel='vcan0',
              receive_own_messages=True)

message = can.Message(arbitration_id=123, is_extended_id=True,
                      data=[0x11, 0x22, 0x33])
bus.send(message, timeout=0.2)