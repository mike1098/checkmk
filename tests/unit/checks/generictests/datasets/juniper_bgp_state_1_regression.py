# yapf: disable
checkname = 'juniper_bgp_state'

info = [
    [u'6', u'2', [100, 96, 1, 34]],
    [u'3', u'2', [100, 96, 1, 38]],
]

discovery = {
    '': [
        (u'100.96.1.34', {}),
        (u'100.96.1.38', {}),
    ]
}

checks = {
    '': [
        (u'100.96.1.34', {}, [(0, u'Status with peer 100.96.1.34 is established', []),
                              (0, 'operational status: running', [])]),
        (u'100.96.1.38', {}, [(2, u'Status with peer 100.96.1.38 is active', []),
                              (0, 'operational status: running', [])]),
    ]
}
