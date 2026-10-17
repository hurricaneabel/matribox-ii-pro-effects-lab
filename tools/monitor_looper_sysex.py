"""Experimental looper monitor: one read-only snapshot query, then input events."""
import argparse,datetime,json
from pathlib import Path

QUERY=bytes.fromhex("f07d4d424c5101f7")

def request_snapshot(mido, output_name):
    with mido.open_output(output_name) as port:
        port.send(mido.Message("sysex",data=QUERY[1:-1]))

STATES={0:'VAZIO',1:'PARADO',2:'ESTADO 2 (a confirmar)',3:'REPRODUZINDO',4:'GRAVANDO',5:'OVERDUB'}

def decode(frame):
    frame=bytes(frame)
    if len(frame) not in (30,38,46) or frame[:5]!=bytes.fromhex('f021254d50') or frame[-1]!=247:
        return None
    size=(len(frame)-14)//2
    if any(v>127 for v in frame[1:-1]) or frame[9:13]!=bytes([size,0,0,0]):
        return None
    nib=frame[13:-1]
    if any(v>15 for v in nib):return None
    data=bytes(nib[i]*16+nib[i+1] for i in range(0,len(nib),2))
    if data[:4]!=b'MBLP' or data[5] not in STATES:return None
    result={'version':data[4],'state':data[5],'label':STATES[data[5]]}
    if data[4]==1 and len(data)==8 and data[6:]==b'\0\0':return result
    if (data[4],len(data)) not in ((2,12),(3,16)):return None
    if data[6]>100 or data[7]>100 or any(v>1 for v in data[8:12]):return None
    result.update(play_volume=data[6],record_level=data[7],placement='PRE' if data[8]==0 else 'POST',native_flag_ff=data[9],drum_sync=bool(data[10]),auto_rec=bool(data[11]))
    if data[4]==3:
        if data[12]>2 or data[14:]!=bytes(2):return None
        result.update(undo_state=data[12],history_index=data[13],undo_status={0:'SEM UNDO DISPONIVEL',1:'CAMADA DESFEITA / REDO DISPONIVEL',2:'CAMADA ATIVA / UNDO DISPONIVEL'}[data[12]])
    return result

def action(previous,current):
    if not previous or previous.get('version')!=3 or current.get('version')!=3:return None
    if previous['history_index']!=current['history_index'] or current['history_index']==255:return None
    if previous['state'] in (0,4,5) or current['state'] in (0,4,5):return None
    return {(2,1):'UNDO',(1,2):'REDO'}.get((previous['undo_state'],current['undo_state']))

def self_test():
    good=bytes.fromhex('f021254d5000003a0008000000040d0402040c05000001000400000000f7')
    assert decode(good)['state']==4
    assert decode(good[:-1]) is None
    for pos,value in [(1,0),(9,9),(11,1),(13,16),(14,0),(22,15),(29,0)]:
        bad=bytearray(good);bad[pos]=value;assert decode(bad) is None,(pos,value)
    print('Validacao offline OK. Nenhuma porta MIDI aberta.')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input');ap.add_argument('--output');ap.add_argument('--no-query',action='store_true');ap.add_argument('--list',action='store_true');ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
    if args.self_test:self_test();return
    import mido
    names=mido.get_input_names()
    outputs=mido.get_output_names()
    if args.list:print(json.dumps({'inputs':names,'outputs':outputs},ensure_ascii=False,indent=2));return
    name=args.input
    if name is None:
        choices=[p for p in names if 'matribox' in p.lower()]
        if len(choices)!=1:raise SystemExit('Use --list e depois --input "nome exato da entrada".')
        name=choices[0]
    if name not in names:raise SystemExit('Entrada MIDI nao encontrada: '+name)
    output=args.output
    if not args.no_query:
        matches=[p for p in outputs if 'matribox' in p.lower()]
        if output is None and len(matches)==1:output=matches[0]
        if output not in outputs:raise SystemExit('Use --list e --output com o nome da saida, ou --no-query para apenas escutar.')
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');log=Path('looper_sysex_'+stamp+'.jsonl')
    print('Pedaleira em modo normal. Consulta unica de estado; nenhuma configuracao sera alterada.' if not args.no_query else 'Somente escuta, sem consulta inicial.');print('Feche o editor/frontend se a porta estiver ocupada.')
    print('Entrada:',name,'\nLog:',log.resolve(),'\nAguardando estados; Ctrl+C encerra.')
    previous=None;previous_snapshot=None
    try:
        with mido.open_input(name) as port,log.open('x',encoding='utf8') as out:
            if not args.no_query:
                request_snapshot(mido,output)
                print('Consulta inicial enviada uma vez. Aguardando resposta e mudancas.',flush=True)
            for msg in port:
                if msg.type!='sysex':continue
                frame=bytes(msg.bytes());event=decode(frame)
                if event is None:continue
                now=datetime.datetime.now().astimezone().isoformat(timespec='milliseconds');signature=tuple(sorted(event.items()));changed=signature!=previous;snapshot=event.copy();event.update(time=now,changed=changed,hex=frame.hex(),undo_redo_action=action(previous_snapshot,snapshot))
                out.write(json.dumps(event,ensure_ascii=False)+'\n');out.flush()
                details=(' | Auto Rec='+str(event['auto_rec'])+' | Drum Sync='+str(event['drum_sync'])+' | Rec Level='+str(event['record_level'])+' | '+event['placement']+' | Play Vol='+str(event['play_volume'])) if event['version']>=2 else ''
                if event['version']==3:details+=' | '+event['undo_status']
                if event.get('undo_redo_action'):details+=' | '+event['undo_redo_action']+' utilizado'
                print(now,event['label']+details,'(mudanca)' if changed else '(resumo solicitado ou reconexao)',flush=True);previous=signature;previous_snapshot=snapshot
    except KeyboardInterrupt:print('\nMonitor encerrado.')

if __name__=='__main__':main()
