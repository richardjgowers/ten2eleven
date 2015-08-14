'''
Copy to /Users/treddy/anaconda/lib/python2.7/lib2to3/fixes/
Then run with: 2to3 -f agmethods test_dummy_old_MDA_code.py 
'''

from lib2to3.fixer_base import BaseFix
from lib2to3.fixer_util import Name, Call, LParen, RParen, ArgList, Dot
from lib2to3 import pytree


class FixAgmethods(BaseFix):

    PATTERN = """
        power< head =any+
                trailer< dot = '.' method=('residues'|'charges'|'indices'|
                                         'masses'|'names'|'types'|
                                         'radii'|'resids'|'resnames'|
                                         'resnums'|'segids')>
                                parens=trailer< '(' ')' >
                                tail=any*>
    """

    def transform(self, node, results):
        head = results['head']
        method = results['method'][0]
        tail = results['tail']
        syms = self.syms
        method_name = method.value
        head = [n.clone() for n in head]
        tail = [n.clone() for n in tail]
        args = head + [pytree.Node(syms.trailer, [Dot(), Name(method_name, prefix = method.prefix)])]
        new = pytree.Node(syms.power, args)
        return new
