#! /usr/bin/env python
"""
Sample for python PCSC wrapper module: perform a simple transaction

__author__ = "http://www.gemalto.com"

Copyright 2001-2009 gemalto
Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com

This file is part of pyscard.

pyscard is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.

pyscard is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyscard; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

from smartcard.scard import *


try:
    hresult, hcontext = SCardEstablishContext( SCARD_SCOPE_USER )
    if hresult!=0:
        raise error, 'Failed to establish context: ' + SCardGetErrorMessage(hresult)
    print 'Context established!'

    try:
        hresult, readers = SCardListReaders( hcontext, [] )
        if hresult!=0:
            raise error, 'Failed to list readers:: ' + SCardGetErrorMessage(hresult)
        print 'PCSC Readers:', readers

        if len(readers)<1:
            raise error, 'No smart card readers'

        for zreader in readers:
            print 'Trying to perform transaction on card in', zreader

            try:
                hresult, hcard, dwActiveProtocol = SCardConnect(
                    hcontext, zreader, SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
                if hresult!=0:
                    raise error, 'unable to connect: ' + SCardGetErrorMessage(hresult)
                print 'Connected with active protocol', dwActiveProtocol

                try:
                    hresult = SCardBeginTransaction( hcard )
                    if hresult!=0:
                        raise error, 'failed to begin transaction: ' + SCardGetErrorMessage(hresult)
                    print 'Beginning transaction'

                    hresult, reader, state, protocol, atr = SCardStatus( hcard )
                    if hresult!=0:
                        raise error, 'failed to get status: ' + SCardGetErrorMessage(hresult)
                    print 'ATR:',
                    for i in xrange(len(atr)):
                        print "0x%.2X" % atr[i],
                    print ""

                finally:
                    hresult = SCardEndTransaction( hcard, SCARD_LEAVE_CARD )
                    if hresult!=0:
                        raise error, 'failed to end transaction: ' + SCardGetErrorMessage(hresult)
                    print 'Transaction ended'

                    hresult = SCardDisconnect( hcard, SCARD_UNPOWER_CARD )
                    if hresult!=0:
                        raise error, 'failed to disconnect: ' + SCardGetErrorMessage(hresult)
                    print 'Disconnected'
            except error, (message):
                print error, message

    finally:
        hresult = SCardReleaseContext( hcontext )
        if hresult!=0:
            raise error, 'failed to release context: ' + SCardGetErrorMessage(hresult)
        print 'Released context.'

except error:
    import sys
    print sys.exc_info()[0], ':', sys.exc_info()[1]

import sys
if 'win32'==sys.platform:
    print 'press Enter to continue'
    sys.stdin.read(1)
