/* Copyright (c) 2016, Google Inc.
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
 * SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
 * OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
 * CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE. */

#include <openssl/curve25519.h>

#include <assert.h>
#include <string.h>

#include <openssl/bytestring.h>
#include <openssl/mem.h>
#include <openssl/rand.h>
#include <openssl/sha.h>

#include "../fipsmodule/bn/internal.h"
#include "../internal.h"
#include "./internal.h"


// The following precomputation tables are for the following
// points used in the SPAKE2 protocol.
//
// N:
//   x: 49918732221787544735331783592030787422991506689877079631459872391322455579424
//   y: 54629554431565467720832445949441049581317094546788069926228343916274969994000
//   encoded: 10e3df0ae37d8e7a99b5fe74b44672103dbddcbd06af680d71329a11693bc778
//
// M:
//   x: 31406539342727633121250288103050113562375374900226415211311216773867585644232
//   y: 21177308356423958466833845032658859666296341766942662650232962324899758529114
//   encoded: 5ada7e4bf6ddd9adb6626d32131c6b5c51a1e347a3478f53cfcf441b88eed12e
//
// These points and their precomputation tables are generated with the
// following Python code. For a description of the precomputation table,
// see curve25519.c in this directory.
//
// Exact copies of the source code are kept in bug 27296743.

/*
import hashlib
import ed25519 as E  # http://ed25519.cr.yp.to/python/ed25519.py

SEED_N = 'edwards25519 point generation seed (N)'
SEED_M = 'edwards25519 point generation seed (M)'

def genpoint(seed):
    v = hashlib.sha256(seed).digest()
    it = 1
    while True:
        try:
            x,y = E.decodepoint(v)
        except Exception, e:
            print e
            it += 1
            v = hashlib.sha256(v).digest()
            continue
        print "Found in %d iterations:" % it
        print "  x = %d" % x
        print "  y = %d" % y
        print " Encoded (hex)"
        print E.encodepoint((x,y)).encode('hex')
        return (x,y)

def gentable(P):
    t = []
    for i in range(1,16):
        k = ((i >> 3 & 1) * (1 << 192) +
             (i >> 2 & 1) * (1 << 128) +
             (i >> 1 & 1) * (1 <<  64) +
             (i      & 1))
        t.append(E.scalarmult(P, k))
    return ''.join(E.encodeint(x) + E.encodeint(y) for (x,y) in t)

def printtable(table, name):
    print "static const uint8_t %s[15 * 2 * 32] = {" % name,
    for i in range(15 * 2 * 32):
        if i % 12 == 0:
            print "\n   ",
        print " 0x%02x," % ord(table[i]),
    print "\n};"

if __name__ == "__main__":
    print "Searching for N"
    N = genpoint(SEED_N)
    print "Generating precomputation table for N"
    Ntable = gentable(N)
    printtable(Ntable, "kSpakeNSmallPrecomp")

    print "Searching for M"
    M = genpoint(SEED_M)
    print "Generating precomputation table for M"
    Mtable = gentable(M)
    printtable(Mtable, "kSpakeMSmallPrecomp")
*/

