#!/usr/bin/env python3
"""Put shortcut chips on a Nova Launcher "Nova Now" card (Nova 8.9.x), more than the six the card editor allows.

Root only. Stop Nova, copy /data/data/com.teslacoilsw.launcher/files/datastore/cards.datastore off the phone, run:
    python3 nova_card_chips.py cards.datastore cards.new "CompositeCard:<card name>" fork.risin42.nagramx xft_<chat>_<topic> ...
then copy cards.new back over cards.datastore (same owner and SELinux label) and start Nova. Nova pins every chip itself on start.
With no shortcut ids it only prints the chips that card has now."""
import sys

M=(1<<64)-1
def rotl(x,r): return ((x<<r)|(x>>(64-r)))&M
def fmix(k):
    k^=k>>33; k=(k*0xff51afd7ed558ccd)&M; k^=k>>33; k=(k*0xc4ceb9fe1a85ec53)&M; k^=k>>33; return k
def h128(data, seed=0):
    n=len(data); h1=seed; h2=seed; c1=0x87c37b91114253d5; c2=0x4cf5ad432745937f
    nb=n//16
    for i in range(nb):
        k1=int.from_bytes(data[i*16:i*16+8],'little'); k2=int.from_bytes(data[i*16+8:i*16+16],'little')
        k1=(k1*c1)&M; k1=rotl(k1,31); k1=(k1*c2)&M; h1^=k1
        h1=rotl(h1,27); h1=(h1+h2)&M; h1=(h1*5+0x52dce729)&M
        k2=(k2*c2)&M; k2=rotl(k2,33); k2=(k2*c1)&M; h2^=k2
        h2=rotl(h2,31); h2=(h2+h1)&M; h2=(h2*5+0x38495ab5)&M
    t=data[nb*16:]; k1=0;k2=0
    if len(t)>8:
        k2=int.from_bytes(t[8:],'little'); k2=(k2*c2)&M; k2=rotl(k2,33); k2=(k2*c1)&M; h2^=k2
    if len(t)>0:
        k1=int.from_bytes(t[:8],'little'); k1=(k1*c1)&M; k1=rotl(k1,31); k1=(k1*c2)&M; h1^=k1
    h1^=n; h2^=n; h1=(h1+h2)&M; h2=(h2+h1)&M; h1=fmix(h1); h2=fmix(h2); h1=(h1+h2)&M; h2=(h2+h1)&M
    return h1,h2
def rv(b, p):
    r = 0; s = 0
    while True:
        c = b[p]; p += 1; r |= (c & 0x7f) << s; s += 7
        if c < 0x80: return r, p
def ev(n):
    o = bytearray()
    while True:
        c = n & 0x7f; n >>= 7
        if n: o.append(c | 0x80)
        else: o.append(c); return bytes(o)
def fields(b):
    p = 0; out = []
    while p < len(b):
        k, p = rv(b, p); f, w = k >> 3, k & 7
        if w == 0: v, p = rv(b, p)
        elif w == 2: l, p = rv(b, p); v = b[p:p+l]; p += l
        else: raise ValueError("wire %d" % w)
        out.append((f, w, v))
    return out
def enc(fl):
    o = bytearray()
    for f, w, v in fl:
        o += ev(f << 3 | w)
        if w == 0: o += ev(v)
        else: o += ev(len(v)) + v
    return bytes(o)
def read(path):
    d = open(path, 'rb').read(); n, p = rv(d, 0); ents = []
    for _ in range(n):
        l, p = rv(d, p); ents.append(d[p:p+l]); p += l
    assert p == len(d), "trailing bytes"
    return ents
def write(path, ents):
    o = ev(len(ents))
    for e in ents: o += ev(len(e)) + e
    open(path, 'wb').write(o)
def action(pkg, sid, user=0):
    a, b = h128(("%s/%s#%d" % (pkg, sid, user)).encode())
    ih = enc([(1, 0, 256), (2, 0, a), (3, 0, b)])
    content = enc([(1, 2, pkg.encode()), (2, 2, sid.encode()), (3, 0, user), (4, 2, ih), (5, 0, 1)])
    return enc([(1, 2, b"com.teslacoilsw.launcher.search.hero.ShortcutContent"), (2, 2, content)])
def actions_of(ents, key):
    for e in ents:
        f = fields(e)
        if any(x[0] == 2 and x[2] == key.encode() for x in f):
            card = [x for x in f if x[0] == 3][0][2]
            body = [x for x in fields(card) if x[0] == 2][0][2]
            res = []
            for x in fields(body):
                if x[0] == 5:
                    c = [y for y in fields(x[2]) if y[0] == 2][0][2]
                    res.append([y[2].decode() for y in fields(c) if y[0] == 2][0])
            return res
def set_actions(ents, key, pkg, ids):
    out = []
    for e in ents:
        f = fields(e)
        if any(x[0] == 2 and x[2] == key.encode() for x in f):
            nf = []
            for x in f:
                if x[0] == 3:
                    cf = fields(x[2]); ncf = []
                    for y in cf:
                        if y[0] == 2:
                            body = [z for z in fields(y[2]) if z[0] != 5]
                            # actions go right after the featured content (field 4), before any later fields
                            idx = max([i for i, z in enumerate(body) if z[0] <= 4] + [-1]) + 1
                            body = body[:idx] + [(5, 2, action(pkg, s)) for s in ids] + body[idx:]
                            y = (2, 2, enc(body))
                        ncf.append(y)
                    x = (3, 2, enc(ncf))
                nf.append(x)
            e = enc(nf)
        out.append(e)
    return out
if __name__ == '__main__':
    src, dst, key, pkg = sys.argv[1:5]; ids = sys.argv[5:]
    ents = read(src)
    print("before:", actions_of(ents, key))
    if ids:
        ents = set_actions(ents, key, pkg, ids); write(dst, ents)
        print("after:", actions_of(read(dst), key))
