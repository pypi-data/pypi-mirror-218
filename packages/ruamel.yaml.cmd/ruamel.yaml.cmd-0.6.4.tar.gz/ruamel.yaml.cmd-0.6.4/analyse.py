import sys
import os
import resource
import time
import datetime
import json
from pathlib import Path

import blake3

import ruamel.yaml


class Analyse:
    def __init__(self, args):
        self._args = args
        d = Path(
            os.environ.get('XDG_CONFIG_HOME', os.path.join(os.environ['HOME'], '.config'))
        )
        d.mkdir(exist_ok=True)
        self.results = d / 'yaml' / 'results.jsonl'

    @property
    def yaml(self):
        try:
            return self._yaml

        except AttributeError:
            pass
        self._yaml = res = ruamel.yaml.YAML(typ=self._args.typ, pure=self._args.pure)
        return res

    def __call__(self, infp, filename='<stdin>'):
        input = infp.read()
        infp.seek(0)
        lines = input.count(b'\n')
        b3sum = blake3.blake3(input).hexdigest()
        fsb = len(input)
        fs = fsb / (1024 * 1024)
        del input
        start = time.time()
        _ = self.yaml.load(infp)
        duration = time.time() - start
        memkb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform == 'darwin':
            memkb //= 1024
        memmb = memkb / 1024
        print(f'file: {fs:.2f}Mb time: {duration:.2f}s memory: {memmb:.1f}Mb')
        data = dict(
            dts=datetime.datetime.now().replace(microsecond=0).isoformat(),
            b3sum=b3sum,
            file_name=filename,
            file_size=fsb,
            file_lines=lines,
            duration=duration,
            memkb=memkb,
            version=ruamel.yaml.version_info,
            typ=self._args.typ,
            pure=self._args.pure,
        )
        with self.results.open('a') as fp:
            json.dump(data, fp)
            fp.write('\n')