static const uint8_t kSpakeNSmallPrecomp[15 * 2 * 32] = {
    0x20, 0x1b, 0xc5, 0xb3, 0x43, 0x17, 0x71, 0x10, 0x44, 0x1e, 0x73, 0xb3,
    0xae, 0x3f, 0xbf, 0x9f, 0xf5, 0x44, 0xc8, 0x13, 0x8f, 0xd1, 0x01, 0xc2,
    0x8a, 0x1a, 0x6d, 0xea, 0x4d, 0x00, 0x5d, 0x6e, 0x10, 0xe3, 0xdf, 0x0a,
    0xe3, 0x7d, 0x8e, 0x7a, 0x99, 0xb5, 0xfe, 0x74, 0xb4, 0x46, 0x72, 0x10,
    0x3d, 0xbd, 0xdc, 0xbd, 0x06, 0xaf, 0x68, 0x0d, 0x71, 0x32, 0x9a, 0x11,
    0x69, 0x3b, 0xc7, 0x78, 0x93, 0xf1, 0x57, 0x97, 0x6e, 0xf0, 0x6e, 0x45,
    0x37, 0x4a, 0xf4, 0x0b, 0x18, 0x51, 0xf5, 0x4f, 0x67, 0x3c, 0xdc, 0xec,
    0x84, 0xed, 0xd0, 0xeb, 0xca, 0xfb, 0xdb, 0xff, 0x7f, 0xeb, 0xa8, 0x23,
    0x68, 0x87, 0x13, 0x64, 0x6a, 0x10, 0xf7, 0x45, 0xe0, 0x0f, 0x32, 0x21,
    0x59, 0x7c, 0x0e, 0x50, 0xad, 0x56, 0xd7, 0x12, 0x69, 0x7b, 0x58, 0xf8,
    0xb9, 0x3b, 0xa5, 0xbb, 0x4d, 0x1b, 0x87, 0x1c, 0x46, 0xa7, 0x17, 0x9d,
    0x6d, 0x84, 0x45, 0xbe, 0x7f, 0x95, 0xd2, 0x34, 0xcd, 0x89, 0x95, 0xc0,
    0xf0, 0xd3, 0xdf, 0x6e, 0x10, 0x4a, 0xe3, 0x7b, 0xce, 0x7f, 0x40, 0x27,
    0xc7, 0x2b, 0xab, 0x66, 0x03, 0x59, 0xb4, 0x7b, 0xc7, 0xc7, 0xf0, 0x39,
    0x9a, 0x33, 0x35, 0xbf, 0xcc, 0x2f, 0xf3, 0x2e, 0x68, 0x9d, 0x53, 0x5c,
    0x88, 0x52, 0xe3, 0x77, 0x90, 0xa1, 0x27, 0x85, 0xc5, 0x74, 0x7f, 0x23,
    0x0e, 0x93, 0x01, 0x3e, 0xe7, 0x2e, 0x2e, 0x95, 0xf3, 0x0d, 0xc2, 0x25,
    0x25, 0x39, 0x39, 0x3d, 0x6e, 0x8e, 0x89, 0xbd, 0xe8, 0xbb, 0x67, 0x5e,
    0x8c, 0x66, 0x8b, 0x63, 0x28, 0x1e, 0x4e, 0x74, 0x85, 0xa8, 0xaf, 0x0f,
    0x12, 0x5d, 0xb6, 0x8a, 0x83, 0x1a, 0x77, 0x76, 0x5e, 0x62, 0x8a, 0xa7,
    0x3c, 0xb8, 0x05, 0x57, 0x2b, 0xaf, 0x36, 0x2e, 0x10, 0x90, 0xb2, 0x39,
    0xb4, 0x3e, 0x75, 0x6d, 0x3a, 0xa8, 0x31, 0x35, 0xc2, 0x1e, 0x8f, 0xc2,
    0x79, 0x89, 0x35, 0x16, 0x26, 0xd1, 0xc7, 0x0b, 0x04, 0x1f, 0x1d, 0xf9,
    0x9c, 0x05, 0xa6, 0x6b, 0xb5, 0x19, 0x5a, 0x24, 0x6d, 0x91, 0xc5, 0x31,
    0xfd, 0xc5, 0xfa, 0xe7, 0xa6, 0xcb, 0x0e, 0x4b, 0x18, 0x0d, 0x94, 0xc7,
    0xee, 0x1d, 0x46, 0x1f, 0x92, 0xb1, 0xb2, 0x4a, 0x2b, 0x43, 0x37, 0xfe,
    0xc2, 0x15, 0x11, 0x89, 0xef, 0x59, 0x73, 0x3c, 0x06, 0x76, 0x78, 0xcb,
    0xa6, 0x0d, 0x79, 0x5f, 0x28, 0x0b, 0x5b, 0x8c, 0x9e, 0xe4, 0xaa, 0x51,
    0x9a, 0x42, 0x6f, 0x11, 0x50, 0x3d, 0x01, 0xd6, 0x21, 0xc0, 0x99, 0x5e,
    0x1a, 0xe8, 0x81, 0x25, 0x80, 0xeb, 0xed, 0x5d, 0x37, 0x47, 0x30, 0x70,
    0xa0, 0x4e, 0x0b, 0x43, 0x17, 0xbe, 0xb6, 0x47, 0xe7, 0x2a, 0x62, 0x9d,
    0x5d, 0xa6, 0xc5, 0x33, 0x62, 0x9d, 0x56, 0x24, 0x9d, 0x1d, 0xb2, 0x13,
    0xbc, 0x17, 0x66, 0x43, 0xd1, 0x68, 0xd5, 0x3b, 0x17, 0x69, 0x17, 0xa6,
    0x06, 0x9e, 0x12, 0xb8, 0x7c, 0xd5, 0xaf, 0x3e, 0x21, 0x1b, 0x31, 0xeb,
    0x0b, 0xa4, 0x98, 0x1c, 0xf2, 0x6a, 0x5e, 0x7c, 0x9b, 0x45, 0x8f, 0xb2,
    0x12, 0x06, 0xd5, 0x8c, 0x1d, 0xb2, 0xa7, 0x57, 0x5f, 0x2f, 0x4f, 0xdb,
    0x52, 0x99, 0x7c, 0x58, 0x01, 0x5f, 0xf2, 0xa5, 0xf6, 0x51, 0x86, 0x21,
    0x2f, 0x5b, 0x8d, 0x6a, 0xae, 0x83, 0x34, 0x6d, 0x58, 0x4b, 0xef, 0xfe,
    0xbf, 0x73, 0x5d, 0xdb, 0xc4, 0x97, 0x2a, 0x85, 0xf3, 0x6c, 0x46, 0x42,
    0xb3, 0x90, 0xc1, 0x57, 0x97, 0x50, 0x35, 0xb1, 0x9d, 0xb7, 0xc7, 0x3c,
    0x85, 0x6d, 0x6c, 0xfd, 0xce, 0xb0, 0xc9, 0xa2, 0x77, 0xee, 0xc3, 0x6b,
    0x0c, 0x37, 0xfa, 0x30, 0x91, 0xd1, 0x2c, 0xb8, 0x5e, 0x7f, 0x81, 0x5f,
    0x87, 0xfd, 0x18, 0x02, 0x5a, 0x30, 0x4e, 0x62, 0xbc, 0x65, 0xc6, 0xce,
    0x1a, 0xcf, 0x2b, 0xaa, 0x56, 0x3e, 0x4d, 0xcf, 0xba, 0x62, 0x5f, 0x9a,
    0xd0, 0x72, 0xff, 0xef, 0x28, 0xbd, 0xbe, 0xd8, 0x57, 0x3d, 0xf5, 0x57,
    0x7d, 0xe9, 0x71, 0x31, 0xec, 0x98, 0x90, 0x94, 0xd9, 0x54, 0xbf, 0x84,
    0x0b, 0xe3, 0x06, 0x47, 0x19, 0x9a, 0x13, 0x1d, 0xef, 0x9d, 0x13, 0xf3,
    0xdb, 0xc3, 0x5c, 0x72, 0x9e, 0xed, 0x24, 0xaa, 0x64, 0xed, 0xe7, 0x0d,
    0xa0, 0x7c, 0x73, 0xba, 0x9b, 0x86, 0xa7, 0x3b, 0x55, 0xab, 0x58, 0x30,
    0xf1, 0x15, 0x81, 0x83, 0x2f, 0xf9, 0x62, 0x84, 0x98, 0x66, 0xf6, 0x55,
    0x21, 0xd8, 0xf2, 0x25, 0x64, 0x71, 0x4b, 0x12, 0x76, 0x59, 0xc5, 0xaa,
    0x93, 0x67, 0xc3, 0x86, 0x25, 0xab, 0x4e, 0x4b, 0xf6, 0xd8, 0x3f, 0x44,
    0x2e, 0x11, 0xe0, 0xbd, 0x6a, 0xf2, 0x5d, 0xf5, 0xf9, 0x53, 0xea, 0xa4,
    0xc8, 0xd9, 0x50, 0x33, 0x81, 0xd9, 0xa8, 0x2d, 0x91, 0x7d, 0x13, 0x2a,
    0x11, 0xcf, 0xde, 0x3f, 0x0a, 0xd2, 0xbc, 0x33, 0xb2, 0x62, 0x53, 0xea,
    0x77, 0x88, 0x43, 0x66, 0x27, 0x43, 0x85, 0xe9, 0x5f, 0x55, 0xf5, 0x2a,
    0x8a, 0xac, 0xdf, 0xff, 0x9b, 0x4c, 0x96, 0x9c, 0xa5, 0x7a, 0xce, 0xd5,
    0x79, 0x18, 0xf1, 0x0b, 0x58, 0x95, 0x7a, 0xe7, 0xd3, 0x74, 0x65, 0x0b,
    0xa4, 0x64, 0x30, 0xe8, 0x5c, 0xfc, 0x55, 0x56, 0xee, 0x14, 0x14, 0xd3,
    0x45, 0x3b, 0xf8, 0xde, 0x05, 0x3e, 0xb9, 0x3c, 0xd7, 0x6a, 0x52, 0x72,
    0x5b, 0x39, 0x09, 0xbe, 0x82, 0x23, 0x10, 0x4a, 0xb7, 0xc3, 0xdc, 0x4c,
    0x5d, 0xc9, 0xf1, 0x14, 0x83, 0xf9, 0x0b, 0x9b, 0xe9, 0x23, 0x84, 0x6a,
    0xc4, 0x08, 0x3d, 0xda, 0x3d, 0x12, 0x95, 0x87, 0x18, 0xa4, 0x7d, 0x3f,
    0x23, 0xde, 0xd4, 0x1e, 0xa8, 0x47, 0xc3, 0x71, 0xdb, 0xf5, 0x03, 0x6c,
    0x57, 0xe7, 0xa4, 0x43, 0x82, 0x33, 0x7b, 0x62, 0x46, 0x7d, 0xf7, 0x10,
    0x69, 0x18, 0x38, 0x27, 0x9a, 0x6f, 0x38, 0xac, 0xfa, 0x92, 0xc5, 0xae,
    0x66, 0xa6, 0x73, 0x95, 0x15, 0x0e, 0x4c, 0x04, 0xb6, 0xfc, 0xf5, 0xc7,
    0x21, 0x3a, 0x99, 0xdb, 0x0e, 0x36, 0xf0, 0x56, 0xbc, 0x75, 0xf9, 0x87,
    0x9b, 0x11, 0x18, 0x92, 0x64, 0x1a, 0xe7, 0xc7, 0xab, 0x5a, 0xc7, 0x26,
    0x7f, 0x13, 0x98, 0x42, 0x52, 0x43, 0xdb, 0xc8, 0x6d, 0x0b, 0xb7, 0x31,
    0x93, 0x24, 0xd6, 0xe8, 0x24, 0x1f, 0x6f, 0x21, 0xa7, 0x8c, 0xeb, 0xdb,
    0x83, 0xb8, 0x89, 0xe3, 0xc1, 0xd7, 0x69, 0x3b, 0x02, 0x6b, 0x54, 0x0f,
    0x84, 0x2f, 0xb5, 0x5c, 0x17, 0x77, 0xbe, 0xe5, 0x61, 0x0d, 0xc5, 0xdf,
    0x3b, 0xcf, 0x3e, 0x93, 0x4f, 0xf5, 0x89, 0xb9, 0x5a, 0xc5, 0x29, 0x31,
    0xc0, 0xc2, 0xff, 0xe5, 0x3f, 0xa6, 0xac, 0x03, 0xca, 0xf5, 0xff, 0xe0,
    0x36, 0xce, 0xf3, 0xe2, 0xb7, 0x9c, 0x02, 0xe9, 0x9e, 0xd2, 0xbc, 0x87,
    0x2f, 0x3d, 0x9a, 0x1d, 0x8f, 0xc5, 0x72, 0xb8, 0xa2, 0x01, 0xd4, 0x68,
    0xb1, 0x84, 0x16, 0x10, 0xf6, 0xf3, 0x52, 0x25, 0xd9, 0xdc, 0x4c, 0xdd,
    0x0f, 0xd6, 0x4a, 0xcf, 0x60, 0x96, 0x7e, 0xcc, 0x42, 0x0f, 0x64, 0x9d,
    0x72, 0x46, 0x04, 0x07, 0xf2, 0x5b, 0xf4, 0x07, 0xd1, 0xf4, 0x59, 0x71,
};

