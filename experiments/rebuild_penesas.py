"""Experimental offline reconstruction for the exact documented GP-200 input.
Requires a locally supplied firmware; contains no donor firmware bytes.
No device communication. See docs/penesas.md for tested scope and limitations.
"""
import argparse
import struct
import json
import math
import hashlib
from pathlib import Path
from capstone import *
from capstone.arm import *


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gp-firmware", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    OUT=Path(args.output); OUT.mkdir(parents=True,exist_ok=True)
    # Sole effect source is GP firmware. No Matribox ELF or relocation inventory is read.
    fw=Path(args.gp_firmware).read_bytes()
    if hashlib.sha256(fw).hexdigest() != 'c368618773097b07c556c951eb10792f9d57be929323366648eb6e083d0d23af':
     raise ValueError('Only the documented GP-200 V1.8.2 input is supported')
    rec=fw[0x43ed8c:0x4413ac]; core=rec[0xac:0x21e0]; const=rec[0x21e0:0x261c]
    BASE=0x39200; PREFIX=40
    INTERNAL=b'FaunDrive\0'; CONST_BASE=struct.unpack_from('<I',rec,0x14)[0]-const.index(INTERNAL)
    init,process=struct.unpack_from('<II',rec,0x18)
    md=Cs(CS_ARCH_ARM, CS_MODE_THUMB|CS_MODE_LITTLE_ENDIAN); md.detail=True
    # Follow branch targets from exported entries. Literal pools are not scanned as instructions.
    queue=[(init&~1)-BASE,(process&~1)-BASE]; instructions={}; outside=[]
    while queue:
     start=queue.pop()
     if start<0 or start>=len(core): outside.append(start);continue
     for ins in md.disasm(core[start:],BASE+start):
      q=ins.address-BASE
      if q in instructions:break
      instructions[q]=ins
      if ins.mnemonic.startswith('b') and ins.operands and ins.operands[0].type==ARM_OP_IMM:
       target=ins.operands[0].imm-BASE
       if 0<=target<len(core):queue.append(target)
       else:outside.append(target)
      if ins.mnemonic in ('cbz','cbnz') and ins.operands[-1].type==ARM_OP_IMM:queue.append(ins.operands[-1].imm-BASE)
      if ins.mnemonic in ('b','b.w','bx','bx.w'):break
      if ins.mnemonic in ('pop','pop.w') and ins.cc in (ARM_CC_AL,ARM_CC_INVALID) and any(op.type==ARM_OP_REG and op.reg==ARM_REG_PC for op in ins.operands):break
      if ins.mnemonic=='udf':break
    # Recover address pairs within short instruction windows, validating both encoding/register and RAM range.
    ordered=sorted(instructions);pairs=[]
    for q in ordered:
     ins=instructions[q]
     if ins.mnemonic!='movw':continue
     reg=ins.operands[0].reg;lo=ins.operands[1].imm
     for r in ordered[ordered.index(q)+1:ordered.index(q)+81]:
      nxt=instructions[r]
      if r-q>256:break
      if nxt.mnemonic=='movt' and nxt.operands[0].reg==reg:
       addr=lo|(nxt.operands[1].imm<<16)
       if 0x20200000<=addr<0x20300000 or CONST_BASE<=addr<CONST_BASE+len(const):pairs.append((q,r,addr))
       break
      if reg in nxt.regs_access()[1]:break
    literal_pointers=[];relative=[]
    for q in ordered:
     ins=instructions[q]
     if ins.mnemonic not in ('ldr','ldr.w') or len(ins.operands)<2:continue
     mem=ins.operands[1]
     if mem.type!=ARM_OP_MEM or mem.mem.base!=ARM_REG_PC:continue
     slot=((ins.address+4)&~3)+mem.mem.disp-BASE
     if slot<0 or slot+4>len(core):continue
     value=struct.unpack_from('<I',core,slot)[0]
     if 0x20200000<=value<0x20300000 or CONST_BASE<=value<CONST_BASE+len(const):literal_pointers.append((slot,value))
     reg=ins.operands[0].reg
     for r in ordered[ordered.index(q)+1:ordered.index(q)+8]:
      nxt=instructions[r]
      if r-q>24:break
      ops=nxt.operands
      if nxt.mnemonic in ('add','add.w') and len(ops)>=2 and ops[0].type==ARM_OP_REG and ops[0].reg==reg and any(op.type==ARM_OP_REG and op.reg==ARM_REG_PC for op in ops[1:]):
       target=(value if value<0x80000000 else value-0x100000000)+nxt.address+4
       constbase=CONST_BASE
       if constbase<=target<constbase+len(const):relative.append((slot,r,target-constbase))
       elif BASE+len(core)<=target<BASE+len(core)+len(const):relative.append((slot,r,target-(BASE+len(core))))
       break
      if reg in nxt.regs_access()[1]:break
    ram_addresses=[p[2] for p in pairs if 0x20200000<=p[2]<0x20300000]+[p[1] for p in literal_pointers if 0x20200000<=p[1]<0x20300000]
    RAM_BASE=min(ram_addresses)&~7
    assert 0x20200000<=RAM_BASE<0x20300000
    # Conservative state allocation: round referenced-address extent up to a page.
    # This does not claim to infer all array sizes from machine code.
    RAM_SIZE=((max(ram_addresses)-RAM_BASE+64+4095)//4096)*4096
    symbols=[('',0,0,0,0)];symidx={};relocs=[]
    def symbol(name,value,size,info,section):
     key=(value,info&15,section)
     if key not in symidx:
      symidx[key]=len(symbols);symbols.append((name,value,size,info,section))
     return symidx[key]
    def relocation(off,t,idx):relocs.append((off,(idx<<8)|t))
    code=bytearray(PREFIX)+bytearray(core)+bytearray(b'\x00\x20\x70\x47')
    struct.pack_into('<I',code,20,struct.unpack_from('<I',rec,0x10)[0]);code[36:40]=b'\xaa\x55\xaa\xff'
    entry=PREFIX+len(core)+1
    si=symbol('gp_penesas_init',(init&~1)-BASE+PREFIX+1,0,0x12,1)
    sp=symbol('gp_penesas_process',(process&~1)-BASE+PREFIX+1,0,0x12,1)
    symbol('module_entry',entry,4,0x12,1)
    namepos=const.index(INTERNAL);sn=symbol('algorithm_name',0x10000000+namepos,len(INTERNAL),0x11,2)
    relocation(24,2,sn);relocation(28,2,si);relocation(32,2,sp)
    def clearimm(off):
     h1,h2=struct.unpack_from('<HH',code,off);struct.pack_into('<HH',code,off,h1&~0x40f,h2&~0x70ff)
    for low,high,addr in pairs:
     isram=0x20200000<=addr<0x20300000
     idx=symbol(f'{"state" if isram else "const"}_{addr-(RAM_BASE if isram else CONST_BASE):04x}',(0x20000000 if isram else 0x10000000)+addr-(RAM_BASE if isram else CONST_BASE),0,0x11,3 if isram else 2)
     clearimm(low+PREFIX);clearimm(high+PREFIX);relocation(low+PREFIX,47,idx);relocation(high+PREFIX,48,idx)
    for slot,addr in sorted(set(literal_pointers)):
     isram=0x20200000<=addr<0x20300000
     idx=symbol(f'{"state" if isram else "const"}_{addr-(RAM_BASE if isram else CONST_BASE):04x}',(0x20000000 if isram else 0x10000000)+addr-(RAM_BASE if isram else CONST_BASE),0,0x11,3 if isram else 2)
     struct.pack_into('<I',code,slot+PREFIX,0);relocation(slot+PREFIX,2,idx)
    for slot,anchor,targetoff in sorted(set(relative)):
     idx=symbol(f'const_{targetoff:04x}',0x10000000+targetoff,0,0x11,2)
     # Loader computes existing addend + S - P; ADD PC later uses its own anchor.
     addend=slot-(anchor+4)
     struct.pack_into('<I',code,slot+PREFIX,addend&0xffffffff);relocation(slot+PREFIX,3,idx)
    (OUT/'recovery.json').write_text(json.dumps({'pairs':pairs,'literal_pointers':literal_pointers,'relative':relative,'outside':outside})); assert pairs and not outside
    # Construct ELF and every section/symbol/relocation table from scratch.
    strings=bytearray(b'\0');symdata=bytearray()
    for name,value,size,info,section in symbols:
     no=len(strings) if name else 0
     if name:strings.extend(name.encode()+b'\0')
     symdata.extend(struct.pack('<IIIBBH',no,value,size,info,0,section))
    reld= b''.join(struct.pack('<II',*r) for r in sorted(relocs))
    shnames=['','ER_IROM','ER_SROM','ER_IRAM','.dynstr','.dynsym','.dyn','.shstrtab']
    shstr=bytearray(b'\0');shnos=[0]
    for name in shnames[1:]:shnos.append(len(shstr));shstr.extend(name.encode()+b'\0')
    payloads=[b'',bytes(code),const,b'',bytes(strings),bytes(symdata),reld,bytes(shstr)]
    types=[0,1,1,8,3,11,9,3];flags=[0,6,2,3,0,0,0,0];addresses=[0,0,0x10000000,0x20000000,0,0,0,0]
    blob=bytearray(52);sections=[]
    for i,data in enumerate(payloads):
     if i==0:sections.append((0,)*10);continue
     while len(blob)%8:blob.append(0)
     off=len(blob);blob.extend(data)
     size=RAM_SIZE if i==3 else len(data)
     link=4 if i==5 else 5 if i==6 else 0;info=1 if i==5 else 0;entsize=16 if i==5 else 8 if i==6 else 0
     sections.append((shnos[i],types[i],flags[i],addresses[i],off,size,link,info,8 if i in (1,2,3) else 4 if i in (5,6) else 1,entsize))
    while len(blob)%4:blob.append(0)
    shoff=len(blob)
    for section in sections:blob.extend(struct.pack('<10I',*section))
    ident=b'\x7fELF\x01\x01\x01'+b'\0'*9
    blob[:52]=struct.pack('<16sHHIIIIIHHHHHH',ident,3,40,1,entry,0,shoff,0x05000400,52,0,0,40,len(sections),7)
    OUT.mkdir(exist_ok=True);(OUT/'penesas_gp_reconstruido.elf').write_bytes(blob)
    # Rebuild Matribox-style descriptor using GP parameter values and strings.
    modelptr,catptr=struct.unpack_from('<II',rec,0x34);model=rec[modelptr-4:].split(b'\0')[0];cat=rec[catptr-4:].split(b'\0')[0]
    count=struct.unpack_from('<I',rec,0x40)[0];pool=bytearray();offsets={}
    def addstr(s):
     if s not in offsets:offsets[s]=len(pool);pool.extend(s+b'\0')
     return offsets[s]
    modeloff,catof=addstr(model),addstr(cat);params=bytearray();plist=[]
    for i in range(count):
     raw=rec[0x48+24*i:0x48+24*(i+1)];ptr=struct.unpack_from('<I',raw)[0];name=rec[ptr-4:].split(b'\0')[0];no=addstr(name)
     params.extend(struct.pack('<HH',0xffff,no)+raw[4:]);plist.append(name.decode())
    desc=struct.pack('<II4BHH',struct.unpack_from('<I',rec,0x10)[0],0xffffffff,count,0,255,0,modeloff,catof)+params+pool
    metadata=bytearray(8)+desc
    while len(metadata)%8:metadata.append(255)
    struct.pack_into('<II',metadata,0,len(metadata)+len(blob),len(metadata));(OUT/'penesas_registro_experimental.bin').write_bytes(metadata+blob)
    manifest={'source':'GP-200_USB_Firmware_V1.8.2.bin','source_sha256':hashlib.sha256(fw).hexdigest(),'source_record_offset':'0x43ed8c','code_offset_in_record':'0xac','const_offset_in_record':'0x21e0','recovered_CONST_base':hex(CONST_BASE),'recovered_RAM_base':hex(RAM_BASE),'RAM_allocation':RAM_SIZE,'RAM_allocation_policy':'conservative 4096-byte page, not exact inferred state size','CFG_instruction_sites':len(instructions),'outside_CFG_targets':outside,'recovered_MOV_pairs':len(pairs),'recovered_literal_RAM_pointers':literal_pointers,'recovered_PC_relative_constants':relative,'relocations_generated':len(relocs),'symbols_generated':len(symbols),'ELF_bytes':len(blob),'code_bytes':len(code),'constant_bytes':len(const),'entry':hex(entry),'init':hex((init&~1)-BASE+PREFIX+1),'process':hex((process&~1)-BASE+PREFIX+1),'parameter_names':plist,'metadata_bytes':len(metadata),'GP_core_branches_preserved':True,'reference_ELF_read_by_builder':False}
    (OUT/'construcao.json').write_text(json.dumps(manifest,indent=2),encoding='utf8');(OUT/'code.bin').write_bytes(code)
    print(json.dumps(manifest,indent=2))






if __name__ == "__main__":
    main()
