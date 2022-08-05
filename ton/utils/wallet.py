import codecs

from hashlib import sha256 as hasher
from tvm_valuetypes.cell import deserialize_boc, Cell


def seqno_extractor(result, data):
    data_cell = deserialize_boc(codecs.decode(codecs.encode(data["data"], 'utf-8'), 'base64'))
    seqno = int.from_bytes(data_cell.data.data[0:32].tobytes(), 'big')
    result['seqno'] = seqno


def v3_extractor(result, data):
    seqno_extractor(result, data)
    try:
        data_cell = deserialize_boc(codecs.decode(codecs.encode(data["data"], 'utf-8'), 'base64'))
        wallet_id = int.from_bytes(data_cell.data.data[32:64].tobytes(), 'big')
        result['wallet_id'] = wallet_id
    except Exception as e:
        print('Extracting wallet_id failed:', str(e))


def v3_builder(wallet_id: int, public_key: bytes):
    cell = Cell()
    cell.data.put_arbitrary_uint(0, 32)  # seqno
    cell.data.put_arbitrary_uint(int(wallet_id), 32)
    cell.data.put_arbitrary_uint(int.from_bytes(public_key, byteorder='big'), 256)
    return cell


def v4_builder(wallet_id: int, public_key: bytes):
    cell = v3_builder(wallet_id, public_key)
    cell.data.put_arbitrary_uint(0, 1)  # empty plugins dict
    return cell


def sha256(x):
    if not isinstance(x, bytes):
        x = codecs.encode(x, 'utf-8')
    h = hasher()
    h.update(x)
    return h.digest()