static const uint8_t kSpakeMSmallPrecomp[15 * 2 * 32] = {
    0xc8, 0xa6, 0x63, 0xc5, 0x97, 0xf1, 0xee, 0x40, 0xab, 0x62, 0x42, 0xee,
    0x25, 0x6f, 0x32, 0x6c, 0x75, 0x2c, 0xa7, 0xd3, 0xbd, 0x32, 0x3b, 0x1e,
    0x11, 0x9c, 0xbd, 0x04, 0xa9, 0x78, 0x6f, 0x45, 0x5a, 0xda, 0x7e, 0x4b,
    0xf6, 0xdd, 0xd9, 0xad, 0xb6, 0x62, 0x6d, 0x32, 0x13, 0x1c, 0x6b, 0x5c,
    0x51, 0xa1, 0xe3, 0x47, 0xa3, 0x47, 0x8f, 0x53, 0xcf, 0xcf, 0x44, 0x1b,
    0x88, 0xee, 0xd1, 0x2e, 0x03, 0x89, 0xaf, 0xc0, 0x61, 0x2d, 0x9e, 0x35,
    0xeb, 0x0e, 0x03, 0xe0, 0xb7, 0xfb, 0xa5, 0xbc, 0x44, 0xbe, 0x0c, 0x89,
    0x0a, 0x0f, 0xd6, 0x59, 0x47, 0x9e, 0xe6, 0x3d, 0x36, 0x9d, 0xff, 0x44,
    0x5e, 0xac, 0xab, 0xe5, 0x3a, 0xd5, 0xb0, 0x35, 0x9f, 0x6d, 0x7f, 0xba,
    0xc0, 0x85, 0x0e, 0xf4, 0x70, 0x3f, 0x13, 0x90, 0x4c, 0x50, 0x1a, 0xee,
    0xc5, 0xeb, 0x69, 0xfe, 0x98, 0x42, 0x87, 0x1d, 0xce, 0x6c, 0x29, 0xaa,
    0x2b, 0x31, 0xc2, 0x38, 0x7b, 0x6b, 0xee, 0x88, 0x0b, 0xba, 0xce, 0xa8,
    0xca, 0x19, 0x60, 0x1b, 0x16, 0xf1, 0x25, 0x1e, 0xcf, 0x63, 0x66, 0x1e,
    0xbb, 0x63, 0xeb, 0x7d, 0xca, 0xd2, 0xb4, 0x23, 0x5a, 0x01, 0x6f, 0x05,
    0xd1, 0xdc, 0x41, 0x73, 0x75, 0xc0, 0xfd, 0x30, 0x91, 0x52, 0x68, 0x96,
    0x45, 0xb3, 0x66, 0x01, 0x3b, 0x53, 0x89, 0x3c, 0x69, 0xbc, 0x6c, 0x69,
    0xe3, 0x51, 0x8f, 0xe3, 0xd2, 0x84, 0xd5, 0x28, 0x66, 0xb5, 0xe6, 0x06,
    0x09, 0xfe, 0x6d, 0xb0, 0x72, 0x16, 0xe0, 0x8a, 0xce, 0x61, 0x65, 0xa9,
    0x21, 0x32, 0x48, 0xdc, 0x7a, 0x1d, 0xe1, 0x38, 0x7f, 0x8c, 0x75, 0x88,
    0x3d, 0x08, 0xa9, 0x4a, 0x6f, 0x3d, 0x9f, 0x7f, 0x3f, 0xbd, 0x57, 0x6b,
    0x19, 0xce, 0x3f, 0x4a, 0xc9, 0xd3, 0xf9, 0x6e, 0x72, 0x7b, 0x5b, 0x74,
    0xea, 0xbe, 0x9c, 0x7a, 0x6d, 0x9c, 0x40, 0x49, 0xe6, 0xfb, 0x2a, 0x1a,
    0x75, 0x70, 0xe5, 0x4e, 0xed, 0x74, 0xe0, 0x75, 0xac, 0xc0, 0xb1, 0x11,
    0x3e, 0xf2, 0xaf, 0x88, 0x4d, 0x66, 0xb6, 0xf6, 0x15, 0x4f, 0x3c, 0x6c,
    0x77, 0xae, 0x47, 0x51, 0x63, 0x9a, 0xfe, 0xe1, 0xb4, 0x1a, 0x12, 0xdf,
    0xe9, 0x54, 0x8d, 0x3b, 0x30, 0x2a, 0x75, 0xe3, 0xe5, 0x29, 0xb1, 0x4c,
    0xb0, 0x7c, 0x6d, 0xb5, 0xae, 0x85, 0xdb, 0x1e, 0x38, 0x55, 0x96, 0xa5,
    0x5b, 0x9f, 0x15, 0x23, 0x28, 0x36, 0xb8, 0xa2, 0x41, 0xb4, 0xd7, 0x19,
    0x91, 0x8d, 0x26, 0x3e, 0xca, 0x9c, 0x05, 0x7a, 0x2b, 0x60, 0x45, 0x86,
    0x8b, 0xee, 0x64, 0x6f, 0x5c, 0x09, 0x4d, 0x4b, 0x5a, 0x7f, 0xb0, 0xc3,
    0x26, 0x9d, 0x8b, 0xb8, 0x83, 0x69, 0xcf, 0x16, 0x72, 0x62, 0x3e, 0x5e,
    0x53, 0x4f, 0x9c, 0x73, 0x76, 0xfc, 0x19, 0xef, 0xa0, 0x74, 0x3a, 0x11,
    0x1e, 0xd0, 0x4d, 0xb7, 0x87, 0xa1, 0xd6, 0x87, 0x6c, 0x0e, 0x6c, 0x8c,
    0xe9, 0xa0, 0x44, 0xc4, 0x72, 0x3e, 0x73, 0x17, 0x13, 0xd1, 0x4e, 0x3d,
    0x8e, 0x1d, 0x5a, 0x8b, 0x75, 0xcb, 0x59, 0x2c, 0x47, 0x87, 0x15, 0x41,
    0xfe, 0x08, 0xe9, 0xa6, 0x97, 0x17, 0x08, 0x26, 0x6a, 0xb5, 0xbb, 0x73,
    0xaa, 0xb8, 0x5b, 0x65, 0x65, 0x5b, 0x30, 0x9e, 0x62, 0x59, 0x02, 0xf8,
    0xb8, 0x0f, 0x32, 0x10, 0xc1, 0x36, 0x08, 0x52, 0x98, 0x4a, 0x1e, 0xf0,
    0xab, 0x21, 0x5e, 0xde, 0x16, 0x0c, 0xda, 0x09, 0x99, 0x6b, 0x9e, 0xc0,
    0x90, 0xa5, 0x5a, 0xcc, 0xb0, 0xb7, 0xbb, 0xd2, 0x8b, 0x5f, 0xd3, 0x3b,
    0x3e, 0x8c, 0xa5, 0x71, 0x66, 0x06, 0xe3, 0x28, 0xd4, 0xf8, 0x3f, 0xe5,
    0x27, 0xdf, 0xfe, 0x0f, 0x09, 0xb2, 0x8a, 0x09, 0x5a, 0x23, 0x61, 0x0d,
    0x2d, 0xf5, 0x44, 0xf1, 0x5c, 0xf8, 0x82, 0x4e, 0xdc, 0x78, 0x7a, 0xab,
    0xc3, 0x57, 0x91, 0xaf, 0x65, 0x6e, 0x71, 0xf1, 0x44, 0xbf, 0xed, 0x43,
    0x50, 0xb4, 0x67, 0x48, 0xef, 0x5a, 0x10, 0x46, 0x81, 0xb4, 0x0c, 0xc8,
    0x48, 0xed, 0x99, 0x7a, 0x45, 0xa5, 0x92, 0xc3, 0x69, 0xd6, 0xd7, 0x8a,
    0x20, 0x1b, 0xeb, 0x8f, 0xb2, 0xff, 0xec, 0x6d, 0x76, 0x04, 0xf8, 0xc2,
    0x58, 0x9b, 0xf2, 0x20, 0x53, 0xc4, 0x74, 0x91, 0x19, 0xdd, 0x2d, 0x12,
    0x53, 0xc7, 0x6e, 0xd0, 0x02, 0x51, 0x3c, 0xa6, 0x7d, 0x80, 0x75, 0x6b,
    0x1d, 0xdf, 0xf8, 0x6a, 0x52, 0xbb, 0x81, 0xf8, 0x30, 0x45, 0xef, 0x51,
    0x85, 0x36, 0xbe, 0x8e, 0xcf, 0x0b, 0x9a, 0x46, 0xe8, 0x3f, 0x99, 0xfd,
    0xf7, 0xd9, 0x3e, 0x84, 0xe5, 0xe3, 0x37, 0xcf, 0x98, 0x7f, 0xeb, 0x5e,
    0x5a, 0x53, 0x77, 0x1c, 0x20, 0xdc, 0xf1, 0x20, 0x99, 0xec, 0x60, 0x40,
    0x93, 0xef, 0x5c, 0x1c, 0x81, 0xe2, 0xa5, 0xad, 0x2a, 0xc2, 0xdb, 0x6b,
    0xc1, 0x7e, 0x8f, 0xa9, 0x23, 0x5b, 0xd9, 0x0d, 0xfe, 0xa0, 0xac, 0x11,
    0x28, 0xba, 0x8e, 0x92, 0x07, 0x2d, 0x07, 0x40, 0x83, 0x14, 0x4c, 0x35,
    0x8d, 0xd0, 0x11, 0xff, 0x98, 0xdb, 0x00, 0x30, 0x6f, 0x65, 0xb6, 0xa0,
    0x7f, 0x9c, 0x08, 0xb8, 0xce, 0xb3, 0xa8, 0x42, 0xd3, 0x84, 0x45, 0xe1,
    0xe3, 0x8f, 0xa6, 0x89, 0x21, 0xd7, 0x74, 0x02, 0x4d, 0x64, 0xdf, 0x54,
    0x15, 0x9e, 0xba, 0x12, 0x49, 0x09, 0x41, 0xf6, 0x10, 0x24, 0xa1, 0x84,
    0x15, 0xfd, 0x68, 0x6a, 0x57, 0x66, 0xb3, 0x6d, 0x4c, 0xea, 0xbf, 0xbc,
    0x60, 0x3f, 0x52, 0x1c, 0x44, 0x1b, 0xc0, 0x4a, 0x25, 0xe3, 0xd9, 0x4c,
    0x9a, 0x74, 0xad, 0xfc, 0x9e, 0x8d, 0x0b, 0x18, 0x66, 0x24, 0xd1, 0x06,
    0xac, 0x68, 0xc1, 0xae, 0x14, 0xce, 0xb1, 0xf3, 0x86, 0x9f, 0x87, 0x11,
    0xd7, 0x9f, 0x30, 0x92, 0xdb, 0xec, 0x0b, 0x4a, 0xe8, 0xf6, 0x53, 0x36,
    0x68, 0x12, 0x11, 0x5e, 0xe0, 0x34, 0xa4, 0xff, 0x00, 0x0a, 0x26, 0xb8,
    0x62, 0x79, 0x9c, 0x0c, 0xd5, 0xe5, 0xf5, 0x1c, 0x1a, 0x16, 0x84, 0x4d,
    0x8e, 0x5d, 0x31, 0x7e, 0xf7, 0xe2, 0xd3, 0xa1, 0x41, 0x90, 0x61, 0x5d,
    0x04, 0xb2, 0x9a, 0x18, 0x9e, 0x54, 0xfb, 0xd1, 0x61, 0x95, 0x1b, 0x08,
    0xca, 0x7c, 0x49, 0x44, 0x74, 0x1d, 0x2f, 0xca, 0xc4, 0x7a, 0xe1, 0x8b,
    0x2f, 0xbb, 0x96, 0xee, 0x19, 0x8a, 0x5d, 0xfb, 0x3e, 0x82, 0xe7, 0x15,
    0xdb, 0x29, 0x14, 0xee, 0xc9, 0x4d, 0x9a, 0xfb, 0x9f, 0x8a, 0xbb, 0x17,
    0x37, 0x1b, 0x6e, 0x28, 0x6c, 0xf9, 0xff, 0xb5, 0xb5, 0x8b, 0x9d, 0x88,
    0x20, 0x08, 0x10, 0xd7, 0xca, 0x58, 0xf6, 0xe1, 0x32, 0x91, 0x6f, 0x36,
    0xc0, 0xad, 0xc1, 0x57, 0x5d, 0x76, 0x31, 0x43, 0xf3, 0xdd, 0xec, 0xf1,
    0xa9, 0x79, 0xe9, 0xe9, 0x85, 0xd7, 0x91, 0xc7, 0x31, 0x62, 0x3c, 0xd2,
    0x90, 0x2c, 0x9c, 0xa4, 0x56, 0x37, 0x7b, 0xbe, 0x40, 0x58, 0xc0, 0x81,
    0x83, 0x22, 0xe8, 0x13, 0x79, 0x18, 0xdb, 0x3a, 0x1b, 0x31, 0x0d, 0x00,
    0x6c, 0x22, 0x62, 0x75, 0x70, 0xd8, 0x96, 0x59, 0x99, 0x44, 0x79, 0x71,
    0xa6, 0x76, 0x81, 0x28, 0xb2, 0x65, 0xe8, 0x47, 0x14, 0xc6, 0x39, 0x06,
};

