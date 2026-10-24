"""Reproduce the v0.3 workflow checks without modifying frozen source files.

Standard library only. Environment strings are simulated, not native OS tests.
Writes run_outputs/regression_results.json; isolated trials use temporary copies.
"""
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    source=Path(__file__).resolve().parent
    frozen=['verification_results.json','witness_k3.json','witness_k4.json']
    required=['verify_obstructions.py','verify_revision.py',*frozen]
    records=[]
    with tempfile.TemporaryDirectory(prefix='no35_regression_') as tmp:
        root=Path(tmp)/'package'
        root.mkdir()
        for name in required:
            shutil.copyfile(source/name,root/name)
        shutil.copytree(source/'prior',root/'prior')
        before={n:(root/n).read_bytes() for n in frozen}
        for mode in ['documented_order','changed_environment']:
            for script in ['verify_obstructions.py','verify_revision.py']:
                if mode=='changed_environment':
                    code=("import runpy;from unittest.mock import patch\n"
                          "with patch('platform.python_version',return_value='3.13.17-SIMULATED'),"
                          "patch('platform.platform',return_value='Windows-SIMULATED'):\n"
                          " runpy.run_path("+repr(str(root/script))+",run_name='__main__')")
                    cmd=[sys.executable,'-c',code]
                else:
                    cmd=[sys.executable,str(root/script)]
                run=subprocess.run(cmd,cwd=tmp,capture_output=True,text=True)
                if run.returncode:
                    raise RuntimeError(script+' failed: '+run.stderr)
                records.append({'mode':mode,'script':script,'returncode':run.returncode})
            generated=json.loads((root/'run_outputs/verification_results.json').read_text())
            baseline=json.loads(before['verification_results.json'])
            for obj in [generated,baseline]:
                obj.pop('python');obj.pop('platform')
            assert generated==baseline,'Mathematical results differ'
            assert all((root/n).read_bytes()==before[n] for n in frozen)
        for name in ['verification_results.json','witness_k3.json']:
            target=root/name
            bad=json.loads(before[name])
            if name=='verification_results.json':
                bad['rows'][0]['upper_bound']=41
            else:
                bad['upper_bound']=41
            try:
                target.write_text(json.dumps(bad),encoding='utf-8')
                run=subprocess.run([sys.executable,str(root/'verify_revision.py')],
                                   cwd=tmp,capture_output=True,text=True)
                assert run.returncode!=0,'Corrupted evidence was accepted'
                records.append({'negative_control':name+': upper_bound=41','rejected':True})
            finally:
                target.write_bytes(before[name])
        run=subprocess.run([sys.executable,str(root/'verify_revision.py')],
                           cwd=tmp,capture_output=True,text=True)
        assert run.returncode==0,run.stderr
    result={'status':'PASS','checks':records,
            'native_windows_tested':False,'native_python313_tested':False,
            'runtime_python':platform.python_version(),'runtime_os':platform.platform(),
            'regression_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=source/'run_outputs';out.mkdir(exist_ok=True)
    (out/'regression_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    main()
