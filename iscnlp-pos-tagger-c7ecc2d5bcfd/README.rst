POS-Tagger
==========

Install dependencies
^^^^^^^^^^^^^^^^^^^^

::

    pip install -r requirements.txt

Install
^^^^^^^

::

    - git clone https://irshadbhat@bitbucket.org/iscnlp/pos-tagger.git
    - cd pos-tagger
    - sudo python setup.py install

POS-Tagger
^^^^^^^^^^

.. code:: python

    >>> from __future__ import unicode_literals
    >>> from isc_tokenizer import Tokenizer
    >>> from isc_tagger import Tagger
    >>> tk = Tokenizer(lang='hin')
    >>> tagger = Tagger(lang='hin')
    >>> sequence = tk.tokenize("केजरीवाल पर प्रहार करते हुए अखिलेश ने कहा कि जब तक पूरे मामले की जांच रिपोर्ट जनता के"
    ...                        " सामने नहीं आ जाती, कोई कैसे कह सकता है कि जांच निष्पक्ष है या नहीं।")
    >>> sequence
    ['केजरीवाल', 'पर', 'प्रहार', 'करते', 'हुए', 'अखिलेश', 'ने', 'कहा', 'कि', 'जब', 'तक', 'पूरे', 'मामले', 'की', 'जांच', 'रिपोर्ट', 'जनता', 'के', 'सामने', 'नहीं', 'आ', 'जाती', ',', 'कोई', 'कैसे', 'कह', 'सकता', 'है', 'कि', 'जांच', 'निष्पक्ष', 'है', 'या', 'नहीं', '।']
    >>> tagger.tag(sequence)
    [('केजरीवाल', 'NNP'), ('पर', 'PSP'), ('प्रहार', 'NN'), ('करते', 'VM'), ('हुए', 'VAUX'), ('अखिलेश', 'NNP'), ('ने', 'PSP'), ('कहा', 'VM'), ('कि', 'CC'), ('जब', 'PRP'), ('तक', 'PSP'), ('पूरे', 'JJ'), ('मामले', 'NN'), ('की', 'PSP'), ('जांच', 'NNC'), ('रिपोर्ट', 'NN'), ('जनता', 'NN'), ('के', 'PSP'), ('सामने', 'NST'), ('नहीं', 'NEG'), ('आ', 'VM'), ('जाती', 'VAUX'), (',', 'SYM'), ('कोई', 'PRP'), ('कैसे', 'WQ'), ('कह', 'VM'), ('सकता', 'VAUX'), ('है', 'VAUX'), ('कि', 'CC'), ('जांच', 'NN'), ('निष्पक्ष', 'JJ'), ('है', 'VM'), ('या', 'CC'), ('नहीं', 'NEG'), ('।', 'SYM')]
    >>>
    >>>
    >>> tagger = Tagger(lang='eng')
    >>> tagger.tag('The quick brown fox jumps over the lazy dog .'.split())
    [('The', u'DET'), ('quick', u'ADJ'), ('brown', u'ADJ'), ('fox', u'NOUN'), ('jumps', u'VERB'), ('over', u'ADP'), ('the', u'DET'), ('lazy', u'ADJ'), ('dog', u'NOUN'), ('.', u'PUNCT')]

POS text files directly from Command Line Interface. It is highly recommended to tokenize the text files before POS-tagging.

.. parsed-literal::

    irshad@iscnlp$ isc-tagger -h
    usage: isc-tagger [-h] [-v] [-i] [-o] [-l] [-u]
    
    POS-Tagger for Indian Languages
    
    optional arguments:
      -h, --help        show this help message and exit
      -v, --version     show program's version number and exit
      -i , --input      <input-file>
      -o , --output     <output-file>
      -l , --language   select language (3 letter ISO-639 code) {hin, urd, eng}
      -u, --ud          set this flag to predict universal tags