SPAKE2_CTX *SPAKE2_CTX_new(enum spake2_role_t my_role,
                           const uint8_t *my_name, size_t my_name_len,
                           const uint8_t *their_name, size_t their_name_len) {
  SPAKE2_CTX *ctx = OPENSSL_malloc(sizeof(SPAKE2_CTX));
  if (ctx == NULL) {
    return NULL;
  }

  OPENSSL_memset(ctx, 0, sizeof(SPAKE2_CTX));
  ctx->my_role = my_role;

  CBS my_name_cbs, their_name_cbs;
  CBS_init(&my_name_cbs, my_name, my_name_len);
  CBS_init(&their_name_cbs, their_name, their_name_len);
  if (!CBS_stow(&my_name_cbs, &ctx->my_name, &ctx->my_name_len) ||
      !CBS_stow(&their_name_cbs, &ctx->their_name, &ctx->their_name_len)) {
    SPAKE2_CTX_free(ctx);
    return NULL;
  }

  return ctx;
}

void SPAKE2_CTX_free(SPAKE2_CTX *ctx) {
  if (ctx == NULL) {
    return;
  }

  OPENSSL_free(ctx->my_name);
  OPENSSL_free(ctx->their_name);
  OPENSSL_free(ctx);
}

// left_shift_3 sets |n| to |n|*8, where |n| is represented in little-endian
// order.
static void left_shift_3(uint8_t n[32]) {
  uint8_t carry = 0;
  unsigned i;

  for (i = 0; i < 32; i++) {
    const uint8_t next_carry = n[i] >> 5;
    n[i] = (n[i] << 3) | carry;
    carry = next_carry;
  }
}

