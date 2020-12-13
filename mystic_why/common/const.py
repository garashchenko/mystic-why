ENABLE_PER_LED_MSG = [
    0x52,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x08,
    0xFF,
    0x00,
    0x00,
    0x80,
    0x00,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x2A,
    0xFF,
    0x00,
    0x00,
    0x80,
    0x00,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x2A,
    0xFF,
    0x00,
    0x00,
    0x80,
    0x00,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x08,
    0xFF,
    0x00,
    0x00,
    0x80,
    0x00,
    0x28,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x08,
    0xFF,
    0x00,
    0x00,
    0x80,
    0x00,
    0x28,
    0x00,
    0x00,
    0x00,
    0x00,
    0x28,
    0x00,
    0x00,
    0x00,
    0x82,
    0x00,
    0x78,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x28,
    0x00,
    0x00,
    0x00,
    0x80,
    0x00,
    0x25,
    0xFF,
    0x00,
    0x00,
    0xA9,
    0xFF,
    0x00,
    0x00,
    0x87,
    0x00,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x28,
    0x00,
    0xFF,
    0x00,
    0x80,
    0x00,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x28,
    0x00,
    0xFF,
    0x00,
    0x80,
    0x00,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x28,
    0x00,
    0xFF,
    0x00,
    0x80,
    0x00,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x28,
    0x00,
    0xFF,
    0x00,
    0x80,
    0x00,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x28,
    0x00,
    0xFF,
    0x00,
    0x80,
    0x00,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x28,
    0x00,
    0xFF,
    0x00,
    0x80,
    0x00,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x28,
    0x00,
    0xFF,
    0x00,
    0x80,
    0x00,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x28,
    0x00,
    0xFF,
    0x00,
    0x80,
    0x00,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x28,
    0x00,
    0xFF,
    0x00,
    0x80,
    0x00,
    0x01,
    0xFF,
    0x00,
    0x00,
    0x2A,
    0xFF,
    0x00,
    0x00,
    0x80,
    0x00,
    0x00
]
FULL_LIGHT_MSG = [0x52,
            0x01,
            0x00,  # COLOR 1 (index 2)
            0x00,  # COLOR 1 (index 3)
            0x00,  # COLOR 1 (index 4)
            0x08,  # separator?
            0x00,  # COLOR 2 ( index 6)
            0x00,  # COLOR 2 (index 7)
            0x00,  # COLOR 2 (index 8)
            0x80,
            0x00,
            0x01,
            0xFF,
            0x00,
            0x00,
            0x2A,
            0xFF,
            0x00,
            0x00,
            0x80,
            0x00,
            0x01,
            0xFF,
            0x00,
            0x00,
            0x2A,
            0xFF,
            0x00,
            0x00,
            0x80,
            0x00,
            0x01,
            0x00,  # COLOR 3 (index 32)
            0x00,  # COLOR 3 (index 33)
            0x00,  # COLOR 3 (index 34)
            0x08,  # SEPARATOR
            0x00,  # COLOR 4 (index 36)
            0x00,  # COLOR 4 (index 37)
            0x00,  # COLOR 4 (index 38)
            0x80,
            0x00,
            0x64,
            0x01,
            0x00,  # COLOR 5 (index 43)
            0x00,  # COLOR 5 (index 44)
            0x00,  # COLOR 5 (index 45)
            0x08,
            0x00,  # COLOR 6 (index 47)
            0x00,  # COLOR 6 (index 48)
            0x00,  # COLOR 6 (index 49)
            0x80,
            0x00,
            0x64,
            0x00,
            0x00,
            0x00,
            0x00,
            0x28,
            0x00,
            0x00,
            0x00,
            0x82,
            0x4C,
            0x0A,
            0x01,
            0xFF,
            0x00,
            0x00,
            0x28,
            0x00,
            0x00,
            0x00,
            0x80,
            0x00,
            0x01,
            0x00,  # COLOR 7 (index 75)
            0x00,  # COLOR 7 (index 76)
            0x00,  # COLOR 7 (index 78)
            0x08,
            0x00,  # COLOR 8 (index 80)
            0x00,  # COLOR 8 (index 81)
            0x00,  # COLOR 8 (index 82)
            0x81,
            0x00,
            0x01,
            0xFF,
            0x00,
            0x00,
            0x28,
            0x00,
            0xFF,
            0x00,
            0x80,
            0x00,
            0x01,
            0xFF,
            0x00,
            0x00,
            0x28,
            0x00,
            0xFF,
            0x00,
            0x80,
            0x00,
            0x01,
            0xFF,
            0x00,
            0x00,
            0x28,
            0x00,
            0xFF,
            0x00,
            0x80,
            0x00,
            0x01,
            0xFF,
            0x00,
            0x00,
            0x28,
            0x00,
            0xFF,
            0x00,
            0x80,
            0x00,
            0x01,
            0xFF,
            0x00,
            0x00,
            0x28,
            0x00,
            0xFF,
            0x00,
            0x80,
            0x00,
            0x01,
            0xFF,
            0x00,
            0x00,
            0x28,
            0x00,
            0xFF,
            0x00,
            0x80,
            0x00,
            0x01,
            0xFF,
            0x00,
            0x00,
            0x28,
            0x00,
            0xFF,
            0x00,
            0x80,
            0x00,
            0x01,
            0xFF,
            0x00,
            0x00,
            0x28,
            0x00,
            0xFF,
            0x00,
            0x80,
            0x00,
            0x01,
            0xFF,
            0x00,
            0x00,
            0x28,
            0x00,
            0xFF,
            0x00,
            0x80,
            0x00,
            0x01,
            0xFF,
            0x00,
            0x00,
            0x2A,
            0xFF,
            0x00,
            0x00,
            0x80,
            0x00,
            0x00
            ]
PER_LED_MSG_HEADER = [83, 37, 6, 0, 0]

FULL_LIGHT_ONBOARD   = 75
FULL_LIGHT_JRAINBOW1 = 32
FULL_LIGHT_JRAINBOW2 = 43

ONBOARD_LED_COUNT = 7
JRAINBOW1_LED_COUNT = 40
JRAINBOW2_LED_COUNT = 40
CORSAIR_LED_COUNT = 120
EMPTY_TRAIL_LEN = 99

HID_STATE_REPORT_ID = 82
HID_STATE_REPORT_LEN = 185

MSI_PRODUCT_STRING = 'MYSTIC LIGHT '

SETTINGS_FILE = 'default.json'
