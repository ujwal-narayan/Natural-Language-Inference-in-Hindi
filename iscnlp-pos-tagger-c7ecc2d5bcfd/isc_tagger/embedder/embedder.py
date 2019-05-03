#!/usr/bin/env python
#! -*- coding:utf-8 -*-

# `load_wordvec` taken from `gensim.Word2Vec.load_word2vec_format`

from __future__ import unicode_literals

import os
import re
import sys
import string

from six.moves import xrange
from numpy import array, dtype, zeros, linalg, fromstring, float32 as REAL

EMBD_DIR = "%s/../embeddings/" % os.path.dirname(os.path.abspath(__file__))
EMBD_DIR = os.path.abspath( EMBD_DIR)

if sys.version_info[0] > 2:
    unicode = str


def to_unicode(text, encoding='utf8', errors='strict'):
    if isinstance(text, unicode):
        return text
    return unicode(text, encoding, errors=errors)


class WordVec():
    def __init__(self):
        self.vocab = {}
        self.index2word = []

    def __getitem__(self, x):
        word_id = self.vocab[x]
        return self.syn0[word_id]

    def load_wordvec(self, fname, encoding='utf8', unicode_errors='strict'):
        with open(fname, 'rb') as fin:
            header = to_unicode(fin.readline())
            vocab_size, vector_size = map(int, header.split())
            self.vocab_size = vocab_size
            self.vector_size = vector_size
            self.syn0 = zeros((vocab_size, vector_size), dtype=REAL)

            def add_word(word, weights):
                word_id = len(self.vocab)
                if word in self.vocab:
                    return
                else:
                    self.vocab[word] = word_id
                self.syn0[word_id] = weights
                self.index2word.append(word)

            binary_len = dtype(REAL).itemsize * vector_size
            for line_no in xrange(vocab_size):
                # mixed text and binary: read text first, then binary
                word = []
                while True:
                    ch = fin.read(1)
                    if ch == b' ':
                        break
                    if ch != b'\n':
                        word.append(ch)
                word = to_unicode(b''.join(word), encoding=encoding,
                                  errors=unicode_errors)
                weights = fromstring(fin.read(binary_len), dtype=REAL)
                add_word(word, weights)
        return self


class TagEmbedder(object):
    def __init__(self, window=2, lang='hin'):
        self.window = window
        self.indic = lang in ['hin']
        self.roman = lang == 'eng'
        self.n_words = 2 * self.window + 1
        self.c3vm = WordVec().load_wordvec('%s/%s_c3.vec' % (EMBD_DIR, lang))
        self.b3vm = WordVec().load_wordvec('%s/%s_b3.vec' % (EMBD_DIR, lang))
        self.wvm = WordVec().load_wordvec('%s/%s_word.vec' % (EMBD_DIR, lang))
        self.isdigit = re.compile('[0-9٠-٩۰-۹]').search
        self.punkt = set('%s' % string.punctuation) | set('، ۔ ؟ ؛'.split())
        if self.roman:
            self.isurl = re.compile(r'^(http://|https://|www\.|'
                                    r'.*?[a-z][a-z][.].*?[a-z][a-z])').search
            self.c2vm = WordVec().load_wordvec('%s/%s_c2.vec' % (EMBD_DIR, lang))
            self.b2vm = WordVec().load_wordvec('%s/%s_b2.vec' % (EMBD_DIR, lang))

    def _get_gensim_embd(self, feats):
        vec = []
        c3i = self.n_words
        b3i = c3i + 1
        for i, x in enumerate(feats[:self.n_words]):
            if x == '__PAD__':
                vec.extend(self.wvm.syn0[-2]*.01)
            elif x in self.wvm.vocab:
                vec.extend(self.wvm[x])
            elif x[0] in self.punkt:
                vec.extend(self.wvm[x[0]])
            elif self.roman:
                if x.lower() in self.wvm.vocab:
                    vec.extend(self.wvm[x.lower()])
                elif x.title() in self.wvm.vocab:
                    vec.extend(self.wvm[x.title()])
                elif self.isdigit(x):
                    vec.extend(self.wvm['__NUM__'])
                elif self.isurl(x):
                    vec.extend(self.wvm['__URL__'])
                else:
                    vec.extend(self.wvm.syn0[-1]*.01)
            elif self.isdigit(x):
                vec.extend(self.wvm['127'])
            else:
                vec.extend(self.wvm.syn0[-1]*.01)
        if feats[c3i] in self.c3vm.vocab:
            vec.extend(self.c3vm[feats[c3i]])
        else:
            vec.extend(self.c3vm.syn0[-1]*.01)
        if feats[b3i] in self.b3vm.vocab:
            vec.extend(self.b3vm[feats[b3i]])
        else:
            vec.extend(self.b3vm.syn0[-1]*.01)
        if self.roman:
            if feats[b3i + 1] in self.c2vm.vocab:
                vec.extend(self.c2vm[feats[b3i + 1]])
            else:
                vec.extend(self.c2vm.syn0[-1]*.01)
            if feats[b3i + 2] in self.b2vm.vocab:
                vec.extend(self.b2vm[feats[b3i + 2]])
            else:
                vec.extend(self.b2vm.syn0[-1]*.01)
        return vec

    def get_feats(self, sequence):
        feats = []
        dummies = ["__PAD__"] * self.window
        vec = dummies + sequence + dummies
        for i in range(self.window, len(vec) - self.window):
            cword = vec[i]  # current word
            # current word with its context
            context = vec[i - self.window: i] + [cword] + vec[
                i + 1: i + (self.window + 1)]
            if self.indic:
                cword = ' '.join(cword)
                cword = re.sub(r' ([aVYZ])', r'\1', cword)
                cword = cword.split()
            # current word suffix
            context.append(''.join(cword[-3:]))
            # current word prefix
            context.append(''.join(cword[:3]))
            if self.roman:
                # length 2 suffix
                context.append(cword[-2:])
                # length 2 prefix
                context.append(cword[:2])
            feat_vec = self._get_gensim_embd(context)
            feats.append(feat_vec)
        return array(feats)