typedef struct {
  BN_ULONG words[32 / sizeof(BN_ULONG)];
} scalar;

// kOrder is the order of the prime-order subgroup of curve25519.
static const scalar kOrder = {
    {TOBN(0x5812631a, 0x5cf5d3ed), TOBN(0x14def9de, 0xa2f79cd6),
     TOBN(0x00000000, 0x00000000), TOBN(0x10000000, 0x00000000)}};

// scalar_cmov copies |src| to |dest| if |mask| is all ones.
static void scalar_cmov(scalar *dest, const scalar *src, crypto_word_t mask) {
  bn_select_words(dest->words, mask, src->words, dest->words,
                  OPENSSL_ARRAY_SIZE(dest->words));
}

// scalar_double sets |s| to |2×s|.
static void scalar_double(scalar *s) {
  bn_add_words(s->words, s->words, s->words, OPENSSL_ARRAY_SIZE(s->words));
}

// scalar_add sets |dest| to |dest| plus |src|.
static void scalar_add(scalar *dest, const scalar *src) {
  bn_add_words(dest->words, dest->words, src->words,
               OPENSSL_ARRAY_SIZE(dest->words));
}

int SPAKE2_generate_msg(SPAKE2_CTX *ctx, uint8_t *out, size_t *out_len,
                         size_t max_out_len, const uint8_t *password,
                         size_t password_len) {
  if (ctx->state != spake2_state_init) {
    return 0;
  }

  if (max_out_len < sizeof(ctx->my_msg)) {
    return 0;
  }

  uint8_t private_tmp[64];
  RAND_bytes(private_tmp, sizeof(private_tmp));
  x25519_sc_reduce(private_tmp);
  // Multiply by the cofactor (eight) so that we'll clear it when operating on
  // the peer's point later in the protocol.
  left_shift_3(private_tmp);
  OPENSSL_memcpy(ctx->private_key, private_tmp, sizeof(ctx->private_key));

  ge_p3 P;
  x25519_ge_scalarmult_base(&P, ctx->private_key);

  // mask = h(password) * <N or M>.
  uint8_t password_tmp[SHA512_DIGEST_LENGTH];
  SHA512(password, password_len, password_tmp);
  OPENSSL_memcpy(ctx->password_hash, password_tmp, sizeof(ctx->password_hash));
  x25519_sc_reduce(password_tmp);

  // Due to a copy-paste error, the call to |left_shift_3| was omitted after
  // the |x25519_sc_reduce|, just above. This meant that |ctx->password_scalar|
  // was not a multiple of eight to clear the cofactor and thus three bits of
  // the password hash would leak. In order to fix this in a unilateral way,
  // points of small order are added to the mask point such that it is in the
  // prime-order subgroup. Since the ephemeral scalar is a multiple of eight,
  // these points will cancel out when calculating the shared secret.
  //
  // Adding points of small order is the same as adding multiples of the prime
  // order to the password scalar. Since that's faster, that is what is done
  // below. The prime order (kOrder) is a large prime, thus odd, thus the LSB
  // is one. So adding it will flip the LSB. Adding twice it will flip the next
  // bit and so one for all the bottom three bits.

  scalar password_scalar;
  OPENSSL_memcpy(&password_scalar, password_tmp, sizeof(password_scalar));

  // |password_scalar| is the result of |x25519_sc_reduce| and thus is, at
  // most, $l-1$ (where $l$ is |kOrder|, the order of the prime-order subgroup
  // of Ed25519). In the following, we may add $l + 2×l + 4×l$ for a max value
  // of $8×l-1$. That is < 2**256, as required.

  if (!ctx->disable_password_scalar_hack) {
    scalar order = kOrder;
    scalar tmp;

    OPENSSL_memset(&tmp, 0, sizeof(tmp));
    scalar_cmov(&tmp, &order,
                constant_time_eq_w(password_scalar.words[0] & 1, 1));
    scalar_add(&password_scalar, &tmp);

    scalar_double(&order);
    OPENSSL_memset(&tmp, 0, sizeof(tmp));
    scalar_cmov(&tmp, &order,
                constant_time_eq_w(password_scalar.words[0] & 2, 2));
    scalar_add(&password_scalar, &tmp);

    scalar_double(&order);
    OPENSSL_memset(&tmp, 0, sizeof(tmp));
    scalar_cmov(&tmp, &order,
                constant_time_eq_w(password_scalar.words[0] & 4, 4));
    scalar_add(&password_scalar, &tmp);

    assert((password_scalar.words[0] & 7) == 0);
  }

  OPENSSL_memcpy(ctx->password_scalar, password_scalar.words,
                 sizeof(ctx->password_scalar));

  ge_p3 mask;
  x25519_ge_scalarmult_small_precomp(&mask, ctx->password_scalar,
                                     ctx->my_role == spake2_role_alice
                                         ? kSpakeMSmallPrecomp
                                         : kSpakeNSmallPrecomp);

  // P* = P + mask.
  ge_cached mask_cached;
  x25519_ge_p3_to_cached(&mask_cached, &mask);
  ge_p1p1 Pstar;
  x25519_ge_add(&Pstar, &P, &mask_cached);

  // Encode P*
  ge_p2 Pstar_proj;
  x25519_ge_p1p1_to_p2(&Pstar_proj, &Pstar);
  x25519_ge_tobytes(ctx->my_msg, &Pstar_proj);

  OPENSSL_memcpy(out, ctx->my_msg, sizeof(ctx->my_msg));
  *out_len = sizeof(ctx->my_msg);
  ctx->state = spake2_state_msg_generated;

  OPENSSL_cleanse(private_tmp, 64);

  return 1;
}