sources = {
    # Wallets
    'v1r1': "te6cckEBAQEARAAAhP8AIN2k8mCBAgDXGCDXCx/tRNDTH9P/0VESuvKhIvkBVBBE+RDyovgAAdMfMSDXSpbTB9QC+wDe0aTIyx/L/8ntVEH98Ik=",
    'v1r2': "te6cckEBAQEAUwAAov8AIN0gggFMl7qXMO1E0NcLH+Ck8mCBAgDXGCDXCx/tRNDTH9P/0VESuvKhIvkBVBBE+RDyovgAAdMfMSDXSpbTB9QC+wDe0aTIyx/L/8ntVNDieG8=",
    'v1r3': "te6cckEBAQEAXwAAuv8AIN0gggFMl7ohggEznLqxnHGw7UTQ0x/XC//jBOCk8mCBAgDXGCDXCx/tRNDTH9P/0VESuvKhIvkBVBBE+RDyovgAAdMfMSDXSpbTB9QC+wDe0aTIyx/L/8ntVLW4bkI=",
    'v2r1': "te6cckEBAQEAVwAAqv8AIN0gggFMl7qXMO1E0NcLH+Ck8mCDCNcYINMf0x8B+CO78mPtRNDTH9P/0VExuvKhA/kBVBBC+RDyovgAApMg10qW0wfUAvsA6NGkyMsfy//J7VShNwu2",
    'v2r2': "te6cckEBAQEAYwAAwv8AIN0gggFMl7ohggEznLqxnHGw7UTQ0x/XC//jBOCk8mCDCNcYINMf0x8B+CO78mPtRNDTH9P/0VExuvKhA/kBVBBC+RDyovgAApMg10qW0wfUAvsA6NGkyMsfy//J7VQETNeh",
    'v3r1': "te6cckEBAQEAYgAAwP8AIN0gggFMl7qXMO1E0NcLH+Ck8mCDCNcYINMf0x/TH/gjE7vyY+1E0NMf0x/T/9FRMrryoVFEuvKiBPkBVBBV+RDyo/gAkyDXSpbTB9QC+wDo0QGkyMsfyx/L/8ntVD++buA=",
    'v3r2': "te6cckEBAQEAcQAA3v8AIN0gggFMl7ohggEznLqxn3Gw7UTQ0x/THzHXC//jBOCk8mCDCNcYINMf0x/TH/gjE7vyY+1E0NMf0x/T/9FRMrryoVFEuvKiBPkBVBBV+RDyo/gAkyDXSpbTB9QC+wDo0QGkyMsfyx/L/8ntVBC9ba0=",
    'v4r1': "te6cckECFQEAAvUAART/APSkE/S88sgLAQIBIAIDAgFIBAUE+PKDCNcYINMf0x/THwL4I7vyY+1E0NMf0x/T//QE0VFDuvKhUVG68qIF+QFUEGT5EPKj+AAkpMjLH1JAyx9SMMv/UhD0AMntVPgPAdMHIcAAn2xRkyDXSpbTB9QC+wDoMOAhwAHjACHAAuMAAcADkTDjDQOkyMsfEssfy/8REhMUA+7QAdDTAwFxsJFb4CHXScEgkVvgAdMfIYIQcGx1Z70ighBibG5jvbAighBkc3RyvbCSXwPgAvpAMCD6RAHIygfL/8nQ7UTQgQFA1yH0BDBcgQEI9ApvoTGzkl8F4ATTP8glghBwbHVnupEx4w0kghBibG5juuMABAYHCAIBIAkKAFAB+gD0BDCCEHBsdWeDHrFwgBhQBcsFJ88WUAP6AvQAEstpyx9SEMs/AFL4J28ighBibG5jgx6xcIAYUAXLBSfPFiT6AhTLahPLH1Iwyz8B+gL0AACSghBkc3Ryuo41BIEBCPRZMO1E0IEBQNcgyAHPFvQAye1UghBkc3Rygx6xcIAYUATLBVjPFiL6AhLLassfyz+UEDRfBOLJgED7AAIBIAsMAFm9JCtvaiaECAoGuQ+gIYRw1AgIR6STfSmRDOaQPp/5g3gSgBt4EBSJhxWfMYQCAVgNDgARuMl+1E0NcLH4AD2ynftRNCBAUDXIfQEMALIygfL/8nQAYEBCPQKb6ExgAgEgDxAAGa3OdqJoQCBrkOuF/8AAGa8d9qJoQBBrkOuFj8AAbtIH+gDU1CL5AAXIygcVy//J0Hd0gBjIywXLAiLPFlAF+gIUy2sSzMzJcfsAyEAUgQEI9FHypwIAbIEBCNcYyFQgJYEBCPRR8qeCEG5vdGVwdIAYyMsFywJQBM8WghAF9eEA+gITy2oSyx/JcfsAAgBygQEI1xgwUgKBAQj0WfKn+CWCEGRzdHJwdIAYyMsFywJQBc8WghAF9eEA+gIUy2oTyx8Syz/Jc/sAAAr0AMntVEap808=",
    'v4r2': "te6cckECFAEAAtQAART/APSkE/S88sgLAQIBIAIDAgFIBAUE+PKDCNcYINMf0x/THwL4I7vyZO1E0NMf0x/T//QE0VFDuvKhUVG68qIF+QFUEGT5EPKj+AAkpMjLH1JAyx9SMMv/UhD0AMntVPgPAdMHIcAAn2xRkyDXSpbTB9QC+wDoMOAhwAHjACHAAuMAAcADkTDjDQOkyMsfEssfy/8QERITAubQAdDTAyFxsJJfBOAi10nBIJJfBOAC0x8hghBwbHVnvSKCEGRzdHK9sJJfBeAD+kAwIPpEAcjKB8v/ydDtRNCBAUDXIfQEMFyBAQj0Cm+hMbOSXwfgBdM/yCWCEHBsdWe6kjgw4w0DghBkc3RyupJfBuMNBgcCASAICQB4AfoA9AQw+CdvIjBQCqEhvvLgUIIQcGx1Z4MesXCAGFAEywUmzxZY+gIZ9ADLaRfLH1Jgyz8gyYBA+wAGAIpQBIEBCPRZMO1E0IEBQNcgyAHPFvQAye1UAXKwjiOCEGRzdHKDHrFwgBhQBcsFUAPPFiP6AhPLassfyz/JgED7AJJfA+ICASAKCwBZvSQrb2omhAgKBrkPoCGEcNQICEekk30pkQzmkD6f+YN4EoAbeBAUiYcVnzGEAgFYDA0AEbjJftRNDXCx+AA9sp37UTQgQFA1yH0BDACyMoHy//J0AGBAQj0Cm+hMYAIBIA4PABmtznaiaEAga5Drhf/AABmvHfaiaEAQa5DrhY/AAG7SB/oA1NQi+QAFyMoHFcv/ydB3dIAYyMsFywIizxZQBfoCFMtrEszMyXP7AMhAFIEBCPRR8qcCAHCBAQjXGPoA0z/IVCBHgQEI9FHyp4IQbm90ZXB0gBjIywXLAlAGzxZQBPoCFMtqEssfyz/Jc/sAAgBsgQEI1xj6ANM/MFIkgQEI9Fnyp4IQZHN0cnB0gBjIywXLAlAFzxZQA/oCE8tqyx8Syz/Jc/sAAAr0AMntVGliJeU="
}

contracts = {
    sha256(sources[name]): {
        'type': name,
        'data_extractor': v3_extractor if name.find('v') == 0 else None,
        'data_builder': {
            'v1': None,
            'v2': None,
            'v3': v3_builder,
            'v4': v4_builder
        }[name[:2]],
    } for name in sources
}