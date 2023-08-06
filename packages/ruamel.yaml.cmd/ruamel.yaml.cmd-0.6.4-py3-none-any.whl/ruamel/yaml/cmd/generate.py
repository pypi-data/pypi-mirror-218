
# Usage:
# yaml generate --levels sm_s1m --size 5 -

import sys
import io
import random
import string

import ruamel.yaml

letters_digits = string.ascii_letters + string.digits


class Generate:
    def __init__(self, args):
        self._levels = args.levels
        self._size = int(args.size)
        self.items = 5

    @property
    def yaml(self):
        try:
            return self._yaml
        except AttributeError:
            pass
        self._yaml = res = ruamel.yaml.YAML()
        return res

    def __call__(self, out):
        levels = self._levels
        if levels[0] == 's':
            return self.root_sequence(out, levels[1:])
        elif levels[0] == 'm':
            return self.root_mapping(out, levels[1:])
        else:
            print(f'unknown root level "{levels[0]}"')
            return -1

    def data(self, levels, flow_style, items=None):
        if not levels:
            typ = 'bfis'
        elif levels[0] == '_':
            return self.data(levels[1:], flow_style=True)
        elif levels[0] == '1':
            return self.data(levels[1:], flow_style, items=1)
        elif levels[0] in 'sm':
            if items is None:
                items = self.items
            typ = levels[0]
            levels = levels[1:]
            if typ == 's':  # generate sequence
                d = ruamel.yaml.CommentedSeq()
                if flow_style:
                    d.fa.set_flow_style()
                for _ in range(items):
                    d.append(self.data(levels, flow_style, items=items))
                return d
            elif typ == 'm':  # generate mapping
                d = ruamel.yaml.CommentedMap()
                if flow_style:
                    d.fa.set_flow_style()
                for _ in range(items):
                    d[self.gen_str(not_in=d)] = self.data(levels, flow_style, items=items)
                return d
        else:
            typ = levels[0]
        return self.gen_typ(random.choice(typ))

    def gen_typ(self, typ):
        assert len(typ) == 1
        if typ == 'b':
            return random.choice([True, False])
        elif typ == 'i':
            return random.randint(10000, 99999)
        elif typ == 'f':
            return random.randint(10000, 99999) / 100000
        elif typ == 's':
            return self.gen_str()
        else:
            return None

    def gen_str(self, length=5, not_in=None):
        """generate string of length that is not already in not_in"""
        while True:
            res = random.choice(string.ascii_letters)
            while len(res) < length:
                res += random.choice(string.ascii_letters)
            if not_in and res in not_in:
                continue
            return res

    def root_sequence(self, out, levels):
        size = 0
        if levels and levels[0] == 'F':
            levels = levels[1:]
            flow_style = True
        else:
            flow_style = False
        while size < (self._size * 1024):
            buf = io.BytesIO()
            data = [self.data(levels, flow_style=flow_style)]
            self.yaml.dump(data, buf)
            res = buf.getvalue()
            size += len(res)
            if out == sys.stdout:
                out.write(res.decode('utf-8'))
            else:
                out.write(res)

    def root_mapping(self, out, levels):
        size = 0
        if levels and levels[0] == 'F':
            levels = levels[1:]
            flow_style = True
        else:
            flow_style = False
        keys = set()
        while size < (self._size * 1024):
            buf = io.BytesIO()
            key = self.gen_str(not_in=keys)
            keys.add(key)
            data = {key: self.data(levels, flow_style=flow_style)}
            self.yaml.dump(data, buf)
            res = buf.getvalue()
            size += len(res)
            if out == sys.stdout:
                out.write(res.decode('utf-8'))
            else:
                out.write(res)