static void update_with_length_prefix(SHA512_CTX *sha, const uint8_t *data,
                                      const size_t len) {
  uint8_t len_le[8];
  size_t l = len;
  unsigned i;

  for (i = 0; i < 8; i++) {
    len_le[i] = l & 0xff;
    l >>= 8;
  }

  SHA512_Update(sha, len_le, sizeof(len_le));
  SHA512_Update(sha, data, len);
}

int SPAKE2_process_msg(SPAKE2_CTX *ctx, uint8_t *out_key, size_t *out_key_len,
                       size_t max_out_key_len, const uint8_t *their_msg,
                       size_t their_msg_len) {
  if (ctx->state != spake2_state_msg_generated ||
      their_msg_len != 32) {
    return 0;
  }

  ge_p3 Qstar;
  if (!x25519_ge_frombytes_vartime(&Qstar, their_msg)) {
    // Point received from peer was not on the curve.
    return 0;
  }

  // Unmask peer's value.
  ge_p3 peers_mask;
  x25519_ge_scalarmult_small_precomp(&peers_mask, ctx->password_scalar,
                                    ctx->my_role == spake2_role_alice
                                        ? kSpakeNSmallPrecomp
                                        : kSpakeMSmallPrecomp);

  ge_cached peers_mask_cached;
  x25519_ge_p3_to_cached(&peers_mask_cached, &peers_mask);

  ge_p1p1 Q_compl;
  ge_p3 Q_ext;
  x25519_ge_sub(&Q_compl, &Qstar, &peers_mask_cached);
  x25519_ge_p1p1_to_p3(&Q_ext, &Q_compl);

  ge_p2 dh_shared;
  x25519_ge_scalarmult(&dh_shared, ctx->private_key, &Q_ext);

  uint8_t dh_shared_encoded[32];
  x25519_ge_tobytes(dh_shared_encoded, &dh_shared);

  SHA512_CTX sha;
  SHA512_Init(&sha);
  if (ctx->my_role == spake2_role_alice) {
    update_with_length_prefix(&sha, ctx->my_name, ctx->my_name_len);
    update_with_length_prefix(&sha, ctx->their_name, ctx->their_name_len);
    update_with_length_prefix(&sha, ctx->my_msg, sizeof(ctx->my_msg));
    update_with_length_prefix(&sha, their_msg, 32);
  } else {
    update_with_length_prefix(&sha, ctx->their_name, ctx->their_name_len);
    update_with_length_prefix(&sha, ctx->my_name, ctx->my_name_len);
    update_with_length_prefix(&sha, their_msg, 32);
    update_with_length_prefix(&sha, ctx->my_msg, sizeof(ctx->my_msg));
  }
  update_with_length_prefix(&sha, dh_shared_encoded, sizeof(dh_shared_encoded));
  update_with_length_prefix(&sha, ctx->password_hash,
                            sizeof(ctx->password_hash));

  uint8_t key[SHA512_DIGEST_LENGTH];
  SHA512_Final(key, &sha);

  size_t to_copy = max_out_key_len;
  if (to_copy > sizeof(key)) {
    to_copy = sizeof(key);
  }
  OPENSSL_memcpy(out_key, key, to_copy);
  *out_key_len = to_copy;
  ctx->state = spake2_state_key_generated;

  return 1;
}
